from krita import *
from PyQt5.QtWidgets import *
from PyQt5 import uic

from .colorPlannerForm import Ui_colorPlannerForm
from .colorPlannerMaskSelectForm import Ui_colorPlannerMaskSelectForm

def ErrorMessage(message, title="", informative_text=""):
    msgBox = QMessageBox()
    msgBox.setText(message)
    msgBox.setWindowTitle(title)
    msgBox.setInformativeText(informative_text)
    msgBox.setStandardButtons(QMessageBox.Ok)
    msgBox.setDefaultButton(QMessageBox.Ok)
    msgBox.exec_()

class ColorPlannerMaskSelect(QWidget):
    def __init__(self, parent, node):
        # Initialize Parent
        super().__init__(parent)
        
        self.Ui = Ui_colorPlannerMaskSelectForm()
        self.Ui.setupUi(self)

        self.node = node

        self.Ui.label.setText("{}:".format(self.node.name()))
        self.Ui.maskCheckBox.setChecked(True)

class ColorPlannerDocker(DockWidget):
    def __init__(self):
        # Initialize Parent
        super().__init__()
        # Set Name of window
        self.setWindowTitle("Color Planner")

        # Get main widget
        mainWidget = QWidget(self)
        self.setWidget(mainWidget)

        # Initialize Ui
        self.Ui = Ui_colorPlannerForm()
        self.Ui.setupUi(mainWidget)

        # set up scrollarea
        scrollWidget = QWidget(self.Ui.scrollArea)
        self.Ui.scrollArea.setWidget(scrollWidget)
        self.scroll_layout = QVBoxLayout(scrollWidget)

        # Connect actions
        self.Ui.selectCurrentLayerAsBaseButton.clicked.connect(self.selectBaseLayer)

        # Variables
        self.baseLayer = None
        self.mask_dict_idx = {}

    def selectBaseLayer(self):
        # Get active document and layer
        doc = Krita.instance().activeDocument()
        current_node = doc.activeNode()

        # Check that we have a paint layer.
        if current_node.type() != 'paintlayer':
            ErrorMessage("Layer type ({}) is not currently supported for main layer.".format(current_node.type()))
            return

        # Check that the selected layer is locked.
        if not current_node.locked():
            ErrorMessage("Selected layer is currently unlocked.",
                         informative_text="Please lock the layer and try again.")
            return

        # Check that selectionmasks are children of the active node.
        selectionmasks = []
        for node in current_node.childNodes():
            if node.type() == 'selectionmask':
                selectionmasks.append(node)

        # Check whether we have selection masks
        if len(selectionmasks) == 0:
            ErrorMessage("The selected layer does not have any selection masks!",
                         informative_text="Please add selection masks to the selected layer and try again.")
            return

        # Clear existing mask selection widgets
        while not self.scroll_layout.isEmpty():
            self.scroll_layout.removeItem(self.scroll_layout.itemAt(0))

        # mask selection widgets
        for mask in selectionmasks:
            self.scroll_layout.addWidget(ColorPlannerMaskSelect(self.Ui.scrollArea.widget(),mask))
        self.scroll_layout.addItem(QSpacerItem(40,20,QSizePolicy.Minimum, QSizePolicy.Expanding))

    def canvasChanged(self, canvas):
        # Need to implement!!
        pass

Krita.instance().addDockWidgetFactory(DockWidgetFactory("colorPlannerDocker", DockWidgetFactoryBase.DockRight, ColorPlannerDocker))
