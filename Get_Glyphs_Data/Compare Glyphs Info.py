#MenuTitle: Compare Glyphs info
# -*- coding: utf-8 -*-
__doc__="""
Displays all information about glyphs in the font.
Version 1.2, dating 17 November 2015.
Consult the Glyphs manual for information about the installation of scripts. Contact Artengar on GitHub for changes in the code.
"""
try:
	import vanilla
except Exception:
	Message("Missing Modules", "There are python modulles missing. Go to the menu Glyphs -> Preferences -> latest tab and click on Modules -> Install Modules", OKButton=None)
default_master = "Regular"
default_master_id = 0
all_masters = []
process_always = ["space"]
uppercase = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]
lowercase = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]
numbers = ["one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "zero"]
#####If more letters added, pay attention to the first printed collumn (width)! -> 	Add spaces



#This is the list of print commands:
def print_first_column(glyph_name, number_of_lines):#The name of the glyph or an empty space
	start_of_line = "          " #10 spaces
	if number_of_lines ==0:
		length = len(glyph_name)
		start_of_line = glyph_name + start_of_line[length:]
		print start_of_line,
	else:
		print start_of_line,

def print_header():#Print the header on top
	global default_master
	global masters
	try:
		for master in masters:
			if not master.name == default_master:
				column_text = "                     " #21 spaces (double of the normal columns)
			elif master.name == default_master:
				column_text = "          " #10 spaces (equal to normal columns)
			item = str(master.name)
			length = len(item)
			length2 = len(column_text)
			if len(item) > len(column_text):
				column_text = item[:length2-1] + "+"
			else:
				column_text = column_text[length:] + item
			print column_text, " |",
		print
	except Exception, ex:
		print "Error: Could not make a header: %s"%ex,

def print_second_column(property_name):#The property name
	property_width = "                    " #20 spaces if the proportions are also printed
	length = len(property_name)
	property_width = property_width[length:] + property_name
	print property_width, " |",

def print_next_columns(item): #These are all values
	column_text = "          " #10 spaces
	item = str(round(item, 1))
	length = len(item)
	column_text = column_text[length:] + item
	print column_text,

def print_proportions(proportion):
	column_text = "        " #8 spaces
	if proportion == "None":
		length = len(proportion)
		column_text = column_text[length:] + "  " + proportion
	else:
		proportion = str(round(proportion, 1))
		length = len(proportion)
		column_text = column_text[length:] + "=" + proportion + "%"
	print column_text,



#Collect all data to print
def print_data(glyph):
	try:
		#Glyph name should only be printed on the first line
		number_of_lines = 0
		#get the total width
		if Glyphs.defaults["com.Artengar.CompareGlyphsInfo.TotalWidth"] == True:
			print_first_column(glyph, number_of_lines)
			print_second_column("TotalWidth")
			for master in masters:
				try:
					layer = font.glyphs[glyph].layers[master.id]
					print_next_columns(layer.width)
					#if desired, get the proportions of both current master and default master
					if Glyphs.defaults["com.Artengar.CompareGlyphsInfo.Proportions"] == True:
						if not master.name == default_master:
							#Compare the old and new values
							global default_master_id
							layer = font.glyphs[glyph].layers[master.id]
							new_width = layer.width
							old_layer = font.glyphs[glyph].layers[default_master_id]
							old_info = old_layer.width
							if old_info == 0:
								print_proportions("None")
							else:
								proportion = new_width/old_info*100
								print_proportions(round(proportion, 1))
					print " |",
				except Exception, ex:
					print "Error: %s"%ex,
			number_of_lines +=1
			print
		#get the total width
		if Glyphs.defaults["com.Artengar.CompareGlyphsInfo.TotalLetterWidth"] == True:
			print_first_column(glyph, number_of_lines)
			print_second_column("Total Letter Width")
			for master in masters:
				try:
					layer = font.glyphs[glyph].layers[master.id]
					letter_width = layer.width - layer.LSB - layer.RSB
					print_next_columns(letter_width)
					#if desired, get the proportions of both current master and default master
					if Glyphs.defaults["com.Artengar.CompareGlyphsInfo.Proportions"] == True:
						if not master.name == default_master:
							layer = font.glyphs[glyph].layers[master.id]
							new_width = layer.width
							old_layer = font.glyphs[glyph].layers[default_master_id]
							old_info = old_layer.width
							if old_info == 0:
								print_proportions("None")
							else:
								proportion = new_width/old_info*100
								print_proportions(proportion)
					print " |",
				except Exception, ex:
					print "Error: %s"%ex,
			number_of_lines +=1
			print
		#get the left sidebearing
		if Glyphs.defaults["com.Artengar.CompareGlyphsInfo.LeftSideBearing"] == True:
			print_first_column(glyph, number_of_lines)
			print_second_column("Left SideBearing")
			for master in masters:
				try:
					layer = font.glyphs[glyph].layers[master.id]
					print_next_columns(layer.LSB)
					#if desired, get the proportions of both current master and default master
					if Glyphs.defaults["com.Artengar.CompareGlyphsInfo.Proportions"] == True:
						if not master.name == default_master:
							layer = font.glyphs[glyph].layers[master.id]
							new_LSB = layer.LSB
							old_layer = font.glyphs[glyph].layers[default_master_id]
							old_info = old_layer.LSB
							if old_info == 0:
								print_proportions("None")
							else:
								proportion = new_LSB/old_info*100
								print_proportions(proportion)
					print " |",
				except Exception, ex:
					print "Error: %s"%ex,
			number_of_lines +=1
			print
		#get the right sidebearing
		if Glyphs.defaults["com.Artengar.CompareGlyphsInfo.RightSideBearing"] == True:
			print_first_column(glyph, number_of_lines)
			print_second_column("Right SideBearing")
			for master in masters:
				try:
					layer = font.glyphs[glyph].layers[master.id]
					print_next_columns(layer.RSB)
					#if desired, get the proportions of both current master and default master
					if Glyphs.defaults["com.Artengar.CompareGlyphsInfo.Proportions"] == True:
						if not master.name == default_master:
							layer = font.glyphs[glyph].layers[master.id]
							new_RSB = layer.RSB
							old_layer = font.glyphs[glyph].layers[default_master_id]
							old_info = old_layer.RSB
							if old_info == 0:
								print_proportions("None")
							else:
								proportion = new_RSB/old_info*100
								print_proportions(proportion)
					print " |",
				except Exception, ex:
					print "Error: %s"%ex,
			number_of_lines +=1
			print
	except Exception, ex:
		print "Error: %s"%ex
		return
	print



def check_if_glyph_in_font(glyph):
	global all_letters
	if glyph in all_letters:
		return True
	else:
		print_first_column(glyph, 0)
		#print_second_column(" ")
		print "This glyph is not present in the font"



def select_data():
	Glyphs.clearLog()
	print "(View & print this log in a monospace font so all values are aligned)"
	print "In the font %s are the values through the different masters:"%font.familyName
	print
	print
	#print a header
	print_first_column("Empty", 1)
	print_second_column(" ")
	print_header()
	print
	#print the data for each desired glyph:
	for glyph in process_always:
		print_data(glyph)
	if Glyphs.defaults["com.Artengar.CompareGlyphsInfo.UseUppercase"] == True:
		for glyph in uppercase:
			#Check if the glyph is in the font.
			if check_if_glyph_in_font(glyph):
				#print the glyph name and make an equal room after it.
				print_data(glyph)
	if Glyphs.defaults["com.Artengar.CompareGlyphsInfo.UseLowercase"] == True:
		for glyph in lowercase:
			#Check if the glyph is in the font.
			if check_if_glyph_in_font(glyph):
				#print the glyph name and make an equal room after it.
				print_data(glyph)
	if Glyphs.defaults["com.Artengar.CompareGlyphsInfo.UseNumber"] == True:
		for glyph in numbers:
			#Check if the glyph is in the font.
			if check_if_glyph_in_font(glyph):
				#print the glyph name and make an equal room after it.
				print_data(glyph)



class show_window(object):
	def __init__(self):
		global all_masters
		windowWidth  = 220
		windowHeight = 410
		self.w = vanilla.FloatingWindow(( windowWidth, windowHeight ), "Compare Glyphs information", autosaveName = "com.artengar.CompareGlyphsInfo.mainwindow"
		)

		self.w.text_1 = vanilla.TextBox( (20, 15, -20, 30), "Compare in the active font:", sizeStyle='small' )
		self.w.UseUppercase = vanilla.CheckBox( (20, 35, -20, 20), "the uppercase", value=True, callback=self.SavePreferences, sizeStyle='small' )
		self.w.UseLowercase = vanilla.CheckBox( (20, 55, -20, 20), "the lowercase", value=True, callback=self.SavePreferences, sizeStyle='small' )
		self.w.UseNumber = vanilla.CheckBox( (20, 75, -20, 20), "the numbers", value=True, callback=self.SavePreferences, sizeStyle='small' )
		self.w.text_2 = vanilla.TextBox( (20, 110, -20, 45), "and display for each master in each glyph the next items:", sizeStyle='small' )
		self.w.TotalWidth = vanilla.CheckBox( (20, 143, -20, 20), "the total glyph width", value=False, callback=self.SavePreferences, sizeStyle='small' )
		self.w.TotalLetterWidth = vanilla.CheckBox( (20, 163, -20, 20), "the total shape width", value=False, callback=self.SavePreferences, sizeStyle='small' )
		self.w.LeftSideBearing = vanilla.CheckBox( (20, 183, -20, 20), "the left sidebearing", value=True, callback=self.SavePreferences, sizeStyle='small' )
		self.w.RightSideBearing = vanilla.CheckBox( (20, 203, -20, 20), "the right sidebearing", value=True, callback=self.SavePreferences, sizeStyle='small' )
		self.w.Proportions = vanilla.CheckBox( (20, 243, -20, 20), "Print also the proportions", value=True, callback=self.SavePreferences, sizeStyle='small' )
		self.w.text_3 = vanilla.TextBox( (20, -145, -20, 60), "Define the Master that is the comparison for other Masters:", sizeStyle='small' )
		self.w.Change_master = vanilla.PopUpButton( (20, -105, -20, 20), all_masters, sizeStyle='small', callback=self.Change_master)
		self.w.Button = vanilla.Button( (20, -40, -20, 15), "Compare selected glyphs", callback=self.action, sizeStyle='small' )
		
		#Finisch window
		if not self.LoadPreferences():
			print "Preferences could not be loaded or are not yet set."
		self.w.open()
		self.w.makeKey()
		
	def SavePreferences(self, sender):
		try:
			Glyphs.defaults["com.Artengar.CompareGlyphsInfo.UseUppercase"] = self.w.UseUppercase.get()
			Glyphs.defaults["com.Artengar.CompareGlyphsInfo.UseLowercase"] = self.w.UseLowercase.get()
			Glyphs.defaults["com.Artengar.CompareGlyphsInfo.UseNumber"] = self.w.UseNumber.get()
			Glyphs.defaults["com.Artengar.CompareGlyphsInfo.TotalWidth"] = self.w.TotalWidth.get()
			Glyphs.defaults["com.Artengar.CompareGlyphsInfo.TotalLetterWidth"] = self.w.TotalLetterWidth.get()
			Glyphs.defaults["com.Artengar.CompareGlyphsInfo.LeftSideBearing"] = self.w.LeftSideBearing.get()
			Glyphs.defaults["com.Artengar.CompareGlyphsInfo.RightSideBearing"] = self.w.RightSideBearing.get()
			Glyphs.defaults["com.Artengar.CompareGlyphsInfo.Proportions"] = self.w.Proportions.get()
		except:
			print "Preferences could not be saved"
			return False
		return True
		
	def LoadPreferences(self):
		try:
			NSUserDefaults.standardUserDefaults().registerDefaults_(
				{
					"com.Artengar.CompareGlyphsInfo.UseUppercase": True,
					"com.Artengar.CompareGlyphsInfo.UseLowercase": True,
					"com.Artengar.CompareGlyphsInfo.UseNumber": False,
					"com.Artengar.CompareGlyphsInfo.TotalWidth": True,
					"com.Artengar.CompareGlyphsInfo.TotalLetterWidth": True,
					"com.Artengar.CompareGlyphsInfo.LeftSideBearing": True,
					"com.Artengar.CompareGlyphsInfo.RightSideBearing": True,
					"com.Artengar.CompareGlyphsInfo.Proportions": True
				}
			)
			self.w.UseUppercase.set( Glyphs.defaults["com.Artengar.CompareGlyphsInfo.UseUppercase"] )
			self.w.UseLowercase.set( Glyphs.defaults["com.Artengar.CompareGlyphsInfo.UseLowercase"] )
			self.w.UseNumber.set( Glyphs.defaults["com.Artengar.CompareGlyphsInfo.UseNumber"] )
			self.w.TotalWidth.set( Glyphs.defaults["com.Artengar.CompareGlyphsInfo.TotalWidth"] )
			self.w.TotalLetterWidth.set( Glyphs.defaults["com.Artengar.CompareGlyphsInfo.TotalLetterWidth"] )
			self.w.LeftSideBearing.set( Glyphs.defaults["com.Artengar.CompareGlyphsInfo.LeftSideBearing"] )
			self.w.RightSideBearing.set( Glyphs.defaults["com.Artengar.CompareGlyphsInfo.RightSideBearing"] )
			self.w.Proportions.set( Glyphs.defaults["com.Artengar.CompareGlyphsInfo.Proportions"] )
		except:
			return False
		return True
	
	def Change_master(self, sender):
		global default_master
		global default_master_id
		global all_masters
		#Get the id of the entered master name
		try:
			default_master = self.w.Change_master.getItems()[self.w.Change_master.get()]
			for master in masters:
				if master.name == default_master:
					default_master_id = master.id
		except Exception, ex:
			print "Error: %s"%ex,
	
	def action(self, sender):
		if Glyphs.defaults["com.Artengar.CompareGlyphsInfo.TotalWidth"] == False and Glyphs.defaults["com.Artengar.CompareGlyphsInfo.TotalLetterWidth"] == False and Glyphs.defaults["com.Artengar.CompareGlyphsInfo.LeftSideBearing"] == False and Glyphs.defaults["com.Artengar.CompareGlyphsInfo.RightSideBearing"] == False:
			Message("No options selected", "Please select properties to process", OKButton=None)
			return
		else:
			try:
				self.w.close()
				select_data()
				Message("Script completed", "All desired letters are compared through all their masters. You can view the tables in the Macro panel (enlarge that window for best view) and you can copy it there for use in an other program.", OKButton=None)
				Glyphs.showMacroWindow()
			except Exception, ex:
				print "Error: %s"%ex



if len(Glyphs.fonts) <=0:
	Message("Error", "There are no fonts open. The script cannot continue", OKButton=None)
else:
	#Get everything that is in the active font 
	font = Glyphs.font
	masters = Glyphs.font.masters
	for master in masters:
		all_masters.append(str(master.name))
	#Set the master where the others should be compared with.
	try:
		default_master = all_masters[0]
	except Exception, ex:
		print "Error: %s"%ex,
	#Get the id of the entered master name
	for master in masters:
		if master.name == default_master:
			default_master_id = master.id
	all_letters = []
	for item in Glyphs.font.glyphs:
		all_letters.append(item.name)
	show_window()