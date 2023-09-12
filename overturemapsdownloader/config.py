import logging
from pathlib import Path
from overturemapsdownloader.yaml_helper import read_yaml_file

# Initialize logging
logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] %(levelname)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)


class Config:
    def __init__(self, config_dict):
        for key, value in config_dict.items():
            if key == "themes":
                self.themes = [Config(theme_dict) for theme_dict in value]
            elif isinstance(value, dict):
                setattr(self, key.lower(), Config(value))
            else:
                setattr(self, key.lower(), value)

    def update_attribute(self, attribute_name, new_values):
        attribute = getattr(self, attribute_name, None)
        if attribute is not None:
            for key, value in new_values.items():
                setattr(attribute, key.lower(), value)
        else:
            raise AttributeError(f"{attribute_name} not found in Config.")

    def to_dict(self):
        result = {}
        for key, value in self.__dict__.items():
            if isinstance(value, Config):
                result[key] = value.to_dict()
            elif isinstance(value, list):
                result[key] = [
                    item.to_dict() if isinstance(item, Config) else item
                    for item in value
                ]
            else:
                result[key] = value
        return result

    def format_url(self, url_name, theme=None, ptype=None):
        if hasattr(self.urls, url_name.lower()):
            url_template = getattr(self.urls, url_name.lower())
            final_theme = theme if theme else self.global_variables.default_theme
            final_type = ptype if ptype else self.global_variables.default_type
            return url_template.format(
                release=self.global_variables.release,
                theme=final_theme,
                ptype=final_type,
            )
        else:
            return None


def load_config(yaml_file=None, **kwargs):
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

    config = Config(config_data)
    return config


if __name__ == "__main__":
    config = load_config("config.yml")

    if config is None:
        logging.error("Failed to load config.")
        exit(1)

    # Scenario 1: Retrieve S3 URL with default theme and type
    url1 = config.format_url("Amazon_S3")
    logging.info(f"Scenario 1: S3 URL with default theme and type: {url1}")

    # Scenario 2: Retrieve Azure URL with default theme and type
    url2 = config.format_url("Microsoft_Azure")
    logging.info(f"Scenario 2: Azure URL with default theme and type: {url2}")

    # Scenario 3: Retrieve S3 URL with specific theme and type
    url3 = config.format_url("Amazon_S3", theme="buildings", ptype="building")
    logging.info(f"Scenario 3: S3 URL with specific theme and type: {url3}")

    # Scenario 4: Retrieve Azure URL with specific theme and default type
    url4 = config.format_url("Microsoft_Azure", theme="admins")
    logging.info(f"Scenario 4: Azure URL with specific theme and default type: {url4}")

    # Scenario 5: Update global variables and retrieve S3 URL
    config.update_attribute("global_variables", {"release": "2023-08-01-beta.1"})
    url5 = config.format_url("Amazon_S3")
    logging.info(f"Scenario 5: S3 URL with updated release: {url5}")

    # Scenario 6: Print the entire configuration as a dictionary
    logging.info(f"Scenario 6: Config as dict: {config.to_dict()}")
