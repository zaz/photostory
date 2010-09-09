#!/usr/bin/env python
# Installation script for Photostory

from distutils.core import setup
import os

# Change the paths to point to the correct directories:
os.system('patch -b photostory install.diff')

setup(name='Photostory',
      version='0.9',
      description='Photostory lets you use your webcam to photo yourself\
 every day, then compile them into a video.',
      #long_description='''XXX''',
      author='Photostory Team',
      #author_email='https://launchpad.net/~photostory-team/+contactuser',
      maintainer='Joel Auterson',
      maintainer_email='joel.auterson@googlemail.com',
      keywords=['photo', 'story', 'daily', 'picture', 'webcam', 'story',
                'video'],
      url='http://launchpad.net/photostory',
      license='GNU GPL v3',
      data_files=[
                  ('share/bin', ['photostory']),
                  ('share/applications/', ['photostory.desktop']),
                  ('share/icons/hicolor/scalable/apps', ['photostory.svg']),
                 ],
      requires=['gst', 'gtk2']
     )