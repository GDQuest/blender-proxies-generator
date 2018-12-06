## UNDER DEVELOPMENT

# Blender Power Sequencer Proxy

This is a [standalone python package](https://pypi.org/project/bpsproxy/) as well as a module which is used under the hood in the [Blender Power Sequencer add-on](https://github.com/GDquest/Blender-power-sequencer) to generate better proxies to be used in Blender.


## Install

It can be installed as a standalone command line utility [via PiPy](https://pypi.org/project/bpsproxy/): `pip install [--user] bpsproxy`. *Note* that you have to have `$HOME/.local/bin` included in your `$PATH` environment variable (on unix) if you're going to install the utility locally (using `--user` when executing `pip`).


## Usage

After installing the script, get help by writing `bpsproxy -h`:

```
usage: bpsproxy [-h] [-p {webm,mp4,nvenc}] [-s {25,50,100} [{25,50,100} ...]]
                [-v] [--dry-run]
                [working_directory]

Create proxies for Blender VSE using FFMPEG.

positional arguments:
  working_directory     The directory containing media to create proxies for

optional arguments:
  -h, --help            show this help message and exit
  -p {webm,mp4,nvenc}, --preset {webm,mp4,nvenc}
                        a preset name for proxy encoding
  -s {25,50,100} [{25,50,100} ...], --sizes {25,50,100} [{25,50,100} ...]
                        A list of sizes of the proxies to render, either 25,
                        50, or 100
  -v, --verbose         Increase verbosity level (eg. -vvv).
  --dry-run             Run the script without actual rendering or creating
                        files and folders. For DEBUGGING purposes
```

## External Dependencies

`BPSProxy` requires

- `ffmpeg`
- `ffprobe`

to be available in the `$PATH` environment variable in order to work. In case `BPSProxy` will catch a missing dependency it will throw a message error similar to this:

```
ERROR:BPS:BPSProxy couldn't find external dependencies:
[X] ffmpeg: NOT FOUND
[X] ffprobe: NOT FOUND
Check if you have them properly installed and available in the PATH environemnt variable.
~ Exiting.
```
