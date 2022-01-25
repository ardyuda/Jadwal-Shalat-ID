import os

def install(source):
    os.system(f'cmd /c "pip install {source}"')

try:
    import tkinter
except ImportError:
    install('tkinter')

try:
    import cryptocode
except ImportError:
    install('cryptocode')

try:
    import bs4
except ImportError:
    install('beautifulsoup4')

try:
    import requests
except ImportError:
    install('request')