from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.slider import Slider


class XMLColumn(BoxLayout):
  def __init__(self, **kwargs):
    super(XMLColumn, self).__init__(**kwargs)
    self.build()

  def build(self):
    self.text_label = Label()

    self.add_widget(self.text_label)
    return self

  def update_text_label(self, val):
    self.text_label.text = val