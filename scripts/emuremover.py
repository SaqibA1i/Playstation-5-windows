import os
import xbmc
import time

curr = xbmc.getInfoLabel("Skin.String(running)")
def string_num(sztr):
    return int(sztr.replace(' ', ''))

num = int(curr.replace('a', ''))
i = num
xbmc.executebuiltin('Notification(Removing,Please wait...,1000,C:/Cover/splash.png)')
while i < 99:
    tempemu2 = xbmc.getInfoLabel("Skin.String(emu{}name)".format(i))
    if tempemu2 == '':
        break
    # T = second
    tempemu2 = xbmc.getInfoLabel("Skin.String(emu{}name)".format(i+1))
    tempruns2 = xbmc.getInfoLabel("Skin.String(emu{}runs)".format(i+1))
    # first = T
    xbmc.executebuiltin('Skin.SetString(emu{}name, {})'.format(i,tempemu2))
    xbmc.executebuiltin('Skin.SetString(emu{}runs, {})'.format(i,tempruns2))
    while(tempemu2 == xbmc.getInfoLabel("Skin.String(emu{}name)".format(num)) or tempruns2 == xbmc.getInfoLabel("Skin.String(emu{}runs)".format(num))):
        time.sleep(0.05) 
    i = i + 1


xbmc.executebuiltin('Skin.SetString(othergameamount, {})'.format(' ' + str(string_num(xbmc.getInfoLabel("Skin.String(othergameamount)")) - 1)))
xbmc.executebuiltin('Skin.SetString(running, 0)')
xbmc.executebuiltin('Notification(Removing,Game has been removed from library,3000,/script.hellow.world.png)')

