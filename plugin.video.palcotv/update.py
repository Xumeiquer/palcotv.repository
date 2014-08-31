# -*- coding: utf-8 -*-
#------------------------------------------------------------
# PalcoTV - XBMC Add-on by Juarrox (juarrox@gmail.com)
# Version 0.2.9 (18.07.2014)
#------------------------------------------------------------
# License: GPL (http://www.gnu.org/licenses/gpl-3.0.html)
# Gracias a la librería plugintools de Jesús (www.mimediacenter.info)


import os
import sys
import urllib
import urllib2
import re
import shutil
import zipfile

import xbmc
import xbmcgui
import xbmcaddon
import xbmcplugin

import plugintools


libdir = xbmc.translatePath(os.path.join('special://xbmc/system/players/dvdplayer/', ''))
art = xbmc.translatePath(os.path.join('special://home/addons/plugin.video.palcotv/art', ''))
playlists = xbmc.translatePath(os.path.join('special://home/addons/plugin.video.palcotv/playlists', ''))
tmp = xbmc.translatePath(os.path.join('special://home/addons/plugin.video.palcotv/tmp', ''))
icon = art + 'icon.png'
fanart = 'fanart.jpg'


def bajalib(params, platform):
    plugintools.log("palcoTV.bajalib "+platform)

    url = "https://dl.dropboxusercontent.com/u/8036850/librtmp/librtmp-" + platform + ".zip"
    dl_Dialog = xbmcgui.DialogProgress()

    dl_msg = dl_Dialog.create("palcoTV","Actualizando librerías... ")

    try:
        librtmp_zipfile = "librtmp-" + platform + ".zip"
        url = "https://dl.dropboxusercontent.com/u/8036850/librtmp/" + librtmp_zipfile
        plugintools.log("librtmp_zipfile= "+librtmp_zipfile)
        plugintools.log("url= "+url)
        # f = urllib2.urlopen(url)
        # file = open(playlists + "listas.zip", "wb")
        # file.write(f.read())
        # file.close()

    except IOError:
        return -1


    try:
        f = urllib2.urlopen(url)
        file = open(playlists + librtmp_zipfile, "wb")
        file.write(f.read())
        file.close()

    except IOError:
        return -1


    zfobj = zipfile.ZipFile(playlists + librtmp_zipfile)

    for name in zfobj.namelist():
        index = name.rfind('/')
        if index != -1:
            #entry contains path
            if not os.path.exists(playlists+name[:index+1]):
                try:
                    #create the directory structure
                    os.makedirs(os.path.join(playlists, name[:index+1]))
                except IOError:
                    return -1 #failure
                    
        if not name.endswith('/'):
            #entry contains a filename
            try:
                outfile = open(os.path.join(playlists, name), 'wb')
                outfile.write(zfobj.read(name))
                outfile.close()
            except IOError:
                pass #There was a problem. Continue...

    zfobj.close()

    try:
        os.remove(playlists + librtmp_zipfile)
        dl_Dialog.close()
        shutil.copyfile(playlists + 'librtmp.dll', libdir + 'librtmp.dll')
    except IOError:
        pass
    
    return 0 #succesful
    


      


def get_system_platform(params):
    plugintools.log("PalcoTV.get_system_platform " + repr(params))    
   
    if xbmc.getCondVisibility( "system.platform.ipad" ):
        platform = "linux"
        # Var / Stash /Applications/ XBMC.app / Frameworks / librtmp.0.dylib
        libdir = xbmc.translatePath(os.path.join('special://xbmc/Frameworks/', ''))
        plugintools.log("dir= "+libdir)
        filename = "librtmp.0.dylib"
        shutil.copyfile(libdir + 'librtmp.0.dylib', libdir + 'librtmp.0.dylib')

        # fh = open(libdir + filename, "wb")
        bajalib(params, platform)

    if xbmc.getCondVisibility( "system.platform.iphone" ):
        platform = "iphone"
        # Var / Stash /Applications/ XBMC.app / Frameworks / librtmp.0.dylib
        libdir = xbmc.translatePath(os.path.join('special://xbmc/Frameworks/', ''))
        plugintools.log("dir= "+libdir)
        filename = "librtmp.0.dylib"
        shutil.copyfile(libdir + 'librtmp.0.dylib', libdir + 'librtmp.0.dylib')

        # fh = open(libdir + filename, "wb")
        bajalib(params, platform)

    if xbmc.getCondVisibility( "system.platform.appletv" ):
        platform = "appletv"
        # Var / Stash /Applications/ XBMC.app / Frameworks / librtmp.0.dylib
        libdir = xbmc.translatePath(os.path.join('special://xbmc/Frameworks/', ''))
        plugintools.log("dir= "+libdir)
        filename = "librtmp.0.dylib"
        shutil.copyfile(libdir + 'librtmp.0.dylib', libdir + 'librtmp.0.dylib')

        # fh = open(libdir + filename, "wb")
        bajalib(params, platform)         

    elif xbmc.getCondVisibility( "system.platform.linux" ):
        platform = "linux"

    elif xbmc.getCondVisibility( "system.platform.android" ):
        platform = "android"
        # /data / data / org.xbmc.xbmc / lib / librtmp.so
        libdir = xbmc.translatePath(os.path.join('special://xbmc/data/data/org.xbmc.xbmc/lib/', ''))
        plugintools.log("dir= "+libdir)
        filename = "librtmp.so"
        shutil.copyfile(libdir + 'librtmp.so', libdir + 'librtmp.so')        
        
        
    elif xbmc.getCondVisibility( "system.platform.windows" ):
        platform = "windows"
        # Program Files (x86)/XBMC/system/players/dvdplayer/librtmp.dll
        # Archivos de Programa/XBMC/system/players/dvdplayer/librtmp.dll
        # Da igual porque special://xbmc/ apunta a la carpeta de instalación de XBMC
        libdir = xbmc.translatePath(os.path.join('special://xbmc/system/players/dvdplayer/', ''))
        plugintools.log("dir= "+libdir)
        filename = "librtmp_update.dll"
        shutil.copyfile(libdir + 'librtmp.dll', libdir + 'librtmp_bakup.dll')

        # fh = open(libdir + filename, "wb")
        bajalib(params, platform)
                
    elif xbmc.getCondVisibility( "system.platform.osx" ):
        platform = "osx"
        # Var / Stash /Applications/ XBMC.app / Frameworks / librtmp.0.dylib
        libdir = xbmc.translatePath(os.path.join('special://xbmc/Frameworks/', ''))
        plugintools.log("dir= "+libdir)
        filename = "librtmp.0.dylib"
        shutil.copyfile(libdir + 'librtmp.0.dylib', libdir + 'librtmp.0.dylib')

        # fh = open(libdir + filename, "wb")
        bajalib(params, platform)        
    else:
        platform = "unknow"
        
    plugintools.log("plataforma= "+platform)

    


