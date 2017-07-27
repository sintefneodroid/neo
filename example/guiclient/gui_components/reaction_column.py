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
    self.motor_1_label = Label(text="Motor_1 strength:")
    self.motor_1_slider = Slider(min=-100, max=100, value=0)
    self.motor_2_label = Label(text="Motor_2 strength:")
    self.motor_2_slider = Slider(min=-100, max=100, value=0)
    self.motor_3_label = Label(text="Motor_3 strength:")
    self.motor_3_slider = Slider(min=-100, max=100, value=0)
    self.motor_4_label = Label(text="Motor_4 strength:")
    self.motor_4_slider = Slider(min=-100, max=100, value=0)
    self.spacer = Label()
    self.step_button.bind(on_release=self.on_step_button)
    self.reset_button.bind(on_release=self.on_reset_button)

    self.add_widget(self.step_button)
    self.add_widget(self.reset_button)
    self.add_widget(self.motor_1_label)
    self.add_widget(self.motor_1_slider)
    self.add_widget(self.motor_2_label)
    self.add_widget(self.motor_2_slider)
    self.add_widget(self.motor_3_label)
    self.add_widget(self.motor_3_slider)
    self.add_widget(self.motor_4_label)
    self.add_widget(self.motor_4_slider)
    self.add_widget(self.spacer)
    return self

  def on_step_button(self, value):
    motions = [
      float(self.motor_1_slider.value),
      float(self.motor_2_slider.value),
      float(self.motor_3_slider.value),
      float(self.motor_4_slider.value)
    ]
    self._on_step_callback(motions)
    # global _stream, _connected
    # if _connected:
    #    send_json(_stream, 'step')
    #    self.left_column.transforms_text.text = receive_json(_stream)
    #    image = receive_image(_stream)
    #    self.left_column.load_image(image)

  def on_reset_button(self, value):
    self._on_reset_callback()
    # global _stream
    # yield send_json(_stream, 'step')
