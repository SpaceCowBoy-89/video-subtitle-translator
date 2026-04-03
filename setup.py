"""
Setup script for creating a standalone macOS application bundle.
"""

from setuptools import setup

APP = ['main.py']
DATA_FILES = []
OPTIONS = {
    'argv_emulation': False,
    'packages': [
        'PySide6',
        'deepl',
        'whisper',
        'pysrt',
        'ffmpeg',
        'torch',
        'numpy',
    ],
    'includes': [
        'app',
        'app.core',
        'app.workers',
        'app.gui',
    ],
    'excludes': [
        'matplotlib',
        'scipy',
        'pandas',
        'PIL',
    ],
    'plist': {
        'CFBundleName': 'Video Subtitle Translator',
        'CFBundleDisplayName': 'Video Subtitle Translator',
        'CFBundleIdentifier': 'com.translator.videosubtitles',
        'CFBundleVersion': '1.0.0',
        'CFBundleShortVersionString': '1.0.0',
        'NSHumanReadableCopyright': '2024',
        'NSHighResolutionCapable': True,
        'LSMinimumSystemVersion': '10.15',
        'CFBundleDocumentTypes': [
            {
                'CFBundleTypeName': 'Video Files',
                'CFBundleTypeRole': 'Viewer',
                'LSItemContentTypes': [
                    'public.movie',
                    'public.video',
                ],
                'LSHandlerRank': 'Alternate',
            },
            {
                'CFBundleTypeName': 'Subtitle Files',
                'CFBundleTypeRole': 'Viewer',
                'LSItemContentTypes': [
                    'public.subtitle',
                ],
                'LSHandlerRank': 'Alternate',
            },
        ],
    },
}

setup(
    name='VideoSubtitleTranslator',
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)
