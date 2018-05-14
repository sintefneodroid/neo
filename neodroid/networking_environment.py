import time
import warnings

from neodroid import messaging
from neodroid.environment import Environment
from neodroid.utilities.debug import ClientEvents, message_client_event

WAIT_TIME = 0.2

class NetworkingEnvironment(Environment):

  def __init__(self,
               *,
               ip='localhost',
               port=6969,
               connect_to_running=False,
               on_connected_callback=None,
               on_disconnected_callback=None,
               on_timeout_callback=None,
               **kwargs):
    super().__init__(**kwargs)

    # Networking
    self._ip = ip
    self._port = port
    self._connect_to_running = connect_to_running
    self._external_on_connected_callback = on_connected_callback
    self._external_on_disconnected_callback = on_disconnected_callback
    self._external_on_timeout_callback = on_timeout_callback

  def __next__(self):
    if not self._is_connected_to_server:
      return
    return self._react()

  def _setup_connection(self):
    warnings.warn('Connecting to server')

    self._message_server = messaging.MessageClient(
        self._ip,
        self._port,
        on_timeout_callback=self.__on_timeout_callback__,
        on_connected_callback=self.__on_connected_callback__,
        on_disconnected_callback=self.__on_disconnected_callback__,
        verbose=self._verbose)

    while self.description is None:
      print('.')
      self._reset()
      time.sleep(WAIT_TIME)

    self._is_connected_to_server = True

  @message_client_event(event=ClientEvents.CONNECTED)
  def __on_connected_callback__(self):
    '''

'''
    if self._external_on_connected_callback:
      self._external_on_connected_callback()

  @message_client_event(event=ClientEvents.DISCONNECTED)
  def __on_disconnected_callback__(self):
    '''

'''
    self._is_connected_to_server = False
    if self._external_on_disconnected_callback:
      self._external_on_disconnected_callback()

  @message_client_event(event=ClientEvents.TIMEOUT)
  def __on_timeout_callback__(self):
    '''

'''
    if self._external_on_timeout_callback:
      self._external_on_timeout_callback()

  @property
  def is_connected(self):
    return self._is_connected_to_server

  def __str__(self):
    return f'<NetworkingEnvironment>\n' \
           f'  <ObservationSpace>{self.observation_space}</ObservationSpace>\n' \
           f'  <ActionSpace>{self.action_space}</ActionSpace>\n' \
           f'  <Description>{self.description}</Description>\n' \
           f'  <IsConnected>{self.is_connected}</IsConnected>\n' \
           f'</NetworkingEnvironment>'
