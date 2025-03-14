from PyQt5 import QtCore, QtWidgets, uic
from PyQt5.QtCore import QPoint, QSize, QRect
from widgets.test_options_tree import TestOptionsTreeWidget
from widgets.test_case_table import TestCaseTableWidget
from widgets.tool_list import ToolListWidget
from widgets.plotly_graph import PlotlyGraphWidget
from floating_widget import FloatingWidget
from constants import WIDGET_NAMES

class DockApp(QtWidgets.QMainWindow):
    WIDGETS = ["test_option", "test_cases", "tools", "graph"]

    def __init__(self):
        super().__init__()
        self.settings = QtCore.QSettings("config.ini", QtCore.QSettings.IniFormat)
        
        # Load UI file
        uic.loadUi('main_window.ui', self)
        
        # Initialize widget variables
        self.widget_dict = {name: None for name in self.WIDGETS}
        self.free_mode_widget_states = {}
        self.dock_mode_widget_states = {}

        self.initUI()

    def initUI(self):
        # Connect action signals
        self.actionQuit.triggered.connect(self.close)
        self.actionMode_1.triggered.connect(self.enable_free_mode)
        self.actionMode_2.triggered.connect(self.enable_default_mode)
        self.actionExport_2.triggered.connect(self.export_data)
        self.actionVersion.triggered.connect(self.show_version)

        # View 메뉴에 위젯 액션 추가
        viewMenu = self.menuBar().findChild(QtWidgets.QMenu, "menuViews")
        if viewMenu:
            self.widget_actions = {}
            for widget_name in self.WIDGETS:
                action = QtWidgets.QAction(WIDGET_NAMES[widget_name], self, checkable=True)
                action.triggered.connect(lambda checked, name=widget_name: self.toggle_widget(name, checked))
                viewMenu.addAction(action)
                self.widget_actions[widget_name] = action

        # Initialize widgets
        self.init_widgets()

        # Set initial widget states
        self.set_initial_widget_states()

        # Load initial widget states from config.ini
        self.load_widget_states_from_config()

    def init_widgets(self):
        def load_geometry(name, default_pos, default_size):
            pos = self.settings.value(f"{name}_pos", default_pos, type=QPoint)
            size = self.settings.value(f"{name}_size", default_size, type=QSize)
            return pos, size

        for widget_name in self.WIDGETS:
            widget_content = self.create_widget_content(widget_name)
            pos, size = load_geometry(widget_name, QPoint(50, 50), QSize(400, 300))
            widget_content.setGeometry(QRect(pos.x(), pos.y(), size.width(), size.height()))
            floating_widget = FloatingWidget(WIDGET_NAMES[widget_name], parent=self.centralwidget)
            floating_widget.setWidget(widget_content)
            floating_widget.setObjectName(widget_name)
            floating_widget.hide()
            self.widget_dict[widget_name] = floating_widget

    def create_widget_content(self, widget_name):
        """Create the content for each widget."""
        if widget_name == "test_option":
            return TestOptionsTreeWidget()
        elif widget_name == "test_cases":
            return TestCaseTableWidget()
        elif widget_name == "tools":
            return ToolListWidget()
        elif widget_name == "graph":
            return PlotlyGraphWidget()

    def set_initial_widget_states(self):
        """Set initial visibility of widgets."""
        for widget_name in self.WIDGETS:
            visible = self.settings.value(f"{widget_name}_visible", True, type=bool)  # Default to visible=True
            if visible:
                self.widget_dict[widget_name].show()
            else:
                self.widget_dict[widget_name].hide()

    def load_widget_states_from_config(self):
        """Load widget states from config.ini."""
        for mode_prefix in ["free_mode", "dock_mode"]:
            for widget_name in self.WIDGETS:
                name = f"{mode_prefix}_{widget_name}"
                pos = self.settings.value(f"{name}_pos", None, type=QPoint)
                size = self.settings.value(f"{name}_size", None, type=QSize)
                if pos and size:
                    state_dict = {"pos": pos, "size": size}
                    if mode_prefix == "free_mode":
                        self.free_mode_widget_states[widget_name] = state_dict
                    elif mode_prefix == "dock_mode":
                        self.dock_mode_widget_states[widget_name] = state_dict

    def enable_free_mode(self):
        print("Mode 1 (Free Positioning) Activated")
    
    def enable_default_mode(self):
        print("Mode 2 (Default Docking) Activated")
        
        # Save current free mode states
        self.save_widget_states(self.free_mode_widget_states)
        
        # Restore dock mode states
        self.restore_widget_states(self.dock_mode_widget_states)
        
        # Enable nested docking
        self.setDockNestingEnabled(True)

    def restore_widget_states(self, state_dict):
        """Restore the position and size of widgets."""
        for widget_name in state_dict.keys():
            widget = self.widget_dict.get(widget_name)
            if widget:
                pos = state_dict[widget_name]['pos']
                size = state_dict[widget_name]['size']
                widget.setGeometry(QRect(pos, size))

    def save_widget_states(self, state_dict):
        """Save the position and size of widgets."""
        for widget_name in state_dict.keys():
            widget = self.widget_dict.get(widget_name)
            if widget:
                state_dict[widget.objectName()] = {
                    'pos': widget.pos(),
                    'size': widget.size()
                }

    def toggle_widget(self, name: str, checked: bool):
       pass

    def export_data(self):
        print("Exporting data...")
    
    def show_version(self):
        print("Showing version information...")
