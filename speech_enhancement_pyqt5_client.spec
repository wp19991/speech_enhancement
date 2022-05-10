# -*- mode: python ; coding: utf-8 -*-
import sys
sys.setrecursionlimit(5000)

block_cipher = None


a = Analysis(['app.py'],
             pathex=[],
             binaries=[],
             datas=[(r"res\*",r"res"),
             (r"config\config.toml",r"config"),
             (r"config\skin\white.qss",r"config\skin"),
             (r"models\db.sql",r"models"),
             (r'C:\DevelopmentTools\Miniconda3\Miniconda3\envs\bysj\Lib\site-packages\librosa\util\example_data\*',r'librosa\util\example_data'),
             (r"core\speech_enhancement_core\SEGAN\model.pkl",r"core\speech_enhancement_core\SEGAN")],
             hiddenimports=['sklearn.utils._typedefs','sklearn', 'sklearn.tree', 'sklearn.tree._utils',
                           'sklearn.neighbors._quad_tree','sklearn.neighbors._typedefs', 'sklearn.utils._cython_blas',
                           'sklearn.utils.sparsetools._graph_validation','sklearn.neighbors._partition_nodes',
                           'sklearn.utils.sparsetools._graph_tools', 'sklearn.utils.lgamma'],
             hookspath=[],
             hooksconfig={},
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)

for d in a.datas:
  if '_C.cp38-win_amd64.pyd' in d[0]:
    a.datas.remove(d)
    break

pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)

exe = EXE(pyz,
          a.scripts, 
          [],
          exclude_binaries=True,
          name='speech_enhancement_pyqt5_client',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=False,
          disable_windowed_traceback=False,
          target_arch=None,
          codesign_identity=None,
          entitlements_file=None , icon='res\\icon\\探测声音.ico',
          version="file_verison_info.txt")
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas, 
               strip=False,
               upx=True,
               upx_exclude=[],
               name='speech_enhancement_pyqt5_client')
