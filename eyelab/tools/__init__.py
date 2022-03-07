from .inspection import Inspection
from .pen import Pen
from .splinetool import Spline


def line_tools():
    return {"inspection": Inspection(), "spline": Spline()}


def area_tools():
    return {"inspection": Inspection(), "pen": Pen()}


def basic_tools():
    return {"inspection": Inspection()}
