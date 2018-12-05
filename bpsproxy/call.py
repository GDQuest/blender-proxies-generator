# import multiprocessing as mp
import os
import subprocess as sp
import sys
from functools import partial
from itertools import chain
from tqdm import tqdm
from .utils import get_dir, kickstart

WINDOWS = ('win32', 'cygwin')


def call_makedirs(cfg, clargs, **kwargs):
    path_i = kwargs['path_i']
    path_d = map(partial(get_dir, cfg, clargs, **kwargs), path_i)
    path_d = chain(*path_d)
    path_d = (os.makedirs(p, exist_ok=True) for p in path_d)
    kickstart(path_d)


def call(cfg, clargs, *, cmds, **kwargs):
    kwargs_s = {'stdout': sp.PIPE,
                'stderr': sp.STDOUT,
                'universal_newlines': True,
                'check': kwargs.get('check', True),
                'shell': kwargs.get('shell', False),
                'creationflags': sp.CREATE_NEW_PROCESS_GROUP if sys.platform in WINDOWS else 0}
    if kwargs_s['shell']:
        cmds = map(lambda cmd: (cmd[0], ' '.join(cmd[1])), cmds)
    n = len(kwargs['path_i'])
    ps = tqdm(map(lambda cmd: sp.run(cmd[1], **kwargs_s), cmds),
              total=n,
              unit='file' if n == 1 else 'files')
    return [p.stdout for p in ps]

