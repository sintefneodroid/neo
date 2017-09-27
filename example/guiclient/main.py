import neodroid as neo
from gui import NeoGUI
from neodroid.models import Reaction, EnvironmentState, Motion
from utilities import get_masked_depth_image

_gui = None
_neo_environment = None


def on_connected_callback():
  global _neo_environment
  _gui.update_connect_button('Disconnect')
  #state = _neo_environment.get_environment()
  #print(state)
  #update_callback(state)


def on_disconnected_callback():
  global _stream
  _stream = None
  _gui.update_connect_button('Connect')


def on_connect_callback(ip_address, port, launch_environment, environment):
  global _neo_environment
  if _neo_environment and _neo_environment.is_connected():
    _neo_environment.close(on_disconnected_callback)
  else:
    _neo_environment = neo.NeodroidEnvironment(ip_address, int(port), on_connected_callback=on_connected_callback, name=environment, connect_to_running=(not launch_environment))


def update_callback(state):
  update_environment_widgets(state)


def on_step_callback(actor_name, slider_values):
  motions = [
    Motion(str(actor_name), str(slider_values[0][0]), slider_values[0][1]),
    Motion(str(actor_name), str(slider_values[1][0]), slider_values[1][1]),
    Motion(str(actor_name), str(slider_values[2][0]), slider_values[2][1]),
    Motion(str(actor_name), str(slider_values[3][0]), slider_values[3][1])
  ]
  new_state = _neo_environment.step(Reaction(False, motions))
  update_callback(new_state)

def on_reset_callback():
  new_state = _neo_environment.step(Reaction(True, []))
  update_callback(new_state)


def update_environment_widgets(environment_state):
  try:
    _gui.update_xml_text_label(str(environment_state))
    _gui.update_position_label(str(environment_state.get_actors()[0].get_position()))
    _gui.update_rotation_label(str(environment_state.get_actors()[0].get_rotation()))
    _gui.update_reward_label(str(environment_state.get_reward_for_last_step()))
    _gui.update_energi_label(str(environment_state.get_total_energy_spent_since_reset()))
    _gui.update_time_label(str(environment_state.get_time_since_reset()))
  except:
    print('Failed at updating rest of GUI')

  try:
    _gui.update_depth_image(environment_state.get_observers()[1].get_data())
    _gui.update_segmentation_image(environment_state.get_observers()[2].get_data())
    _gui.update_instance_segmentation_image(environment_state.get_observers()[3].get_data())
    _gui.update_rgb_image(environment_state.get_observers()[4].get_data())
    _gui.update_infrared_shadow_image(environment_state.get_observers()[5].get_data())
    #combined_image = get_masked_depth_image(environment_state.get_observers()[0].get_data(),                             #           environment_state.get_observers()[1].get_data(), 50, 200)
    #_gui.update_combined_image(combined_image)
  except:
    print('Failed at updating Images')


def main():
  global _gui
  _gui = NeoGUI(on_connect_callback=on_connect_callback,
                on_step_callback=on_step_callback,
                on_reset_callback=on_reset_callback)
  _gui.run()


if __name__ == '__main__':
  main()
