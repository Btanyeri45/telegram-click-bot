import argparse
import subprocess
import sys
import webbrowser


def open(url: str):
    s = sys.platform
    if s == 'windows':
        proc = subprocess.run(['start', url], capture_output=True)
        c = proc.returncode
    elif s == 'linux':
        proc = subprocess.run(['xdg-open', url], capture_output=True)
        c = proc.returncode
    else:
        webbrowser.open(url, new=2, autoraise=False)
        c = 1
    return c


def args():
    parser = argparse.ArgumentParser()
    parser.add_argument('url', type=str)
    return parser.parse_args()


if __name__ == '__main__':
    _ = open(args().url)
