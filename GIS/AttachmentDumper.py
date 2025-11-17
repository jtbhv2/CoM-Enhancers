import arcpy #you have to copy paste this script into Esri conda env
import os

layer = "floodswithpics"  
output_folder = r"C:\Users\brian.stlouis\Documents\FloodPictures"  

selected_ids = [row[0] for row in arcpy.da.SearchCursor(layer, ["GLOBALID"])]

attachment_table = "floodswithpics__ATTACH"

with arcpy.da.SearchCursor(attachment_table, ["REL_GLOBALID", "DATA", "ATT_NAME"]) as cursor:
    for rel_gid, data, name in cursor:
        if rel_gid in selected_ids:

            folder_path = os.path.join(output_folder, rel_gid)
            if not os.path.exists(folder_path):
                os.makedirs(folder_path)


            file_path = os.path.join(folder_path, name)
            with open(file_path, 'wb') as f:
                f.write(data)