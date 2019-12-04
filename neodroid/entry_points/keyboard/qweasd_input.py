#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from neodroid.environments.unity_environment import SingleUnityEnvironment
from warg.named_ordered_dictionary import NOD

__author__ = "Christian Heider Nielsen"

from pynput import keyboard


def up():
    if "ActorY_" in ENVIRONMENT.description.actuators:
        return {"ActorY_": ENVIRONMENT.description.actuator("ActorY_").motion_space.max}
    raise KeyError(f"Could not find actuator ActorY_")


def down():
    if "ActorY_" in ENVIRONMENT.description.actuators:
        return {"ActorY_": ENVIRONMENT.description.actuator("ActorY_").motion_space.min}
    raise KeyError(f"Could not find actuator ActorY_")


def left():
    if "ActorX_" in ENVIRONMENT.description.actuators:
        return {"ActorX_": ENVIRONMENT.description.actuator("ActorX_").motion_space.min}
    raise KeyError(f"Could not find actuator ActorX_")


def right():
    if "ActorX_" in ENVIRONMENT.description.actuators:
        return {"ActorX_": ENVIRONMENT.description.actuator("ActorX_").motion_space.max}
    raise KeyError(f"Could not find actuator ActorX_")


def backward():
    if "ActorZ_" in ENVIRONMENT.description.actuators:
        return {"ActorZ_": ENVIRONMENT.description.actuator("ActorZ_").motion_space.min}
    raise KeyError(f"Could not find actuator ActorZ_")


def forward():
    if "ActorZ_" in ENVIRONMENT.description.actuators:
        return {"ActorZ_": ENVIRONMENT.description.actuator("ActorZ_").motion_space.max}
    raise KeyError(f"Could not find actuator ActorZ_")


def reset():
    return "reset"


ENVIRONMENT = SingleUnityEnvironment(connect_to_running=True)
ENVIRONMENT.reset()

CURRENT_COMBINATIONS = set()  # The currently active modifiers
STEP_I = 0
AUTO_RESET = False

COMBINATIONS = {
    keyboard.KeyCode(char="q"): down,
    keyboard.KeyCode(char="w"): forward,
    keyboard.KeyCode(char="e"): up,
    keyboard.KeyCode(char="a"): right,
    keyboard.KeyCode(char="s"): backward,
    keyboard.KeyCode(char="d"): left,
    keyboard.KeyCode(char="x"): exit,
    keyboard.KeyCode(char="r"): reset,
}


def listen_for_combinations():
    print(f"\n\nPress any of:\n{COMBINATIONS}\n\n")
    print("")
    return keyboard.Listener(on_press=on_press, on_release=on_release)


def on_press(key):
    global STEP_I
    if any([key in COMBINATIONS]):
        if key not in CURRENT_COMBINATIONS:
            CURRENT_COMBINATIONS.add(key)
        actions = COMBINATIONS[key]()
        terminated = False
        signal = 0

        if ENVIRONMENT.is_connected:
            if actions == "reset":
                obs = ENVIRONMENT.reset()
                STEP_I = 0
            else:
                obs, signal, terminated, _ = ENVIRONMENT.react(
                    actions
                ).to_gym_like_output()
            STEP_I += 1
            print(NOD.nod_of(STEP_I, obs, signal, terminated).as_dict())

            if AUTO_RESET and terminated:
                ENVIRONMENT.reset()
                STEP_I = 0


def on_release(key):
    if any([key in COMBINATIONS]):
        if key in CURRENT_COMBINATIONS:
            CURRENT_COMBINATIONS.remove(key)


def main():
    with listen_for_combinations() as listener:
        listener.join()


if __name__ == "__main__":

    main()
