import os


def tap(x, y):
    os.system(f"adb shell input tap {x} {y}")

def screenshot(fp="screen"):
    os.system(f"adb exec-out screencap -p > {fp}.png")

screenshot()