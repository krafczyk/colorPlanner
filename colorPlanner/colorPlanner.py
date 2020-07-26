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

def ErrorMessage(message, title="", informative_text=""):
    msgBox = QMessageBox()
    msgBox.setText(message)
    msgBox.setWindowTitle(title)
    msgBox.setInformativeText(informative_text)
    msgBox.setStandardButtons(QMessageBox.Ok)
    msgBox.setDefaultButton(QMessageBox.Ok)
    msgBox.exec_()

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
        doc = Krita.instance().activeDocument()
        if doc is None:
            ErrorMessage("No currently active document!")
            return

        print("refreshMainLayers called!")
        root = doc.rootNode()
        nodes = root.childNodes()

        if len(nodes) == 0:
            ErrorMessage("The current document has no layers!")
            return

        # Get layer names
        layer_names = []
        for node in nodes:
            layer_names.append(node.name())

        # Reset combo box
        layer_cmbbox = self.Ui.mainLayerComboBox
        layer_cmbbox.clear()
        layer_cmbbox.addItems(layer_names)

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
