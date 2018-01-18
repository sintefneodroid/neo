from gui import NeoGUI

import neodroid as neo
from neodroid.models import Motion, Reaction
from neodroid.models.configuration import Configuration
from neodroid.models.reaction_parameters import ReactionParameters

_gui = None
_neo_environment = None


def on_connected_callback():
  global _neo_environment
  _gui.update_connect_button('Disconnect')


def on_disconnected_callback():
  _gui.update_connect_button('Connect')


def on_connect_callback(ip_address, port, launch_environment, environment):
  global _neo_environment
  if _neo_environment and _neo_environment.is_connected:
    _neo_environment.close(on_disconnected_callback)
  else:
    _neo_environment = neo.NeodroidEnvironment(ip_address,
                                               int(port),
                                               on_connected_callback=on_connected_callback,
                                               name=environment,
                                               connect_to_running=(
                                                 not launch_environment))


def update_callback(state):
  update_environment_widgets(state)


def on_step_callback(actor_name, slider_values):
  motions = [
    Motion(str(actor_name), str(slider_values[0][0]), slider_values[0][1]),
    Motion(str(actor_name), str(slider_values[1][0]), slider_values[1][1])
    # Motion(str(actor_name), str(slider_values[2][0]), slider_values[2][1]),
    # Motion(str(actor_name), str(slider_values[3][0]), slider_values[3][1])
    ]
  parameters = ReactionParameters(True, True, False, False, False)
  new_state = _neo_environment.react(Reaction(parameters, [], motions))
  update_callback(new_state)


def on_reset_callback(slider_values):
  configurations = [
    Configuration(str(slider_values[0][0]), slider_values[0][1])
    ]
  parameters = ReactionParameters(False, False, True, True, True)
  new_state = _neo_environment.react(Reaction(parameters, configurations, []))
  update_callback(new_state)


def update_environment_widgets(state):
  _gui.update_xml_text_label(str(state))

  try:
    _gui.update_reward_label(str(state.signal))
    _gui.update_energy_label(str(state.total_energy_spent))
    _gui.update_frame_label(str(state.frame_number))
    _gui.update_interrupted_label(str(state.terminated))
    #_gui.update_time_label(str(state.get_time_since_reset))
  except BaseException:
    print('Failed at updating rest of GUI')

  try:

    _gui.update_normal_image(state.observer('NormalCamera').observation_value)
    _gui.update_motion_image(state.observer('FlowCamera').observation_value)
    _gui.update_depth_image(state.observer('DepthCamera').observation_value)
    _gui.update_segmentation_image(state.observer('SegmentationCamera').observation_value)
    _gui.update_instance_segmentation_image(state.observer('InstanceSegmentationCamera').observation_value)
    _gui.update_rgb_image(state.observer('RGBCamera').observation_value)
    _gui.update_infrared_shadow_image(state.observer('InfraredShadowCamera').observation_value)
  except BaseException:
    print('Failed at updating Images')


def main():
  global _gui
  _gui = NeoGUI(on_connect_callback=on_connect_callback,
                on_step_callback=on_step_callback,
                on_reset_callback=on_reset_callback)
  _gui.run()


if __name__ == '__main__':
  main()
