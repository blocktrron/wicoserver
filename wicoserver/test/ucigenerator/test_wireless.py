from django.test import TestCase

from wicoserver import models
from wicoserver.ucigenerator import wireless


class WirelessUCIGeneratorTestCase(TestCase):
    def test_generate_vap_configuration(self):
        site = models.Site(name="TestSite")
        site.save()
        ssid = models.SSID(name="WirelessVAP", encryption=models.SSID.EncryptionMethods.WPA2_PSK, psk="psk2psk2")
        ssid.save()
        ssid.sites.add(site)
        ssid.save()

        vap_configuration = wireless.generate_vap_configuration(ssid, 0)
        self.assertEqual("wifi-iface", vap_configuration["_type"])
        self.assertEqual("ap", vap_configuration["options"]["mode"])
        self.assertEqual("WirelessVAP", vap_configuration["options"]["ssid"])
        self.assertEqual("unencap", vap_configuration["options"]["network"])
        self.assertEqual("unencap0", vap_configuration["options"]["ifname"])
        self.assertEqual("0", vap_configuration["options"]["disabled"])
        self.assertEqual("radio0", vap_configuration["options"]["device"])
        self.assertEqual("psk2psk2", vap_configuration["options"]["psk"])
        self.assertEqual("psk2", vap_configuration["options"]["encryption"])

    def test_generate_wireless_configuration(self):
        site = models.Site(name="TestSite", legacy_rates=0, country="DE")
        site.save()

        ap = models.AccessPoint(name="Koala", model="OCEDO Koala", site=site, uplink_port="eth0")
        ap.save()

        radio0 = models.Radio(access_point=ap, radio_idx=0, htmode=models.Radio.HTModes.HT20, min_channel=1, max_channel=13, channel=11, path="pcie1")
        radio0.save()

        radio1 = models.Radio(access_point=ap, radio_idx=1, htmode=models.Radio.HTModes.VHT80, min_channel=36, max_channel=64, channel=40, path="pcie0")
        radio1.save()

        ssid = models.SSID(name="WirelessVAP", encryption=models.SSID.EncryptionMethods.WPA2_PSK, psk="psk2psk2")
        ssid.save()
        ssid.sites.add(site)
        ssid.save()

        wireless_configuration = ap_configuration = wireless.generate_wireless_configuration(ap)
        for section in wireless_configuration["sections"]:
            if section["_name"] == "radio0":
                radio_config = section
                self.assertEqual("wifi-device", radio_config["_type"])
                self.assertEqual("mac80211", radio_config["options"]["type"])
                self.assertEqual("11g", radio_config["options"]["hwmode"])
                self.assertEqual("pcie1", radio_config["options"]["path"])
                self.assertEqual("HT20", radio_config["options"]["htmode"])
                self.assertEqual("DE", radio_config["options"]["country"])
                self.assertEqual("11", radio_config["options"]["channel"])
                self.assertEqual("0", radio_config["options"]["legacy_rates"])
                self.assertEqual("0", radio_config["options"]["disabled"])
            elif section["_name"] == "radio1":
                radio_config = section
                self.assertEqual("wifi-device", radio_config["_type"])
                self.assertEqual("mac80211", radio_config["options"]["type"])
                self.assertEqual("11a", radio_config["options"]["hwmode"])
                self.assertEqual("pcie0", radio_config["options"]["path"])
                self.assertEqual("VHT80", radio_config["options"]["htmode"])
                self.assertEqual("DE", radio_config["options"]["country"])
                self.assertEqual("40", radio_config["options"]["channel"])
                self.assertEqual("0", radio_config["options"]["legacy_rates"])
                self.assertEqual("0", radio_config["options"]["disabled"])
            elif section["_name"] == "unencap0":
                vap_configuration = section
                self.assertEqual("wifi-iface", vap_configuration["_type"])
                self.assertEqual("ap", vap_configuration["options"]["mode"])
                self.assertEqual("WirelessVAP", vap_configuration["options"]["ssid"])
                self.assertEqual("unencap", vap_configuration["options"]["network"])
                self.assertEqual("unencap0", vap_configuration["options"]["ifname"])
                self.assertEqual("0", vap_configuration["options"]["disabled"])
                self.assertEqual("radio0", vap_configuration["options"]["device"])
                self.assertEqual("psk2psk2", vap_configuration["options"]["psk"])
                self.assertEqual("psk2", vap_configuration["options"]["encryption"])
            elif section["_name"] == "unencap1":
                vap_configuration = section
                self.assertEqual("wifi-iface", vap_configuration["_type"])
                self.assertEqual("ap", vap_configuration["options"]["mode"])
                self.assertEqual("WirelessVAP", vap_configuration["options"]["ssid"])
                self.assertEqual("unencap", vap_configuration["options"]["network"])
                self.assertEqual("unencap1", vap_configuration["options"]["ifname"])
                self.assertEqual("0", vap_configuration["options"]["disabled"])
                self.assertEqual("radio1", vap_configuration["options"]["device"])
                self.assertEqual("psk2psk2", vap_configuration["options"]["psk"])
                self.assertEqual("psk2", vap_configuration["options"]["encryption"])
            else:
                self.fail("Unexpected config " + section["_name"])