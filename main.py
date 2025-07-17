import os


def tap(x, y):
    os.system(f"adb shell input tap {x} {y}")
