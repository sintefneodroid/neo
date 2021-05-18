import abc

import torch
from torch import nn
import numpy
from collections import deque
import random, copy

import time, datetime
from matplotlib import pyplot

from gym.wrappers import FrameStack

from neodroid import PROJECT_APP_PATH
from draugr.tqdm_utilities import progress_bar
from draugr.torch_utilities import global_torch_device, PTW
from draugr import latest_file
from nes_py.wrappers import JoypadSpace  # NES Emulator for OpenAI Gym
import gym_super_mario_bros  # Super Mario environment for OpenAI Gym

from trolls.gym_wrappers import (
    GrayScaleObservation,
    ResizeObservation,
    SkipRepeatAccumulateLast,
)


class MarioArch(nn.Module):
    ######################################################################
    # After applying the above wrappers to the environment, the final wrapped
    # state consists of 4 gray-scaled consecutive frames stacked together, as
    # shown above in the image on the left. Each time Mario makes an action,
    # the environment responds with a state of this structure. The structure
    # is represented by a 3-D array of size ``[4, 84, 84]``.
    #
    # .. figure:: /_static/img/mario_env.png
    #    :alt: picture
    #
    #

    ######################################################################
    # Agent
    # """""""""
    #
    # We create a class ``Mario`` to represent our agent in the game. Mario
    # should be able to:
    #
    # -  **Act** according to the optimal action policy based on the current
    #    state (of the environment).
    #
    # -  **Remember** experiences. Experience = (current state, current
    #    action, reward, next state). Mario *caches* and later *recalls* his
    #    experiences to update his action policy.
    #
    # -  **Learn** a better action policy over time
    #

    ######################################################################
    # In the following sections, we will populate Mario’s parameters and
    # define his functions.
    #

    ######################################################################
    # Act
    # --------------
    #
    # For any given state, an agent can choose to do the most optimal action
    # (**exploit**) or a random action (**explore**).
    #
    # Mario randomly explores with a chance of ``self.exploration_rate``; when
    # he chooses to exploit, he relies on ``MarioNet`` (implemented in
    # ``Learn`` section) to provide the most optimal action.
    #

    """mini cnn structure
    input -> (conv2d + relu) x 3 -> flatten -> (dense + relu) x 2 -> output"""

    def __init__(self, input_dim, output_dim):
        super().__init__()
        c, h, w = input_dim

        if h != 84:
            raise ValueError(f"Expecting input height: 84, got: {h}")
        if w != 84:
            raise ValueError(f"Expecting input width: 84, got: {w}")

        self.online = nn.Sequential(
            nn.Conv2d(in_channels=c, out_channels=32, kernel_size=8, stride=4),
            nn.ReLU(),
            nn.Conv2d(in_channels=32, out_channels=64, kernel_size=4, stride=2),
            nn.ReLU(),
            nn.Conv2d(in_channels=64, out_channels=64, kernel_size=3, stride=1),
            nn.ReLU(),
            nn.Flatten(),
            nn.Linear(3136, 512),  # 512
            nn.ReLU(),
            nn.Linear(512, output_dim),
        )

        self.target = copy.deepcopy(self.online)

        # Q_target parameters are frozen.
        for p in self.target.parameters():
            p.requires_grad = False

    def forward(self, input, model):
        if model == "online":
            return self.online(input)
        elif model == "target":
            return self.target(input)


class MarioAgent:
    def __init__(self, state_dim, action_dim, save_dir, device):
        self.state_dim = state_dim
        self.action_dim = action_dim
        self.save_dir = save_dir

        self.q_model = (
            MarioArch(self.state_dim, self.action_dim).float().to(device=device)
        )
        self.device = device

        self.exploration_rate = 1
        self.exploration_rate_decay = 0.99999975
        self.exploration_rate_min = 0.1
        self.curr_step = 0

        self.save_every = 33333  # 5e5 # no. of experiences between saving Mario Net

        self.memory = deque(maxlen=40000)  # 100000
        self.batch_size = 16  # 32

        self.gamma = 0.9

        self.optimizer = torch.optim.Adam(self.q_model.parameters(), lr=0.00025)
        self.loss_fn = torch.nn.SmoothL1Loss()

        self.burn_in = 1e4  # min. experiences before training
        self.learn_every = 3  # no. of experiences between updates to Q_online
        self.sync_every = 1e4  # no. of experiences between Q_target & Q_online sync

    def act(self, state):
        """
        Given a state, choose an epsilon-greedy action and update value of step.

        Inputs:
        state(LazyFrame): A single observation of the current state, dimension is (state_dim)
        Outputs:
        action_idx (int): An integer representing which action Mario will perform"""
        # EXPLORE
        if numpy.random.rand() < self.exploration_rate:
            action_idx = numpy.random.randint(self.action_dim)

        # EXPLOIT
        else:
            state = state.__array__()

            state = torch.tensor(state).to(self.device)
            state = state.unsqueeze(0)
            action_values = self.q_model(state, model="online")
            action_idx = torch.argmax(action_values, axis=1).item()

        # decrease exploration_rate
        self.exploration_rate *= self.exploration_rate_decay
        self.exploration_rate = max(self.exploration_rate_min, self.exploration_rate)

        # increment step
        self.curr_step += 1
        return action_idx

    def cache(self, state, next_state, action, reward, done):
        """
        Store the experience to self.memory (replay buffer)

        Inputs:
        state (LazyFrame),
        next_state (LazyFrame),
        action (int),
        reward (float),
        done(bool))
        """
        state = state.__array__()
        next_state = next_state.__array__()

        state = torch.tensor(state).to(self.device)
        next_state = torch.tensor(next_state).to(self.device)
        action = torch.tensor([action]).to(self.device)
        reward = torch.tensor([reward]).to(self.device)
        done = torch.tensor([done]).to(self.device)

        self.memory.append(
            (
                state,
                next_state,
                action,
                reward,
                done,
            )
        )

    def recall(self):
        """
        Retrieve a batch of experiences from memory
        """
        batch = random.sample(self.memory, self.batch_size)
        state, next_state, action, signal, done = map(torch.stack, zip(*batch))
        return state, next_state, action.squeeze(), signal.squeeze(), done.squeeze()

    def td_estimate(self, state, action):
        current_Q = self.q_model(state, model="online")[
            numpy.arange(0, self.batch_size), action
        ]  # Q_online(s,a)
        return current_Q

    @torch.no_grad()
    def td_target(self, signal, next_state, done):
        next_state_q = self.q_model(next_state, model="online")
        best_action = torch.argmax(next_state_q, axis=1)
        next_q = self.q_model(next_state, model="target")[
            numpy.arange(0, self.batch_size), best_action
        ]
        return (signal + (1 - done.float()) * self.gamma * next_q).float()

    def update_q_online(self, td_estimate, td_target):
        loss = self.loss_fn(td_estimate, td_target)
        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()
        return loss.item()

    def sync_q_target(self):
        self.q_model.target.load_state_dict(self.q_model.online.state_dict())

    def load(self, load_path):
        chkpt_dict = torch.load(load_path)
        self.q_model.load_state_dict(chkpt_dict["model"])
        self.exploration_rate = chkpt_dict["exploration_rate"]
        print(
            f"MarioNet loaded from {load_path} at step {str(load_path).split('.')[0].split('_')[-1]}"
        )

    def save(self):
        save_path = (
            self.save_dir / f"mario_net_{int(self.curr_step // self.save_every)}.chkpt"
        )
        torch.save(
            dict(
                model=self.q_model.state_dict(), exploration_rate=self.exploration_rate
            ),
            save_path,
        )
        print(f"MarioNet saved to {save_path} at step {self.curr_step}")

    def learn(self):
        if self.curr_step % self.sync_every == 0:
            self.sync_q_target()
        if self.curr_step % self.save_every == 0:
            self.save()

        if self.curr_step < self.burn_in:
            return None, None
        if self.curr_step % self.learn_every != 0:
            return None, None

        state, next_state, action, reward, done = self.recall()

        td_est = self.td_estimate(state, action)
        td_tgt = self.td_target(reward, next_state, done)

        loss = self.update_q_online(td_est, td_tgt)

        return (td_est.mean().item(), loss)


if __name__ == "__main__":

    def asidjas(
        episodes=40000,
        train=False,
        resized_size=84,
        num_skips=4,
        device=global_torch_device(),
    ):

        ######################################################################
        # Preprocess Environment
        # ------------------------
        #
        # Environment data is returned to the agent in ``next_state``. As you saw
        # above, each state is represented by a ``[3, 240, 256]`` size array.
        # Often that is more information than our agent needs; for instance,
        # Mario’s actions do not depend on the color of the pipes or the sky!
        #
        # We use **Wrappers** to preprocess environment data before sending it to
        # the agent.
        #
        # ``GrayScaleObservation`` is a common wrapper to transform an RGB image
        # to grayscale; doing so reduces the size of the state representation
        # without losing useful information. Now the size of each state:
        # ``[1, 240, 256]``
        #
        # ``ResizeObservation`` downsamples each observation into a square image.
        # New size: ``[1, 84, 84]``
        #
        # ``SkipFrame`` is a custom wrapper that inherits from ``gym.Wrapper`` and
        # implements the ``step()`` function. Because consecutive frames don’t
        # vary much, we can skip n-intermediate frames without losing much
        # information. The n-th frame aggregates rewards accumulated over each
        # skipped frame.
        #
        # ``FrameStack`` is a wrapper that allows us to squash consecutive frames
        # of the environment into a single observation point to feed to our
        # learning model. This way, we can identify if Mario was landing or
        # jumping based on the direction of his movement in the previous several
        # frames.
        #

        env = FrameStack(
            ResizeObservation(
                GrayScaleObservation(
                    SkipRepeatAccumulateLast(
                        JoypadSpace(
                            gym_super_mario_bros.make(
                                "SuperMarioBros-1-1-v0"
                            ),  # pip install gym-super-mario-bros, may need github version
                            [["right"], ["right", "A"]],
                        ),  # Limit the action-space to #   0. walk right #   1. jump right,
                        num_skips=num_skips,
                    )
                ),
                shape=resized_size,
            ),
            num_stack=num_skips,
        )

        checkpoint_dir = PROJECT_APP_PATH.user_data / "mariorl" / "checkpoints"

        save_dir = checkpoint_dir / datetime.datetime.now().strftime(
            "%Y-%m-%dT%H-%M-%S"
        )
        save_dir.mkdir(parents=True)

        mario = MarioAgent(
            state_dim=(num_skips, resized_size, resized_size),
            action_dim=env.action_space.n,
            save_dir=save_dir,
            device=device,
        )

        latest_path = latest_file(
            checkpoint_dir, ".chkpt", raise_on_failure=False, recurse=True
        )
        if latest_path and True:
            mario.load(latest_path)

        with PTW(PROJECT_APP_PATH.user_log / "mario") as writer:
            for e in progress_bar(range(episodes)):
                state = env.reset()

                while True:
                    action = mario.act(state)
                    next_state, signal, terminal, info = env.step(action)

                    if train:
                        mario.cache(state, next_state, action, signal, terminal)
                        q, loss = mario.learn()
                        writer.scalar("loss", loss)
                        writer.scalar("Q", q)
                    else:
                        env.render()

                    writer.scalar("signal", signal)

                    state = next_state
                    if terminal or info["flag_get"]:
                        break

    asidjas()
