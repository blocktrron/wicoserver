from wicoserver import models


def get_bridge_name(vlan: int, vxlan: str = None):
    if vlan is None and vxlan is None:
        return "unencap"
    if vxlan is None:
        return "v" + str(vlan)
    if vlan is None:
        return "vx" + str(vxlan)
    return "v" + str(vlan) + "vx" + str(vxlan)


def generate_network_configuration(ap: models.AccessPoint):
    network = {"sections": []}

    # First we need to get all used VLANs.
    bridges = [(ssid.vlan, ssid.vxlan) for ssid in ap.site.ssid_set.all()]

    # Don't forget our precious management network
    mgmt_vlan = ap.site.mgmt_vlan
    mgmt_vxlan = ap.site.mgmt_vxlan
    bridges.append((mgmt_vlan, mgmt_vxlan))

    # Distinct list
    bridges = list(set(bridges))

    management_bridge = get_bridge_name(mgmt_vlan, mgmt_vxlan)

    for bridge in bridges:
        network["sections"].append(generate_vlan_bridge_configuration(bridge[0], ap.uplink_port))

    return network


def generate_vlan_bridge_configuration(vlan: str, uplink_port: str):
    configuration = {"_type": "bridge", "_name": get_bridge_name(vlan, None), "options": {}}
    configuration["options"]["type"] = "bridge"
    configuration["options"]["ifname"] = uplink_port if vlan is None else uplink_port + "." + vlan
    configuration["options"]["auto"] = "1"

    return configuration
