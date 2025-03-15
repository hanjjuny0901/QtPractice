# dock_app.py
from PyQt5 import QtCore, QtWidgets, uic
from free_mode_manager import FreeModeManager
from dock_mode_manager import DockModeManager
from constants import WIDGET_NAMES
from widgets.test_options_tree import TestOptionsTreeWidget
from widgets.test_case_table import TestCaseTableWidget
from widgets.tool_list import ToolListWidget
from widgets.plotly_graph import PlotlyGraphWidget

class DockApp(QtWidgets.QMainWindow):
    WIDGETS = ["test_option", "test_cases", "tools", "graph"]

    def __init__(self):
        super().__init__()
        
        # 설정 초기화 (config.ini 사용)
        settings_path = QtCore.QStandardPaths.writableLocation(QtCore.QStandardPaths.AppConfigLocation)
        settings_file = f"{settings_path}/config.ini"
        self.settings = QtCore.QSettings(settings_file, QtCore.QSettings.IniFormat)

        # UI 로드
        uic.loadUi('main_window.ui', self)

        # 자유 배치 및 도킹 모드 매니저 생성
        self.free_mode_manager = FreeModeManager(
            parent=self,
            settings=self.settings,
            widget_names=WIDGET_NAMES,
            create_widget_content=self.create_widget_content,
        )
        
        self.dock_mode_manager = DockModeManager(
            parent=self,
            settings=self.settings,
            widget_names=WIDGET_NAMES,
            create_widget_content=self.create_widget_content,
        )

        # 현재 활성화된 모드를 추적하는 플래그
        self.is_free_mode_active = False

        # 프로그램 초기화를 추적하는 플래그
        self.is_initialized = True 

        # 초기화 및 이벤트 연결
        self.initUI()

    def initUI(self):
        """UI 초기화"""
        
        # 메뉴 액션 연결
        self.actionQuit.triggered.connect(self.close)
        
        # 모드 전환 액션 연결
        self.actionMode_1.triggered.connect(self.enable_free_mode)
        self.actionMode_2.triggered.connect(self.enable_dock_mode)

       # 마지막 모드 복원 (기본값: 자유 배치 모드)
        last_mode = self.settings.value("last_mode", None)
        if last_mode is None:
            print("No mode found in settings. Defaulting to free mode.")
            last_mode = "free_mode"

        print(f"Restoring last mode: {last_mode}")  # 디버깅 메시지

        if last_mode == "dock_mode":
            self.enable_dock_mode()
        else:
            self.enable_free_mode()

    def create_widget_content(self, widget_name):
       """위젯 콘텐츠 생성"""
       if widget_name == "test_option":
           return TestOptionsTreeWidget()
       elif widget_name == "test_cases":
           return TestCaseTableWidget()
       elif widget_name == "tools":
           return ToolListWidget()
       elif widget_name == "graph":
           return PlotlyGraphWidget()

    def enable_free_mode(self):
       """자유 배치 모드 활성화"""
       print("Switching to Free Mode")
       self.is_free_mode_active = True  # 자유 배치 모드 활성화

       if hasattr(self.dock_mode_manager, 'deactivate') and not getattr(self, "is_initialized", False):
           self.dock_mode_manager.deactivate()

       self.is_initialized = False
       # 자유 배치 모드 활성화
       self.free_mode_manager.initialize_widgets()
       self.free_mode_manager.activate()

    def enable_dock_mode(self):
       """도킹 모드 활성화"""
       print("Switching to Dock Mode")
       self.is_free_mode_active = False  # 도킹 모드 활성화

       if hasattr(self.free_mode_manager, 'deactivate'):
           self.free_mode_manager.deactivate()
           
       # 도킹 모드 활성화
       self.dock_mode_manager.activate()

    def closeEvent(self, event):
       """애플리케이션 종료 시 상태 저장"""
       
       current_mode = "free_mode" if self.is_free_mode_active else "dock_mode"
       
       # 현재 모드 저장
       self.settings.setValue("last_mode", current_mode)
       print(f"Saving last mode: {current_mode}")  # 디버깅 메시지

       if current_mode == "free_mode":
           self.free_mode_manager.deactivate()
       else:
           self.dock_mode_manager.deactivate()

       super().closeEvent(event)
