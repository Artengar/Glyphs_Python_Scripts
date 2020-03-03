#MenuTitle: PatternCreator
# -*- coding: utf-8 -*-
__doc__="""
PatternCreator fills glyphs with a pattern.
Version 1.5, dating 17 November 2015.
Consult the Glyphs manual for information about the installation of scripts. Contact Artengar on GitHub for changes in the code.
"""
#Multiple options to add: "Replace glyph with pattern" #TO INSERT IN THE DESCRIPTION: or the letter shape 
try:
	import GlyphsApp
	import vanilla
	import math
except Exception:
	Message("Missing Modules", "There are python modulles missing. Go to the menu Glyphs -> Preferences -> latest tab and click on Modules -> Install Modules", OKButton=None)
Value_bottom = 0
Value_top = 500
Value_width = 20
Value_spacing = 20
Value_angle = 0
Horizontal_shift = 0
check = False
Option_list = ["Place a new pattern", "Replace glyph with pattern"] 
Shape_options = ["Stripes", "Horizontal lines", "Planes", "Rhombus", "Dots"]



#Create one vertical stroke.
def Vert_stroke(item, Value_bottom, Value_top, FirstPoint_x, SecondPoint_x, ThirdPoint_x, FourthPoint_x, Value_width, Value_angle):
	try:
		FirstPoint_y = Value_top
		SecondPoint_y = Value_bottom
		ThirdPoint_y = Value_bottom
		FourthPoint_y = Value_top
		
		Stroke = GSPath()
		#If the angle is zero, the strokes are easy
		if Value_angle == 0:
			NodeData = [
				[FirstPoint_x, FirstPoint_y],
				[SecondPoint_x, SecondPoint_y],
				[ThirdPoint_x, ThirdPoint_y],
				[FourthPoint_x, FourthPoint_y]
			]
		#The first and the last stroke are triangles, there are two possible pentagons & the last triangle is different...
		#correct the nodes outside the glyph width for a positive angle
		if Value_angle >= 0:
			#What if the nodes are left of the glyph width?
			if SecondPoint_x < 0:
				SecondPoint_y = Value_top - abs(FirstPoint_x) / math.tan(math.radians(Value_angle))#At this moment, the FourthPoint is not yet cut off.
				SecondPoint_x = 0
			if ThirdPoint_x < 0:
				ThirdPoint_y = Value_top - abs(FourthPoint_x) / math.tan(math.radians(Value_angle))
				ThirdPoint_x = 0
			#What if the nodes are right of the glyph width?
			if ThirdPoint_x > item.width:
				ThirdPoint_x = item.width
			if FourthPoint_x > item.width:
				FourthPoint_y = Value_top - ((abs(FourthPoint_x) - item.width) / math.tan(math.radians(abs(Value_angle))))
				FourthPoint_x = item.width
			if FirstPoint_x > item.width:
				FirstPoint_y = Value_top - ((abs(FirstPoint_x) - item.width) / math.tan(math.radians(abs(Value_angle))))
				FirstPoint_x = item.width
			#Determine the path
			#If the first stroke goes from top to bottom (angle -1), the next code DOES NOT work. First item is a short correction
			if FirstPoint_x == SecondPoint_x and FirstPoint_y == SecondPoint_y and FourthPoint_x == Value_width:
				SecondPoint_x = 0
				SecondPoint_y = Value_bottom
				NodeData = [
					[FirstPoint_x, FirstPoint_y],
					[SecondPoint_x, SecondPoint_y],
					[ThirdPoint_x, ThirdPoint_y],
					[FourthPoint_x, FourthPoint_y]
				]
			#Correct the first triangle: three nodes
			elif FirstPoint_x == SecondPoint_x and FirstPoint_y == SecondPoint_y:
				NodeData = [
					[FirstPoint_x, FirstPoint_y],
					[ThirdPoint_x, ThirdPoint_y],
					[FourthPoint_x, FourthPoint_y]
				]
			#There can be one pentagon 
			elif SecondPoint_x == 0 and ThirdPoint_x > 0:
				NodeData = [
					[FirstPoint_x, FirstPoint_y],
					[SecondPoint_x, SecondPoint_y],
					[0, Value_bottom],
					[ThirdPoint_x, ThirdPoint_y],
					[FourthPoint_x, FourthPoint_y]
				]
			#Correct the latest triangle: three nodes
			elif FourthPoint_y < Value_bottom:
				NodeData = [
					[FirstPoint_x, FirstPoint_y],
					[SecondPoint_x, SecondPoint_y],
					[ThirdPoint_x, ThirdPoint_y]
				]
			#And just the normal strokes	
			else:
				NodeData = [
					[FirstPoint_x, FirstPoint_y],
					[SecondPoint_x, SecondPoint_y],
					[ThirdPoint_x, ThirdPoint_y],
					[FourthPoint_x, FourthPoint_y]
				]
		#correct the nodes outside the glyph width for a negative angle
		#TAKE CARE: THE SECONDPOINT IS AT X-VALUE ZERO, NOT THE FIRSTPOINT!
		elif Value_angle < 0:
			#What if the nodes are left of the glyph width?
			if FirstPoint_x < 0:
				FirstPoint_y = Value_top - abs(FirstPoint_x) / math.tan(math.radians(abs(Value_angle)))
				FirstPoint_x = 0
			if FourthPoint_x < 0:
				FourthPoint_y = Value_top - abs(FourthPoint_x) / math.tan(math.radians(abs(Value_angle)))
				FourthPoint_x = 0
			#What if the nodes are right of the glyph width?
			if SecondPoint_x > item.width:
				SecondPoint_y = Value_bottom + (abs(SecondPoint_x) - item.width) / math.tan(math.radians(abs(Value_angle)))
				SecondPoint_x = item.width
			if ThirdPoint_x > item.width:
				ThirdPoint_y = Value_bottom + (abs(ThirdPoint_x) - item.width) / math.tan(math.radians(abs(Value_angle)))
				ThirdPoint_x = item.width
			if FourthPoint_x > item.width:
				FourthPoint_x = item.width
			#Determine the path
			#If the first stroke goes from top to bottom (ex. angle -1), the next code DOES NOT work. First item is a short correction
			if FirstPoint_x == SecondPoint_x and FirstPoint_y == SecondPoint_y and 0 < FourthPoint_x < Value_width:
				FirstPoint_x = 0
				FirstPoint_y = Value_top
				NodeData = [
					[FirstPoint_x, FirstPoint_y],
					[SecondPoint_x, SecondPoint_y],
					[ThirdPoint_x, ThirdPoint_y],
					[FourthPoint_x, FourthPoint_y]
				]
			#Correct the first triangle: three nodes
			elif FirstPoint_x == SecondPoint_x and FirstPoint_y == SecondPoint_y:
				NodeData = [
					[SecondPoint_x, SecondPoint_y],
					[ThirdPoint_x, ThirdPoint_y],
					[FourthPoint_x, FourthPoint_y]
				]
			#There can be one pentagon if the first 'if' was not activated
			elif FirstPoint_x == 0 and FourthPoint_x > 0:
				NodeData = [
					[FirstPoint_x, FirstPoint_y],
					[SecondPoint_x, SecondPoint_y],
					[ThirdPoint_x, ThirdPoint_y],
					[FourthPoint_x, FourthPoint_y],
					[0, Value_top]
				]
			#Correct the latest triangle: three nodes
			elif ThirdPoint_y > Value_top:
				NodeData = [
					[FirstPoint_x, FirstPoint_y],
					[SecondPoint_x, SecondPoint_y],
					[FourthPoint_x, FourthPoint_y]
				]
			#And just the normal strokes	
			else:
				NodeData = [
					[FirstPoint_x, FirstPoint_y],
					[SecondPoint_x, SecondPoint_y],
					[ThirdPoint_x, ThirdPoint_y],
					[FourthPoint_x, FourthPoint_y]
				]
		
		for Data in NodeData:
			NodeToAdd = GSNode()
			NodeToAdd.type = GSLINE
			NodeToAdd.position = (Data[0], Data[1])
			Stroke.nodes.append( NodeToAdd )
		Stroke.closed = True
		return Stroke
	except Exception, ex:
		print "It was not possible to draw the pattern: %s" %ex



#Create one horizontal stroke.
def Hor_stroke(item, FirstPoint_y, SecondPoint_y, ThirdPoint_y, FourthPoint_y):
	try:
		FirstPoint_x = 0
		SecondPoint_x = 0
		ThirdPoint_x = item.width
		FourthPoint_x = item.width
		
		Stroke = GSPath()
		#Just normal strokes here
		NodeData = [
			[FirstPoint_x, FirstPoint_y],
			[SecondPoint_x, SecondPoint_y],
			[ThirdPoint_x, ThirdPoint_y],
			[FourthPoint_x, FourthPoint_y]
		]
		for Data in NodeData:
			NodeToAdd = GSNode()
			NodeToAdd.type = GSLINE
			NodeToAdd.position = (Data[0], Data[1])
			Stroke.nodes.append( NodeToAdd )
		Stroke.closed = True
		return Stroke		
	except Exception, ex:
		print "It was not possible to draw the stroke: %s" %ex



#Report if the width of some glyphs should be adjusted
def Check_adjust_width(pattern_width, pattern_spacing):
	adjustments_necessairy = False
	for item in Glyphs.font.selectedLayers:
		if item.width % (pattern_width + pattern_spacing) != 0.0:
			item.parent.beginUndo()
			item.parent.color = 0
			item.parent.endUndo()
			adjustments_necessairy = True
	#Show a message when the width of some glyphs must be adjusted:
	if adjustments_necessairy == True:
		Message("Not fitting", "The pattern does not fit into all the glyphs. Those glyphs will take on the colour Red and the glyph width will be enlarged so the pattern can fit in and continue smoothly onto the next glyph(s)\n\nOne condition of this script is that every glyph has at least one complete stroke. If you have a realy strong argumentation why it should not be, contact Artengar on Github for the corresponding changes.", OKButton=None)



#Adjust the width of the glyphs if necessairy
def adjust_width(item, amount):
	if item.width % amount != 0.0:
		plus = 0
		while plus < item.width:
			plus += amount
		item.parent.beginUndo()
		item.width = plus
		item.parent.endUndo()



def get_pattern_height(Value_bottom, Value_top):
	if Value_bottom >= 0 and Value_top >= 0:
		delta = abs(Value_top - Value_bottom)
		return delta
	if Value_bottom <= 0 and Value_top >= 0:
		delta = abs(Value_top + abs(Value_bottom))
		return delta
	if Value_bottom <= 0 and Value_top <= 0: #Make sure that the bottom value is bigger than the top value!
		delta = abs(Value_bottom) - abs(Value_top)
		return delta



def Draw_vertical_strokes(Value_bottom, Value_top, Value_width, Value_spacing, Value_angle):
	#Check if the pattern fits into every glyph width
	Check_adjust_width(Value_width, Value_spacing)
	#Start selecting a glyph
	for item in Glyphs.font.selectedLayers:
		amount = (Value_width + Value_spacing)
		#Adjust the width of the glyphs
		adjust_width(item, amount)
		
		#Determine the horizontal shift (the amount of units that some of the nodes moves due to the angle)
		pattern_height = get_pattern_height(Value_bottom, Value_top)
		#Horizontal shift = negative when the entered angle is negative.
		Horizontal_shift = math.tan(math.radians(Value_angle)) * pattern_height		
		# Additional information for intersections:
		# https://forum.glyphsapp.com/t/how-do-i-intersect-two-shapes/237/2
		
		#Determine all raw x-coördinates of the pattern, starting from the top side of the pattern, counterclockwise
		jump = 0
		while jump < (item.width + abs(Horizontal_shift)):
			if Value_angle >= 0:
				FirstPoint_x = 0 + jump
				SecondPoint_x = 0 + jump - Horizontal_shift #SecondPoind is left from FirstPoint if angle is positive
				ThirdPoint_x = Value_width + jump - Horizontal_shift #SecondPoind is left from FirstPoint if angle is positive
				FourthPoint_x = Value_width + jump
			#If the angle is negative, raw x-coördinates starts earlier
			if Value_angle <= 0:
				FirstPoint_x = 0 + jump + Horizontal_shift #Make horizontal shift positive because the value is negative here
				SecondPoint_x = 0 + jump
				ThirdPoint_x = Value_width + jump
				FourthPoint_x = Value_width + jump + Horizontal_shift
			Pattern_Part = Vert_stroke(item, Value_bottom, Value_top, FirstPoint_x, SecondPoint_x, ThirdPoint_x, FourthPoint_x, Value_width, Value_angle)
			item.parent.beginUndo()
			item.paths.append(Pattern_Part)
			item.parent.endUndo()
			jump += amount



def Draw_horizontal_strokes(Value_bottom, Value_top, Value_height, Value_amount_of_strokes):
	#Start selecting a glyph
	for item in Glyphs.font.selectedLayers:
		try:
			if Value_amount_of_strokes > 1:
				pattern_height = get_pattern_height(Value_bottom, Value_top)
				#determine the amount of space between the strokes
				Value_space_between = ((Value_top - Value_bottom) - (Value_height * Value_amount_of_strokes)) / (Value_amount_of_strokes - 1)
				amount = (Value_height + Value_space_between)
				#Determine the NodeData
				jump = 0
				while jump < pattern_height:
					#Determine all raw x-coördinates of the pattern, starting from the left top side of the pattern, clockwise
					FirstPoint_y = Value_top - Value_height - jump
					SecondPoint_y = Value_top - jump
					ThirdPoint_y = Value_top - jump
					FourthPoint_y = Value_top - Value_height - jump
					Pattern_Part = Hor_stroke(item, FirstPoint_y, SecondPoint_y, ThirdPoint_y, FourthPoint_y)
					item.parent.beginUndo()
					item.paths.append(Pattern_Part)
					item.parent.endUndo()
					jump += amount
			elif Value_amount_of_strokes <= 1:
				#Determine all raw x-coördinates of the pattern, starting from the left top side of the pattern, clockwise
				FirstPoint_y = Value_height
				SecondPoint_y = Value_height
				ThirdPoint_y = 0
				FourthPoint_y = 0
				Pattern_Part = Hor_stroke(item, FirstPoint_y, SecondPoint_y, ThirdPoint_y, FourthPoint_y)
				item.parent.beginUndo()
				item.paths.append(Pattern_Part)
				item.parent.endUndo()
		except Exception, ex:
			print "The entered values are not valid. Are they all numbers? %s"%ex



#Draw the patterns with different pieces:
def Draw_pieces(shape, Value_bottom, Value_top, Value_shape_height, Value_shape_width, Value_vert_spacing, Value_hor_spacing):
	#Check if the pattern fits into every glyph width
	Check_adjust_width(Value_shape_width, Value_hor_spacing)
	#Start selecting a glyph
	for item in Glyphs.font.selectedLayers:
		pattern_height = get_pattern_height(Value_bottom, Value_top)
		amount_horizontal = (Value_shape_width + Value_hor_spacing)
		amount_vertical = (Value_shape_height + Value_vert_spacing)
		#Adjust the width of the glyphs
		adjust_width(item, amount_horizontal)
		#Determine the NodeData
		#First make a distinction between the different lines
		jump = 0
		while jump < pattern_height:
			#Then make a distinction between different shapes on a line.
			number = 0
			while number < item.width:
				#Determine all raw x-coördinates of the pattern, starting from the left top side of the pattern, clockwise
				if shape == "Planes":
					FirstPoint_x = 0 + number
					FirstPoint_y = Value_top - jump
					SecondPoint_x = 0 + number
					SecondPoint_y = Value_top - Value_shape_height - jump
					ThirdPoint_x = Value_shape_width + number
					ThirdPoint_y = Value_top - Value_shape_height - jump
					FourthPoint_x = Value_shape_width + number
					FourthPoint_y = Value_top - jump
				elif shape == "Rhombus":
					FirstPoint_x = (Value_shape_width/2) + number
					FirstPoint_y = Value_top - jump
					SecondPoint_x = 0 + number
					SecondPoint_y = Value_top - (Value_shape_height/2) - jump
					ThirdPoint_x = (Value_shape_width/2) + number
					ThirdPoint_y = Value_top - Value_shape_height - jump
					FourthPoint_x = Value_shape_width + number
					FourthPoint_y = Value_top - (Value_shape_height/2) - jump
				elif shape == "Dots":
					FirstNode_x = (Value_shape_width/2) - ((Value_shape_width/2)*0.55) + number
					FirstNode_y = Value_top - jump
					SecondNode_x = 0 + number
					SecondNode_y = Value_top - (Value_shape_height/2) + ((Value_shape_height/2)*0.55) - jump
					FirstPoint_x = 0 + number
					FirstPoint_y = Value_top - (Value_shape_height/2) - jump
					ThirdNode_x = 0 + number
					ThirdNode_y = Value_top - (Value_shape_width/2) - ((Value_shape_width/2)*0.55) - jump
					FourthNode_x = (Value_shape_width/2) - ((Value_shape_width/2)*0.55) + number
					FourthNode_y = Value_top - Value_shape_height - jump
					SecondPoint_x = (Value_shape_width/2) + number
					SecondPoint_y = Value_top - Value_shape_height - jump
					FifthNode_x = (Value_shape_width/2) + ((Value_shape_width/2)*0.55) + number
					FifthNode_y = Value_top - Value_shape_height - jump
					SixthNode_x = (Value_shape_width/2) + (Value_shape_width/2) + number
					SixthNode_y = Value_top - (Value_shape_width/2) - ((Value_shape_width/2)*0.55) - jump
					ThirdPoint_x = Value_shape_width + number
					ThirdPoint_y = Value_top - (Value_shape_height/2) - jump
					SeventhNode_x = (Value_shape_width/2) + (Value_shape_width/2) + number
					SeventhNode_y = Value_top - (Value_shape_width/2) + ((Value_shape_width/2)*0.55) - jump
					EightNode_x = (Value_shape_width/2) + ((Value_shape_width/2)*0.55) + number
					EightNode_y = Value_top - jump
					FourthPoint_x = (Value_shape_width/2) + number
					FourthPoint_y = Value_top - jump
				#Draw the shapes
				if shape == "Planes" or shape == "Rhombus":
					try:
						Piece = GSPath()
						NodeData = [
							[FirstPoint_x, FirstPoint_y],
							[SecondPoint_x, SecondPoint_y],
							[ThirdPoint_x, ThirdPoint_y],
							[FourthPoint_x, FourthPoint_y]
						]
			
						for Data in NodeData:
							NodeToAdd = GSNode()
							NodeToAdd.type = GSLINE
							NodeToAdd.position = (Data[0], Data[1])
							Piece.nodes.append( NodeToAdd )
						Piece.closed = True
					except Exception, ex:
						print "It was not possible to draw the pattern: %s" %ex
				if shape == "Dots":
					try:
						Piece = GSPath()
						aHandle = GSOFFCURVE
						aNode = GSCURVE
						NodeData = [
							[FirstNode_x, FirstNode_y, aHandle],
							[SecondNode_x, SecondNode_y, aHandle],
							[FirstPoint_x, FirstPoint_y, aNode],
							[ThirdNode_x, ThirdNode_y, aHandle],
							[FourthNode_x, FourthNode_y, aHandle],
							[SecondPoint_x, SecondPoint_y, aNode],
							[FifthNode_x, FifthNode_y, aHandle],
							[SixthNode_x, SixthNode_y, aHandle],
							[ThirdPoint_x, ThirdPoint_y, aNode],
							[SeventhNode_x, SeventhNode_y, aHandle],
							[EightNode_x, EightNode_y, aHandle],
							[FourthPoint_x, FourthPoint_y, aNode]
						]
			
						for Data in NodeData:
							NodeToAdd = GSNode()
							NodeToAdd.type = Data[2]
							if Data[2] == GSCURVE:
								NodeToAdd.connection = GSSMOOTH
							NodeToAdd.position = (Data[0], Data[1])
							Piece.nodes.append( NodeToAdd )
						Piece.closed = True
					except Exception, ex:
						print "It was not possible to draw the pattern: %s" %ex
				
				item.parent.beginUndo()
				item.paths.append(Piece)
				item.parent.endUndo()
				number += amount_horizontal
			jump += amount_vertical
			#Don't cross the bottom line
			if (Value_top - amount_vertical) < Value_bottom:
				break




#The program itself:
class run_program(object):
	def __init__(self):
		#Grid
		Column1 = 20
		Column2 = Column1 + 115
		Row01 = 15
		Row02 = Row01 + 45
		Row03 = Row02 + 0 #25
		Row04 = Row03 + 45 #130
		Row05 = Row04 + 25
		Row06 = Row05 + 25
		Row07 = Row06 + 25
		Row08 = Row07 + 25 #230
		Row09 = Row08 + 25
		Row10 = Row09 + 25
		Row11 = Row10 + 25 #320
		Row12 = Row11 + 25
		windowHeight = Row12 + 85 #Currently 395
		windowWidth = Column2 + 135 #270
		#Create a window
		self.window = vanilla.FloatingWindow(
			(windowWidth, windowHeight),
			"PatternCreator", #Title Bar Title
			autosaveName = "com.Artengar.PatternCreator.mainwindow"
			)
		#General options
		self.window.text_1 = vanilla.TextBox( (Column1, Row01, -20, 45), "PatternCreator fills in the glyph space of the selected glyphs.", sizeStyle='small')
		self.window.Change_options = vanilla.PopUpButton( (Column1, Row02, -15, 17), Option_list, sizeStyle='small', callback=self.Change_Options)
		self.window.Change_options.show(False)
		self.window.Change_shape = vanilla.PopUpButton( (Column1, Row03, -15, 17), Shape_options, sizeStyle='small', callback=self.Change_Shape)
		#General options for everything
		self.window.text_top = vanilla.TextBox( (Column1, Row04, -20, 45), "Top:", sizeStyle='small')
		self.window.top = vanilla.EditText( (Column2, Row04, 100, 19), 500, callback=self.SavePreferences, sizeStyle = 'small')
		self.window.text_bottom = vanilla.TextBox( (Column1, Row05, -20, 45), "Bottom:", sizeStyle='small')
		self.window.bottom = vanilla.EditText( (Column2, Row05, 100, 19), 0, callback=self.SavePreferences, sizeStyle = 'small')
		#The first items to create lines
		self.window.text_width = vanilla.TextBox( (Column1, Row06, -20, 45), "Width:", sizeStyle='small')
		self.window.width = vanilla.EditText( (Column2, Row06, 100, 19), 20, callback=self.SavePreferences, sizeStyle = 'small')
		self.window.text_hor_spacing = vanilla.TextBox( (Column1, Row07, -20, 45), "Horizontal spacing:", sizeStyle='small')
		self.window.hor_spacing = vanilla.EditText( (Column2, Row07, 100, 19), 20, callback=self.SavePreferences, sizeStyle = 'small')
		self.window.text_adjustments = vanilla.TextBox( (Column1, Row08, -20, 45), "The width of the glyph will be adjusted so the pattern fits in the total width.", sizeStyle='small')
		self.window.text_angle = vanilla.TextBox( (Column1, Row09+10, -20, 45), "Slanted Angle:", sizeStyle='small')
		self.window.angle = vanilla.EditText( (Column2, Row09+10, 100, 19), 0, callback=self.SavePreferences, sizeStyle = 'small')
		self.window.text_angle_warning = vanilla.TextBox( (Column1, Row10+10, -20, 60), "Not all angles are usable. Keep in mind that the pattern of this glyph should continue on the pattern of the next glyph. The script will take this into account.", sizeStyle='small')
		#The items for the second choice
		self.window.text_height = vanilla.TextBox( (Column1, Row06, -20, 45), "Stroke height:", sizeStyle='small')
		self.window.height = vanilla.EditText( (Column2, Row06, 100, 19), 20, callback=self.SavePreferences, sizeStyle = 'small')
		self.window.text_amount_of_strokes = vanilla.TextBox( (Column1, Row07, -20, 45), "Amount of strokes:", sizeStyle='small')
		self.window.amount_of_strokes = vanilla.EditText( (Column2, Row07, 100, 19), 20, callback=self.SavePreferences, sizeStyle = 'small')
		self.window.text_warning1 = vanilla.TextBox( (Column1, Row08, -20, 45), "Make sure that your amount of stripes fits in the distance between the bottom and the top!", sizeStyle='small')
		self.window.text_height.show(False)
		self.window.height.show(False)
		self.window.text_amount_of_strokes.show(False)
		self.window.amount_of_strokes.show(False)
		self.window.text_warning1.show(False)
		#The items for the third choice
		self.window.text_shape_height = vanilla.TextBox( (Column1, Row06, -20, 45), "Shape height:", sizeStyle='small')
		self.window.shape_height = vanilla.EditText( (Column2, Row06, 100, 19), 20, callback=self.SavePreferences, sizeStyle = 'small')
		self.window.text_shape_width = vanilla.TextBox( (Column1, Row07, -20, 45), "Shape Width:", sizeStyle='small')
		self.window.shape_width = vanilla.EditText( (Column2, Row07, 100, 19), 20, callback=self.SavePreferences, sizeStyle = 'small')
		self.window.text_vert_shape_spacing = vanilla.TextBox( (Column1, Row08, -20, 45), "Vertical spacing:", sizeStyle='small')
		self.window.vert_shape_spacing = vanilla.EditText( (Column2, Row08, 100, 19), 20, callback=self.SavePreferences, sizeStyle = 'small')
		self.window.text_hor_shape_spacing = vanilla.TextBox( (Column1, Row09, -20, 45), "Horizontal spacing:", sizeStyle='small')
		self.window.hor_shape_spacing = vanilla.EditText( (Column2, Row09, 100, 19), 20, callback=self.SavePreferences, sizeStyle = 'small')
		self.window.text_warning2 = vanilla.TextBox( (Column1, Row10, -20, 45), "Little shapes are always nice, but how more you have, the slower your font will become... Proceed with caution.", sizeStyle='small')
		self.window.text_shape_height.show(False)
		self.window.shape_height.show(False)
		self.window.text_shape_width.show(False)
		self.window.shape_width.show(False)
		self.window.text_vert_shape_spacing.show(False)
		self.window.vert_shape_spacing.show(False)
		self.window.text_hor_shape_spacing.show(False)
		self.window.hor_shape_spacing.show(False)
		self.window.text_warning2.show(False)
		#The items for the third choice
		self.window.text_dot_diameter = vanilla.TextBox( (Column1, Row06, -20, 45), "Dot diameter:", sizeStyle='small')
		self.window.dot_diameter = vanilla.EditText( (Column2, Row06, 100, 19), 20, callback=self.SavePreferences, sizeStyle = 'small')
		self.window.text_dot_diameter.show(False)
		self.window.dot_diameter.show(False)
		#The button to start
		self.window.Execute = vanilla.Button( (Column1, windowHeight-35, -Column1, 15), "Draw the pattern", callback=self.Draw, sizeStyle='small')
		self.LoadPreferences()
		self.window.open()
		self.window.makeKey()
		
	#Save the prefs
	def SavePreferences(self, sender):
		try:
			check = False
			Glyphs.defaults["com.Artengar.PatternCreator.top"] = self.window.top.get()
			Glyphs.defaults["com.Artengar.PatternCreator.bottom"] = self.window.bottom.get()
			Glyphs.defaults["com.Artengar.PatternCreator.width"] = self.window.width.get()
			Glyphs.defaults["com.Artengar.PatternCreator.hor_spacing"] = self.window.hor_spacing.get()
			Glyphs.defaults["com.Artengar.PatternCreator.angle"] = self.window.angle.get()
			Glyphs.defaults["com.Artengar.PatternCreator.height"] = self.window.height.get()
			Glyphs.defaults["com.Artengar.PatternCreator.amount_of_strokes"] = self.window.amount_of_strokes.get()
			Glyphs.defaults["com.Artengar.PatternCreator.shape_height"] = self.window.shape_height.get()
			Glyphs.defaults["com.Artengar.PatternCreator.shape_width"] = self.window.shape_width.get()
			Glyphs.defaults["com.Artengar.PatternCreator.vert_shape_spacing"] = self.window.vert_shape_spacing.get()
			Glyphs.defaults["com.Artengar.PatternCreator.hor_shape_spacing"] = self.window.hor_shape_spacing.get()
			Glyphs.defaults["com.Artengar.PatternCreator.dot_diameter"] = self.window.dot_diameter.get()
			return True
		except:
			print "Could not save prefs"
			return False
		
	#Search for existing prefs:
	def LoadPreferences(self): 
		try:
			NSUserDefaults.standardUserDefaults().registerDefaults_(
				{
					"com.Artengar.PatternCreator.top": 500,
					"com.Artengar.PatternCreator.bottom": 0,
					"com.Artengar.PatternCreator.width": 20,
					"com.Artengar.PatternCreator.hor_spacing": 20,
					"com.Artengar.PatternCreator.text_angle": 0,
					"com.Artengar.PatternCreator.height": 25,
					"com.Artengar.PatternCreator.amount_of_strokes": 4,
					"com.Artengar.PatternCreator.shape_height": 25,
					"com.Artengar.PatternCreator.shape_width": 4,
					"com.Artengar.PatternCreator.vert_shape_spacing": 5,
					"com.Artengar.PatternCreator.hor_shape_spacing": 5,
					"com.Artengar.PatternCreator.dot_diameter": 20
				}
			)
			self.window.top.set(Glyphs.defaults["com.Artengar.PatternCreator.top"])
			self.window.bottom.set(Glyphs.defaults["com.Artengar.PatternCreator.bottom"])
			self.window.width.set(Glyphs.defaults["com.Artengar.PatternCreator.width"])
			self.window.hor_spacing.set(Glyphs.defaults["com.Artengar.PatternCreator.hor_spacing"])
			self.window.angle.set(Glyphs.defaults["com.Artengar.PatternCreator.angle"])
			self.window.height.set(Glyphs.defaults["com.Artengar.PatternCreator.height"])
			self.window.amount_of_strokes.set(Glyphs.defaults["com.Artengar.PatternCreator.amount_of_strokes"])
			self.window.shape_height.set(Glyphs.defaults["com.Artengar.PatternCreator.shape_height"])
			self.window.shape_width.set(Glyphs.defaults["com.Artengar.PatternCreator.shape_width"])
			self.window.vert_shape_spacing.set(Glyphs.defaults["com.Artengar.PatternCreator.vert_shape_spacing"])
			self.window.hor_shape_spacing.set(Glyphs.defaults["com.Artengar.PatternCreator.hor_shape_spacing"])
			self.window.dot_diameter.set(Glyphs.defaults["com.Artengar.PatternCreator.dot_diameter"])
			return True
		except:
			print "Could not load prefs"
			return False
	
	def Change_Options(self, sender):
		print "Options are changed"
		return
		
	def Change_Shape(self, sender):
		#Determine the shape
		try:
			shape = self.window.Change_shape.getItems()[self.window.Change_shape.get()]
		except:
			print "Could not determine the shape... Shape is:", shape
			return False
		try:
			#Determine which items are visible (overwrites the previous instructions)
			if shape == "Stripes":
				self.window.text_width.show(True)
				self.window.width.show(True)
				self.window.text_hor_spacing.show(True)
				self.window.hor_spacing.show(True)
				self.window.text_adjustments.show(True)
				self.window.text_angle.show(True)
				self.window.angle.show(True)
				self.window.text_angle_warning.show(True)
				#items 2
				self.window.text_height.show(False)
				self.window.height.show(False)
				self.window.text_amount_of_strokes.show(False)
				self.window.amount_of_strokes.show(False)
				self.window.text_warning1.show(False)
				#items 3
				self.window.text_shape_height.show(False)
				self.window.shape_height.show(False)
				self.window.text_shape_width.show(False)
				self.window.shape_width.show(False)
				self.window.text_vert_shape_spacing.show(False)
				self.window.vert_shape_spacing.show(False)
				self.window.text_hor_shape_spacing.show(False)
				self.window.hor_shape_spacing.show(False)
				self.window.text_warning2.show(False)
				#items 4
				self.window.text_dot_diameter.show(False)
				self.window.dot_diameter.show(False)
			elif shape == "Horizontal lines":
				self.window.text_width.show(False)
				self.window.width.show(False)
				self.window.text_hor_spacing.show(False)
				self.window.hor_spacing.show(False)
				self.window.text_adjustments.show(False)
				self.window.text_angle.show(False)
				self.window.angle.show(False)
				self.window.text_angle_warning.show(False)
				#items 2
				self.window.text_height.show(True)
				self.window.height.show(True)
				self.window.text_amount_of_strokes.show(True)
				self.window.amount_of_strokes.show(True)
				self.window.text_warning1.show(True)
				#items 3
				self.window.text_shape_height.show(False)
				self.window.shape_height.show(False)
				self.window.text_shape_width.show(False)
				self.window.shape_width.show(False)
				self.window.text_vert_shape_spacing.show(False)
				self.window.vert_shape_spacing.show(False)
				self.window.text_hor_shape_spacing.show(False)
				self.window.hor_shape_spacing.show(False)
				self.window.text_warning2.show(False)
				#items 4
				self.window.text_dot_diameter.show(False)
				self.window.dot_diameter.show(False)
			elif shape == "Planes" or shape == "Rhombus" or shape == "Dots":
				self.window.text_width.show(False)
				self.window.width.show(False)
				self.window.text_hor_spacing.show(False)
				self.window.hor_spacing.show(False)
				self.window.text_adjustments.show(False)
				self.window.text_angle.show(False)
				self.window.angle.show(False)
				self.window.text_angle_warning.show(False)
				#items 2
				self.window.text_height.show(False)
				self.window.height.show(False)
				self.window.text_amount_of_strokes.show(False)
				self.window.amount_of_strokes.show(False)
				self.window.text_warning1.show(False)
				#items 3
				if shape == "Planes" or shape == "Rhombus":
					self.window.text_shape_height.show(True)
					self.window.shape_height.show(True)
					self.window.text_shape_width.show(True)
					self.window.shape_width.show(True)
					self.window.text_dot_diameter.show(False)
					self.window.dot_diameter.show(False)
				if shape == "Dots":
					self.window.text_shape_height.show(False)
					self.window.shape_height.show(False)
					self.window.text_shape_width.show(False)
					self.window.shape_width.show(False)
					self.window.text_dot_diameter.show(True)
					self.window.dot_diameter.show(True)
				self.window.text_vert_shape_spacing.show(True)
				self.window.vert_shape_spacing.show(True)
				self.window.text_hor_shape_spacing.show(True)
				self.window.hor_shape_spacing.show(True)
				self.window.text_warning2.show(True)
				#items 4 ->
				#See above
		except Exception, ex:
			print "Error in determining the corresponding options: %s"%ex
			return False
		return
		
	def Draw(self, sender):
		#Determine the shape
		font.disableUpdateInterface()
		try:
			shape = self.window.Change_shape.getItems()[self.window.Change_shape.get()]
		except:
			print "Could not determine the shape... Shape is:", shape
			return False
		#Get the values for each type of pattern
		try:
			#General options:
			Value_top = float(self.window.top.get())
			Value_bottom = float(self.window.bottom.get())
			if Value_top < Value_bottom:
				Message("Top and Bottom not correct", "The top has to be above the bottom.", OKButton=None)
				return
			
			##########
			if shape == "Stripes":
				#First check if all these variables are decimals!
				Value_width = float(self.window.width.get())
				Value_spacing = float(self.window.hor_spacing.get())
				Value_angle = float(self.window.angle.get())
				if Value_width <= 0 or Value_spacing < 0:
					Message("Incorrect values", "Patterncreator detected a value that is not possible. The Width should be more than zero, the spacing can be zero or more.", OKButton=None)
					return
				if not -85 <= Value_angle <= 85:
					Message("Angle to large", "The entered angle is to large. Stay between -85 and 85 degrees.", OKButton=None)
					return
				Draw_vertical_strokes(Value_bottom, Value_top, Value_width, Value_spacing, Value_angle)
			
			##########
			elif shape == "Horizontal lines":
				Value_height = float(self.window.height.get())
				Value_amount_of_strokes = float(self.window.amount_of_strokes.get())
				if Value_height <= 0 or Value_amount_of_strokes <= 0:
					Message("Warning: cannot create a pattern", "A stroke height with value 0 or less is not possible, nor is it possible to create a pattern with zero strokes...", OKButton=None)
					return
				if not 0 < (Value_height * Value_amount_of_strokes) <= (Value_top - Value_bottom):
					Message("Warning: it does not fit", "There are more strokes than there is space... Please choose smaller or choose lesser strokes.", OKButton=None)
					return
				Draw_horizontal_strokes(Value_bottom, Value_top, Value_height, Value_amount_of_strokes)
			
			##########
			elif shape == "Planes" or shape == "Rhombus" or shape == "Dots":
				if shape == "Dots":
					Value_shape_height = float(self.window.dot_diameter.get())
					Value_shape_width = Value_shape_height
					if Value_shape_height <= 10:
						Message("Warning: to little", "It is not recommended to make the pattern that little, as it is barely visible. Choose an other diameter.", OKButton=None)
						return
				elif shape == "Planes" or shape == "Rhombus":
					Value_shape_height = float(self.window.shape_height.get())
					Value_shape_width = float(self.window.shape_width.get())
				Value_vert_spacing = float(self.window.vert_shape_spacing.get())
				Value_hor_spacing = float(self.window.hor_shape_spacing.get())
				#Check if the amount of paths to draw is to large
				if check == False:
					amount_of_shapes = 0
					for item in Glyphs.font.selectedLayers:
						amount_of_shapes = amount_of_shapes + (get_pattern_height(Value_bottom, Value_top) / (Value_shape_height + Value_vert_spacing)) * (item.width / (Value_shape_width + Value_hor_spacing))
					if amount_of_shapes >= 125:
						Message("Warning: much chapes", "You are about to draw a lot of shapes. This will slow down Glyphs and later on, also your font. You may continue at your own risk by pressing the button an other time.", OKButton=None)
						print "Shapes to draw: ", amount_of_shapes
						global check
						check = True #check is set to False by restarting the program.
						return
				if Value_shape_height <= 0 or Value_shape_width <= 0:
					Message("Warning: cannot create a pattern", "A shape height or shape width with value 0 or less is not possible.", OKButton=None)
					return
				Draw_pieces(shape, Value_bottom, Value_top, Value_shape_height, Value_shape_width, Value_vert_spacing, Value_hor_spacing)
			
		except Exception, ex:
			Message("Not valid", "There is something serious malfunctioning: %s. First try restarting Glyphs or choose an other font and make sure there is a selection."%ex, OKButton=None)
			return False
		font.enableUpdateInterface()
		self.window.close()



#Let the script do his work:
if len(Glyphs.fonts) <=0:
	Message("No open fonts", "There are no fonts open. The PatternCreator can't do his work.", OKButton=None)
else:
	Glyphs.clearLog()
	run_program()
	font = Glyphs.font