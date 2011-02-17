#!/usr/bin/env python
# Installation script for Photostory

from distutils.core import setup
import os

setup(name='Photostory',
      version='1.0',
      description='Photostory lets you use your webcam to photo yourself\
 every day, then compile them into a video.',
      #long_description='''XXX''',
      author='Photostory Team',
      author_email='photostory-team@lists.launchpad.net',
      maintainer='Joel Auterson',
      maintainer_email='joel.auterson@googlemail.com',
      keywords=['photo', 'story', 'daily', 'picture', 'webcam', 'story',
                'video'],
      url='http://launchpad.net/photostory',
      license='GNU GPL v3',
      scripts=['photostory', 'photostory_reminder'],
      data_files=[
                  ('share/applications/', ['photostory.desktop']),
                  ('share/icons/hicolor/scalable/apps', ['photostory.svg']),
                 ],
      requires=['gst', 'gtk2']
     )
