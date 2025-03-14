from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5 import QtWidgets
import plotly.express as px
import logging
import sys  # sys 모듈 추가

logger = logging.getLogger(__name__)

class PlotlyGraphWidget(QtWidgets.QWidget):
    """Plotly 그래프를 표시하는 위젯"""
    def __init__(self):
        super().__init__()
        self.view = QWebEngineView()
        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(self.view)
        self.setLayout(layout)
        self.update_graph()

    def update_graph(self, data=None):
        """그래프 업데이트 (데이터 변경 시)"""
        try:
            if data is None:
                # 기본 데이터셋 사용
                df = px.data.tips()
            else:
                df = data

            fig = px.scatter(df, x="total_bill", y="tip", color="size", size="size")
            
            # 레이아웃 업데이트
            fig.update_layout(
                autosize=True,
                margin=dict(l=10, r=10, t=10, b=10),
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)'
            )
            
            self.view.setHtml(fig.to_html(include_plotlyjs='cdn'))
        except Exception as e:
            logger.error(f"Error creating graph: {e}", exc_info=True)
            # 오류 처리 (예: 사용자에게 메시지 표시)

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    widget = PlotlyGraphWidget()
    widget.show()
    sys.exit(app.exec_())