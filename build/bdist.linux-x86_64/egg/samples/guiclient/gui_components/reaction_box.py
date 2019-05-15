#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'cnheider'

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput

from .motion_view import MotionView


class ReactionBox(BoxLayout):

  def __init__(self, on_step_callback, on_reset_callback, **kwargs):
    super().__init__(**kwargs)
    self._on_step_callback = on_step_callback
    self._on_reset_callback = on_reset_callback
    # self.upper_spacer = Label()
    self.actor_input = TextInput(text='Actor')  # , multiline=False)
    self.motor_1 = MotionView('Motor1')
    self.motor_2 = MotionView('Motor2')
    # self.motor_3 = MotionView('ManipulatorSingleAxisZ')
    # self.motor_4 = MotionView('ManipulatorSingleAxisRotX')
    self.step_button = Button(text='Step')
    self.configuration_1 = MotionView('Configurable')
    self.reset_button = Button(text='Reset')
    # self.bottom_spacer = Label()
    self.assemble_components()

  def assemble_components(self):
    self.step_button.bind(on_release=self.on_step_button)
    self.reset_button.bind(on_release=self.on_reset_button)

    # self.add_widget(self.upper_spacer)
    self.add_widget(self.actor_input)
    self.add_widget(self.motor_1)
    self.add_widget(self.motor_2)
    # self.add_widget(self.motor_3)
    # self.add_widget(self.motor_4)
    self.add_widget(self.step_button)
    self.add_widget(self.configuration_1)
    self.add_widget(self.reset_button)
    # self.add_widget(self.bottom_spacer)
    return self

  def on_step_button(self, value):
    motions = [
      (
        str(self.motor_1.motor_input.text),
        float(self.motor_1.motor_slider.value),
        ),
      (str(self.motor_2.motor_input.text), float(self.motor_2.motor_slider.value))
      # (str(self.motor_3.motor_input.text),
      # float(self.motor_3.motor_slider.value)),
      # (str(self.motor_4.motor_input.text),
      # float(self.motor_4.motor_slider.value)),
      ]
    self._on_step_callback(self.actor_input.text, motions)

  def on_reset_button(self, value):
    configurations = [
      (
        str(self.configuration_1.motor_input.text),
        float(self.configuration_1.motor_slider.value),
        )
      ]
    self._on_reset_callback(configurations)
