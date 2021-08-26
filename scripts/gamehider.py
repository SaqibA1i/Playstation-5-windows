import os
import xbmc
import time
 
num = int(xbmc.getInfoLabel("Skin.String(running)"))
gamename = xbmc.getInfoLabel("Skin.String(snapname)")
gameType = xbmc.getInfoLabel("Skin.String(gameType)")

xbmc.executebuiltin("Skin.ToggleSetting({}{}visible)".format(gameType,num))
visible = xbmc.getInfoLabel("Skin.HasSetting({}{}visible)".format(gameType, num))
time.sleep(0.1) 
if visible:
    xbmc.executebuiltin('Skin.SetString(snapico,encrypted.png)')  
    xbmc.executebuiltin('Notification(Hidden, {} has been hidden from library,2000)'.format(gamename))
else:
    
    xbmc.executebuiltin('Skin.SetString(snapico,gamess.png)')
    xbmc.executebuiltin('Notification(Visible, {} has been added back to library,2000)'.format(gamename))

