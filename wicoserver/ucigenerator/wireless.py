from wicoserver import models
from wicoserver.ucigenerator.network import get_bridge_name


def generate_wireless_configuration(ap: models.AccessPoint):
    radios = list(ap.radio_set.all())
    ssids = ap.site.ssid_set.all()


def generate_vap_configuration(ssid : models.SSID, radio_idx : int):
    configuration = {"_type": "wifi-iface", "options": {}}
    configuration["options"]["mode"] = "ap"
    configuration["options"]["ssid"] = ssid.name
    configuration["options"]["network"] = get_bridge_name(ssid.vlan, ssid.vxlan)
    configuration["options"]["psk"] = ssid.psk
    configuration["options"]["encryption"] = ssid.encryption[0]
