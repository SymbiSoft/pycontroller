# Introduction #

You have a macbook and don't have a apple remote controller for control slides when making a presentation ? If you got a cellphone with bluetooth, you now can use MacMote (Mobile remote controller app) to control the slides of your presentation.

Currently, the client is implemented in Python for S60 (Nokia cellphones) and the server is written purely in Python programming language using Objective-C Framework to send events for the MAC OS session.

For bluetooth it uses LightBlue (a python binding for Mac OS X).

Until now. The release is in 0.1. It only supports touchscreen devices.

Devices tested:  5800 XM.


Attention: MacMote client needs to be installed in the same drive where you installed Python for S60 runtime, i.e, you must install it in drive 'C' if you had installed Python in drive 'C'.

Attention: The Mac OS supported must have the PyObjC bridge (natively supported for Mac OS > 10.5.x). You may try to install the binding by yourself at their [website](http://pyobjc.sourceforge.net/)

# Support #

If you wanna port the controller for your symbian device, take a look at the source code provided at our project source folder.  You can port for your non-touchscreen devices!

# Video #

http://www.youtube.com/watch?v=h20QPSNC2Fc

# Screenshots #

![http://dl.dropbox.com/u/1977573/Scr000013.jpg](http://dl.dropbox.com/u/1977573/Scr000013.jpg)           ![http://dl.dropbox.com/u/1977573/Scr000015.jpg](http://dl.dropbox.com/u/1977573/Scr000015.jpg)
# Usage #

## Client ##

First, you have to download the latest version of the .sis package (macmote-version.sis)  for your cellphone. Check it at the Downloads section.  After downloading it, you have to pass it by bluetooth/cable or by Nokia PC Suite the package to your cellphone.

Don't forget before install it, to download and install the latest version of the [PyS60](https://garage.maemo.org/projects/pys60/) Runtime (by the time of the 0.1 release it was 1.9.7).

After install the mobile app (macmote-version.sis). You will see the icon of MacMote inside of Applications folder at your cellphone.

## Server ##

First, make sure that you have the PyOBJC binding working properly at your Mac OS.  To check it, just type at your terminal:
```
   $$ /usr/bin/python
   $$ Python 2.5.4 (r254:67917, Dec 23 2008, 14:57:27) 
        [GCC 4.0.1 (Apple Computer, Inc. build 5363)] on darwin 
        Type "help", "copyright", "credits" or "license" for more information. 
         >>> import objc
         >>>
```

If it doesn't show a 'ImportError' message. It's everything Ok!  If not make sure you have typed /usr/bin before python command. It's necessary to run the native python that comes with your Mac OS system.

Now, you have to install the LightBlue framework. It's necessary for the bluetooth connection. Download and install it from this [webpage](http://lightblue.sourceforge.net/). There you can find the instructions how to install it. To check if it's working, type at your terminal:

```
   >>>import lightblue
   >>>
```

If it's everything ok, you can now run the server.  Download the server.py from the downloads section and run by typing :

```
  $$ usr/bin/python server.py

```

It will appear the message at console 'server started'.  Now, run the client at your cellphone and connect it to the server. Open your slides at Keynote or Powerpoint and put it in SlideShow mode.  Press the upper button to go through slides or down button to go back the slides. In this release you can also use the stop watch to see the time passed at your presentation! An interesting tool for managing the time of your presentation!

Enjoy it!

This application was developed for my personal use, and i decided to share it here! Please forgive me for any bugs or misleading/poor interface!



