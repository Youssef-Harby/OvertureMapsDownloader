import logging
import dask.dataframe as dd
import dask
import geopandas as gpd
import dask_geopandas as dgpd
from dask.diagnostics import ProgressBar
from shapely.geometry import Polygon, box

ProgressBar().register()
from dask.distributed import Client, LocalCluster

# cluster = LocalCluster()
# client = Client(cluster)
dask.config.set({"dataframe.query-planning": False})


def compute_dataframe(df):
    try:
        result = df.compute()
        return result
    except Exception as e:
        logging.error(f"Error computing DataFrame: {str(e)}")
        return None


def get_df_from_parquet(
    parquet_path,
    engine="pyarrow",
    storage_options={"anon": True},
    parquet_file_extensions=False,
):
    """
    Reads a Dask DataFrame from a Parquet file.
    """
    try:
        logging.info(f"Reading Parquet file from {parquet_path}")
        df = dd.read_parquet(
            parquet_path,
            engine=engine,
            index="id",
            dtype_backend=engine,
            storage_options=storage_options,
            parquet_file_extensions=parquet_file_extensions,
        )
        return df
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        return None


def make_gdf_from_df(df, crs="EPSG:4326"):
    try:
        if "geometry" in df.columns:
            # Ensure the 'geometry' column is processed as expected
            geometry = df["geometry"].map_partitions(
                gpd.GeoSeries.from_wkb, meta=gpd.GeoSeries()
            )
            df["geometry"] = (
                geometry  # Explicitly assigning the processed column back to the DataFrame
            )

            # Convert to GeoDataFrame
            gdf = dgpd.from_dask_dataframe(df, geometry="geometry")
            gdf.crs = crs

            # Debug output
            print("Conversion successful, GeoDataFrame created.")
            return gdf
        else:
            raise ValueError("Geometry column missing in DataFrame")
    except Exception as e:
        logging.error(f"Failed to convert DataFrame to GeoDataFrame: {str(e)}")
        return None


def get_clipped_gdf(gdf, bbox_filter):
    if isinstance(bbox_filter, tuple):
        bbox_filter = box(*bbox_filter)  # Create Polygon from tuple
    elif isinstance(bbox_filter, Polygon):
        bbox_filter = gpd.GeoSeries(
            [bbox_filter]
        )  # Convert Polygon to GeoSeries if not already

    local_gdf = gdf.compute()  # Compute to get GeoDataFrame

    clipped_gdf = local_gdf[local_gdf.geometry.within(bbox_filter.iloc[0])]
    return clipped_gdf


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    bbox_filter = (31.429, 29.998, 31.531, 30.102)  # Example bbox coordinates

    df = get_df_from_parquet(
        parquet_path="s3://overturemaps-us-west-2/release/2023-07-26-alpha.0/theme=places/type=*/*",
    )

    if df is not None:
        gdf = make_gdf_from_df(df)
        clipped_gdf = get_clipped_gdf(gdf, bbox_filter)
        print(clipped_gdf.head())
    else:
        logging.error("Could not read the DataFrame from the Parquet file.")
