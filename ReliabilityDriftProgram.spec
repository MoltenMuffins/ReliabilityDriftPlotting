# -*- mode: python -*-

block_cipher = None


a = Analysis(['ReliabilityDriftProgram.py'],
             pathex=[
                    'C:\\Users\\econ\\Documents\\Python\\ReliabilityDrift',
                    'C:/Users/econ/AppData/Local/Continuum/anaconda3/pkgs/plotly-3.7.0-py_0/site-packages/plotly/offline'
                    ],
             binaries=[],
             datas=[
                    ('C:/Users/econ/AppData/Local/Continuum/anaconda3/pkgs/plotly-3.7.0-py_0', './plotly/'),
                    ('C:/Users/econ/AppData/Local/Continuum/anaconda3/pkgs/plotly-3.7.0-py_0/site-packages/plotly/offline/', './plotly/offline/'),
                    ('C:/Users/econ/AppData/Local/Continuum/anaconda3/pkgs/plotly-3.7.0-py_0/site-packages/plotly/package_data/plotly.min.js', './plotly/package_data/')
                    ],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='ReliabilityDriftProgram',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          runtime_tmpdir=None,
          console=True,
          icon='C:/Users/econ/Documents/Python/ReliabilityDrift/ReliabilityDriftIcon.ico')
