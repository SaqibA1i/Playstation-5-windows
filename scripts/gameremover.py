import os
import xbmc
import time

def string_num(sztr):
    return int(sztr.replace(' ', ''))

rem_in_progress = xbmc.getInfoLabel("Skin.HasSetting(removing)")
time.sleep(0.1)
if not rem_in_progress:
    xbmc.executebuiltin("Skin.ToggleSetting(removing)")
    num = string_num(xbmc.getInfoLabel("Skin.String(running)"))
    gamename = xbmc.getInfoLabel("Skin.String(snapname)")
    gameico = xbmc.getInfoLabel("Skin.String(snapico)")
    i = num
    gameType = xbmc.getInfoLabel("Skin.String(gameType)")
    xbmc.executebuiltin('Notification(Removing,Please wait...,1000,C:/Cover/splash.png)')
    while i < 199:
        tempgame2 = xbmc.getInfoLabel("Skin.String({}{}name)".format(gameType,i))
        if tempgame2 == '':
            break
        # T = second
        tempgame2 = xbmc.getInfoLabel("Skin.String({}{}name)".format(gameType,i+1))
        tempruns2 = xbmc.getInfoLabel("Skin.String({}{}runs)".format(gameType,i+1))
        # first = T
        xbmc.executebuiltin('Skin.SetString({}{}name, {})'.format(gameType,i,tempgame2))
        xbmc.executebuiltin('Skin.SetString({}{}runs, {})'.format(gameType,i,tempruns2))
        while(tempruns2 != xbmc.getInfoLabel("Skin.String({}{}runs)".format(gameType,i)) or tempgame2 != xbmc.getInfoLabel("Skin.String({}{}name)".format(gameType,i))):
            time.sleep(0.05) 
        i = i + 1
    xbmc.executebuiltin('Skin.SetString({}amount, {})'.format(gameType, int(xbmc.getInfoLabel("Skin.String({}amount)".format(gameType))) - 1))
    xbmc.executebuiltin('Skin.SetString(running, 0)')
    xbmc.executebuiltin("Skin.ToggleSetting(removing)")
    xbmc.executebuiltin('Notification(Removed, {} has been removed from library,2000)'.format(gamename))

