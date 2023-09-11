from overturemapsdownloader.yaml_helper import read_yaml_file


def get_columns_from_om_schema_yaml(yaml_path):
    columns = []
    schema = read_yaml_file(yaml_path)

    # handle geometry field
    if "geometry" in schema["properties"]:
        columns.append("geometry")

    # handle properties
    if "properties" in schema["properties"]:
        prop_schema = schema["properties"]["properties"]["properties"]

        for k, v in prop_schema.items():
            if "type" in v and v["type"] == "object":
                for sub_k in v["properties"].keys():
                    columns.append(f"{k}.{sub_k}")
            else:
                columns.append(k)

    return columns


if __name__ == "__main__":
    yaml_path = "overturemapsdownloader/schemas/schema/places/place.yaml"
    columns = get_columns_from_om_schema_yaml(yaml_path)
    print("Columns:", columns)
