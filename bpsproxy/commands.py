import os.path as osp
from itertools import chain
from .utils import get_path


def get_commands_check(cfg, clargs, **kwargs):
    cmd = ('ffprobe -v error -select_streams v:0 -show_entries stream=nb_frames -of'
           ' default=noprint_wrappers=1:nokey=1 {file}')
    out = map(lambda s: kwargs['path_o_1'].format(size=s), clargs.sizes)
    out = map(lambda f: cmd.format(file=f), out)
    out = (cmd.format(file=kwargs['path_i_1']) + ' && ' + ' && '.join(out)).split()
    return iter((out,))


def get_commands_image_1(cfg, clargs, **kwargs):
    cmd = 'ffmpeg -y -v quiet -stats -i {path_i_1} {common_all}'
    common = '-f apng -filter:v scale=iw*{size}:ih*{size} {path_o_1}'
    common_all = map(lambda s: kwargs['path_o_1'].format(size=s), clargs.sizes)
    common_all = map(lambda s: common.format(size=s[0]/100.0, path_o_1=s[1]),
                     zip(clargs.sizes, common_all))
    common_all = ' '.join(common_all)
    out = cmd.format(path_i_1=kwargs['path_i_1'], common_all=common_all).split()
    return iter((out,))


def get_commands_video_1(cfg, clargs, **kwargs):
    cmd = 'ffmpeg -y -v quiet -stats -i {path_i_1} {common_all}'
    common = ('-pix_fmt yuv420p'
              ' -g 1'
              ' -sn -an'
              ' -vf colormatrix=bt601:bt709'
              ' -vf scale=iw*{size}:ih*{size}'
              ' {preset}'
              ' {path_o_1}')
    common_all = map(lambda s: kwargs['path_o_1'].format(size=s), clargs.sizes)
    common_all = map(lambda s: common.format(preset=cfg['presets'][clargs.preset],
                                             size=s[0]/100.0,
                                             path_o_1=s[1]),
                     zip(clargs.sizes, common_all))
    common_all = ' '.join(common_all)
    out = cmd.format(path_i_1=kwargs['path_i_1'], common_all=common_all).split()
    return iter((out,))


def get_commands(cfg, clargs, *, what, **kwargs):
    get_commands_f = {'video': get_commands_video_1,
                      'image': get_commands_image_1,
                      'check': get_commands_check}
    ps = (kwargs['path_i']
          if what not in cfg['extensions'] else
          filter(lambda p: osp.splitext(p)[1] in cfg['extensions'][what], kwargs['path_i']))
    ps = map(lambda p: (p, get_path(cfg, clargs, p, **kwargs)), ps)
    out = chain.from_iterable(map(lambda p: get_commands_f[what](cfg, clargs, path_i_1=p[0],
                                                                 path_o_1=p[1], **kwargs), ps))
    return map(lambda c: (what, c), out)


def get_commands_vi(cfg, clargs, **kwargs):
    ws = filter(lambda x: x is not 'all', cfg['extensions'])
    return chain.from_iterable(map(lambda w: get_commands(cfg, clargs, what=w, **kwargs), ws))

