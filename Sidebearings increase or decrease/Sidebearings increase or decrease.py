#MenuTitle: Increase or decrease selected sidebearings
# -*- coding: utf-8 -*-
__doc__="""
'This script will increase or decrease all sidebearings in the selected glyphs' - a script for the Glyphs app created by Artengar (Maarten Renckens)
	"""

# Open the Python environment with the menu Window > Macro Panel and copy-paste this code in it. Alternatively, this file can be downloaded and placed into the Glyphs scripts folder for later use.
# Then, adjust the values which should be added to the sidebearings over here. A positive value is an addition, a negative value is a subtraction:
addLeftSidebearing = 1
addRightSidebearing = 1

# Next, if the script is used in the Macro Panel, there is a button 'Run' on the lower right. Click on it and Glyphs will adjust the sidebearings.
# Of course, all white spaces need to be re-evaluated by the eye afterwards. Not all letters require the same increments!


# Next lines run the actual code:
# First, the console is emtied, to make place for new information:
Glyphs.clearLog()
# Then, the actions are executed:
for selectedLayer in Glyphs.font.selectedLayers:
	selectedLayer.parent.beginUndo()
	#selectedLayer.paths = 0
	selectedLayer.LSB += addLeftSidebearing
	selectedLayer.RSB += addRightSidebearing
	print("Space added to the letter:", selectedLayer.name)
	print("    Current Leftside:", selectedLayer.RSB, ", current right side:", selectedLayer.RSB)
	selectedLayer.parent.endUndo()

