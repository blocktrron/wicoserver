from wicoserver import models


def get_bridge_name(vlan: int, vxlan: str = None):
    if vlan is None and vxlan is None:
        return "unencap"
    if vxlan is None:
        return "v" + vlan
    if vlan is None:
        return "vx" + vxlan
    return "v" + vlan + "vx" + vxlan


def generate_network_configuration(ap: models.AccessPoint):


def generate_bridge_configuration(name: str, uplink_port: str):
    configuration = {"_type": "bridge", "_name": name, "options": {}}
    configuration["options"]["type"] = "bridge"
    configuration["options"]["ifname"] = uplink_port
    configuration["options"]["auto"] = "1"
    configuration["options"][""]