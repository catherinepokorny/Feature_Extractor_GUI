# -*- coding: utf-8 -*-
"""
Created on Wed Feb  1 15:26:39 2023

@author: catpo
"""

def FeatureExtraction(polygonFile, pointFile, polygonField, pointField, polygonValue, pointValue, outputFile):
    import arcpy
    polygonQuery = '"{0}" = \'{1}\''.format(polygonField, polygonValue)          # query string
    arcpy.management.MakeFeatureLayer(polygonFile,"polygonLayer", polygonQuery)# produce layer based on query string

    # select target points from point file
    if pointValue:   # not None, so the query string needs to use pointValue
        pointQuery = '"{0}" = \'{1}\''.format(pointField, pointValue)
    else:            # pointValue is None, so the query string aks for entries that are not NULL and not the empty string
        pointQuery = '"{0}" IS NOT NULL AND "{0}" <> \'\''.format(pointField) 
    arcpy.management.MakeFeatureLayer(pointFile,"pointLayer", pointQuery)        # produce layer based on query string
      
    # select only points of interest in point layer that are within the target polygon    
    arcpy.management.SelectLayerByLocation("pointLayer", "WITHIN", "polygonLayer")
 
    # write selection to output file
    arcpy.CopyFeatures_management("pointLayer", outputFile)
 
    # clean up layers    
    arcpy.Delete_management("polygonLayer")
    arcpy.Delete_management("pointLayer")
    
def importArcpyIfAvailable():
    """test whether arcpy is available for import"""
    try: # test whether we can import arcpy
        import arcpy
    except:
        return False
    return True    

def runningAsScriptTool():
    """test whether this program is run as a script tool in ArcGIS"""
    try: # test whether we can access an opened ArcGIS project
        import arcpy
        arcpy.mp.ArcGISProject("CURRENT")
    except:
        return False
    return True
    
    
