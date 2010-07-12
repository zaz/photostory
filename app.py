#!/usr/bin/python

#Photostory 0.9
#by Joel Auterson (joel.auterson@googlemail.com)
#http://www.launchpad.net/photostory

import pygst
pygst.require("0.10")
import gst
import pygtk
import gtk
from time import strftime
import time
import os.path
import cPickle

class Main:


    def __init__(self):

        pipeline = None
        xvimagesink = None
        movie = None
        pic=None
        self.db = cPickle.load(open('data/db', 'rb'))
        self.ind = int(cPickle.load(open('data/num', 'rb')))
        todayPicName = "pictures/" + str(self.ind) + ".png"
        todayDate = None

        def chooseDay(cal):
            dateTuple = cal.get_date()
            if dateTuple in self.db:
                pic.set_from_file(self.db[dateTuple])
            else:
                pic.set_from_file("data/nopic.png")

        def closedown(win):
            print 'ind ' + str(self.ind)
            print 'db' + str(self.db)
            cPickle.dump(self.db, open('data/db', 'wb'))
            cPickle.dump(self.ind, open('data/num', 'wb'))
            gtk.main_quit()

        def about(aboutBut):
            dAbout = gtk.AboutDialog()
            dAbout.set_name("Photostory")
            dAbout.set_comments("Photostory is an application that lets you tell the story of your life in pictures, by taking a snapshot of you each day. You can then make these into a video to share with friends or on the internet.")
            response = dAbout.run()
            if response == -6:
                dAbout.destroy()

        def movify(filmBut):

            def movGen(movButton):

                movPath = movEntry.get_text()
                movDia.destroy()

                filmPipe = gst.Pipeline("filmPipe")
                filmSrc = gst.element_factory_make("multifilesrc", "filmSrc")
                filmSrc.set_property("location", "pictures/%d.png")
                filmFilt1 = gst.element_factory_make("capsfilter", "filmFilt1")
                filmCap1 = gst.Caps("image/png,framerate=5/1,pixel-aspect-ratio=1/1")
                filmFilt1.set_property("caps", filmCap1)
                filmPngDec = gst.element_factory_make("pngdec", "filmPngDec")
                filmff = gst.element_factory_make("ffmpegcolorspace", "filmff")
                filmFilt2 = gst.element_factory_make("capsfilter", "filmFilt2")
                filmCap2 = gst.Caps("video/x-raw-yuv")
                filmFilt2.set_property("caps", filmCap2)
                filmTheora = gst.element_factory_make("xvidenc", "filmTheora")
                filmOggmux = gst.element_factory_make("ffmux_mp4", "filmOggmux")
                filmFilesink = gst.element_factory_make("filesink", "filmFilesink")
                filmFilesink.set_property("location", movPath)

                filmPipe.add(filmSrc, filmFilt1, filmPngDec, filmff, filmFilt2, filmTheora, filmOggmux, filmFilesink)
                gst.element_link_many(filmSrc, filmFilt1, filmPngDec, filmff, filmFilt2, filmTheora, filmOggmux, filmFilesink)
                filmPipe.set_state(gst.STATE_PLAYING)
                time.sleep(5)
                filmBut.set_sensitive(True)

            movDia = gtk.Window(gtk.WINDOW_TOPLEVEL)
            filmBut.set_sensitive(False)
            movVbox = gtk.VBox(homogeneous=False, spacing=2)
            movLabel = gtk.Label("Here you can create a video made up of all your pictures.\nRemember, the path MUST end in '.mp4'.")

            movLabel_2 = gtk.Label("Path:")
            movEntry = gtk.Entry()
            movHbox_1 = gtk.HBox(homogeneous=True)
            movButton = gtk.Button(label="Create")
            movDia.add(movVbox)
            movVbox.pack_start(movLabel, expand=False)
            movVbox.pack_start(movHbox_1, expand=False)
            movVbox.pack_start(movButton, expand=False)
            movHbox_1.pack_start(movLabel_2, expand=False)
            movHbox_1.pack_start(movEntry, expand=False)
            movButton.connect("clicked", movGen)
            movDia.show_all()

        def capture(takeBut):
            pipeline.set_state(gst.STATE_NULL)
            stillPipe = gst.Pipeline("stillPipe")
            stillCam = gst.element_factory_make("v4l2src", "stillPipe")
            stillFilt = gst.element_factory_make("capsfilter", "stillFilt")
            stillCap = gst.Caps("video/x-raw-yuv,width=640,height=480")
            stillFilt.set_property("caps", stillCap)
            ffmpegcolorspace = gst.element_factory_make("ffmpegcolorspace", "ffmpegcolorspace")
            pngEnc = gst.element_factory_make("pngenc", "pngenc")
            filesink = gst.element_factory_make("filesink", "filesink")
            filesink.set_property("location", todayPicName)
            self.db[todayDate] = todayPicName
            cal.freeze()
            cal.select_month(todayDate[1], todayDate[0])
            cal.select_day(todayDate[2])
            cal.thaw()
            stillPipe.add(stillCam, stillFilt, ffmpegcolorspace, pngEnc, filesink)
            gst.element_link_many(stillCam, stillFilt, ffmpegcolorspace, pngEnc, filesink)
            stillPipe.set_state(gst.STATE_PLAYING)
            time.sleep(1)
            stillPipe.set_state(gst.STATE_NULL)
            xvimagesink.set_xwindow_id(movie.window.xid)
            pipeline.set_state(gst.STATE_PLAYING)
            pic.set_from_file(todayPicName)
            self.ind += 1
            takeBut.set_label("Picture taken this day.")
            takeBut.set_sensitive(False)

        #Interface
        win = gtk.Window(gtk.WINDOW_TOPLEVEL)
        win.connect("destroy", closedown)
        win.set_default_size(900, 600)
        win.set_resizable(False)
        win.set_title("Photostory")
        win.set_icon_from_file("data/icon.svg")
        movie = gtk.DrawingArea()
        hbox = gtk.HBox(homogeneous=False, spacing=3)
        vbox1 = gtk.VBox(homogeneous=False)
        vbox2 = gtk.VBox(homogeneous = False)   
        filmBut = gtk.Button(label="Create Film")
        filmBut.connect("clicked", movify)
        shareBut = gtk.Button(label="Share Video")
        hbox2 = gtk.HBox(homogeneous=True)
        leftBut = gtk.Button(label="Previous")
        rightBut = gtk.Button(label="Next")
        aboutBut = gtk.Button(label="About")
        aboutBut.connect("clicked", about)
        pic = gtk.Image()
        cal = gtk.Calendar()
        todayDate = cal.get_date()
        cal.connect("day-selected", chooseDay)
        takeBut = gtk.Button(label="Take today's picture")
        takeBut.connect("clicked", capture)
        win.add(hbox)
        hbox.pack_start(vbox1, expand=False)
        hbox.pack_start(vbox2)
        vbox1.pack_start(pic)
        vbox1.pack_start(hbox2)
        hbox2.pack_start(filmBut, expand=False)
        #hbox2.pack_start(shareBut)
        #hbox2.pack_start(leftBut)
        #hbox2.pack_start(rightBut)
        hbox2.pack_start(aboutBut)
        hbox.pack_start(vbox2)
        vbox2.pack_start(movie)
        vbox2.pack_start(cal, expand=False, padding=50)
        vbox2.pack_start(takeBut, expand=False)
        if todayDate in self.db:
            pic.set_from_file(self.db[todayDate])
            takeBut.set_label("Picture taken for this day.")
            takeBut.set_sensitive(False)
        else:
            pic.set_from_file("data/nopic.png")

        win.show_all()

        #Pipeline stuff - feed
        pipeline = gst.Pipeline("mypipeline")

        camera = gst.element_factory_make("v4l2src", "camera")
        camera.set_property("device", "/dev/video0")

        caps = gst.Caps("video/x-raw-yuv,width=640,height=480,framerate=30/1")
        filt = gst.element_factory_make("capsfilter", "filter")
        filt.set_property("caps", caps)

        xvimagesink = gst.element_factory_make("xvimagesink", "sink")

        pipeline.add(camera, filt, xvimagesink)
        gst.element_link_many(camera, filt, xvimagesink)

        xvimagesink.set_xwindow_id(movie.window.xid)

        pipeline.set_state(gst.STATE_PLAYING)
        

start=Main()
gtk.main()
