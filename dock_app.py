from PyQt5 import QtCore, QtWidgets, uic
from PyQt5.QtWidgets import QMdiArea, QMdiSubWindow, QDockWidget
from constants import WIDGET_NAMES
from widgets.test_options_tree import TestOptionsTreeWidget
from widgets.test_case_table import TestCaseTableWidget
from widgets.tool_list import ToolListWidget
from widgets.plotly_graph import PlotlyGraphWidget
import json

class DockApp(QtWidgets.QMainWindow):
    WIDGETS = ["test_option", "test_cases", "tools", "graph"]

    def __init__(self):
        super().__init__()

        # 설정 초기화 (config.ini 사용)
        settings_file = QtCore.QDir.currentPath() + "/config.ini"
        self.settings = QtCore.QSettings(settings_file, QtCore.QSettings.IniFormat)

        # UI 로드
        uic.loadUi('main_window.ui', self)

        # MDI 영역 설정
        self.mdi_area = QMdiArea()
        self.setCentralWidget(self.mdi_area)

        # 위젯 초기화 (한 번만 생성)
        self.widgets = self.initialize_widgets()

        # 현재 활성화된 모드를 추적하는 플래그
        self.is_free_mode_active = False

        # UI 초기화 및 이벤트 연결
        self.initUI()

    def initUI(self):
        """UI 초기화"""

        # 메뉴 액션 연결
        self.actionQuit.triggered.connect(self.close)

        # 모드 전환 액션 연결
        self.actionMode_1.triggered.connect(self.enable_free_mode)
        self.actionMode_2.triggered.connect(self.enable_dock_mode)

        # 마지막 모드 복원 (기본값: 자유 배치 모드)
        last_mode = self.settings.value("last_mode", "free_mode")

        if last_mode == "dock_mode":
            self.enable_dock_mode(is_initialization=True)
        else:
            self.enable_free_mode(is_initialization=True)

    def initialize_widgets(self):
        """위젯 초기화 (한 번만 생성)"""
        widgets = {
            "test_option": TestOptionsTreeWidget(),
            "test_cases": TestCaseTableWidget(),
            "tools": ToolListWidget(),
            "graph": PlotlyGraphWidget()
        }
        return widgets

    def enable_free_mode(self, is_initialization=False):
        """자유 배치 모드 활성화"""
        print("Switching to Free Mode")
        self.is_free_mode_active = True

        if not is_initialization:
            dock_state = self.saveState()
            self.settings.setValue("dock_state", dock_state)
            self.settings.sync()  # 변경 사항 즉시 기록

        for sub_window in self.mdi_area.subWindowList():
            sub_window.close()
            sub_window.deleteLater()

        for dock_widget in self.findChildren(QDockWidget):
            self.removeDockWidget(dock_widget)
            dock_widget.deleteLater()

        for widget_name, widget in self.widgets.items():
            sub_window = QMdiSubWindow()
            sub_window.setWidget(widget)
            sub_window.setWindowTitle(WIDGET_NAMES[widget_name])
            self.mdi_area.addSubWindow(sub_window)
            self.restore_mdi_state()
            sub_window.show()

     #   if is_initialization:
        #    self.restore_mdi_state()

    def enable_dock_mode(self, is_initialization=False):
        """도킹 모드 활성화"""
        print("Switching to Dock Mode")
        self.is_free_mode_active = False

        if not is_initialization:
            mdi_state = self.save_mdi_state()
            mdi_state_json = json.dumps(mdi_state)
            self.settings.setValue("mdi_state", mdi_state_json)
            self.settings.sync()  # 변경 사항 즉시 기록

        for sub_window in self.mdi_area.subWindowList():
            widget = sub_window.widget()
            if widget:
                widget.setParent(None)
                sub_window.setWidget(None)
            sub_window.close()
            sub_window.deleteLater()

        for dock_widget in self.findChildren(QDockWidget):
            self.removeDockWidget(dock_widget)
            dock_widget.deleteLater()

        for widget_name, widget in self.widgets.items():
            dock_widget = QDockWidget(WIDGET_NAMES[widget_name], self)
            dock_widget.setObjectName(f"{widget_name}_dock")
            dock_widget.setAllowedAreas(QtCore.Qt.AllDockWidgetAreas)
            dock_widget.setWidget(widget)
            self.addDockWidget(QtCore.Qt.LeftDockWidgetArea, dock_widget)

       # if is_initialization:
            dock_state = self.settings.value("dock_state")
            if dock_state:
                print("Restoring dock mode state...")
                self.restoreState(dock_state)

    def save_mdi_state(self):
        """현재 MDI 서브 윈도우의 위치와 크기를 저장"""
        mdi_state = {}
        
        for sub_window in self.mdi_area.subWindowList():
            widget_name = sub_window.windowTitle()
            geometry = sub_window.geometry()
            
            mdi_state[widget_name] = {
                "x": geometry.x(),
                "y": geometry.y(),
                "width": geometry.width(),
                "height": geometry.height(),
                "z_order": len(mdi_state["windows"])  
            }
        
        return mdi_state

def restore_mdi_state(self):
        """저장된 MDI 서브 윈도우의 위치와 크기 및 Z-Order를 복원"""
        
        mdi_state_json = self.settings.value("mdi_state", "{}")

        if isinstance(mdi_state_json, QtCore.QByteArray):
            try:
                mdi_state_json = bytes(mdi_state_json).decode("utf-8")
            except UnicodeDecodeError:
                print("Failed decoding mdi state. Using default empty state.")
                mdi_state_json = "{}"

        try:
            mdi_state = json.loads(mdi_state_json)["windows"]
            
        except (json.JSONDecodeError, KeyError):
            print("MDI state JSON invalid. Using default empty state.")
            return

        for window_data in mdi_state:
            
            for sub_window in self.mdi_area.subWindowList():
                if sub_window.windowTitle() == window_data["name"]:
                    sub_window.setGeometry(
                        QtCore.QRect(
                            window_data["x"],
                            window_data["y"],
                            window_data["width"],
                            window_data["height"]
                        )
                    )
                    break

    def closeEvent(self, event):
        
       current_mode = "free_mode" if self.is_free_mode_active else "dock_mode"
       
       # 현재 모드 저장
       self.settings.setValue("last_mode", current_mode)

       # 현재 상태 저장
       if current_mode == "free_mode":
           mdi_state_dict = self.save_mdi_state()
           mdi_state_json = json.dumps(mdi_state_dict)
           self.settings.setValue("mdi_state", mdi_state_json)
           self.settings.sync()  # 변경 사항 즉시 기록
       else:
           dock_state = self.saveState()
           self.settings.setValue("dock_state", dock_state)
           self.settings.sync()  # 변경 사항 즉시 기록

       print(f"Saving last mode: {current_mode}")

       super().closeEvent(event)