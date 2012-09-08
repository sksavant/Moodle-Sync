#!/usr/bin/env python
import sys
import gtk
import pygtk
import gnomeapplet

pygtk.require("2.0")

def moodle_applet(applet,iid):
    label=gtk.Label("Moodle Sync")
    applet.add(label)
    applet.show_all()
    print ("Started Applet")
    #Do something

    return True

if __name__=='__main_': #testing
    print('Starting')
    if len(sys.argv) > 1 and sys.argv[1] == "-d":
        mainWindow=gtk.Window()
        mainWindow.set_title("Moodle Applet")
        mainWindow.connect("destroy",gtk.main_quit)
        applet=gnomeapplet.Applet()
        moodle_applet(applet,None)
        applet.reparent(mainWindow)
        mainWindow.show_all()
        gtk.main()
        sys.exit()
    else:
        gnomeapplet.bonobo_moodle('OAFIID:MoodleApplet',gnomeapplet.Applet.__gtype,"Moodle Sync","0.1",moodle_applet)
