import os
import xbmc
import time
def string_num(sztr):
    return int(sztr.replace(' ', ''))

num = string_num(xbmc.getInfoLabel("Skin.String(running)"))
gameType = xbmc.getInfoLabel("Skin.String(gameType)")
prog = xbmc.getInfoLabel("Skin.String(tempprogress)")
time.sleep(0.5)
try:
    if int(prog) >= 100:
        xbmc.executebuiltin('Skin.SetString({}{}progress, 100)'.format(gameType, num))
    else:
        xbmc.executebuiltin('Skin.SetString({}{}progress, {})'.format(gameType, num,prog))
    xbmc.executebuiltin('Notification(Progress,Progress is successfully set!,1000,C:/Cover/splash.png)')
except:
        xbmc.executebuiltin('Notification(Progress,Enter a valid number)')