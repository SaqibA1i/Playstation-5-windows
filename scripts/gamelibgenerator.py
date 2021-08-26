import os
import xbmc
import time

def update_lib(gameType):
    gamePath =  os.path.expanduser('~') + "/AppData/Roaming/Kodi/addons/skin.playstation5/media/posters/launch/"+gameType
    newGames = 0
    j=0
    for filename in os.listdir(gamePath):
        i = 1
        shouldContinue = True
        if filename.endswith(".lnk"):
            j = j + 1 
            gameName = filename.split(".")[0]
            while shouldContinue:
                tempGame = ""
                tempGame = xbmc.getInfoLabel("Skin.String({}{}name)".format(gameType, i))
                time.sleep(0.1)
                if tempGame == gameName:
                    shouldContinue = False
                elif tempGame == "":
                    xbmc.executebuiltin('Skin.SetString({}{}name,{})'.format(gameType, i,gameName))
                    xbmc.executebuiltin('Skin.SetString({}{}progress,0)'.format(gameType, i))
                    xbmc.executebuiltin('Skin.SetString({}{}runs,0)'.format(gameType, i))
                    xbmc.executebuiltin('Skin.SetBool({}{}visible)'.format(gameType, i))
                    newGames = newGames + 1
                    shouldContinue = False
                    xbmc.executebuiltin('Skin.SetString({}amount, {})'.format(gameType, i))
                i = i + 1 
    if newGames != 0:
        xbmc.executebuiltin('Notification({} library changed ,{} new games have been added,2000)'.format(gameType, newGames))
    xbmc.executebuiltin('Skin.SetString({}amount,{})'.format(gameType, j))

update_lib("game")
update_lib("othergame")