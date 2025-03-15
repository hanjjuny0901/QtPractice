# dock_mode_manager.py
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt

class DockModeManager:
    def __init__(self, parent, settings, widget_names, create_widget_content):
        """
        도킹 모드 관리 클래스
        :param parent: QMainWindow 객체 (self)
        :param settings: QSettings 객체
        :param widget_names: 위젯 이름 딕셔너리
        :param create_widget_content: 위젯 콘텐츠 생성 함수
        """
        self.parent = parent
        self.settings = settings
        self.widget_names = widget_names
        self.create_widget_content = create_widget_content
        self.widget_dict = {}

        # 중첩 도킹 활성화 및 코너 설정
        self.parent.setDockNestingEnabled(True)
        self.parent.setCorner(Qt.BottomRightCorner, Qt.RightDockWidgetArea)
        self.parent.setCorner(Qt.BottomLeftCorner, Qt.LeftDockWidgetArea)

    def activate(self):
        """도킹 모드 활성화"""
        print("Dock Mode Activated")

        # 도킹 위젯 생성 및 추가
        for name in self.widget_names:
            dock_widget = QtWidgets.QDockWidget(self.widget_names[name], self.parent)
            dock_widget.setObjectName(f"{name}_dock")  # 고유 objectName 설정
            
            # 모든 방향에서 도킹 가능하도록 설정
            dock_widget.setAllowedAreas(Qt.AllDockWidgetAreas)
            
            # 콘텐츠 위젯 생성 및 추가
            content_widget = self.create_widget_content(name)
            content_widget.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
            dock_widget.setWidget(content_widget)

            # 기본적으로 왼쪽 도킹 영역에 추가 (초기 위치 설정 제거 가능)
            self.parent.addDockWidget(Qt.LeftDockWidgetArea, dock_widget)

            # 딕셔너리에 저장
            self.widget_dict[name] = dock_widget

        # 이전 상태 복원 시도 (위젯 생성 후 호출)
        dock_state = self.settings.value("dock_state")
        if dock_state:
            print("Restoring saved dock state...")
            if not self.parent.restoreState(dock_state):
                print("Failed to restore state.")

    def deactivate(self):
        """도킹 모드 비활성화"""
        print("Dock Mode Deactivated")
        
        # 현재 상태 저장 (도킹 위젯이 활성화된 상태에서 저장)
        state = self.parent.saveState()
        self.settings.setValue("dock_state", state)

        # 도킹 위젯 제거 및 삭제
        for widget in self.widget_dict.values():
            self.parent.removeDockWidget(widget)
            widget.deleteLater()

    def restore_state(self):
        """도킹 상태 복원"""
        dock_state = self.settings.value("dock_state")
        if dock_state:
            print(f"Restoring saved state: {dock_state}")
            if not self.parent.restoreState(dock_state):
                print("Failed to restore state.")
