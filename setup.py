from setuptools import setup

APP = ['kindle_extractor_gui.py']
DATA_FILES = []
OPTIONS = {
    'argv_emulation': True,
    'packages': ['tkinter'],
    'iconfile': None,  # You can add an icon file path here if you want
    'plist': {
        'CFBundleName': 'Kindle Extractor',
        'CFBundleDisplayName': 'Kindle Extractor',
        'CFBundleGetInfoString': "Convert Kindle highlights to markdown",
        'CFBundleIdentifier': "com.kindleextractor",
        'CFBundleVersion': "1.0.0",
        'CFBundleShortVersionString': "1.0.0",
    }
}

setup(
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)
