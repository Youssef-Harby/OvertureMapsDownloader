import logging
from overturemapsdownloader.dask_qrys import (
    get_clipped_gdf,
    get_df_from_parquet,
    make_gdf_from_df,
)
from overturemapsdownloader.utils_helper import read_geospatial_data


def om_dask_to_parquet(config):
    bbox_filter = read_geospatial_data(
        config.global_variables.bbox_file_path,
        as_shapely_str=True,
        output_format="Custom",
    )

    df = get_df_from_parquet(
        parquet_path=config.format_url("Amazon_S3"),
        # columns=get_columns_from_om_schema_yaml(schema_yaml_path),
    )

    if df is not None:
        gdf = make_gdf_from_df(df, int(config.global_variables.default_epsg))

        # TODO: Add filter by country (also in config)
        if config.global_variables.filter_by_bbox:
            clipped_gdf = get_clipped_gdf(gdf, bbox_filter)
            logging.info(f"Clipped GeoDataFrame: {clipped_gdf}")
            print(clipped_gdf.head(10))
            if clipped_gdf is not None:
                logging.info(
                    f'Writing GeoDataFrame to "{config.global_variables.output_file_path}"'
                )
                clipped_gdf.to_parquet(config.global_variables.output_file_path)
                logging.info("GeoDataFrame written to Parquet file.")
            else:
                logging.error("Could not clip the GeoDataFrame.")
        elif config.global_variables.filter_by_country:
            pass

    else:
        logging.error("Could not read the DataFrame from the Parquet file.")


if __name__ == "__main__":
    om_dask_to_parquet()
