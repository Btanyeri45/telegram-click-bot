import argparse
import subprocess
import sys
import webbrowser


def open(url):
    s = sys.platform
    p = 1
    if s == 'windows':
        proc = subprocess.run(['start', f'{url}'], capture_output=True)
        p = proc.returncode
    elif s == 'linux':
        proc = subprocess.run(['xdg-open', f'{url}'], capture_output=True)
        p = proc.returncode
    else:
        webbrowser.open(url, new=2, autoraise=False)
    return p


def args():
    parser = argparse.ArgumentParser()
    parser.add_argument('url', type=str)
    return parser.parse_args()


if __name__ == '__main__':
    _ = open(args().url)
