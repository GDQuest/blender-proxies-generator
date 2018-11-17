"""
Tool to render video proxies using FFMPEG
Offers mp4 and webm options
"""
import argparse as ap
import glob as g
import os.path as osp

from .commands import get_commands_all
from .config import CONFIG as C


def find_files(directory='.',
               ignored_directory=C['proxy_directory'],
               extensions=C['extensions']['all']):
    xs = g.iglob('{}/**'.format(osp.abspath(directory)), recursive=True)
    xs = filter(lambda x: osp.isfile(x), xs)
    xs = filter(lambda x: ignored_directory not in osp.dirname(x), xs)
    xs = [x for x in xs if osp.splitext(x)[1] in extensions]
    return xs


def parse_arguments(cfg):
    """
    Returns an argparse object with all command line arguments
    """
    p = ap.ArgumentParser(description='Create proxies for Blender VSE using FFMPEG.')
    p.add_argument('working_directory', nargs='?', default='.',
                   help='The directory containing media to create proxies for')
    p.add_argument('-p', '--preset',
                   default='mp4',
                   choices=cfg['presets'],
                   help='a preset name for proxy encoding')
    p.add_argument('-s', '--sizes',
                   nargs='+',
                   type=int,
                   default=[25],
                   choices=cfg['proxy_sizes'],
                   help='A list of sizes of the proxies to render, either 25, 50, or 100')
    p.add_argument('--dry-run',
                   action='store_true',
                   help=('Run the script without actual rendering or creating files and'
                         ' folders. For DEBUGGING purposes'))
    return p.parse_args()


def main():
    clargs = parse_arguments(C)
    for c in get_commands_all(C, clargs, **{'path_i': find_files()}):
        print(' '.join(c[1]))
        break

