from krita import *
from PyQt5.QtWidgets import *
from PyQt5 import uic

from .colorPlannerForm import Ui_colorPlannerForm

#class MyExtension(Extension):
#    def __init__(self, parent):
#        super().__init__(parent)
#    
#    def setup(self):
#        pass
#
#    def exportDocument(self):
#        # Get the document
#        doc = Krita.instance().activeDocument()
#
#        # Saving a non-existent document causes crashes, so lets check for that first.
#        if doc is not None:
#            # This calls up the save dialog. The save dialog returns a tuple.
#            fileName = QFileDialog.getSaveFileName()[0]
#            # And export the document to the fileName location.
#            # InfoObject is a dictionary with specific export options, but when we make an empty one Krita will use the export defaults.
#            doc.exportImage(fileName, InfoObject())
#
#    def createActions(self, window):
#        action = window.createAction("myAction", "My Script", "Tools/Scripts")
#        action.triggered.connect(self.exportDocument)
#
#Krita.instance().addExtension(MyExtension(Krita.instance()))

class ColorPlannerDocker(DockWidget):
    def __init__(self):
        # Initialize Parent
        super().__init__()
        # Set Name of window
        self.setWindowTitle("Color Planner")

        # Get main widget
        mainWidget = QWidget(self)
        self.setWidget(mainWidget)

        self.Ui = Ui_colorPlannerForm()
        self.Ui.setupUi(mainWidget)

        self.Ui.refreshMainLayers.clicked.connect(self.refreshMainLayers)

    def refreshMainLayers(self):
        print("refreshMainLayers called!")
        #Krita.instance().

    def exportDocument(self):
        # Get the document
        doc = Krita.instance().activeDocument()

        # Saving a non-existent document causes crashes, so lets check for that first.
        if doc is not None:
            # This calls up the save dialog. The save dialog returns a tuple.
            fileName = QFileDialog.getSaveFileName()[0]
            # And export the document to the fileName location.
            # InfoObject is a dictionary with specific export options, but when we make an empty one Krita will use the export defaults.
            doc.exportImage(fileName, InfoObject())

    def canvasChanged(self, canvas):
        pass

Krita.instance().addDockWidgetFactory(DockWidgetFactory("colorPlannerDocker", DockWidgetFactoryBase.DockRight, ColorPlannerDocker))
