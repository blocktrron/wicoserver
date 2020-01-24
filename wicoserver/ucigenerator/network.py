import socket
import struct
from ipaddress import IPv4Network
from typing import List

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
    ap_interfaces = filter(lambda ipaddress: ipaddress.vlan is not None or ipaddress.vxlan is not None,
                           ap.ipaddress_set.all())
    bridges += [(network.vlan, network.vxlan) for network in ap_interfaces]

    # Don't forget our precious management network
    mgmt_vlan = ap.site.mgmt_vlan
    mgmt_vxlan = ap.site.mgmt_vxlan
    bridges.append((mgmt_vlan, mgmt_vxlan))

    # Distinct list
    bridges = list(set(bridges))

    management_bridge = get_bridge_name(mgmt_vlan, mgmt_vxlan)

    for bridge in bridges:
        network["sections"].append(generate_vlan_bridge_configuration(bridge[0], ap.uplink_port))

    network["sections"] += generate_management_interface_config(ap)

    return network


def generate_ipv6_management_interface_config(ipaddresses: List[models.IPAddress]):
    i = 0
    configurations = []
    for ipaddress in ipaddresses:
        configuration = {"_type": "interface", "_name": "mgmt6_" + str(i), "options": {}}
        if ipaddress.vlan is None and ipaddress.vxlan is None:
            configuration["options"]["ifname"] = "br-" + get_bridge_name(ipaddress.ap.site.mgmt_vlan,
                                                                         ipaddress.ap.site.mgmt_vxlan)
        else:
            configuration["options"]["ifname"] = "br-" + get_bridge_name(ipaddress.vlan, ipaddress.vxlan)
        configuration["options"]["auto"] = "1"
        if ipaddress.dhcp:
            configuration["options"]["proto"] = "dhcpv6"
        else:
            configuration["options"]["proto"] = "static"
            configuration["options"]["ip6addr"] = ipaddress.address + "/" + str(ipaddress.subnet)
            configuration["options"]["ip6gw"] = ipaddress.gateway
            configuration["options"]["dns"] = ipaddress.dns
        configurations.append(configuration)
        i = i + 1

    return configurations


def generate_ipv4_management_interface_config(ipaddresses: List[models.IPAddress]):
    i = 0
    configurations = []
    for ipaddress in ipaddresses:
        configuration = {"_type": "interface", "_name": "mgmt4_" + str(i), "options": {}}
        if ipaddress.vlan is None and ipaddress.vxlan is None:
            configuration["options"]["ifname"] = "br-" + get_bridge_name(ipaddress.ap.site.mgmt_vlan,
                                                                         ipaddress.ap.site.mgmt_vxlan)
        else:
            configuration["options"]["ifname"] = "br-" + get_bridge_name(ipaddress.vlan, ipaddress.vxlan)
        configuration["options"]["auto"] = "1"
        if ipaddress.dhcp:
            configuration["options"]["proto"] = "dhcp"
        else:
            configuration["options"]["proto"] = "static"
            configuration["options"]["ipaddr"] = ipaddress.address
            configuration["options"]["netmask"] = socket.inet_ntoa(
                struct.pack(">I", (0xffffffff << (32 - int(ipaddress.subnet))) & 0xffffffff))
            configuration["options"]["gateway"] = ipaddress.gateway
            configuration["options"]["dns"] = ipaddress.dns
        configurations.append(configuration)
        i = i + 1

    return configurations


def generate_management_interface_config(ap: models.AccessPoint):
    ip4addresses = list(filter(lambda ip: ip.version == 4, ap.ipaddress_set.all()))
    ip6addresses = list(filter(lambda ip: ip.version == 6, ap.ipaddress_set.all()))

    interface_config = []
    interface_config += generate_ipv4_management_interface_config(ip4addresses)
    interface_config += generate_ipv6_management_interface_config(ip6addresses)

    return interface_config


def generate_vlan_bridge_configuration(vlan: str, uplink_port: str):
    configuration = {"_type": "interface", "_name": get_bridge_name(vlan, None), "options": {}}
    configuration["options"]["type"] = "bridge"
    configuration["options"]["ifname"] = uplink_port if vlan is None else str(uplink_port) + "." + str(vlan)
    configuration["options"]["auto"] = "1"
    configuration["options"]["proto"] = "none"

    return configuration
