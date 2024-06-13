import os

os.system("pip3 install pyinstaller")
os.system("pyinstaller --onefile game.py ai.py --name pbrain-gomoku-ai.exe")