"""
Collection of utility functions, class-independent
"""
import os.path as osp
import subprocess
from collections import deque
from shutil import which


class ToolError(Exception):
    """Raised if external dependencies aren't found on system.
    """
    pass


def checktools(tools):
    tools = [(t, which(t) or '') for t in tools]
    check = {'tools': tools,
             'test': all(map(lambda x: x[1], tools))}
    if not check['test']:
        msg = ["BPSProxy couldn't find external dependencies:"]
        msg += ['[{check}] {tool}: {path}'.format(check='v' if path is not '' else 'X',
                                                  tool=tool, path=path or 'NOT FOUND')
                for tool, path in check['tools']]
        msg += [('Check if you have them properly installed and available in the PATH'
                 ' environemnt variable.'),
                'Exiting...']
        raise ToolError('\n'.join(msg))


def get_frame_count(media_file_path):
    """
    Returns the number of frames in the video, using the ffprobe program
    """
    ffprobe_frame_cmd = [
        "ffprobe",
        "-v",
        "error",
        "-select_streams",
        "v:0",
        "-show_entries",
        "stream=nb_frames",
        "-of",
        "default=noprint_wrappers=1:nokey=1",
        media_file_path,
    ]
    return int(subprocess.check_output(ffprobe_frame_cmd).decode())


def get_path_video(cfg, clargs, path, **kwargs):
    return osp.join(osp.dirname(path), cfg['proxy_directory'], osp.basename(path),
                    'proxy_{size}.avi')


def get_path_image(cfg, clargs, path, **kwargs):
    return osp.join(osp.dirname(path), cfg['proxy_directory'], 'images', '{size}',
                    '{file}_proxy.jpg'.format(file=osp.basename(path)))


def get_path(cfg, clargs, what, path, **kwargs):
    get_path_f = {'video': get_path_video,
                  'image': get_path_image}
    return get_path_f[what](cfg, clargs, path, **kwargs)


def get_dir_video(cfg, clargs, path, **kwargs):
    return iter((osp.join(osp.dirname(path), cfg['proxy_directory'], osp.basename(path)),))


def get_dir_image(cfg, clargs, path, **kwargs):
    ps = osp.join(osp.dirname(path), cfg['proxy_directory'], 'images', '{size}')
    return map(lambda s: ps.format(size=s), clargs.sizes)


def get_dir(cfg, clargs, path, **kwargs):
    get_dir_f = {'video': get_dir_video,
                 'image': get_dir_image}
    what = 'video' if osp.splitext(path)[1] in cfg['extensions']['video'] else 'image'
    return get_dir_f[what](cfg, clargs, path, **kwargs)


def kickstart(it):
    deque(it, maxlen=0)

