import datetime
import os
import wave
from threading import Thread

from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QWidget, QFileDialog
from loguru import logger
from pyaudio import PyAudio, paInt16

from utils import global_var as gl

from ui.sound_recording_frame import Ui_Frame as sound_recording_frame


class sound_recording_win(QWidget, sound_recording_frame):
    def __init__(self, parent=None):
        super(sound_recording_win, self).__init__(parent)
        self.setupUi(self)

        # 保存文件的路径按钮设置
        self.sound_recording_save_path_pushButton.clicked.connect(self.sound_recording_save_path_event)
        self.sound_recording_save_path_lineEdit.setText(os.path.join(os.path.expanduser("~"), 'Desktop'))

        # 设置保存文件名
        self.save_name_pushButton.clicked.connect(self.save_name_event)
        time1_str = datetime.datetime.strftime(datetime.datetime.now(), '%Y_%m_%d_%H_%M_%S')
        self.save_name_lineEdit.setText(time1_str)

        # 默认的保存路径显示
        self.show_save_path_label.setText(
            "文件保存在：" + os.path.join(os.path.expanduser("~"), 'Desktop') + "\\" + time1_str + ".wav")

        # 录音窗口的按钮设置
        self.sound_recording_save_path_start_pushButton.clicked.connect(self.sound_recording_save_path_start_event)
        self.sound_recording_save_path_end_pushButton.clicked.connect(self.pause)

        # 声明PyAudio对象
        self.pa = None
        # 创建定时器
        self.timer = QTimer()
        self.timer.timeout.connect(self.show_time)
        # 计时时间
        self.h = 0
        self.m = 0
        self.s = 0
        # 计时器停止标志，为真则停止，为假则继续
        self.pause_flag = True
        # 创建线程对象
        self.t_record = None
        self.t_discover = None

    def pause(self):
        logger.info("结束录音")
        self.pause_flag = True
        self.sound_recording_save_path_start_pushButton.setEnabled(True)
        self.sound_recording_save_path_end_pushButton.setEnabled(False)
        gl.set_value("is_record", True)

    def show_time(self):
        if self.pause_flag is False:
            self.s += 1
            if self.s == 60:
                self.s = 0
                self.m = self.m + 1
            if self.m == 60:
                self.m = 0
                self.h = self.h + 1

            text = ''
            self.lcdNumber.setDigitCount(5)
            if self.h != 0:
                self.lcdNumber.setDigitCount(8)

            if self.s % 2 != 0 and self.h == 0:
                text = str(self.m) + ':' + str(self.s)
            if self.s % 2 == 0 and self.h == 0:
                text = str(self.m) + ' ' + str(self.s)
            if self.h != 0:
                text = str(self.h) + ':' + text

            self.lcdNumber.display(text)

    def save_name_event(self):
        self.show_save_path_label.setText(
            "文件保存在\n" + self.sound_recording_save_path_lineEdit.text() + "\\" + self.save_name_lineEdit.text() + ".wav")

    def sound_recording_save_path_event(self):
        logger.info("保存文件的路径按钮设置")
        filePath = QFileDialog.getExistingDirectory(self, "选择存储路径", os.path.join(os.path.expanduser("~"), 'Desktop'))
        if filePath == "":
            logger.error("请选择路径")
            return
        self.sound_recording_save_path_lineEdit.setText(filePath)

    def sound_recording_save_path_start_event(self):
        logger.info("开始录音")
        # self.widget.setVisible(True)
        self.sound_recording_save_path_start_pushButton.setEnabled(False)
        self.sound_recording_save_path_end_pushButton.setEnabled(True)

        self.lcdNumber.setDigitCount(4)
        self.lcdNumber.display('0:0')
        # self.timer_dec.start(1000)

        self.timer.start(999)
        self.t_record = Thread(target=self.recording)
        self.t_record.start()
        # self.widget.start_audio()  # 触发MatplotlibWidget的startAudio函数

    def recording(self):
        save_path = os.path.join(self.sound_recording_save_path_lineEdit.text(),
                                 self.save_name_lineEdit.text() + ".wav")
        self.pause_flag = False
        # 创建PyAudio对象
        self.pa = PyAudio()
        # 打开声卡，设置 采样深度为16位、声道数为2、采样率为16、模式为输入、采样点缓存数量为2048
        stream = self.pa.open(format=paInt16, channels=1, rate=48000, input=True, frames_per_buffer=132690)
        # 新建一个列表，用来存储采样到的数据
        record_buf = []
        while True:
            if self.pause_flag is True:
                break
            audio_data = stream.read(2048)  # 读出声卡缓冲区的音频数据
            record_buf.append(audio_data)  # 将读出的音频数据追加到record_buf列表
        wf = wave.open(save_path, 'wb')  # 创建一个音频文件
        wf.setnchannels(1)  # 设置声道数为1
        wf.setsampwidth(2)  # 设置采样深度为2
        wf.setframerate(48000)  # 设置采样率为48000
        # 将数据写入创建的音频文件
        wf.writeframes("".encode().join(record_buf))
        # 写完后将文件关闭
        wf.close()
        # 停止声卡
        stream.stop_stream()
        # 关闭声卡
        stream.close()
        # 终止pyaudio
        self.pa.terminate()
