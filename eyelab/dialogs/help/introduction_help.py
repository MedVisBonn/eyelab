from oat.modules.dialogs.help.help_dialog import HelpWindow

help_text = """
# Introduction

OAT is a multimodal annotation tool for ophthalmological imaging data. All the date is
stored on a server independent from your workstation. From your workstation you
connect to the server to make annotations.

When you add a subjects data to the annotation tool you add it to one of the
subjects collections. By default every subject has an OS, OD and an NA collection,
but you can add custom collections. Data in a collection can be viewed and annotated
together. So for example if you have a dataset with multiple modalities you could
add a collection to every subject which only holds the subjects CFP. This could be used
for blinded grading and annotation.

Collections can be organised into datasets.

## Data Upload

For adding data to the system you can click in the top left corner on File -> Import.
Here you have different options. Currently we support adding VOL and XML exports
from HEYEX as well as folders conaining B-Scans and individual images holding an
enface image. When uploading the data you can select the subject and collection you want
to add the data to. Datasets are not supported in the GUI yet.
After you added a new collection you can see it in the table and after selection
you can click on `Register` if your collections contains two enface images or on
`Annotate` for any number of enface images and OCT volumes.

# How to continue
From here you can continue with one of the following guides depending on your
needs.
+ Registration Guide
+ Layer Annotation Guide
+ Area Annotation Guide
"""


class IntroductionHelp(HelpWindow):
    def __init__(self, parent):
        super().__init__(help_text, parent)
