import geopandas as gpd
import pandas as pd
from pathlib import Path
import fiona
from shapely import wkt, wkb
from shapely.geometry import Polygon
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)


def detect_file_type(filepath: str):
    """
    Detect the type of geospatial file based on its extension.

    :param filepath: The path to the geospatial data file.
    :return: A string representing the file type.
    """
    # Create a Path object and get the file extension (without the dot)
    path = Path(filepath)
    extension = path.suffix[1:].lower()

    # Check if the extension is one of the recognized types
    if extension in ["geojson", "gpkg", "shp", "gdb", "csv", "xls", "xlsx"]:
        return extension
    else:
        raise ValueError(f"Unsupported file type: {extension}")


def remove_extension(full_path):
    """
    Removes the file extension from a given path.

    :param full_path: The full path to the file.
    :return: The file path without the extension.
    """
    path = Path(full_path)
    return str(path.with_suffix(""))


def read_geospatial_data(
    filepath,
    table_name=None,
    as_shapely_str=False,
    geometry_types=["Polygon", "MultiPolygon"],
    output_format="WKT",
):
    """
    Reads a geospatial data file and returns it as a GeoDataFrame or with geometries as Shapely strings.

    :param filepath: The path to the geospatial data file.
    :param table_name: The name of the table or layer to load (for GeoPackage or File Geodatabase).
    :param as_shapely_str: If True, return geometries as Shapely strings.
    :param geometry_types: List of geometry types to filter. Default includes 'Polygon' and 'MultiPolygon'.
    :return: A GeoDataFrame containing the data from the file.
    """
    # Ensure file exists
    if not Path(filepath).exists():
        raise FileNotFoundError(f"File not found: {filepath}")

    # Detect the file type
    file_type = detect_file_type(filepath)

    # Map file type to driver
    driver_map = {
        "geojson": "GeoJSON",
        "shp": "ESRI Shapefile",
        "gpkg": "GPKG",
        "gdb": "OpenFileGDB",
    }

    # Check if the driver is one of the recognized types
    if file_type not in driver_map:
        raise ValueError(f"Unsupported file type: {file_type}")

    try:
        # Read the file
        if file_type in ["gpkg", "gdb"]:
            if table_name is None:
                raise ValueError(f"A table name must be provided for {file_type} files")
            else:
                gdf = gpd.read_file(
                    filepath, layer=table_name, driver=driver_map[file_type]
                )
        else:
            gdf = gpd.read_file(filepath, driver=driver_map[file_type])

        # Filter by geometry type
        gdf = gdf[gdf["geometry"].apply(lambda geom: geom.geom_type in geometry_types)]

        if as_shapely_str:
            first_geom = gdf.loc[0, "geometry"]
            if first_geom.geom_type in geometry_types:
                if output_format == "WKT":
                    return str(first_geom)
                elif output_format == "Custom":
                    if isinstance(first_geom, Polygon):
                        return first_geom
                    else:
                        logging.info(
                            f"The geometry is not a Polygon, it's a {first_geom.geom_type}"
                        )
                        return None
                else:
                    raise ValueError(
                        "Invalid output_format. Choose from 'WKT' or 'Custom'."
                    )
        return gdf

    except Exception as e:
        logging.error(f"An error occurred while reading the file: {e}")


def write_geospatial_data(gdf, filepath, driver=None, layer=None, encoding="utf-8"):
    """
    Writes a GeoDataFrame to a geospatial data file.

    :param gdf: The GeoDataFrame to write.
    :param filepath: The path to the file to write.
    :param driver: The driver to use for writing the file.
    :param layer: The layer to write (for GeoPackage or File Geodatabase).
    :param encoding: The encoding to use for writing the file. Defaults to 'utf-8'.
    :return: newfilepath: The path of the file that was written.
    """
    # Detect the file type if no driver is given
    if driver is None:
        driver = detect_file_type(filepath)
    newfilepath = remove_extension(filepath) + "." + driver

    # Map file type to driver
    driver_map = {
        "geojson": "GeoJSON",
        "shp": "ESRI Shapefile",
        "gpkg": "GPKG",
        "gdb": "OpenFileGDB",
    }

    # Check if the driver is one of the recognized types
    if driver not in driver_map:
        raise ValueError(f"Unsupported file type: {driver}")

    # Write the GeoDataFrame to file
    try:
        if driver == "gdb":
            # Make sure the OpenFileGDB driver is supported
            assert (
                "OpenFileGDB" in fiona.supported_drivers
            ), "OpenFileGDB driver is not supported"
            # Make sure the OpenFileGDB driver supports writing ('w')
            assert (
                "w" in fiona.supported_drivers["OpenFileGDB"]
            ), "OpenFileGDB driver does not support writing"
            gdf.to_file(
                newfilepath, driver=driver_map[driver], layer=layer, encoding=encoding
            )
        elif driver == "gpkg":
            gdf.to_file(
                newfilepath, driver=driver_map[driver], layer=layer, encoding=encoding
            )
        else:
            gdf.to_file(newfilepath, driver=driver_map[driver], encoding=encoding)
    except Exception as e:
        logging.error(f"An error occurred while writing the file: {e}")
    return newfilepath


def detect_geometry_format(geometry_sample):
    """
    Detect the format of the geometry (WKT or WKB).

    :param geometry_sample: A sample geometry to detect.
    :return: A string representing the geometry format ('WKT' or 'WKB').
    """
    if isinstance(geometry_sample, str):
        return "WKT"
    elif isinstance(geometry_sample, bytes):
        return "WKB"
    else:
        try:
            wkt.loads(str(geometry_sample))
            return "WKT"
        except:
            try:
                wkb.loads(bytes(geometry_sample))
                return "WKB"
            except:
                return None
