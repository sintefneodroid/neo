#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "heider"
__doc__ = r"""

           Created on 8/3/22
           """

__all__ = []


def aisjd():
    from omni.isaac.kit import SimulationApp

    # Set rendering parameters and create an instance of kit
    CONFIG = {
        "renderer": "RayTracedLighting",
        "headless": True,
        "width": 1024,
        "height": 1024,
        "num_frames": 10,
    }
    STAGE = "/Isaac/Environments/Simple_Warehouse/full_warehouse.usd"

    kit = SimulationApp(launch_config=CONFIG)


def uhasd():
    import isaacgymenvs
    import torch

    envs = isaacgymenvs.make(
        seed=0,
        task="Ant",
        num_envs=2000,
        sim_device="cuda:0",
        rl_device="cuda:0",
    )
    print("Observation space is", envs.observation_space)
    print("Action space is", envs.action_space)
    obs = envs.reset()
    for _ in range(20):
        obs, reward, done, info = envs.step(
            torch.rand((2000,) + envs.action_space.shape, device="cuda:0")
        )


def uiahsduhasd():
    import gym
    import isaacgymenvs
    import torch

    envs = isaacgymenvs.make(
        seed=0,
        task="Ant",
        num_envs=20,
        sim_device="cuda:0",
        rl_device="cuda:0",
        graphics_device_id=0,
        headless=False,
        multi_gpu=False,
        virtual_screen_capture=True,
        force_render=False,
    )
    envs.is_vector_env = True
    envs = gym.wrappers.RecordVideo(
        envs,
        "./videos",
        step_trigger=lambda step: step % 10000
        == 0,  # record the videos every 10000 steps
        video_length=100,  # for each video record up to 100 steps
    )
    envs.reset()
    print(
        "the image of Isaac Gym viewer is an array of shape",
        envs.render(mode="rgb_array").shape,
    )
    for _ in range(100):
        envs.step(torch.rand((20,) + envs.action_space.shape, device="cuda:0"))


def uhasduh():
    # launch Isaac Sim before any other imports
    # default first two lines in any standalone application
    from omni.isaac.kit import SimulationApp

    simulation_app = SimulationApp({"headless": False})  # we can also run as headless.

    from omni.isaac.core import World
    from omni.isaac.core.objects import DynamicCuboid
    import numpy as np

    world = World()
    world.scene.add_default_ground_plane()
    fancy_cube = world.scene.add(
        DynamicCuboid(
            prim_path="/World/random_cube",
            name="fancy_cube",
            position=np.array([0, 0, 1.0]),
            size=np.array([0.5015, 0.5015, 0.5015]),
            color=np.array([0, 0, 1.0]),
        )
    )
    # Resetting the world needs to be called before querying anything related to an articulation specifically.
    # Its recommended to always do a reset after adding your assets, for physics handles to be propagated properly
    world.reset()
    for i in range(500):
        position, orientation = fancy_cube.get_world_pose()
        linear_velocity = fancy_cube.get_linear_velocity()
        # will be shown on terminal
        print("Cube position is : " + str(position))
        print("Cube's orientation is : " + str(orientation))
        print("Cube's linear velocity is : " + str(linear_velocity))
        # we have control over stepping physics and rendering in this workflow
        # things run in sync
        world.step(render=True)  # execute one physics step and one rendering step

    simulation_app.close()  # close Isaac Sim


def ijsad():
    import getpass

    user = getpass.getuser()
    from omni.isaac.kit import SimulationApp

    # Set the path below to your desired nucleus server
    # Make sure you installed a local nucleus server before this
    simulation_app = SimulationApp(
        {"livesync_usd": f"omniverse://localhost/Users/{user}/temp_jupyter_stage.usd"}
    )


def aisjasdd():
    from omni.isaac.cloner import Cloner  # import Cloner interface
    from omni.isaac.core.utils.stage import get_current_stage
    from pxr import UsdGeom

    # create our base environment with one cube
    base_env_path = "/World/Cube_0"
    UsdGeom.Cube.Define(get_current_stage(), base_env_path)

    # create a Cloner instance
    cloner = Cloner()

    # generate 4 paths that begin with "/World/Cube" - path will be appended with _{index}
    target_paths = cloner.generate_paths("/World/Cube", 4)

    # clone the cube at target paths
    cloner.clone(source_prim_path="/World/Cube_0", prim_paths=target_paths)


def iajsd():
    import isaacgymenvs
    import torch

    envs = isaacgymenvs.make(
        seed=0,
        task="Ant",
        num_envs=2000,
        sim_device="cuda:0",
        rl_device="cuda:0",
    )
    print("Observation space is", envs.observation_space)
    print("Action space is", envs.action_space)
    obs = envs.reset()
    for _ in range(20):
        obs, reward, done, info = envs.step(
            torch.rand((2000,) + envs.action_space.shape, device="cuda:0")
        )
