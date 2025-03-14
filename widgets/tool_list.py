from PyQt5.QtWidgets import QListWidget,QListWidgetItem, QApplication, QMainWindow
from PyQt5.QtCore import pyqtSlot
from typing import List
import sys

class ToolListWidget(QListWidget):
    def __init__(self):
        super().__init__()
        tools = ["Format", "Search", "Replace"]
        self.addItems(tools)
        self.itemClicked.connect(self._item_clicked)

    @pyqtSlot(QListWidgetItem)
    def _item_clicked(self, item):
        """툴 아이템 클릭 시 동작"""
        print(f"Clicked: {item.text()}")
        # 여기에 각 툴에 대한 동작을 구현합니다.
        if item.text() == "Format":
            pass  # Format 기능 구현
        elif item.text() == "Search":
            pass  # Search 기능 구현
        elif item.text() == "Replace":
            pass  # Replace 기능 구현

if __name__ == '__main__':
    app = QApplication(sys.argv)
    
    # 메인 윈도우를 생성하고 ToolListWidget을 추가
    main_window = QMainWindow()
    list_widget = ToolListWidget()
    main_window.setCentralWidget(list_widget)
    
    main_window.show()
    sys.exit(app.exec_())