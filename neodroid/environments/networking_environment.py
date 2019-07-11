#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import logging

from neodroid.interfaces.environment_models import EnvironmentSnapshot
from neodroid.messaging import ClientEvents, message_client_event

__author__ = 'cnheider'

import time
from abc import ABC, abstractmethod

from neodroid import messaging
from .environment import Environment


class NetworkingEnvironment(Environment, ABC):

  def __init__(self,
               *,
               ip='localhost',
               port=6969,
               connect_to_running=False,
               on_connected_callback=None,
               on_disconnected_callback=None,
               on_timeout_callback=None,
               retries=10,
               connect_try_interval=0.1,
               **kwargs):
    super().__init__(**kwargs)

    # Networking
    self._ip = ip
    self._port = port
    self._connect_to_running = connect_to_running
    self._external_on_connected_callback = on_connected_callback
    self._external_on_disconnected_callback = on_disconnected_callback
    self._external_on_timeout_callback = on_timeout_callback
    self._retries = retries
    self._connect_try_interval = connect_try_interval

  def __next__(self) -> EnvironmentSnapshot:
    if not self._is_connected_to_server:
      return
    return self.react()

  def _setup_connection(self, auto_describe=False):
    connect_tries = range(self._retries)

    self._message_server = messaging.MessageClient(self._ip,
                                                   self._port,
                                                   on_timeout_callback=self.__on_timeout_callback__,
                                                   on_connected_callback=self.__on_connected_callback__,
                                                   on_disconnected_callback=self.__on_disconnected_callback__,
                                                   )

    if auto_describe:
      while self.description is None:
        self.describe()
        time.sleep(self._connect_try_interval)
        logging.info(f'Connecting, please make sure that the ip {self._ip} '
                     f'and port {self._port} '
                     f'are cd correct')
        n = next(connect_tries)
        if n == self._retries:
          raise ConnectionError

      self._is_connected_to_server = True
    else:
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

  @abstractmethod
  def _close(self, *args, **kwargs):
    raise NotImplementedError

  def __enter__(self):
    self.reset()
    return self

  def __exit__(self, exc_type, exc_val, exc_tb):
    self.close()

  def close(self, *args, **kwargs):
    self._message_server.teardown()

    return self._close(*args, **kwargs)

  def __repr__(self):
    return (f'<NetworkingEnvironment>\n'
            f'  <IsConnected>{self.is_connected}</IsConnected>\n'
            f'</NetworkingEnvironment>')
