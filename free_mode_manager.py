# free_mode_manager.py
from PyQt5.QtWidgets import QMdiArea, QMdiSubWindow, QWidget
from PyQt5.QtCore import QPoint, QSize, QRect

class FreeModeManager:
    def __init__(self, parent, settings, widget_names, create_widget_content):
        """
        자유 배치 모드 관리 클래스 (MDI 방식)
        :param parent: QMainWindow 객체 (self)
        :param settings: QSettings 객체
        :param widget_names: 위젯 이름 딕셔너리
        :param create_widget_content: 위젯 콘텐츠 생성 함수
        """
        self.parent = parent
        self.settings = settings
        self.widget_names = widget_names
        self.create_widget_content = create_widget_content

        # MDI 영역 생성
        self.mdi_area = QMdiArea()
        self.parent.setCentralWidget(self.mdi_area)

    def initialize_widgets(self):
        """MDI 서브 윈도우 초기화"""
        for widget_name in self.widget_names:
            content_widget = self.create_widget_content(widget_name)
            sub_window = QMdiSubWindow()
            sub_window.setWidget(content_widget)
            sub_window.setWindowTitle(self.widget_names[widget_name])
            sub_window.setGeometry(QRect(
                self.settings.value(f"free_mode_{widget_name}_pos", QPoint(50, 50), type=QPoint),
                self.settings.value(f"free_mode_{widget_name}_size", QSize(400, 300), type=QSize)
            ))
            self.mdi_area.addSubWindow(sub_window)
            sub_window.show()

    def activate(self):
        """자유 배치 모드 활성화"""
        print("Free Mode Activated")
        self.mdi_area.setVisible(True)

    def deactivate(self):
        """자유 배치 모드 비활성화"""
        print("Free Mode Deactivated")
        
        # 현재 상태 저장
        for sub_window in self.mdi_area.subWindowList():
            widget_name = sub_window.windowTitle()
            pos = sub_window.geometry().topLeft()
            size = sub_window.geometry().size()
            self.settings.setValue(f"free_mode_{widget_name}_pos", pos)
            self.settings.setValue(f"free_mode_{widget_name}_size", size)

        # 모든 서브 윈도우 닫기
        for sub_window in self.mdi_area.subWindowList():
            sub_window.close()

        self.mdi_area.setVisible(False)
