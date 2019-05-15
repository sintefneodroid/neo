#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'cnheider'

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.slider import Slider
from kivy.uix.textinput import TextInput


class MotionView(BoxLayout):

  def __init__(self, initial_text='Motor', **kwargs):
    super().__init__(**kwargs)
    self.motor_input = TextInput(text=initial_text)  # , multiline=False)
    self.motor_slider = Slider(min=-100, max=100, value=0)
    self.motor_value = TextInput(text='0.0')  # , multiline=False)
    self.assemble_components()

  def assemble_components(self):
    self.motor_slider.bind(value=self.on_slider_value_change)
    self.motor_value.bind(text=self.on_text_value_change)
    self.add_widget(self.motor_input)
    self.add_widget(self.motor_slider)
    self.add_widget(self.motor_value)
    return self

  def on_text_value_change(self, instance, value):
    self.motor_slider.value = float(self.motor_value.text)

  def on_slider_value_change(self, instance, value):
    self.motor_value.text = str(self.motor_slider.value)
