#MenuTitle: Extract Master
# -*- coding: utf-8 -*-
__doc__="""
The 'Extract Master' script for the app Glyphs created by Artengar (Maarten Renckens) copies the first master to a new file, removing all other masters and layers.
    """

# Delete all masters and layers but the first master
Active_Font = Glyphs.fonts[0]
Glyphs.clearLog()

def CreateCopy(Active_Font):
    copiedFile = Active_Font.copy()
    copiedFile.familyName = "Extracted master from %s" %Active_Font.familyName
    copiedFile.gridSubDivisions = 100#for better details
    #Erase all other masters in the copied font
    copiedFile.disableUpdateInterface()
    
    #Delete masters
    toKeep = copiedFile.masters[0].id
    numberOfMasters = len(copiedFile.masters)
    for i in range( numberOfMasters )[::-1]:
        if copiedFile.masters[i].id != toKeep:
            del copiedFile.masters[i]
    #Delete all Layers in the remaining Master (this is based on Mekkablue's script)
    searchTerms = [ "[]", "{}" ]
    for thisGlyph in copiedFile.glyphs:
        numberOfLayers = len( thisGlyph.layers )
        thisGlyphName = thisGlyph.name

        if str(thisGlyphName)[:7] != "_smart.":
            thisGlyph.beginUndo()
            for i in range( numberOfLayers )[::-1]:
                thisLayer = thisGlyph.layers[i]
                if thisLayer.layerId != thisLayer.associatedMasterId: # not the master layer
                    thisLayerName = thisLayer.name
                    thisLayerShouldBeRemoved = True
                    if thisLayerName: # always delete unnamed layers
                        for parentheses in searchTerms:
                            opening = parentheses[0]
                            closing = parentheses[1]
                            
                            # check if ONE of them is at the END of the layer name, like:
                            # Bold [160], Bold [160[, Bold ]160], Regular {120}
                            if thisLayerName.endswith(opening) or thisLayerName.endswith(closing):
                                thisLayerShouldBeRemoved = False
                                
                    if thisLayerShouldBeRemoved:
                        del thisGlyph.layers[i]
            thisGlyph.endUndo()
            print "Layers deleted in %s." % ( thisGlyphName )
        
        else:
            print "Smart layers kept in %s." % ( thisGlyphName )
        
    copiedFile.enableUpdateInterface()
    Glyphs.fonts.append(copiedFile)
    return copiedFile
    
CreateCopy(Active_Font)
