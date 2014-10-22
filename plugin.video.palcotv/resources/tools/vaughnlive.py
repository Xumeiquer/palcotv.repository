# -*- coding: utf-8 -*-
#------------------------------------------------------------
# PalcoTV Regex de vaughnlive
# Version 0.1 (17.10.2014)
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
import time

import xbmc
import xbmcgui
import xbmcaddon
import xbmcplugin

import plugintools



home = xbmc.translatePath(os.path.join('special://home/addons/plugin.video.palcotv/', ''))
tools = xbmc.translatePath(os.path.join('special://home/addons/plugin.video.palcotv/resources/tools', ''))
addons = xbmc.translatePath(os.path.join('special://home/addons/', ''))
resources = xbmc.translatePath(os.path.join('special://home/addons/plugin.video.palcotv/resources', ''))
art = xbmc.translatePath(os.path.join('special://home/addons/plugin.video.palcotv/art', ''))
tmp = xbmc.translatePath(os.path.join('special://home/addons/plugin.video.palcotv/tmp', ''))
playlists = xbmc.translatePath(os.path.join('special://home/addons/playlists', ''))

icon = art + 'icon.png'
fanart = 'fanart.jpg'


def resolve_vaughnlive(params):
    plugintools.log("[PalcoTV-0.3.0].resolve_vaughnlive " + repr(params) )

    vaughnlive_user = {"rtmp": "" , "swfurl": "http://vaughnlive.tv/800021294/swf/VaughnSoftPlayer.swf" , "pageurl": "http://www.vaughnlive.tv/", "token":'#ed%h0#w18623jsda6523l'}

    # Construimos diccionario 'vaughn_user'
    url = params.get("url")
    url = url.strip()
    url_extracted = url.split(" ")
    for entry in url_extracted:
        if entry.startswith("rtmp"):
            entry = entry.replace("rtmp=", "")         
            vaughnlive_user["rtmp"]=entry
        elif entry.startswith("playpath"):
            entry = entry.replace("playpath=", "")
            vaughnlive_user["playpath"]=entry            
        elif entry.startswith("swfUrl"):
            entry = entry.replace("swfUrl=", "")
            vaughnlive_user["swfurl"]=entry
        elif entry.startswith("pageUrl"):
            entry = entry.replace("pageUrl=", "")
            vaughnlive_user["pageurl"]=entry
        elif entry.startswith("token"):
            entry = entry.replace("token=", "")
            vaughnlive_user["token"]=entry           
            

    # Obtenemos gettime y servidor paralelo (edge server)...
    gettime = str(int(round(time.time() * 1000)))
    server_edge = 'http://mvn.vaughnsoft.net/video/edge/live_alx_nxtv' + gettime + '.33434'
    vaughnlive_user["rtmp"]=server_edge
    plugintools.log("server_edge= "+server_edge)
    
    request_headers=[]
    request_headers.append(["User-Agent","Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_3) AppleWebKit/537.31 (KHTML, like Gecko) Chrome/26.0.1410.65 Safari/537.31"])
    request_headers.append(["Referer","http://www.vaughnlive.tv/"])
    body,response_headers = plugintools.read_body_and_headers(server_edge, headers=request_headers)      
    body = body.strip()
    plugintools.log("body= "+body)
    matches = re.compile('(.*?);').findall(body)
    rtmp_server = matches[0]        
    vaughnlive_user["rtmp"] = 'rtmp://' + rtmp_server + '/live?'
    body = body.replace(rtmp_server, "")
    body = body.replace("0m0", "")
    body = body.replace(";", "")
    
    decrypted = decrypt_vaughnlive(body)
    plugintools.log("decrypted= "+decrypted)
    
    rtmp_fixed = vaughnlive_user.get("rtmp") + decrypted
    vaughnlive_user["rtmp"]=rtmp_fixed
    play_vaughnlive(vaughnlive_user, params)



def play_vaughnlive(vaughnlive_user, params):
    plugintools.log("[PalcoTV-0.3.0].vaughnlive User= " + repr(vaughnlive_user) )
    
    # Construimos la URL decodificada...
    url_decoded = vaughnlive_user.get("rtmp") + " playpath=" + vaughnlive_user.get("playpath") + " live=1 timeout=20"
    url = url_decoded.strip()
    plugintools.play_resolved_url(url_decoded)

    # Reproducimos URL decodificada...
    # plugintools.add_item(action="play", title=params.get("title"), url = url_decoded , folder = False, isPlayable = True)
    params["url"]=url_decoded
    # return url


def decrypt_vaughnlive(body):
	retVal=""
	body = body.split(":")
	print body

	for val in body:
            val = int(val)/84/5
            val=chr(val)
            retVal = retVal + val            
            
        plugintools.log("val= "+retVal)
        return retVal
        
        
        
