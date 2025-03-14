from PyQt5.QtWidgets import QTableWidget, QComboBox, QSpinBox, QWidget, QHBoxLayout, QLineEdit, QLabel, QTableWidgetItem, QApplication, QMainWindow
from typing import List, Tuple
import sys

class TestCaseTableWidget(QTableWidget):
    def __init__(self):
        super().__init__(18, 7)
        headers = ["TC ID", "평가 시나리오", "Domain 개수", "Publisher", "Subscriber", "데이터 크기 범위", "Qos Policy"]
        self.setHorizontalHeaderLabels(headers)
        
        scenario_options = ["기본 성능", "패킷 개수", "메시지 드랍율", "Subscriber 개수", "Domain 개수"]
        pub_sub_options = ["AP1", "AP2", "MCU"]
        qos_options = ["Volatile", "Transient-local", "Transit", "Persistent"]
        
        # 크기 입력 위젯 레이아웃 생성 (재사용)
        size_widget = self._create_size_widget()
        
        for row in range(18):
            self.setItem(row, 0, QTableWidgetItem(str(row + 1)))
            self.setCellWidget(row, 1, self._create_combo_box(scenario_options, 0))
            self.setCellWidget(row, 2, self._create_spin_box(1, 100, 1))
            self.setCellWidget(row, 3, self._create_combo_box(pub_sub_options, 0))
            self.setCellWidget(row, 4, self._create_combo_box(pub_sub_options, 0))
            self.setCellWidget(row, 5, size_widget)
            self.setCellWidget(row, 6, self._create_combo_box(qos_options, 0))

    def _create_combo_box(self, items: List[str], default_index: int = 0) -> QComboBox:
        """콤보 박스 생성"""
        combo = QComboBox()
        combo.addItems(items)
        combo.setCurrentIndex(default_index)
        return combo

    def _create_spin_box(self, min_val: int, max_val: int, default_val: int) -> QSpinBox:
        """스핀 박스 생성"""
        spin = QSpinBox()
        spin.setRange(min_val, max_val)
        spin.setValue(default_val)
        return spin

    def _create_size_widget(self) -> QWidget:
        """크기 입력 위젯 생성"""
        size_widget = QWidget()
        size_layout = QHBoxLayout(size_widget)
        size_layout.setContentsMargins(2, 2, 2, 2)
        min_edit = QLineEdit("100")
        max_edit = QLineEdit("100")
        size_layout.addWidget(min_edit)
        size_layout.addWidget(QLabel("~"))
        size_layout.addWidget(max_edit)
        size_widget.setLayout(size_layout)  # 레이아웃 설정 추가
        return size_widget

if __name__ == '__main__':
    app = QApplication(sys.argv)
    
    # 메인 윈도우를 생성하고 TestCaseTableWidget을 추가
    main_window = QMainWindow()
    table_widget = TestCaseTableWidget()
    main_window.setCentralWidget(table_widget)
    
    main_window.show()
    sys.exit(app.exec_())