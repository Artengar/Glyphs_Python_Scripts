#MenuTitle: Calculate possible kerning combinations
# -*- coding: utf-8 -*-
__doc__="""
'Calculate possible kerning combinations'-script for the app Glyphs created by Artengar (Maarten Renckens)
This script just counts all possible kerning pairs present in the active master, in stead of the pairs presented in Glyphs itself (which only count the groups).
	"""

##Necessary info
import GlyphsApp;
fontMaster = Glyphs.font.selectedFontMaster.id;
ActiveFont = Glyphs.font;
totalKerningPairs = 0;
				
##Start the script if a font is opened
if len(Glyphs.fonts) <=0:
	Message("No open fonts", "There are no fonts open. The script can't do its work.", OKButton=None)
else:
	Glyphs.clearLog() #Cleans all junk from the log
	KerningLog = ActiveFont.kerning
	
	#Get information about the present kerning
	for heading in KerningLog:
		#And count the possible kerning pairs
		totalKerningPairsHere = 0
		#Start with calculating how many times the left item or group is present.
		for LeftItem in KerningLog.get(heading):
			#If a group, calculate the amount of times that the LeftItem is present.
			if LeftItem[0] == '@':
				#Count how many times this group is present.
				tempAmountOfPresencesLeft=0
				for glyph in ActiveFont.glyphs:
					if glyph.rightKerningGroup != None:
						if '@MMK_L_' + glyph.rightKerningGroup == LeftItem:
							tempAmountOfPresencesLeft+=1
			#If not a group, it is 1 time present
			else:
				tempAmountOfPresencesLeft=1
			print 'LeftItem =',LeftItem,' #times =',tempAmountOfPresencesLeft
			
			#Calculate  how many times the right item or group is present
			for RightItem in KerningLog.get(heading).get(LeftItem):
				tempAmountOfPresencesRight=0
				#If a group, calculate the amount of times that the RightItem is present.
				if RightItem[0] == '@':
					#Count how many times this group is present.
					tempAmountOfPresencesRight=0
					for glyph in ActiveFont.glyphs:
						if glyph.leftKerningGroup != None:
							if '@MMK_R_' + glyph.leftKerningGroup == RightItem:
								tempAmountOfPresencesRight+=1
				#If not a group, it is 1 time present
				else:
					tempAmountOfPresencesRight=1
				print '\\\RightItem =',RightItem,' #times =',tempAmountOfPresencesRight
				
				totalKerningPairsHere = tempAmountOfPresencesLeft*tempAmountOfPresencesRight
				totalKerningPairs+=totalKerningPairsHere
	print '------------------------------'
	print 'Amount of possible Kerning Pairs in the active master = %s'%totalKerningPairs
	
Glyphs.showMacroWindow()
