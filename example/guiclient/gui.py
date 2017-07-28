from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from gui_components import EnvironmentStateColumn, ReactionColumn, StaturBar, XMLColumn

class NeoGUI(App):
    def __init__(self, on_step_callback, on_reset_callback, on_connect_callback, **kwargs):
        super(NeoGUI, self).__init__(**kwargs)
        self._on_step_callback=on_step_callback
        self._on_reset_callback = on_reset_callback
        self._on_connect_callback=on_connect_callback

    def build(self):
        self.parent_rows = BoxLayout(orientation='vertical')
        self.columns = BoxLayout(orientation='horizontal')

        #Upper Part(Columns)
        self.xml_column = XMLColumn(size_hint=(0.45,1.0))
        self.state_column = EnvironmentStateColumn(orientation='vertical')
        self.reaction_column = ReactionColumn(on_step_callback=self._on_step_callback,
                                              on_reset_callback=self._on_reset_callback,
                                              orientation='vertical',
                                              size_hint=(0.12,1.0),
                                              spacing=10,
                                              padding=10)

        self.columns.add_widget(self.xml_column)
        self.columns.add_widget(self.state_column)
        self.columns.add_widget(self.reaction_column)
        self.parent_rows.add_widget(self.columns)

        #Status Bar
        self.status_bar = StaturBar(on_connect_callback=self._on_connect_callback,
                                    orientation='horizontal',
                                    size_hint=(1.0,0.05))
        self.parent_rows.add_widget(self.status_bar)
        return self.parent_rows

    def update_depth_image(self, depth_image):
        self.state_column.update_depth_image(depth_image)

    def update_light_mask_image(self, light_mask_image):
      self.state_column.update_light_mask_image(light_mask_image)

    def update_combined_image(self, combined_image):
      self.state_column.update_combined_image(combined_image)

    def update_position_label(self, value : str):
        self.state_column.update_position_label(value)

    def update_rotation_label(self, value : str):
        self.state_column.update_rotation_label(value)

    def update_reward_label(self, value : str):
        self.state_column.update_reward_label(value)

    def update_energi_label(self, value : str):
        self.state_column.update_energi_label(value)

    def update_time_label(self, value: str):
      self.state_column.update_time_label(value)

    def update_connect_button(self, value : str):
        self.status_bar.update_connect_button(value)

    def update_xml_text_label(self, value:str):
      self.xml_column.update_text_label(value)