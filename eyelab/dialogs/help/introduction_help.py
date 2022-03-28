from eyelab.dialogs.help.help_dialog import HelpWindow

help_text = """
# Introduction

EyeLab is a multimodal annotation tool for ophthalmological imaging data.

Get started by importing data in one of the supported file formats

## Currently supported file formats

+ Data exported from HEXEX in the .xml or .vol format
+ Data from the RETOUCH challenge
+ AMD and Control Dataset from  (Farsiu 2014)
+ Import B-scans from folder (sorting the file names is expected to result in the correct B-scan order
+ Saving and opening of .eye files, EyeLabs file format.

## The Workspace:

Your workspace consists of a combined Enface and Volume view. On the right you have an overview
where annotations are managed for the OCT volume as well as for the Enface image.

## Navigation

You can zoom in and out using the mouse wheel. With the standard **Inspection** tool you can
move the image around if you want to see another part. If you press CTRL while using the mouse
wheel on the Volume view, you scroll through adjacent B-scans. Use CRTL + x to toggle a
linked navigation where B-scans change based on your mouse position in the enface.

## How to continue
From here you can continue with one of the following guides depending on your
needs.
+ Layer Annotation Guide
+ Area Annotation Guide
"""


class IntroductionHelp(HelpWindow):
    def __init__(self, parent):
        super().__init__(help_text, parent)
