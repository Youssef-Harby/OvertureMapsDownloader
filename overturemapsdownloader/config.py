# config.py
import logging
from pathlib import Path
from overturemapsdownloader.yaml_helper import (
    read_yaml_file,
)

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] %(levelname)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)


class Config:
    def __init__(self, config_dict):
        for key, value in config_dict.items():
            if isinstance(value, dict):
                setattr(self, key.lower(), Config(value))
            else:
                setattr(self, key.lower(), value)

    def set_final_url(self, url_name, final_url):
        if hasattr(self.urls, url_name.lower()):
            setattr(self.urls, url_name.lower(), final_url)

    def format_url(self, url_name, theme=None, type_=None):
        if hasattr(self.urls, url_name.lower()):
            url_template = getattr(self.urls, url_name.lower())
            return url_template.format(
                release=self.global_variables.release,
                theme=theme if theme else self.global_variables.default_theme,
                type=type_ if type_ else self.global_variables.default_type,
            )
        else:
            return None


def load_config(yaml_file=None, final_urls=None, **kwargs):
    if yaml_file is None:
        default_path = Path(__file__).parent.parent / "config.yml"
        if default_path.exists():
            yaml_file = default_path
        else:
            yaml_file = input(
                "Default config.yml not found. Please enter the path to the config.yml file: "
            )
            yaml_file = Path(yaml_file)
            if not yaml_file.exists():
                logging.error(f"No such file found: {yaml_file}")
                return None

    config_data = read_yaml_file(yaml_file)
    if config_data is None:
        logging.error("Configuration not loaded due to an error in the YAML file.")
        return None

    if kwargs:
        for key, value in kwargs.items():
            if key in config_data:
                config_data[key].update(value)
            else:
                config_data[key] = value

    config = Config(config_data)

    if final_urls:
        for url_name, final_url in final_urls.items():
            config.set_final_url(url_name, final_url)

    return config


# Examples
if __name__ == "__main__":
    config = load_config()
    if config is None:
        logging.warning("Configuration not loaded.")
        exit(1)

    # Using the S3 credentials (add your own logic here)
    if hasattr(config, "s3_credentials"):
        logging.info(f"S3 Access Key: {config.s3_credentials.access_key}")
        logging.info(f"S3 Secret Key: {config.s3_credentials.secret_key}")

    logging.info(config.format_url("Amazon_S3"))
    logging.info(config.format_url("Microsoft_Azure", theme="places", type_="place"))

    # Example using keyword arguments and setting a final URL
    config2 = load_config(
        global_variables={
            "release": "2023",
            "s3_region": "us-west-1",
            "default_theme": "admins",
            "default_type": "*/*",
        },
        final_urls={
            "Amazon_S3": "s3://overturemaps-us-west-2/beta/{release}/theme={theme}/type={type}"
        },
    )
    logging.info(config2.format_url("Amazon_S3"))
