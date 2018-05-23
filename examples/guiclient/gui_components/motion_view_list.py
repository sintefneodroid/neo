#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'cnheider'

from kivy.adapters.dictadapter import DictAdapter
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.listview import CompositeListItem, ListItemButton, ListItemLabel, ListView

integers_dict = {str(i):{'text':str(i), 'is_selected':False} for i in range(100)}


class MotionViewList(GridLayout):

  def __init__(self, **kwargs):
    kwargs['cols'] = 2
    super().__init__(**kwargs)

    def args_converter(row_index, row_data):
      return {
        'text':       row_data['text'],
        'size_hint_y':None,
        'height':     25,
        'cls_dicts':  [
          {
            'cls':   ListItemLabel,
            'kwargs':{
              'text':row_data['text'], 'is_representing_cls':True
              },
            },
          {
            'cls':   ListItemLabel,
            'kwargs':{
              'text':               'Middle-{0}'.format(row_data['text']),
              'is_representing_cls':True,
              },
            },
          {
            'cls':   ListItemLabel,
            'kwargs':{
              'text':               'End-{0}'.format(row_data['text']),
              'is_representing_cls':True,
              },
            },
          {'cls':ListItemButton, 'kwargs':{'text':row_data['text']}},
          ],
        }

    item_strings = ['{0}'.format(index) for index in range(100)]

    dict_adapter = DictAdapter(
        sorted_keys=item_strings,
        data=integers_dict,
        args_converter=args_converter,
        selection_mode='single',
        allow_empty_selection=False,
        cls=CompositeListItem,
        )

    self.list_view = ListView(adapter=dict_adapter)

    self.step_button = Button(text='Step')
    self.reset_button = Button(text='Reset')
    # self.spacer = Label()
    self.assemble_components()

  def assemble_components(self):
    self.step_button.bind(on_release=self.on_step_button)
    self.reset_button.bind(on_release=self.on_reset_button)

    self.add_widget(self.list_view)
    self.add_widget(self.step_button)
    self.add_widget(self.reset_button)
    # self.add_widget(self.spacer)
    return self

  def on_step_button(self):
    pass

  def on_reset_button(self):
    pass


if __name__ == '__main__':
  from kivy.base import runTouchApp

  runTouchApp(MotionViewList(width=800))
