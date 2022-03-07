from oat.modules.dialogs.help.help_dialog import HelpWindow

help_text = """
# Layer Annotation Guide

If you want to annotate a OCT layer you first have to add a new annotation layer.
Therefore you first select the correct modality tab Then you click on the plus
sign below the annotation layer overview and add a new line annotation for the
OCT layer you want to annotate.

When you click on a line annotation layer in the overview it is selected and you
can choose between a **Inspection** tool and the **Curve** tool. By default the
**Curve** tool is selected when you click on a line annotation layer.

Using the **Curve** tool OCT layer annotation is done by adding and manipulating
control points of a curve. These control points consist of a red circle the curve
has to pass through and two blue rectangles which control at which angle the
curve enters and leaves the red control point. You can add a control point with
a double click and move it around by dragging it to another position.

## Computing the ideal RPE
When annotations for the RPE and the BM exist, you can compute the ideal RPE.
Simply right click on the RPE annotation to compute the ideal RPE for the current
B-Scan. Then you can continue to correct the computed ideal RPE if necessary.
The ideal RPE is computed from the RPE as a offset to the BM. If there are major
problems with the computed ideal RPE this might be due to mistakes in the BM
or RPE annotation.




"""


class LayerAnnotationHelp(HelpWindow):
    def __init__(self, parent):
        super().__init__(help_text, parent)
