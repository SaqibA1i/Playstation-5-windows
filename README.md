# PlayStation 5 front End on windows
#### _Have the PS5 experience even when it is out of stock_

## Project Motivation
Computer building and gaming has been a hobby of mine for as long as I can remember. The technical aspect of bulding a computer, slotting in a rtx 2080 ti with a rx 5600 CPU is a thrill console gamers might never understand. 
> Suffice to say I am part of the PC master race and will always prefer the mighty PC over the mere mortal consoles.
> But there is one thing that console gamers have over PC gaming, and that is simplicity

Simplicity in how the PS5 launchs, hides and sorts the games, use of controller and just the overall simplicity in its user interface.

To make my point clear, this:
![PS5 UI](https://www.siliconera.com/wp-content/uploads/2020/10/ps5-ui-ps5-ux-playstation-5-ui-playstation-5-ux.jpg)

looks MUCH better, then this: 

![Windows Gaming](https://www.tenforums.com/attachments/gaming/177703d1519053837t-cant-delete-steam-game-shortcuts-untitled.png)

Moreover, using emulaters is a rather tedious process
 1. Search for the emulater
 2. Wait for the emulator app to open (which takes up computer resources)
 2. In some casses you may need to re add the games as configuration has been removed

So I set out on a developement journey to address the following concerns I had:

| Issue |
| ------ |
| Present a nice and clean UI 
| Ability to hide / sort / launch games within the interface 
| Have controller support, to navigate the UI
| Report on the controller battery health
| Ability to launch not only native window games, but have the same set of features for games running using emulaters

## ![](https://icons-for-free.com/iconfiles/png/128/super+tiny+icons+kodi-1324450744765209471.png)Kodi
Kodi is a free media player that can be installed on not only windows but IOS and even android. 
##### Present a nice and clean UI
Kodi uses a XML based language for its UI, so with alot of help from  [Kodi's documentation](https://kodi.wiki/view/Development) and pre existing skins such as Toyota12303 playstation 4 skin I was able to acheive the look of the PS5 interface.
##### Hide / Sort / Launch games/emulaters
The scripts are called from the interface for example:
```xml
<onclick>
    RunScript(special://skin/scripts/{SCRIPT_NAME}.py)
</onclick>
```
kodi provides following methods which can be called by a custom pyton script to provide functionality to the skin i.e.:
- xbmc.executebuiltin(...)
- xbmc.getInfoLabel(...)

- ```Launch and Sort Games``` Games are sorted based on many times they are launched.
    ```
    > scripts/gamelauncher.py
    ```
- ```Hide``` 
    ```
    > scripts/gamehider.py
    ```
- ```Remove Games``` The following script is called when a game is to be removed 
    ```
    > scripts/emuremover.py # To remove emulater games
    > scripts/gameremover.py # To remove native window games
    ```
##### Controller support
Kodi comes with controller support. 
##### Report on Controller Battery Health
In order to report the battery information a third party package had to be used. 
> HUGE PROBLEM: Kodi does not allow the support of third party python packages! Therefore I had to manually seperate the useful pieces of code within the [Xinput-Python](https://github.com/Zuzu-Typ/XInput-Python) package and was sucessfully able to report controller battery.
