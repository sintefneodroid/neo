#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'cnheider'

from kivy.core.image import Image as CoreImage
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.label import Label


class EnvironmentStateBox(BoxLayout):

  def __init__(self, **kwargs):
    super().__init__(**kwargs)

    self.depth_image = Image(source='images/default.png')
    self.segmentation_image = Image(source='images/default.png')
    self.normal_image = Image(source='images/default.png')
    self.motion_image = Image(source='images/default.png')
    self.instance_segmentation_image = Image(source='images/default.png')
    self.rgb_image = Image(source='images/default.png')
    self.infrared_shadow_image = Image(source='images/default.png')

    self.reward_label = Label(text='Reward: ', size_hint=(1.0, 0.05))
    self.energy_label = Label(
        text='Energy Spent Since Reset: ', size_hint=(1.0, 0.05)
        )
    self.time_label = Label(text='Time Since Reset: ', size_hint=(1.0, 0.05))
    self.frame_label = Label(text='Frame: ', size_hint=(1.0, 0.05))
    self.interrupted_label = Label(text='Interrupted: ', size_hint=(1.0, 0.05))

    # self.direction_label = Label(text='Direction: ', size_hint=(1.0, 0.05))
    # self.position_label = Label(text='Position: ', size_hint=(1.0, 0.05))
    # self.rotation_label = Label(text='Rotation: ', size_hint=(1.0, 0.05))

    self.image_row_layout = BoxLayout(orientation='horizontal')
    self.assemble_components()

  def assemble_components(self):

    self.image_row_layout.add_widget(self.rgb_image)
    self.image_row_layout.add_widget(self.segmentation_image)
    self.image_row_layout.add_widget(self.instance_segmentation_image)
    self.image_row_layout.add_widget(self.depth_image)
    self.image_row_layout.add_widget(self.infrared_shadow_image)
    self.image_row_layout.add_widget(self.normal_image)
    self.image_row_layout.add_widget(self.motion_image)

    self.add_widget(self.image_row_layout)

    # self.add_widget(self.position_label)
    # self.add_widget(self.rotation_label)
    # self.add_widget(self.direction_label)

    self.add_widget(self.frame_label)
    self.add_widget(self.interrupted_label)
    self.add_widget(self.reward_label)
    self.add_widget(self.energy_label)
    self.add_widget(self.time_label)

    return self

  def update_depth_image(self, depth_image_data):
    try:
      depth_image = CoreImage(depth_image_data, ext='png')
      self.depth_image.texture = depth_image.texture
    except BaseException:
      print('Image not valid')

  def update_normal_image(self, normal_image_data):
    try:
      normal_image = CoreImage(normal_image_data, ext='png')
      self.normal_image.texture = normal_image.texture
    except BaseException:
      print('Image not valid')

  def update_motion_image(self, motion_image_data):
    try:
      motion_image = CoreImage(motion_image_data, ext='png')
      self.motion_image.texture = motion_image.texture
    except BaseException:
      print('Image not valid')

  def update_segmentation_image(self, segmentation_image_data):
    try:
      segmentation_image = CoreImage(segmentation_image_data, ext='png')
      self.segmentation_image.texture = segmentation_image.texture
    except BaseException:
      print('Image not valid')

  def update_instance_segmentation_image(self, instance_segmentation_image_data):
    try:

      instance_segmentation_image = CoreImage(
          instance_segmentation_image_data, ext='png'
          )
      self.instance_segmentation_image.texture = instance_segmentation_image.texture
    except BaseException:
      print('Image not valid')

  def update_infrared_shadow_image(self, infrared_shadow_image_data):
    try:
      infrared_shadow_image = CoreImage(infrared_shadow_image_data, ext='png')
      self.infrared_shadow_image.texture = infrared_shadow_image.texture
    except BaseException:
      print('Image not valid')

  def update_rgb_image(self, rgb_image_data):
    try:
      rgb_image = CoreImage(rgb_image_data, ext='png')
      self.rgb_image.texture = rgb_image.texture
    except BaseException:
      print('Image not valid')

  def update_reward_label(self, value: str):
    self.reward_label.text = 'Reward: ' + value

  def update_frame_label(self, value: str):
    self.frame_label.text = 'Frame: ' + value

  def update_interrupted_label(self, value: str):
    self.interrupted_label.text = 'Interrupted: ' + value

  def update_energy_label(self, value: str):
    self.energy_label.text = 'Energy Spent Since Reset: ' + value

  def update_time_label(self, value: str):
    self.time_label.text = 'Time Since Reset: ' + value

  def update_direction_label(self, value: str):
    pass
    # self.direction_label.text = 'Direction: ' + value

  def update_position_label(self, value: str):
    pass
    # self.position_label.text = 'Position: ' + value

  def update_rotation_label(self, value: str):
    pass
    # self.rotation_label.text = 'Rotation: ' + value
