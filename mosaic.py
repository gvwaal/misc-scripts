print("importing os...")
import os
print("importing arcpy...")
import arcpy

arcpy.env.workspace = r"C:\Users\Gerrit\GIS\optimal_agate_picking\DEM_zips"

gdb_list = os.listdir(r"C:\Users\Gerrit\GIS\optimal_agate_picking\DEM_zips")

dem_list = []

for directory in gdb_list:
    new_dir = os.path.join("C:\\Users\\Gerrit\\GIS\\optimal_agate_picking\\DEM_zips\\" + directory.rstrip('\r\n'))
    os.chdir(new_dir)
    dem_name = os.path.join(new_dir + r"\dem_1m_m")
    dem_list.append(dem_name)
    print("appending " + directory)
    os.chdir(r"C:\Users\Gerrit\GIS\optimal_agate_picking\DEM_zips")

print("mosaicing...")
arcpy.MosaicToNewRaster_management(dem_list, r"C:\Users\Gerrit\GIS\optimal_agate_picking\dem_1m.gdb", "north_shore_1m", "", "32_BIT_FLOAT", 1, 1)

print("complete")