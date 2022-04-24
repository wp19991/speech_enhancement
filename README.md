## 语音增强客户端

## 项目结构

- 具体参考我写的这个项目的框架来建立的
- `https://github.com/wp19991/PyQt5_example`

## 基本界面

![启动界面](./doc/img/1.png)
![主界面1](./doc/img/2.png)
![主界面2](./doc/img/5.png)
![主界面3](./doc/img/6.png)
![录音界面](./doc/img/3.png)
![关于界面](./doc/img/4.png)

## 功能介绍

- 输入语音文件
    - [√]打开文件
    - [√]输入路径

- 录音
    - [×]选择录音设备
    - [√]显示当前录音的大小状态（是否进行录音）

- 进行处理
    - [√]切换不同的处理
    - [√]选择模型
    - [√]进行处理的按钮
    - [√]显示处理的进度

- 保存处理好的语音文件
    - [√]选择输出目录

- 播放语音文件
    - [√]播放语音文件
    - [×]控制声音大小

- 显示图片plt
    - [√]显示处理进度
    - [√]噪音的图片
    - [√]处理之后的图片

- 显示帮助
    - [√]显示作者信息
    - [×]输出帮助文档pdf文件

## Environmental installation

```bash
# 创建conda环境
conda create -n bysj python=3.8
# 激活conda环境
conda activate bysj

# Installation Library
pip install -r requirements.txt

# 需要下载模型文件model.pkl保存到下面的目录里面
# 下载地址：https://wp19991.oss-cn-hangzhou.aliyuncs.com/model.pkl
/core/speech_enhancement_core/SEGAN/model.pkl

# 安装PyAudio
# pyaudio安装不上的话就去官网（https://pypi.org/）下载whl文件，然后pip install *.whl
pip install other/PyAudio-0.2.11-cp38-cp38-win_amd64.whl

# 打包
pyinstaller speech_enhancement_pyqt5_client.spec
```