import os
import xbmc
import time
import struct

# change the current working directory
os.chdir(os.path.expanduser('~') + "/AppData/Roaming/Kodi/addons/skin.playstation5/")
# Description: given the path of the shortcut and returns the target field
def get_target(path):
    with open(path, 'rb') as stream:
        content = stream.read()
        # skip first 20 bytes (HeaderSize and LinkCLSID)
        # read the LinkFlags structure (4 bytes)
        lflags = struct.unpack('I', content[0x14:0x18])[0]
        position = 0x18
        # if the HasLinkTargetIDList bit is set then skip the stored IDList 
        # structure and header
        if (lflags & 0x01) == 1:
            position = struct.unpack('H', content[0x4C:0x4E])[0] + 0x4E
        last_pos = position
        position += 0x04
        # get how long the file information is (LinkInfoSize)
        length = struct.unpack('I', content[last_pos:position])[0]
        # skip 12 bytes (LinkInfoHeaderSize, LinkInfoFlags, and VolumeIDOffset)
        position += 0x0C
        # go to the LocalBasePath position
        lbpos = struct.unpack('I', content[position:position+0x04])[0]
        position = last_pos + lbpos
        # read the string at the given position of the determined length
        size= (length + last_pos) - position - 0x02
        temp = struct.unpack('c' * size, content[position:position+size])
        target = ''.join([chr(ord(a)) for a in temp])
    return target

def awaiter(prop, value):
    xbmc.executebuiltin('Skin.SetString({}, {})'.format(prop, value))
    time.sleep(0.1)

game = ""
gameType = xbmc.getInfoLabel("Skin.String(gameType)")
num = int(xbmc.getInfoLabel("Skin.String(running)"))
homePath = os.getcwd() + "/media/posters/launch/" + gameType + "/"

xbmc.executebuiltin('Notification(Launching,Hold the PS button to exit a game,1000)')
if gameType == "apps":
    game = xbmc.getInfoLabel("Skin.String(snapname)")
    while (game == ""):
        time.sleep(0.1) 
    game = homePath + game + ".lnk"
    os.startfile(game)
    xbmc.executebuiltin('ActivateWindow(9091)')
else:
    try: 
        #add one to the running
        prevrans = int(xbmc.getInfoLabel("Skin.String({}{}runs)".format(gameType, num))) + 1
        awaiter(gameType + str(num) + "runs", prevrans)
        game = xbmc.getInfoLabel("Skin.String(snapname)")
        while (game == ""):
            time.sleep(0.1) 
        game = homePath + game + ".lnk"
        # launches the emulater
        if gameType == "othergame":
            emulater_game_path = get_target(game)
            if not os.path.exists(emulater_game_path):
                xbmc.executebuiltin('Notification(Error Launching, Game shortcut does not exist, 2000)') 
            # wiiu comes before wii else dolphin is run for wiiu games
            if "wiiu" in game.lower():
                os.popen(os.getcwd() + "/Emulaters/cemu/Cemu.exe -f -g\"" + emulater_game_path + "\"")
            elif "wii" in game.lower():
                os.popen(os.getcwd() + "/Emulaters/dolphin/dolphin.exe -b -e \"" + emulater_game_path + "\"")
            elif "ps2" in game.lower():
                os.popen(os.getcwd() + "/Emulaters/pcsx2/pcsx2.exe --nogui \"" + emulater_game_path + "\"")
            elif "ps3" in game.lower():
                os.popen(os.getcwd() + "/Emulaters/rcps3/rpcs3.exe --no-gui \"" + emulater_game_path + "\"")
            else:
                xbmc.executebuiltin('Skin.SetString(snapico,DefaultIconError.png)')
                xbmc.executebuiltin('Notification(Error Launching, The emulator does not exist, 3000)')
        elif gameType == "game":
            os.startfile(game)
        xbmc.executebuiltin('ActivateWindow(9091)')
        #check prev if running is lesser -> Swap and keep looping
        i = num
        while i > 1: 
            # Check how many times the previous game has run
            lastgame = int(xbmc.getInfoLabel("Skin.String({}{}runs)".format(gameType, i - 1)))
            if lastgame < prevrans:
                # T = last
                tempgame = xbmc.getInfoLabel("Skin.String({}{}name)".format(gameType,i-1))
                tempruns = xbmc.getInfoLabel("Skin.String({}{}runs)".format(gameType,i-1))
                temphidden = xbmc.getInfoLabel("Skin.HasSetting({}{}visible)".format(gameType,i-1))
                tempprogress = xbmc.getInfoLabel("Skin.String({}{}progress)".format(gameType,i-1))
                # last = Current
                tempgame3 = xbmc.getInfoLabel("Skin.String({}{}name)".format(gameType,i))
                tempruns3 = xbmc.getInfoLabel("Skin.String({}{}runs)".format(gameType,i))
                temphidden3 = xbmc.getInfoLabel("Skin.HasSetting({}{}visible)".format(gameType,i))
                tempprogress3 = xbmc.getInfoLabel("Skin.String({}{}progress)".format(gameType,i))
                awaiter(gameType+str(i-1)+"name",tempgame3)
                awaiter(gameType+str(i-1)+"runs",tempruns3)
                xbmc.executebuiltin('Skin.SetBool({}{}visible)'.format(gameType, i-1))
                if not temphidden3:
                    xbmc.executebuiltin('Skin.ToggleSetting({}{}visible)'.format(gameType, i-1))
                awaiter(gameType+str(i-1)+"progress",tempprogress3)
                # Current = T
                awaiter(gameType+str(i)+"name",tempgame)
                awaiter(gameType+str(i)+"runs",tempruns)
                xbmc.executebuiltin('Skin.SetBool({}{}visible)'.format(gameType, i))
                if not temphidden:
                    xbmc.executebuiltin('Skin.ToggleSetting({}{}visible)'.format(gameType, i))
                awaiter(gameType+str(i)+"progress",tempprogress)
            else:
                break
            i = i - 1
    except:
        xbmc.executebuiltin('Skin.SetString(snapico,DefaultIconError.png)')
        if not os.path.exists(game):
            xbmc.executebuiltin('Notification(Error Launching, Game shortcut does not exist,2000)')
        else:
            xbmc.executebuiltin('Notification(Error Launching, Could not launch game,2000)')   

