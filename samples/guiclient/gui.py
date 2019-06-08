#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from .gui_components import EnvironmentStateBox, ReactionBox, StatusBar, XMLBox

__author__ = 'cnheider'

from kivy.app import App
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout


class NeoGUI(App):

  def __init__(
      self, on_step_callback, on_reset_callback, on_connect_callback, **kwargs
      ):
    super().__init__(**kwargs)
    self._on_step_callback = on_step_callback
    self._on_reset_callback = on_reset_callback
    self._on_connect_callback = on_connect_callback
    Window.clearcolor = (1, 1, 1, 1)

    self.parent_rows = BoxLayout(orientation='vertical')
    self.columns = BoxLayout(orientation='horizontal')
    self.inner_rows = BoxLayout(orientation='vertical')

    # Upper Part(Columns)
    self.xml_column = XMLBox(size_hint=(0.5, 1.0))
    self.state_box = EnvironmentStateBox(orientation='vertical')
    self.reaction_column = ReactionBox(
        on_step_callback=self._on_step_callback,
        on_reset_callback=self._on_reset_callback,
        orientation='vertical',
        # size_hint=(0.2,1.0),
        spacing=10,
        padding=10,
        )

    # Status Bar

    self.status_bar = StatusBar(
        on_connect_callback=self._on_connect_callback,
        orientation='horizontal',
        size_hint=(1.0, 0.05),
        )

  def build(self):
    self.inner_rows.add_widget(self.state_box)
    self.inner_rows.add_widget(self.reaction_column)
    self.columns.add_widget(self.xml_column)
    self.columns.add_widget(self.inner_rows)
    self.parent_rows.add_widget(self.columns)

    self.parent_rows.add_widget(self.status_bar)
    return self.parent_rows

  def update_depth_image(self, depth_image):
    self.state_box.update_depth_image(depth_image)

  def update_normal_image(self, normal_image):
    self.state_box.update_normal_image(normal_image)

  def update_motion_image(self, motion_image):
    self.state_box.update_motion_image(motion_image)

  def update_segmentation_image(self, segmentation_image):
    self.state_box.update_segmentation_image(segmentation_image)

  def update_instance_segmentation_image(self, instance_segmentation_image):
    self.state_box.update_instance_segmentation_image(instance_segmentation_image)

  def update_infrared_shadow_image(self, infrared_shadow_image):
    self.state_box.update_infrared_shadow_image(infrared_shadow_image)

  def update_rgb_image(self, rgb_image):
    self.state_box.update_rgb_image(rgb_image)

  def update_position_label(self, value: str):
    self.state_box.update_position_label(value)

  def update_rotation_label(self, value: str):
    self.state_box.update_rotation_label(value)

  def update_reward_label(self, value: str):
    self.state_box.update_reward_label(value)

  def update_energy_label(self, value: str):
    self.state_box.update_energy_label(value)

  def update_frame_label(self, value: str):
    self.state_box.update_frame_label(value)

  def update_interrupted_label(self, value: str):
    self.state_box.update_interrupted_label(value)

  def update_direction_label(self, value: str):
    self.state_box.update_direction_label(value)

  def update_time_label(self, value: str):
    self.state_box.update_time_label(value)

  def update_connect_button(self, value: str):
    self.status_bar.update_connect_button(value)

  def update_xml_text_label(self, value: str):
    self.xml_column.update_text_label(value)
