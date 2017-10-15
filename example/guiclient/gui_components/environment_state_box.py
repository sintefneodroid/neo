from kivy.core.image import Image as CoreImage
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.label import Label


class EnvironmentStateBox(BoxLayout):
  def __init__(self, **kwargs):
    super(EnvironmentStateBox, self).__init__(**kwargs)
    self.depth_image = Image(source='images/default.png')
    self.segmentation_image = Image(source='images/default.png')
    self.instance_segmentation_image = Image(source='images/default.png')
    self.rgb_image = Image(source='images/default.png')
    self.infrared_shadow_image = Image(source='images/default.png')
    self.position_label = Label(text='Position: ', size_hint=(1.0, 0.05))
    self.rotation_label = Label(text='Rotation: ', size_hint=(1.0, 0.05))
    self.reward_label = Label(text='Reward: ', size_hint=(1.0, 0.05))
    self.energy_label = Label(text='Energy Spent Since Reset: ',
                              size_hint=(1.0, 0.05))
    self.time_label = Label(text='Time Since Reset: ', size_hint=(1.0, 0.05))

    self.image_row_layout = BoxLayout(orientation='horizontal')
    self.assemble_components()

  def assemble_components(self):
    self.image_row_layout.add_widget(self.rgb_image)
    self.image_row_layout.add_widget(self.segmentation_image)
    self.image_row_layout.add_widget(self.instance_segmentation_image)
    self.image_row_layout.add_widget(self.depth_image)
    self.image_row_layout.add_widget(self.infrared_shadow_image)

    self.add_widget(self.image_row_layout)
    self.add_widget(self.position_label)
    self.add_widget(self.rotation_label)
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

  def update_segmentation_image(self, segmentation_image_data):
    try:
      segmentation_image = CoreImage(segmentation_image_data, ext='png')
      self.segmentation_image.texture = segmentation_image.texture
    except BaseException:
      print('Image not valid')

  def update_instance_segmentation_image(self,
                                         instance_segmentation_image_data):
    try:
      instance_segmentation_image = CoreImage(instance_segmentation_image_data,
                                              ext='png')
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

  def update_position_label(self, value: str):
    self.position_label.text = 'Position: ' + value

  def update_rotation_label(self, value: str):
    self.rotation_label.text = 'Rotation: ' + value

  def update_reward_label(self, value: str):
    self.reward_label.text = 'Reward: ' + value

  def update_energy_label(self, value: str):
    self.energy_label.text = 'Energy Spent Since Reset: ' + value

  def update_time_label(self, value: str):
    self.time_label.text = 'Time Since Reset: ' + value
