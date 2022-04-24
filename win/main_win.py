from PyQt5 import QtCore
from PyQt5.QtGui import QMouseEvent
from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtWidgets import QMainWindow
from loguru import logger
from core.MySystemTrayIcon import MySystemTrayIcon

from ui.main_window import Ui_MainWindow as main_window
from win.about_form import about_win
from win.close_dialog import close_dialog
from win.help_form import help_win
from win.main_widget import main_widget
from win.sound_recording_form import sound_recording_win


class main_win(QMainWindow, main_window):
    def __init__(self):
        super(main_win, self).__init__()
        self.setupUi(self)

        # 隐藏原始的框,关闭缩小按钮事件绑定
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.close_pushButton.clicked.connect(self.close_event)
        self.min_pushButton.clicked.connect(self.showMinimized)
        self._startPos = None
        self._endPos = None

        # 程序托盘图标
        self.show_tray_icon = close_dialog(parent=self)
        self.tray_icon = MySystemTrayIcon()
        self.tray_icon.init(self)  # 将自己传进去
        self.tray_icon.show()

        self.main_pushButton.clicked.connect(self.main_pushButton_event)
        self.about_pushButton.clicked.connect(self.about_pushButton_event)
        self.sound_recording_pushButton.clicked.connect(self.sound_recording_pushButton_event)
        self.help_pushButton.clicked.connect(self.help_pushButton_event)

        self.main_widget = main_widget(self)
        self.main_layout.addWidget(self.main_widget)
        self.main_widget.show()

    def mousePressEvent(self, e: QMouseEvent):
        if e.button() == Qt.LeftButton:
            self._isTracking = True
            self._startPos = QPoint(e.x(), e.y())

    def mouseMoveEvent(self, e: QMouseEvent):  # 重写移动事件
        self._endPos = e.pos() - self._startPos
        self.move(self.pos() + self._endPos)

    def mouseReleaseEvent(self, e: QMouseEvent):
        if e.button() == Qt.LeftButton:
            self._isTracking = False
            self._startPos = None
            self._endPos = None

    def main_pushButton_event(self):
        logger.info("显示主界面")
        while self.main_layout.count():
            p = self.main_layout.itemAt(0).widget()
            p.setParent(None)
            self.main_layout.removeWidget(p)
            p.destroy(True)
        self.main_widget = main_widget(self)
        self.main_layout.addWidget(self.main_widget)
        self.main_widget.show()

    def about_pushButton_event(self):
        logger.info("显示关于界面")
        while self.main_layout.count():
            p = self.main_layout.itemAt(0).widget()
            p.setParent(None)
            self.main_layout.removeWidget(p)
            p.destroy(True)
        self.about_widget = about_win(self)
        self.main_layout.addWidget(self.about_widget)
        self.about_widget.show()

    def sound_recording_pushButton_event(self):
        logger.info("显示录音界面")
        while self.main_layout.count():
            p = self.main_layout.itemAt(0).widget()
            p.setParent(None)
            self.main_layout.removeWidget(p)
            p.destroy(True)
        self.sound_recording_widget = sound_recording_win(self)
        self.main_layout.addWidget(self.sound_recording_widget)
        self.sound_recording_widget.show()

    def help_pushButton_event(self):
        logger.info("显示帮助界面")
        while self.main_layout.count():
            p = self.main_layout.itemAt(0).widget()
            p.setParent(None)
            self.main_layout.removeWidget(p)
            p.destroy(True)
        self.help_widget = help_win(self)
        self.main_layout.addWidget(self.help_widget)
        self.help_widget.show()

    # 关闭的逻辑
    def close_event(self):
        logger.info("是否关闭主窗口")
        self.show_tray_icon.show()
