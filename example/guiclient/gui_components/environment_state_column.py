from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.core.image import Image as CoreImage
from kivy.uix.label import Label

class EnvironmentStateColumn(BoxLayout):
    def __init__(self, **kwargs):
        super(EnvironmentStateColumn, self).__init__(**kwargs)
        self.build()

    def build(self):
        self.depth_image = Image(source='images/default.jpg')
        self.light_mask_image = Image(source='images/default.png')
        self.combined_image = Image(source='images/default.jpg')
        self.position_label = Label(text='Position: ',size_hint=(1.0,0.05))
        self.rotation_label = Label(text='Rotation: ', size_hint=(1.0, 0.05))
        self.reward_label = Label(text='Reward: ', size_hint=(1.0, 0.05))
        self.energi_label = Label(text='Energi Spent Since Reset: ', size_hint=(1.0, 0.05))
        self.time_label = Label(text='Time Since Reset: ', size_hint=(1.0, 0.05))

        self.image_row_layout = BoxLayout(orientation='horizontal')

        self.image_row_layout.add_widget(self.depth_image)
        self.image_row_layout.add_widget(self.light_mask_image)
        self.image_row_layout.add_widget(self.combined_image)

        self.add_widget(self.image_row_layout)
        self.add_widget(self.position_label)
        self.add_widget(self.rotation_label)
        self.add_widget(self.reward_label)
        self.add_widget(self.energi_label)
        self.add_widget(self.time_label)
        return self

    def update_depth_image(self, depth_image_data):
        try:
            depth_image = CoreImage(depth_image_data, ext='png')
            self.depth_image.texture = depth_image.texture
        except:
            print('Image not valid')

    def update_light_mask_image(self, light_mask_image_data):
        try:
            light_mask_image = CoreImage(light_mask_image_data, ext='png')
            self.light_mask_image.texture = light_mask_image.texture
        except:
            print('Image not valid')

    def update_combined_image(self, combined_image_data):
        try:
            combined_image = CoreImage(combined_image_data, ext='png')
            self.combined_image.texture = combined_image.texture
        except:
            print('Image not valid')

    def update_position_label(self, value : str):
        self.position_label.text='Position: ' + value

    def update_rotation_label(self, value : str):
        self.rotation_label.text='Rotation: ' + value

    def update_reward_label(self, value : str):
        self.reward_label.text='Reward: ' + value

    def update_energi_label(self, value: str):
      self.energi_label.text = 'Energi Spent Since Reset: ' + value

    def update_time_label(self, value: str):
      self.time_label.text = 'Time Since Reset: ' + value