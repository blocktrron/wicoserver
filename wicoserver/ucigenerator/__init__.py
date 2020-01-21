def generate_uci_file(settings: dict):
    output = str()
    for section in settings["sections"]:
        output + "config {config_type} '{name}'".format(config_type=section["_type"], name=section["_name"])
        for name, value in section["options"]:
            if type(value) == list:
                for element in value:
                    output + "\tlist {name} '{value}'".format(name=name, value=element)
            else:
                output + "\toption {name} '{value}'".format(name=name, value=value)
    return output
