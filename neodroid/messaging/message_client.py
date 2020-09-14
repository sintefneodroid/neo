#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import logging
from contextlib import suppress

import zmq

from neodroid.messaging.fbs import FStates, deserialise_states, serialise_reactions

__author__ = "Christian Heider Nielsen"


# @singleton
class MessageClient(object):
    """

"""

    def __init__(
        self,
        tcp_address="localhost",
        tcp_port=6969,
        on_timeout_callback=None,
        on_step_done_callback=None,
        on_connected_callback=None,
        on_disconnected_callback=None,
        single_threaded=False,
        writer=logging.info,
    ):

        self._tcp_address = tcp_address
        self._tcp_port = tcp_port

        self._use_ipc_medium = False
        self._expecting_response = False
        self._socket_type = zmq.REQ
        # self._socket_type = zmq.PAIR

        self._on_timeout_callback = on_timeout_callback
        self._on_connected_callback = on_connected_callback
        self._on_step_done = on_step_done_callback
        self._on_disconnected_callback = on_disconnected_callback
        self._writer = writer

        if single_threaded:
            self.build(single_threaded)

        self._context = None
        self._poller = None
        self._request_socket = None

        self.REQUEST_TIMEOUT = 8000  # Milliseconds
        self.REQUEST_RETRIES = 9

        self.LAST_RECEIVED_FRAME_NUMBER = 0

    def open_connection(self):
        """

"""
        self._request_socket = self._context.socket(self._socket_type)

        if not self._request_socket:
            raise RuntimeError("Failed to create ZMQ socket!")

        if self._writer:
            self._writer(
                f"Connecting to server at {self._tcp_address}:{self._tcp_port}"
            )

        if self._use_ipc_medium:
            self._request_socket.connect("ipc:///tmp/neodroid/messages")
            if self._writer:
                self._writer("Using IPC protocol")
        else:
            self._request_socket.connect(f"tcp://{self._tcp_address}:{self._tcp_port}")
            if self._writer:
                self._writer("Using TCP protocol")

        self._on_connected_callback()

        self._poller = zmq.Poller()
        self._poller.register(self._request_socket, zmq.POLLIN)

    def close_connection(self):
        """

"""
        with suppress(zmq.error.ZMQError):
            # if not self._request_socket.closed:
            self._request_socket.setsockopt(zmq.LINGER, 0)
            self._request_socket.close()
            self._poller.unregister(self._request_socket)
            # self._poller.close()

    def teardown(self):
        """

"""
        self.close_connection()
        self._context.term()

    def build(self, single_threaded=False):
        """

@param single_threaded:
@type single_threaded:
"""
        if single_threaded:
            self._context = zmq.Context.instance()

            if not self._context:
                raise RuntimeError("Failed to create ZMQ context!")
        else:
            self._context = zmq.Context()

        self.open_connection()

    def send_receive(self, reactions):
        """

@param reactions:
@type reactions:
@return:
@rtype:
"""
        if self._request_socket is None:
            self.build()

        if not self._expecting_response:
            serialised_reaction = serialise_reactions(reactions)
            self._request_socket.send(serialised_reaction)
            self._expecting_response = True

            retries_left = self.REQUEST_RETRIES

            while self._expecting_response:
                sockets = dict(self._poller.poll(self.REQUEST_TIMEOUT))

                if sockets.get(self._request_socket):
                    response = self._request_socket.recv()
                    if not response:  # or len(response)<4:
                        continue

                    self._expecting_response = False

                    flat_buffer_states = FStates.GetRootAsFStates(response, 0)

                    states, simulator_configuration = deserialise_states(
                        flat_buffer_states
                    )
                    # if LAST_RECEIVED_FRAME_NUMBER==states.frame_number:
                    #  self._writer(f'Received a duplicate frame on frame number: {states.frame_number}')
                    # LAST_RECEIVED_FRAME_NUMBER=states.frame_number

                    return states, simulator_configuration

                else:
                    if self._on_timeout_callback:
                        self._on_timeout_callback()
                    self.close_connection()
                    retries_left -= 1

                    if retries_left <= 0:
                        if self._writer:
                            self._writer("Out of retries, tearing down client")
                        self.teardown()
                        if self._on_disconnected_callback:
                            self._on_disconnected_callback()
                        raise ConnectionError
                    else:
                        if self._writer:
                            self._writer(
                                f"Retrying to connect, attempt: {retries_left:d}/{self.REQUEST_RETRIES:d}"
                            )
                        self.open_connection()
                        self._request_socket.send(serialised_reaction)

            if self._on_step_done:
                self._on_step_done()
