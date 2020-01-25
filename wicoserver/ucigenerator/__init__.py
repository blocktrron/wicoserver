def generate_uci_file(settings: dict):
    output = ""
    for section in settings["sections"]:
        output += "config {config_type} '{name}'\n".format(config_type=section["_type"], name=section["_name"])
        for name, value in section["options"].items():
            if type(value) == list:
                for element in value:
                    output += "\tlist {name} '{value}'\n".format(name=name, value=element)
            else:
                output += "\toption {name} '{value}'\n".format(name=name, value=value)
        output += "\n"
    return output
