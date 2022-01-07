# Brawlhalla Matchup Info
- This program will retrieve the information and statistics of your opponent on Brawlhalla before the start of a 1v1 ranked game, and display it. This includes the current elo, elo max, main legend by level, main weapon, level, true level, most rated legend, time played and if your opponent is passive or aggressive.
- The tool needs a custom mod to work which you can find in the Setup section below.
- The tool does not work if the opponent's nickname contains symbols otherwise it works about 8 out of 10 times with the custom mod. 


## Install
- Download [BrawlhallaMatchupInfo.exe](https://github.com/alexisradice/BrawlhallaMatchupInfo/releases) from releases.
- Run `Brawlhalla Matchup Info.exe`

- Or Download [setupBrawlhallaMatchupInfo.exe](https://github.com/alexisradice/BrawlhallaMatchupInfo/releases) from releases.
- Install and Run `Brawlhalla Matchup Info.exe`
- Read the text Setup section below to use.

## Screenshots
![](https://cdn.discordapp.com/attachments/878657298036322354/928678754870493245/screenshot2.jpg)
![](https://cdn.discordapp.com/attachments/878657298036322354/928678716337442816/screenshot1.jpg)

## How To Use
### Setup
- You need to install this mod before using the app.
![](https://cdn.discordapp.com/attachments/878657298036322354/928678783815401543/screenshot3.jpg)
- To install, download [UI_1.swf](https://cdn.discordapp.com/attachments/878657298036322354/928441195816972319/UI_1.swf) and drag the file into the brawlhalla directory 
- Or Download [BrawlhallaMatchupInfosMod.bmod](https://cdn.discordapp.com/attachments/878657298036322354/928441223516127273/BrawlhallaMatchupInfoMod.bmod) and install with [Brawlhalla Mod Loader](https://github.com/Farbigoz/BHModLoader)


### Use
1) Open the BrawlhallaMatchupInfo program.
1) Select your Brawlhalla ID.
1) Press **Validate** button.
1) Play Brawlhalla in ranked mode.
1) When a game is found:
   - The opponent's information will be displayed on the app. 
   - You can switch between your information and the information of the opponent by pressing the button at the top right of the application.
   

## Technical
- All statistics used are retrieved with the [Brawlhalla API](https://dev.brawlhalla.com/) / [Brawlhalla Open API](https://github.com/barbarbar338/bh-open-api-webpage) and then processed in another API.
- The Passive/Neutral/Agressive status is calculated with the Average Game Length of the player.

- And the True Level is calculated with this formula with the level in X-axis and the xp in Y-axis which allows to find approximately the level of the player if it was not blocked at 100.
![](https://cdn.discordapp.com/attachments/878657298036322354/928678799636312114/screenshot4.jpg)
