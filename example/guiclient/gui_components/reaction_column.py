from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.slider import Slider
from kivy.uix.textinput import TextInput


class ReactionColumn(BoxLayout):
  def __init__(self, on_step_callback, on_reset_callback, **kwargs):
    super(ReactionColumn, self).__init__(**kwargs)
    self._on_step_callback = on_step_callback
    self._on_reset_callback = on_reset_callback
    self.build()

  def build(self):
    self.step_button = Button(text='Step')
    self.reset_button = Button(text='Reset')
    self.actor_input = TextInput(text="Player")
    self.motor_1_input = TextInput(text="PlayerX")
    self.motor_1_slider = Slider(min=-100, max=100, value=0)
    self.motor_2_input = TextInput(text="PlayerY")
    self.motor_2_slider = Slider(min=-100, max=100, value=0)
    self.motor_3_input = TextInput(text="PlayerZ")
    self.motor_3_slider = Slider(min=-100, max=100, value=0)
    self.motor_4_input = TextInput(text="PlayerRotX")
    self.motor_4_slider = Slider(min=-100, max=100, value=0)
    self.spacer = Label()
    self.step_button.bind(on_release=self.on_step_button)
    self.reset_button.bind(on_release=self.on_reset_button)

    self.add_widget(self.actor_input)
    self.add_widget(self.step_button)
    self.add_widget(self.reset_button)
    self.add_widget(self.motor_1_input)
    self.add_widget(self.motor_1_slider)
    self.add_widget(self.motor_2_input)
    self.add_widget(self.motor_2_slider)
    self.add_widget(self.motor_3_input)
    self.add_widget(self.motor_3_slider)
    self.add_widget(self.motor_4_input)
    self.add_widget(self.motor_4_slider)
    self.add_widget(self.spacer)
    return self

  def on_step_button(self, value):
    motions = [(str(self.motor_1_input.text), float(self.motor_1_slider.value)),
               (str(self.motor_2_input.text), float(self.motor_2_slider.value)),
               (str(self.motor_3_input.text), float(self.motor_3_slider.value)),
                (str(self.motor_4_input.text), float(self.motor_4_slider.value)),
               ]
    self._on_step_callback(self.actor_input.text, motions)


  def on_reset_button(self, value):
    self._on_reset_callback()