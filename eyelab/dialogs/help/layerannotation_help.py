from eyelab.dialogs.help.help_dialog import HelpWindow

help_text = """
# Layer Annotation Guide

An OCT Layer in Eyelab is combination of explicit layer heights provided per A-scan,
and a cubic spline curve which can be manipulated by adding, removing or moving the
curves knots.

## Adding a new Layer

Create a new layer using the (+) symbol in the overview on the right. Specify a name
and select Layers from the Type dropdown.

## Layer Annotation

First select the layer you want to annotate from the overview on the right. Selecting a
layer automatically enables the **Curve** tool. You can now start to annotate a layer
by adding control points (double-click) to one or more curves. To add a new curve to
the same layer, click right and then continue adding knots. You can move control
points by left click and hold, and delete them with a right click. Undoing and redoing
actions can be performed using Ctrl+Z / Ctrl+Y or the Edit menu at the top.

If you want to pan around in the image select the **Inspection** tool on the right. This
is especially usefull when you have to navigate to the border of the image after zooming
in.

"""


class LayerAnnotationHelp(HelpWindow):
    def __init__(self, parent):
        super().__init__(help_text, parent)
