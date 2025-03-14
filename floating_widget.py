from PyQt5.QtWidgets import QDockWidget
from PyQt5.QtCore import Qt

class FloatingWidget(QDockWidget):
    def __init__(self, title, parent=None):
        super().__init__(title.capitalize(), parent)
        self.start_pos = None

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.start_pos = event.pos()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton and self.start_pos is not None:
            diff = event.pos() - self.start_pos
            new_pos = self.pos() + diff
            
            # Restrict movement within parent boundaries (centralwidget)
            parent_rect = self.parent().rect()
            
            new_x = max(0, min(new_pos.x(), parent_rect.width() - self.width()))
            new_y = max(0, min(new_pos.y(), parent_rect.height() - self.height()))
            
            # Move the floating window to the restricted position
            self.move(new_x, new_y)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.start_pos = None
