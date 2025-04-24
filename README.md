# DEPRECATED
#### At the time this was made, Valheim was not syncing maps between players and this was a way to get that done. Map syncing has since been added to the game.

---

# ValheimMapCombiner
Sync explored areas and map pins across up to ten character saves at a time. Make sure the game is closed before running. A backup of your original save files is made when you hit submit, they will be in the same location as the character files you loaded in.

![Valheim Map Combiner](https://github.com/SixPraxis/ValheimMapCombiner/blob/master/images/vmcCapture.png)

### Options:

__World ID__ - REQUIRED. Hit the Find Common IDs button to automatically find the worlds that are in common across all selected save files.

__Combine Pins__ - Will read pins across all save files and add them to the map

__Remove Overlapping Pins__ - Removes pins that are touching another pin in order reduce duplicate pins. When two pins are found to be overlapping, the pin from the earliest save file slot is prioritized.

Disabling Steam Cloud saves for Valheim is recommended. Use at your own risk. I am not responsible for any saves that are corrupted or lost while using this program.

### FAQ

__When I hit submit the program hangs:__

A: The program will take a few seconds to complete. There's over 4 million points on a Valheim map to check. If the program never seems to complete, please submit an issue.

__Saving doesn't seem to do anything/When I load the new save nothing has changed:__

A: Steam's cloud service may be restoring your save file to it's pre-modified version. Right click Valheim in steam, go to properties, and uncheck "Keep game saves in the Steam Cloud for Valheim"

__Does this work with save files that use mods?:__

A:  Most mods should work fine. If the mod adds any new fields or adds new features to the map/pins there's a chance this program will not be able to load the save file.
