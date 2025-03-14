from PyQt5.QtWidgets import QTreeWidget, QTreeWidgetItem, QComboBox, QApplication, QMainWindow
from typing import List
import sys

class TestOptionsTreeWidget(QTreeWidget):
    def __init__(self):
        super().__init__()
        self.setHeaderLabels(["Parameter", "Value"])
        self.setColumnWidth(0, 200)
        
        qos_parameters = ["Reliability", "Durability", "Durability service", "Deadline", "Liveliness", "Lifespan", "History", "Resource Limits", "Partition"]
        security_parameters = ["Authentication", "Access Control", "Message encryption", "Message Authentication"]
        
        qos_options = ["Volatile", "Transient-local", "Transit", "Persistent"]
        yes_no_options = ["Yes", "No"]
        
        qos_item = QTreeWidgetItem(self, ["QoS"])
        self._add_items_to_tree(qos_item, qos_parameters, qos_options=qos_options, yes_no_options=yes_no_options)

        security_item = QTreeWidgetItem(self, ["Security"])
        self._add_items_to_tree(security_item, security_parameters, yes_no_options=yes_no_options)

    def _add_items_to_tree(self, parent_item: QTreeWidgetItem, parameters: List[str], qos_options: List[str] = None, yes_no_options: List[str] = None):
        """트리에 아이템 추가"""
        for parameter in parameters:
            item = QTreeWidgetItem(parent_item, [parameter])
            
            if parameter == "Durability" and qos_options:
                combo = self._create_combo_box(qos_options)
            else:
                combo = self._create_combo_box(yes_no_options)
                
            self.setItemWidget(item, 1, combo)

    def _create_combo_box(self, items: List[str]) -> QComboBox:
        """콤보 박스 생성"""
        combo = QComboBox()
        combo.addItems(items)
        return combo

if __name__ == '__main__':
    app = QApplication(sys.argv)
    
    # 메인 윈도우를 생성하고 TestOptionsTreeWidget을 추가
    main_window = QMainWindow()
    tree_widget = TestOptionsTreeWidget()
    main_window.setCentralWidget(tree_widget)
    
    main_window.show()
    sys.exit(app.exec_())