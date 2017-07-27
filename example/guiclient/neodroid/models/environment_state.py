from typing import Dict

from neodroid.models.actor import Actor
from neodroid.models.observer import Observer

class EnvironmentState(object):
    _time_since_reset: float
    _total_energy_spent_since_reset: float
    _actors: Dict[str,Actor]
    _observers: Dict[str,Observer]
    _reward_for_last_step: float

    def __init__(self, time_since_reset:float=0, total_energy_spent_since_reset=0, actors:Dict={}, observers:Dict={}, reward_for_last_step:float=0):
        self._time_since_reset = time_since_reset
        self._total_energy_spent_since_reset = total_energy_spent_since_reset
        self._actors = actors
        self._observers = observers
        self._reward_for_last_step = reward_for_last_step

    def unpack(self, obj):
    #  if b'_time_since_reset' in obj:
        self._time_since_reset = obj[4]#['_time_since_reset']
    #  if b'_total_energy_spent_since_reset' in obj:
        self._total_energy_spent_since_reset = obj[3]#['_total_energy_spent_since_reset']
    #  if b'_actors' in obj:
        self._actors = {key: Actor(key,actor) for key,actor in obj[0].items()}#['_actors']
    #  if b'_observers' in obj:
        self._observers = {key: Observer(key,observer) for (key,observer) in obj[1].items()}#['_observers']
    #  if b'_reward_for_last_step' in obj:
        self._reward_for_last_step = obj[2]#['_reward_for_last_step']
        return self

    def get_time_since_reset(self) -> float:
        return self._time_since_reset

    def get_total_energy_spent_since_reset(self) -> float:
        return self._total_energy_spent_since_reset

    def get_actors(self) -> Dict:
        return self._actors

    def get_observers(self) -> Dict:
        return self._observers

    def get_reward_for_last_step(self) -> float:
        return self._reward_for_last_step