from setuptools import setup


def readme():
    with open('README.rst') as f:
        return f.read()


setup(name='bpsproxy',
      version='0.1.3',
      description='Blender Power Sequencer proxy generator tool',
      long_description=readme(),
      classifiers=[
          'Development Status :: 4 - Beta',
          'Environment :: Console',
          'Intended Audience :: End Users/Desktop',
          'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
          'Natural Language :: English',
          'Programming Language :: Python :: 3.3',
          'Programming Language :: Python :: 3.4',
          'Programming Language :: Python :: 3.5',
          'Programming Language :: Python :: 3.6',
          'Programming Language :: Python :: 3.7',
          'Programming Language :: Python :: 3',
          'Topic :: Multimedia :: Video',
          'Topic :: Utilities'
      ],
      url='https://gitlab.com/razcore/bpsproxy',
      keywords='blender proxy vse sequence editor productivity',
      author='Răzvan C. Rădulescu',
      author_email='razcore.art@gmail.com',
      license='GPLv3',
      packages=['bpsproxy'],
      install_requires=['tqdm'],
      zip_safe=False,
      entry_points={'console_scripts': ['bpsproxy=bpsproxy.__main__:main']},
      include_package_data=True)

