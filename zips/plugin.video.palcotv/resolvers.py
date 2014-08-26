# -*- coding: utf-8 -*-
#------------------------------------------------------------
# PalcoTV - XBMC Add-on by Juarrox (juarrox@gmail.com)
# Version 0.2.9 (18.07.2014)
#------------------------------------------------------------
# License: GPL (http://www.gnu.org/licenses/gpl-3.0.html)
# Librerías Plugintools por Jesús (www.mimediacenter.info)


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

art = xbmc.translatePath(os.path.join('special://home/addons/plugin.video.palcotv/art', ''))
playlists = xbmc.translatePath(os.path.join('special://home/addons/plugin.video.palcotv/playlists', ''))
tmp = xbmc.translatePath(os.path.join('special://home/addons/plugin.video.palcotv/tmp', ''))
icon = art + 'icon.png'
fanart = 'fanart.jpg'




def allmyvideos(params):
    plugintools.log("PalcoTV.allmyvideos " + repr(params))

    url = params.get("url")
    url = url.split("/")
    url_fixed = 'http://www.allmyvideos.net/' +  'embed-' + url[3] +  '.html'
    plugintools.log("url_fixed= "+url_fixed)

    request_headers=[]
    request_headers.append(["User-Agent","Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_3) AppleWebKit/537.31 (KHTML, like Gecko) Chrome/26.0.1410.65 Safari/537.31"])
    body,response_headers = plugintools.read_body_and_headers(url_fixed, headers=request_headers)
    plugintools.log("data= "+body)

    r = re.findall('"file" : "(.+?)"', body)
    for entry in r:
        plugintools.log("vamos= "+entry)
        if entry.endswith("mp4?v2"):
            url = entry
            params["url"]=url
            plugintools.log("url= "+url)
            plugintools.play_resolved_url(url)
            xbmc.executebuiltin("Notification(%s,%s,%i,%s)" % ('PalcoTV', "Resolviendo enlace...", 3 , art+'icon.png'))


def streamcloud(params):
    plugintools.log("PalcoTV.streamcloud " + repr(params))

    url = params.get("url")

    request_headers=[]
    request_headers.append(["User-Agent","Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_3) AppleWebKit/537.31 (KHTML, like Gecko) Chrome/26.0.1410.65 Safari/537.31"])
    body,response_headers = plugintools.read_body_and_headers(url, headers=request_headers)
    plugintools.log("data= "+body)

    # Barra de progreso para la espera de 10 segundos
    progreso = xbmcgui.DialogProgress()
    progreso.create("PalcoTV", "Abriendo Streamcloud..." , url )

    i = 13000
    j = 0
    percent = 0
    while j <= 13000 :
        percent = ((j + ( 13000 / 10.0 )) / i)*100
        xbmc.sleep(i/10)  # 10% = 1,3 segundos
        j = j + ( 13000 / 10.0 )
        msg = "Espera unos segundos, por favor... "
        percent = int(round(percent))
        print percent
        progreso.update(percent, "" , msg, "")
        

    progreso.close()
    
    media_url = plugintools.find_single_match(body , 'file\: "([^"]+)"')
    
    if media_url == "":
        op = plugintools.find_single_match(body,'<input type="hidden" name="op" value="([^"]+)"')
        usr_login = ""
        id = plugintools.find_single_match(body,'<input type="hidden" name="id" value="([^"]+)"')
        fname = plugintools.find_single_match(body,'<input type="hidden" name="fname" value="([^"]+)"')
        referer = plugintools.find_single_match(body,'<input type="hidden" name="referer" value="([^"]*)"')
        hashstring = plugintools.find_single_match(body,'<input type="hidden" name="hash" value="([^"]*)"')
        imhuman = plugintools.find_single_match(body,'<input type="submit" name="imhuman".*?value="([^"]+)">').replace(" ","+")

        post = "op="+op+"&usr_login="+usr_login+"&id="+id+"&fname="+fname+"&referer="+referer+"&hash="+hashstring+"&imhuman="+imhuman
        request_headers.append(["Referer",url])
        body,response_headers = plugintools.read_body_and_headers(url, post=post, headers=request_headers)
        plugintools.log("data= "+body)
        

        # Extrae la URL
        media_url = plugintools.find_single_match( body , 'file\: "([^"]+)"' )
        plugintools.log("media_url= "+media_url)
        plugintools.play_resolved_url(media_url)

        if 'id="justanotice"' in body:
            plugintools.log("[streamcloud.py] data="+body)
            plugintools.log("[streamcloud.py] Ha saltado el detector de adblock")
            return -1

  

def playedto(params):
    plugintools.log("PalcoTV.playedto " + repr(params))

    url = params.get("url")
    url = url.split("/")
    url_fixed = "http://played.to/embed-" + url[3] +  "-640x360.html"
    plugintools.log("url_fixed= "+url_fixed)

    request_headers=[]
    request_headers.append(["User-Agent","Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_3) AppleWebKit/537.31 (KHTML, like Gecko) Chrome/26.0.1410.65 Safari/537.31"])
    body,response_headers = plugintools.read_body_and_headers(url_fixed, headers=request_headers)
    plugintools.log("data= "+body)

    r = re.findall('file(.+?)\n', body)
    
    for entry in r:
        
        entry = entry.replace('",', "")
        entry = entry.replace('"', "")
        entry = entry.replace(': ', "")
        entry = entry.strip()
        plugintools.log("vamos= "+entry)
        
        if entry.endswith("flv"):
            plugintools.play_resolved_url(entry)
            xbmc.executebuiltin("Notification(%s,%s,%i,%s)" % ('PalcoTV', "Resolviendo enlace...", 3 , art+'icon.png'))            
            params["url"]=entry
            plugintools.log("URL= "+entry)



def vidspot(params):
    plugintools.log("PalcoTV.vidspot " + repr(params))

    url = params.get("url")
    url = url.split("/")
    url_fixed = 'http://www.vidspot.net/' +  'embed-' + url[3] +  '.html'
    plugintools.log("url_fixed= "+url_fixed)

    request_headers=[]
    request_headers.append(["User-Agent","Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_3) AppleWebKit/537.31 (KHTML, like Gecko) Chrome/26.0.1410.65 Safari/537.31"])
    body,response_headers = plugintools.read_body_and_headers(url_fixed, headers=request_headers)
    plugintools.log("data= "+body)

    r = re.findall('"file" : "(.+?)"', body)
    for entry in r:
        plugintools.log("vamos= "+entry)
        if entry.endswith("mp4?v2"):
            url = entry
            params["url"]=url
            plugintools.log("url= "+url)
            plugintools.play_resolved_url(url)
            xbmc.executebuiltin("Notification(%s,%s,%i,%s)" % ('PalcoTV', "Resolviendo enlace...", 3 , art+'icon.png'))
    
        
