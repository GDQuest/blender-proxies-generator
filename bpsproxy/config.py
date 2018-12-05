import multiprocessing as mp
from itertools import chain
import logging as lg


CONFIG = {
    'logger': 'BPS',
    'proxy_directory': 'BL_proxy',
    'proxy_sizes': (25, 50, 100),
    'extensions': {
        'video': {'.mp4', '.mkv', '.mov', '.flv', '.mts'},
        'image': {'.png', '.jpg', '.jpeg'}
    },
    'presets': {
        'webm': '-c:v libvpx -crf 25 -speed 16 -threads {}'.format(str(mp.cpu_count())),
        'mp4': '-c:v libx264 -crf 25 -preset faster',
        'nvenc': '-c:v h264_nvenc -qp 25 -preset fast'
    },
    'pre': {'work': '»',
            'done': '•',
            'skip': '~'}
}
CONFIG['extensions']['all'] = set(chain(*CONFIG['extensions'].values()))

LOGGER = lg.getLogger(CONFIG['logger'])
LOGLEV = [lg.INFO, lg.DEBUG]
LOGLEV = [None] + sorted(LOGLEV, reverse=True)

