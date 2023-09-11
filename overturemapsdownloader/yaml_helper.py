# yaml.py
import yaml
import logging

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] %(levelname)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)


def read_yaml_file(filepath):
    try:
        with open(filepath, "r", encoding="utf8") as stream:
            schema_yaml = yaml.safe_load(stream)
            return schema_yaml
    except yaml.YAMLError as exc:
        logging.error(f"Error in reading YAML file {filepath}: {exc}")
        return None
    except FileNotFoundError as fnf_error:
        logging.error(f"File not found: {filepath}")
        return None


def create_yaml_file(filepath, data):
    try:
        with open(filepath, "a", encoding="utf-8") as file:
            yaml.dump(data, file, encoding="utf-8")
    except yaml.YAMLError as exc:
        logging.error(f"Error in writing YAML file {filepath}: {exc}")
        return None
