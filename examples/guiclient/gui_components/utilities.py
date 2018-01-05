from kivy.graphics import Color, Rectangle


def change_background_color(widget, r, g, b, a):
  widget.canvas.before.clear()
  with widget.canvas.before:
    Color(rgba=[r, g, b, a])
    Rectangle(pos=widget.pos, size=widget.size)
