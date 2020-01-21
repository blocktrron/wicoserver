from wicoserver import models
from wicoserver.ucigenerator.network import get_bridge_name

def get_hwmode(channel: int):
    if channel < 14:
        return "11g"
    return "11a"


def generate_wireless_configuration(ap: models.AccessPoint):
    wireless = {"sections": []}
    radios = list(ap.radio_set.all())
    ssids = ap.site.ssid_set.all()
    for radio in radios:
        wireless["sections"].append(generate_radio_configuration(radio))
        for ssid in ssids:
            wireless["sections"].append(generate_vap_configuration(ssid, radio.radio_idx))
    return wireless


def generate_radio_configuration(radio: models.Radio):
    configuration = {"_type": "wifi-device", "_name": "radio" + str(radio.radio_idx), "options": {}}

    configuration["options"]["type"] = "mac80211"
    configuration["options"]["hwmode"] = get_hwmode(radio.channel)
    configuration["options"]["path"] = radio.path
    configuration["options"]["htmode"] = str(models.Radio.HTModes(radio.htmode).label)
    configuration["options"]["country"] = radio.access_point.site.country
    configuration["options"]["channel"] = str(radio.channel)
    configuration["options"]["legacy_rates"] = str(radio.access_point.site.legacy_rates)
    configuration["options"]["disabled"] = "0"
    return configuration


def generate_vap_configuration(ssid : models.SSID, radio_idx : int):
    bridge_name = get_bridge_name(ssid.vlan, ssid.vxlan)
    ifname = bridge_name + str(radio_idx)

    configuration = {"_type": "wifi-iface", "_name": ifname, "options": {}}

    configuration["options"]["mode"] = "ap"
    configuration["options"]["ssid"] = ssid.name
    configuration["options"]["network"] = bridge_name
    configuration["options"]["psk"] = ssid.psk
    configuration["options"]["encryption"] = str(models.SSID.EncryptionMethods(ssid.encryption).label)
    configuration["options"]["device"] = "radio" + str(radio_idx)
    configuration["options"]["disabled"] = "0"
    configuration["options"]["ifname"] = ifname
    return configuration
