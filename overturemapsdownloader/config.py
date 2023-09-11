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

    def format_url(self, url_name, theme=None, type_=None):
        if hasattr(self.urls, url_name.lower()):
            url_template = getattr(self.urls, url_name.lower())
            final_theme = theme if theme else self.global_variables.default_theme
            final_type = type_

            if theme and not type_:
                for theme_item in self.themes:
                    if theme_item.name.lower() == final_theme.lower():
                        final_type = theme_item.types[0] if theme_item.types else None
                        break

            final_type = (
                final_type if final_type else self.global_variables.default_type
            )

            return url_template.format(
                release=self.global_variables.release,
                theme=final_theme,
                type=final_type,
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


# Examples
if __name__ == "__main__":
    config = load_config()
    if config is None:
        logging.warning("Configuration not loaded.")
        exit(1)

    logging.info(config.format_url("Amazon_S3"))
    logging.info(config.format_url("Microsoft_Azure", theme="places"))
