call C:\DevelopmentTools\Miniconda3\miniconda3\Scripts\activate.bat C:\DevelopmentTools\Miniconda3\miniconda3\envs\bysj
pyrcc5 res/app.qrc -o res/app_rc.py
python -m PyQt5.uic.pyuic ui/main_window.ui -o ui/main_window.py --import-from=res
python -m PyQt5.uic.pyuic ui/main_widget.ui -o ui/main_widget.py --import-from=res
python -m PyQt5.uic.pyuic ui/close_dialog.ui -o ui/close_dialog.py --import-from=res
python -m PyQt5.uic.pyuic ui/login_form.ui -o ui/login_form.py --import-from=res
python -m PyQt5.uic.pyuic ui/register_form.ui -o ui/register_form.py --import-from=res
python -m PyQt5.uic.pyuic ui/mysql_form.ui -o ui/mysql_form.py --import-from=res
python -m PyQt5.uic.pyuic ui/about_frame.ui -o ui/about_frame.py --import-from=res
python -m PyQt5.uic.pyuic ui/help_frame.ui -o ui/help_frame.py --import-from=res
python -m PyQt5.uic.pyuic ui/sound_recording_frame.ui -o ui/sound_recording_frame.py --import-from=res