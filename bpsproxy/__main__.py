"""
Tool to render video proxies using FFMPEG
Offers mp4 and webm options
"""
import argparse as ap
import glob as g
import os.path as osp

from .call import call, call_makedirs
from .commands import get_commands_all
from .config import CONFIG as C
from .utils import checktools, ToolError


def find_files(directory='.',
               ignored_directory=C['proxy_directory'],
               extensions=C['extensions']['all']):
    xs = g.iglob('{}/**'.format(osp.abspath(directory)), recursive=True)
    xs = filter(lambda x: osp.isfile(x), xs)
    xs = filter(lambda x: ignored_directory not in osp.dirname(x), xs)
    xs = [x for x in xs if osp.splitext(x)[1] in extensions]
    return len(xs), xs


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
    tools = ['ffmpeg']
    try:
        clargs = parse_arguments(C)
        checktools(tools)
        n, path_i = find_files(clargs.working_directory)
        kwargs = {'path_i': path_i,
                  'n': n}
        call_makedirs(C, clargs, **kwargs)
        call(C, clargs, cmds=get_commands_all(C, clargs, **kwargs), **kwargs)
    except ToolError as e:
        print(e)


# this is so it can be ran as a module: `python3 -m bpsrender` (for testing)
if __name__ == '__main__':
    main()

