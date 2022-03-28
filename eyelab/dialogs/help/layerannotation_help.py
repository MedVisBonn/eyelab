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
layer automatically enables the **Curve** tool. You can now start adding control points
of a cubic spline curve, by double click on the desired location. You can move control
points by left click and hold and delete them with a right click.
These control points consist of a red circle the curve has to pass through and two
blue rectangles which control at which angle the curve enters and leaves the red control
point

If you want to pan around in the image select the **Inspection** tool on the right.

The layer heights are constantly updated to represent the position of the current cubic
spline curve.
"""


class LayerAnnotationHelp(HelpWindow):
    def __init__(self, parent):
        super().__init__(help_text, parent)
