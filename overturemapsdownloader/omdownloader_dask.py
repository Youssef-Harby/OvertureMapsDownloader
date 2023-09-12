import logging
import dask.dataframe as dd
import geopandas as gpd
import dask_geopandas as dgpd
from overturemapsdownloader.utils_helper import read_geospatial_data
from dask.diagnostics import ProgressBar

ProgressBar().register()


def get_df_from_parquet(
    parquet_path,
    engine="pyarrow",
    columns=["geometry"],
    storage_options={"anon": True},
    parquet_file_extensions=False,
):
    """
    Reads a Dask DataFrame from a Parquet file.
    """
    try:
        df = dd.read_parquet(
            parquet_path,
            columns=columns,
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


def make_gdf_from_df(df, crs=4326):
    """
    Converts a Dask DataFrame to a Dask GeoDataFrame.
    """
    # TODO: Make CRS configurable later (config.yml)
    geometry = (
        df["geometry"]
        .map_partitions(gpd.GeoSeries.from_wkb, meta=gpd.GeoSeries(name="geometry"))
        .set_crs(crs)
    )
    return dgpd.from_dask_dataframe(df, geometry=geometry)


def get_clipped_gdf(gdf, bbox_filter):
    """
    Clips the GeoDataFrame using a bounding box.
    """
    return gdf[gdf.geometry.within(bbox_filter)]


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    # TODO: Handle columns with official schemas
    schema_yaml_path = "overturemapsdownloader/schemas/schema/places/place.yaml"

    bbox_filter = read_geospatial_data(
        "examples/bbox.geojson", as_shapely_str=True, output_format="Custom"
    )

    df = get_df_from_parquet(
        parquet_path="s3://overturemaps-us-west-2/release/2023-07-26-alpha.0/theme=places/type=*/*",
        # columns=get_columns_from_om_schema_yaml(schema_yaml_path),
    )

    if df is not None:
        gdf = make_gdf_from_df(df)

        # TODO: Add filter by country (also in config)
        clipped_gdf = get_clipped_gdf(gdf, bbox_filter)

        print(clipped_gdf.head())
    else:
        logging.error("Could not read the DataFrame from the Parquet file.")

    # TODO: Write to file; Parquet by default. Allow user to convert to other formats (e.g., via ogr2ogr).
