"""

 multiarmed_bandits.py  (author: Anson Wong / git: ankonzoid)

 We solve the multi-armed bandit problem using a classical epsilon-greedy
 agent with reward-average sampling to estimate the action-value Q.
 This algorithm follows closely with the notation of Sutton's RL textbook.

 We set up up bandits with a fixed probability distribution of success,
 and receive stochastic rewards from the bandits of +1 for success,
 and 0 reward for failure.

 The update rule for our action-values Q is:

   Q(a) <- Q(a) + 1/(k+1) * (R(a) - Q(a))

 where

   Q(a) = current value estimate of action "a"
   k = number of times action "a" was chosen so far
   R(a) = reward of sampling action bandit (bandit) "a"

 The derivation of the above Q incremental implementation update:

   Q(a;k+1)
   = 1/(k+1) * (R(a_1) + R(a_2) + ... + R(a_k) + R(a))
   = 1/(k+1) * (k*Q(a;k) + R(a))
   = 1/(k+1) * ((k+1)*Q(a;k) + R(a) - Q(a;k))
   = Q(a;k) + 1/(k+1) * (R(a) - Q(a;k))

"""
from matplotlib import pyplot
import numpy


def main():
    # =========================
    # Settings
    # =========================
    bandit_probs = [
        0.10,
        0.50,
        0.60,
        0.80,
        0.10,
        0.25,
        0.60,
        0.45,
        0.75,
        0.65,
    ]  # bandit probabilities of success
    N_experiments = 100  # number of experiments to perform
    N_episodes = 10000  # number of episodes per experiment
    epsilon = 0.1  # probability of random exploration (fraction)
    save_fig = True  # if false -> plot, if true save as file in same directory

    # =========================
    # Define Bandit and Agent class
    # =========================
    class Bandit:
        def __init__(self, bandit_probs):
            self.N = len(bandit_probs)  # number of bandits
            self.prob = bandit_probs  # success probabilities for each bandit

        # Get reward (1 for success, 0 for failure)
        def get_reward(self, action):
            rand = numpy.random.random()  # [0.0,1.0)
            reward = 1 if (rand < self.prob[action]) else 0
            return reward

    class Agent:
        def __init__(self, bandit, epsilon):
            self.epsilon = epsilon
            self.k = numpy.zeros(
                bandit.N, dtype=numpy.int
            )  # number of times action was chosen
            self.Q = numpy.zeros(bandit.N, dtype=numpy.float)  # estimated value

        # Update Q action-value using:
        # Q(a) <- Q(a) + 1/(k+1) * (r(a) - Q(a))
        def update_Q(self, action, reward):
            self.k[action] += 1  # update action counter k -> k+1
            self.Q[action] += (1.0 / self.k[action]) * (reward - self.Q[action])

        # Choose action using an epsilon-greedy agent
        def get_action(self, bandit, force_explore=False):
            rand = numpy.random.random()  # [0.0,1.0)
            if (rand < self.epsilon) or force_explore:
                action_explore = numpy.random.randint(bandit.N)  # explore random bandit
                return action_explore
            else:
                # action_greedy = numpy.argmax(self.Q)  # exploit best current bandit
                action_greedy = numpy.random.choice(
                    numpy.flatnonzero(self.Q == self.Q.max())
                )
                return action_greedy

    # =========================
    # Define an experiment
    # =========================
    def experiment(agent, bandit, N_episodes):
        action_history = []
        reward_history = []
        for episode in range(N_episodes):
            # Choose action from agent (from current Q estimate)
            action = agent.get_action(bandit)
            # Pick up reward from bandit for chosen action
            reward = bandit.get_reward(action)
            # Update Q action-value estimates
            agent.update_Q(action, reward)
            # Append to history
            action_history.append(action)
            reward_history.append(reward)
        return numpy.array(action_history), numpy.array(reward_history)

    # =========================
    #
    # Start multi-armed bandit simulation
    #
    # =========================
    N_bandits = len(bandit_probs)
    print(
        f"Running multi-armed bandits with N_bandits = {N_bandits} and agent epsilon = {epsilon}"
    )
    reward_history_avg = numpy.zeros(N_episodes)  # reward history experiment-averaged
    action_history_sum = numpy.zeros((N_episodes, N_bandits))  # sum action history
    for i in range(N_experiments):
        bandit = Bandit(bandit_probs)  # initialize bandits
        agent = Agent(bandit, epsilon)  # initialize agent
        (action_history, reward_history) = experiment(
            agent, bandit, N_episodes
        )  # perform experiment

        if (i + 1) % (N_experiments / 100) == 0:
            print(f"[Experiment {i + 1}/{N_experiments}]")
            print(f"  N_episodes = {N_episodes}")
            print(f"  bandit choice history = {action_history + 1}")
            print(f"  reward history = {reward_history}")
            print(
                f"  average reward = {numpy.sum(reward_history) / len(reward_history)}"
            )
            print("")
        # Sum up experiment reward (later to be divided to represent an average)
        reward_history_avg += reward_history
        # Sum up action history
        for j, (a) in enumerate(action_history):
            action_history_sum[j][a] += 1

    reward_history_avg /= numpy.float(N_experiments)
    print(f"reward history avg = {reward_history_avg}")

    # =========================
    # Plot reward history results
    # =========================
    pyplot.plot(reward_history_avg)
    pyplot.xlabel("Episode number")
    pyplot.ylabel(f"Rewards collected")
    pyplot.title(
        f"Bandit reward history averaged over {N_experiments} experiments (epsilon = {epsilon})"
    )
    ax = pyplot.gca()
    ax.set_xscale("log", nonposx="clip")
    pyplot.xlim([1, N_episodes])
    if save_fig:
        output_file = "output/rewards.png"
        pyplot.savefig(output_file, bbox_inches="tight")
    else:
        pyplot.show()

    # =========================
    # Plot action history results
    # =========================
    pyplot.figure(figsize=(18, 12))
    for i in range(N_bandits):
        action_history_sum_plot = 100 * action_history_sum[:, i] / N_experiments
        pyplot.plot(
            list(numpy.array(range(len(action_history_sum_plot))) + 1),
            action_history_sum_plot,
            linewidth=5.0,
            label=f"Bandit #{i + 1}",
        )
    pyplot.title(
        f"Bandit action history averaged over {N_experiments} experiments (epsilon = {epsilon})",
        fontsize=26,
    )
    pyplot.xlabel("Episode Number", fontsize=26)
    pyplot.ylabel("Bandit Action Choices (%)", fontsize=26)
    leg = pyplot.legend(loc="upper left", shadow=True, fontsize=26)
    ax = pyplot.gca()
    ax.set_xscale("log", nonposx="clip")
    pyplot.xlim([1, N_episodes])
    pyplot.ylim([0, 100])
    pyplot.xticks(fontsize=24)
    pyplot.yticks(fontsize=24)
    for legobj in leg.legendHandles:
        legobj.set_linewidth(16.0)
    if save_fig:
        output_file = "output/actions.png"
        pyplot.savefig(output_file, bbox_inches="tight")
    else:
        pyplot.show()


# Driver
if __name__ == "__main__":
    main()
