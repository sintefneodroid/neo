#!/usr/bin/env python3 
# -*- coding: utf-8 -*-
__author__ = 'cnheider'

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput


class XMLBox(BoxLayout):

  def __init__(self, **kwargs):
    super().__init__(**kwargs)
    self.text_label = TextInput(font_size=12)
    self.assemble_components()

  def assemble_components(self):
    self.add_widget(self.text_label)
    return self

  def update_text_label(self, val):
    self.text_label.text = val
