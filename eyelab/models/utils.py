import qimage2ndarray
from PySide6 import QtGui, QtWidgets


def array2qgraphicspixmapitem(image):
    return QtWidgets.QGraphicsPixmapItem(
        QtGui.QPixmap().fromImage(qimage2ndarray.array2qimage(image))
    )


def qgraphicspixmapitem2array(pixmapitem):
    return qimage2ndarray.rgb_view(pixmapitem.pixmap().toImage())


def qgraphicspixmap2array(pixmap):
    return qimage2ndarray.rgb_view(pixmap.toImage())
