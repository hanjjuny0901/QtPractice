import sys
import logging
from PyQt5.QtWidgets import QApplication
from dock_app import DockApp

logging.basicConfig(level=logging.INFO, 
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

if __name__ == '__main__':
    try:
        logger.info("Starting the application")
        app = QApplication(sys.argv)
        ex = DockApp()
        ex.show()
        sys.exit(app.exec_())
    except Exception as e:
        logger.error(f"An error occurred: {e}", exc_info=True)
        sys.exit(1)