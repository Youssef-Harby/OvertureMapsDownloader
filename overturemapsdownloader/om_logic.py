import logging
from overturemapsdownloader.omdownloader_dask import (
    get_clipped_gdf,
    get_df_from_parquet,
    make_gdf_from_df,
)
from overturemapsdownloader.utils_helper import read_geospatial_data

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] %(levelname)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)


def om_dask_to_parquet():
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


if __name__ == "__main__":
    om_dask_to_parquet()
