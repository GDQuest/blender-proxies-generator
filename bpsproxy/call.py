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
    path_d = (lambda d: os.makedirs(d, exist_ok=True), path_d)
    kickstart(path_d)


def call(cfg, clargs, *, cmds, **kwargs):
    kwargs_s = {'stdout': sp.PIPE,
                'stderr': sp.STDOUT,
                'universal_newlines': True,
                'creationflags': sp.CREATE_NEW_PROCESS_GROUP if sys.platform in WINDOWS else 0}
    ps = tqdm(map(lambda cmd: sp.Popen(cmd[1], **kwargs_s), cmds),
              total=kwargs['n'],
              unit='file' if kwargs['n'] == 1 else 'files')
    kickstart(ps)

