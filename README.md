# Brawlhalla Matchup Info v1
- this program will retrieve the information and statistics of your opponent on Brawlhalla before the start of a ranked game and display on an application. This includes the current elo, elo max, main legend by level, main weapon, level, true level, most rated legend, time played and passive agressive. 
- The tool does not work if the opponent's nickname contains symbols otherwise it works about 8 out of 10 times with the custom mod and much less without. 


## Install
- Download [BrawlhallaMatchupInfo.exe](https://github.com/alexisradice/BrawlhallaMatchupInfo/releases) from releases.
- Install and run `Brawlhalla Matchup Info.exe`
- Use the [Video Instructions](https://youtube.com/) or read the text Setup section below to use.

## Screenshots
![](https://brawlhalla-matchup-info-api.vercel.app/api/brawl/screenshot2)
![](https://brawlhalla-matchup-info-api.vercel.app/api/brawl/screenshot1)

## How To Use
### Setup
- It is highly recommended to install this custom mod for better detection.
![](https://brawlhalla-matchup-info-api.vercel.app/api/brawl/screenshot3)
- To install download [UI_1.swf](https://brawlhalla-matchup-info-api.vercel.app/api/brawl/UI_1.swf) and drag the file into the brawlhalla directory 
- Or Download [BrawlhallaMatchupInfosMod.bmod](https://brawlhalla-matchup-info-api.vercel.app/api/brawl/BrawlhallaMatchupInfosMod.bmod) and install with [Brawlhalla Mod Loader](https://github.com/Farbigoz/BHModLoader)


### Use
1) Open the BrawlhallaMatchupInfo program.
1) Select your Brawlhalla ID.
1) Press **Validate** button.
1) Play Brawlhalla in ranked mode.
1) When a game is found:
   - The opponent's information will be displayed on the app. 
   - You can switch between your information and the information of the opponent by pressing the button at the top left of the application.
   

## Technical
- All statistics used are retrieved with the [Brawlhalla API](https://dev.brawlhalla.com/) / [Brawlhalla Open API](https://github.com/barbarbar338/bh-open-api-webpage) and then processed in another API.
- The Passive/Neutral/Agressive status is calculated with the Average Game Length of the player.

- And the True Level is calculated with this formula with the level in X-axis and the xp in Y-axis which allows to find approximately the level of the player if it was not blocked at 100.
![](https://brawlhalla-matchup-info-api.vercel.app/api/brawl/screenshot4)
