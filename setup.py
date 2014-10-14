#!/usr/bin/env python2
# Installation script for Photostory

from distutils.core import setup

setup(name='Photostory',
      version='1.0.1',
      description='Photostory lets you use your webcam to photo yourself\
 every day, then compile them into a video.',
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
