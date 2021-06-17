import argparse
import subprocess
import sys
import webbrowser


def open(url):
    _sys = sys.platform
    _prc = 1
    if _sys == 'windows':
        proc = subprocess.run(['start', f'{url}'], capture_output=True)
        _prc = proc.returncode
    elif _sys == 'linux':
        proc = subprocess.run(['xdg-open', f'{url}'], capture_output=True)
        _prc = proc.returncode
    else:
        webbrowser.open(url, new=2, autoraise=False)
    return _prc


def args():
    parser = argparse.ArgumentParser()
    parser.add_argument('url', type=str)
    return parser.parse_args()


if __name__ == '__main__':
    _ = open(args().url)
