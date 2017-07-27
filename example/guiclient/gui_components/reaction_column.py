from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.slider import Slider


class ReactionColumn(BoxLayout):
  def __init__(self, on_step_callback, on_reset_callback, **kwargs):
    super(ReactionColumn, self).__init__(**kwargs)
    self._on_step_callback = on_step_callback
    self._on_reset_callback = on_reset_callback
    self.build()

  def build(self):
    self.step_button = Button(text='Step')
    self.reset_button = Button(text='Reset')
    self.spacer = Label()
    self.step_button.bind(on_release=self.on_step_button)
    self.reset_button.bind(on_release=self.on_reset_button)

    self.add_widget(self.step_button)
    self.add_widget(self.reset_button)
    self.add_widget(self.spacer)
    return self

  def on_step_button(self, value):
    motions = [
    ]
    self._on_step_callback(motions)

  def on_reset_button(self, value):
    self._on_reset_callback()
