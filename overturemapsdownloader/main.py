import typer
import warnings
import logging
from pathlib import Path
from overturemapsdownloader.om_logic import om_dask_to_parquet
from overturemapsdownloader.config import load_config

warnings.simplefilter(action="ignore", category=FutureWarning)

# Setup logging configuration
logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] %(levelname)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)


def callback():
    logging.info("Running a command")


app = typer.Typer(callback=callback)


@app.command()
def omaps(
    theme: str = typer.Option(None, help="Theme of the download, e.g., building"),
    ptype: str = typer.Option(None, help="Type of the parquet, e.g., buildings"),
    bbox: Path = typer.Option(
        None, help="Path to GeoJSON file containing bounding box coordinates"
    ),
    output: Path = typer.Option(None, help="Path to store the output GeoPackage file"),
):
    config = load_config()
    if config is None:
        logging.warning("Configuration not loaded.")
        exit(1)
    if theme:
        config.update_attribute("global_variables", {"default_theme": theme})
        logging.info(f"Theme: {config.global_variables.default_theme}")
    if ptype:
        config.update_attribute("global_variables", {"default_type": ptype})
        logging.info(f"Parquet Type: {config.global_variables.default_type}")
    if bbox:
        config.update_attribute("global_variables", {"filter_by_bbox": "True"})
        config.update_attribute("global_variables", {"bbox_file_path": str(bbox)})
        logging.info(f"Bounding Box File: {config.global_variables.bbox_file_path}")
    if output:
        config.update_attribute("global_variables", {"output_file_path": str(output)})
        logging.info(f"Output File: {config.global_variables.output_file_path}")

    s3_url = config.format_url("Amazon_S3", theme=theme, ptype=ptype)
    logging.info(f"Amazon S3 URL: {s3_url}")

    azure_url = config.format_url("Microsoft_Azure", theme=theme, ptype=ptype)
    logging.info(f"Microsoft Azure URL: {azure_url}")

    # om_dask_to_parquet()


if __name__ == "__main__":
    app()
