#!/usr/bin/env python
# Installation script for Photostory

from distutils.core import setup

setup(name='Photostory',
      version='1.0',
      description='Photostory lets you use your webcam to photo yourself\
 every day, then compile them into a video.',
      long_description='NOTICE: The data storage format has changed between\
 versions 0.9 and 1.0, to continue using Photostory with your previous data\
 you will need to manually run a conversion program. The conversion program\
 can be downloaded from <http://launchpad.net/photostory/trunk/0.9/+download/\
photostory_0.9_to_1.0.py>.',
      author='Photostory Team',
      author_email='photostory@lists.launchpad.net',
      maintainer='Joel Auterson',
      maintainer_email='joel.auterson@googlemail.com',
      keywords=['photo', 'story', 'daily', 'picture', 'webcam', 'story',
                'video'],
      url='http://launchpad.net/photostory',
      license='GNU GPL v3',
      scripts=['photostory', 'photostory_reminder'],
      data_files=[
                  ('/etc/xdg/autostart/', ['photostory_reminder.desktop']),
                  ('share/applications/', ['photostory.desktop']),
                  ('share/icons/hicolor/scalable/apps', ['photostory.svg']),
                 ],
      requires=['gst', 'gtk2']
     )
