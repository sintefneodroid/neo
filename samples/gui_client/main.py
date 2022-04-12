#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from neodroid.environments.droid_environment import DictUnityEnvironment
from neodroid.utilities.specifications.unity_specifications import (
    Configuration,
    Motion,
    Reaction,
    ReactionParameters,
)

__author__ = "Christian Heider Nielsen"
__doc__ = r"""
"""

from gui import NeoGUI

GUI = None
NEODROID_ENVIRONMENT = None


def on_connected_callback():
    global NEODROID_ENVIRONMENT
    GUI.update_connect_button("Disconnect")


def on_disconnected_callback():
    GUI.update_connect_button("Connect")


def on_connect_callback(ip_address, port, launch_environment, environment):
    global NEODROID_ENVIRONMENT
    if NEODROID_ENVIRONMENT and NEODROID_ENVIRONMENT.is_connected:
        NEODROID_ENVIRONMENT.close(on_disconnected_callback)
    else:
        NEODROID_ENVIRONMENT = DictUnityEnvironment(
            ip=ip_address,
            port=int(port),
            on_connected_callback=on_connected_callback,
            connect_to_running=(not launch_environment),
        )


def update_callback(state):
    update_environment_widgets(state)


def on_step_callback(actor_name, slider_values):
    motions = [
        Motion(str(actor_name), str(slider_values[0][0]), slider_values[0][1]),
        Motion(str(actor_name), str(slider_values[1][0]), slider_values[1][1])
        # Motion(str(actor_name), str(slider_values[2][0]), slider_values[2][1]),
        # Motion(str(actor_name), str(slider_values[3][0]), slider_values[3][1])
    ]
    parameters = ReactionParameters(
        terminable=True,
        step=True,
        reset=False,
        configure=False,
        describe=False,
        episode_count=True,
    )
    new_state = NEODROID_ENVIRONMENT.react(
        Reaction(motions=motions, parameters=parameters)
    )
    update_callback(new_state)


def on_reset_callback(slider_values):
    configurations = [Configuration(str(slider_values[0][0]), slider_values[0][1])]
    parameters = ReactionParameters(
        terminable=False, step=False, reset=True, configure=True, describe=True
    )
    new_state = NEODROID_ENVIRONMENT.react(
        Reaction(parameters=parameters, configurations=configurations)
    )
    update_callback(new_state)


def update_environment_widgets(state):
    GUI.update_xml_text_label(str(state))

    try:
        GUI.update_reward_label(str(state.signal))
        GUI.update_energy_label(str(state.total_energy_spent))
        GUI.update_frame_label(str(state.frame_number))
        GUI.update_interrupted_label(str(state.terminated))
        # _gui.update_time_label(str(state.get_time_since_reset))
    except BaseException:
        print("Failed at updating rest of GUI")

    try:

        GUI.update_normal_image(state.sensor("NormalCamera").value)
        GUI.update_motion_image(state.sensor("FlowCamera").value)
        GUI.update_depth_image(state.sensor("DepthCamera").value)
        GUI.update_segmentation_image(state.sensor("SegmentationCamera").value)
        GUI.update_instance_segmentation_image(
            state.sensor("InstanceSegmentationCamera").value
        )
        GUI.update_rgb_image(state.sensor("RGBCamera").value)
        GUI.update_infrared_shadow_image(state.sensor("InfraredShadowCamera").value)
    except BaseException:
        print("Failed at updating Images")


def main():
    global GUI
    GUI = NeoGUI(
        on_connect_callback=on_connect_callback,
        on_step_callback=on_step_callback,
        on_reset_callback=on_reset_callback,
    )
    GUI.run()


if __name__ == "__main__":
    main()
