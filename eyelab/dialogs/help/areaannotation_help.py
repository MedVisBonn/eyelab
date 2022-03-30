from eyelab.dialogs.help.help_dialog import HelpWindow

help_text = """
# Area Annotation Guide

An area annotation in Eyelab is a pixel_map on top of the underlying image. Its color can
be changed, as well as its visibility.

## Adding a new Area Annotation

Create a new area using the (+) symbol in the overview on the right. Specify a name
and select Areas from the Type dropdown.

## Area Annotation

First select the area you want to annotate from the overview on the right. Selecting an
area automatically enables the **Pen** tool. You can now make annotations. The size of the
**Pen** tool can be changed on the right.

If you want to pan around in the image select the **Inspection** tool on the right.
"""


class AreaAnnotationHelp(HelpWindow):
    def __init__(self, parent):
        super().__init__(help_text, parent)
