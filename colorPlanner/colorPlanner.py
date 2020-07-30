from krita import *
from PyQt5.QtWidgets import *
from PyQt5 import uic
import sip

from .colorPlannerForm import Ui_colorPlannerForm
from .colorPlannerMaskSelectForm import Ui_colorPlannerMaskSelectForm
from .colorPlannerDialogForm import Ui_colorPlannerDialogForm

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

class ColorPlannerDialog(QDialog):
    def __init__(self, text, parent):
        # Initialize Parent
        super().__init__(parent)

        self.Ui = Ui_colorPlannerDialogForm()
        self.Ui.setupUi(self)
        self.textLabel = QLabel(text, self)
        self.Ui.verticalLayout.insertWidget(0, self.textLabel)

    def setText(self, text):
        self.textLabel.setText(text)

    @staticmethod
    def dialogAccepted(text):
        dialog = ColorPlannerDialog(text, None)
        dialog.setModal(True)
        res = dialog.exec_()
        if res == QDialog.Accepted:
            return True
        else:
            return False

def nodeRemoval(node):
    # Remove children
    for child in node.childNodes():
        nodeRemoval(child)
        node.removeChildNode(child) # Maybe?
    # Remove self.
    node.remove()

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
        self.Ui.buildMaskCompositorButton.clicked.connect(self.buildMaskCompositor)

        # Variables
        self.clearInternalVariables()

    def clearInternalVariables(self):
        self.baseLayer = None
        self.maskSelectors = []
        # Clear existing mask selection widgets
        while not self.scroll_layout.isEmpty():
            self.scroll_layout.removeItem(self.scroll_layout.itemAt(0))

    def canBuildCompositor(self):
        if self.baseLayer is None:
            return False

        num_checked = 0
        for selector in self.maskSelectors:
            if selector.Ui.maskCheckBox.isChecked():
                num_checked += 1

        if num_checked == 0:
            return False

        return True

    @staticmethod
    def isNodeOnFirstLevel(node):
        doc = Krita.instance().activeDocument()
        root = doc.rootNode()
        found = False
        for child in root.childNodes():
            if child == node:
                found = True
                break
        return found

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

        # Check that the selected layer is on the first 'level'.
        if not ColorPlannerDocker.isNodeOnFirstLevel(current_node):
            ErrorMessage("Nodes not on the first level are currently not supported.")
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

        # We have a valid layer, and can start building the compositor.
        self.clearInternalVariables()

        self.baseLayer = current_node
        # mask selection widgets
        for mask in selectionmasks:
            maskSelector = ColorPlannerMaskSelect(self.Ui.scrollArea.widget(),mask)
            self.scroll_layout.addWidget(maskSelector)
            self.maskSelectors.append(maskSelector)
        self.scroll_layout.addItem(QSpacerItem(40,20,QSizePolicy.Minimum, QSizePolicy.Expanding))

    def buildMaskCompositor(self):
        if not self.canBuildCompositor():
            ErrorMessage("Can't currently build a compositor!")
            return
        
        if not ColorPlannerDocker.isNodeOnFirstLevel(self.baseLayer):
            ErrorMessage("Select node wasn't on the 'first level'! Not currently supported!")
            return

        doc = Krita.instance().activeDocument()
        first_level = doc.rootNode().childNodes()
        to_remove = []
        for node in first_level:
            if node != self.baseLayer:
                to_remove.append(node)

        # User Validation for removal of layers
        if len(to_remove) > 0:

            message = ["First Level Layers which will be deleted:"]
            for node in to_remove:
                message.append("{} ({})".format(node.name(), node.type()))
            message.append("Proceed?")

            full_msg = "\n".join(message)

            if not ColorPlannerDialog.dialogAccepted(full_msg):
                return

        # Remove said layers
        for node in to_remove:
            node.remove()
            #doc.rootNode().removeChildNode(node)

        # Build 'clean' grayscale version of base layer.
        baseClone = self.baseLayer.clone()
        for child in baseClone.childNodes():
            child.remove()
            #self.baseClone.removeChildNode(child)
        baseClone.setLocked(False)
        doc.rootNode().addChildNode(baseClone, self.baseLayer)
        #baseClone.setColorSpace('GRAYA', 'U8', 'Gray-D50-elle-V2-srgbtrc.icc')
        #self.baseLayer.setColorSpace('GRAYA', 'U8', 'Gray-D50-elle-V2-srgbtrc.icc')

        # Add it to the root node for now.

    def canvasChanged(self, canvas):
        # Need to implement!!
        pass

Krita.instance().addDockWidgetFactory(DockWidgetFactory("colorPlannerDocker", DockWidgetFactoryBase.DockRight, ColorPlannerDocker))
