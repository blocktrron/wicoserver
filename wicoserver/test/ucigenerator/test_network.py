from django.test import TestCase

from wicoserver import models
from wicoserver.ucigenerator import network, generate_uci_file


class NetworkUCIGeneratorTestCase(TestCase):
    def test_generate_network_configuration(self):
        site = models.Site(name="TestSite", legacy_rates=0, country="DE")
        site.save()

        ap = models.AccessPoint(name="Koala", model="OCEDO Koala", site=site, uplink_port="eth0")
        ap.save()

        ip4address = models.IPAddress(address="192.168.1.10", subnet="24", gateway="192.168.1.1", dns="192.168.1.1",
                                      vlan=10, ap=ap, version=4, dhcp=False)
        ip4address.save()

        ip6address = models.IPAddress(address="fd00::2", subnet="64", gateway="fd00::1", dns="fd00::1",
                                      vlan=10, ap=ap, version=6, dhcp=False)
        ip6address.save()

        radio0 = models.Radio(access_point=ap, radio_idx=0, htmode=models.Radio.HTModes.HT20, min_channel=1,
                              max_channel=13, channel=11, path="pcie1")
        radio0.save()

        radio1 = models.Radio(access_point=ap, radio_idx=1, htmode=models.Radio.HTModes.VHT80, min_channel=36,
                              max_channel=64, channel=40, path="pcie0")
        radio1.save()

        ssid = models.SSID(name="WirelessVAP", encryption=models.SSID.EncryptionMethods.WPA2_PSK, psk="psk2psk2", vlan=100)
        ssid.save()
        ssid.sites.add(site)
        ssid.save()

        network_configuration = network.generate_network_configuration(ap)

        self.assertEqual(5, len(network_configuration["sections"]))
        for section in network_configuration["sections"]:
            if section["_name"] == "unencap":
                self.assertEqual("interface", section["_type"])
                self.assertEqual(4, len(section["options"]))
                self.assertEqual(ap.uplink_port, section["options"]["ifname"])
                self.assertEqual("1", section["options"]["auto"])
                self.assertEqual("none", section["options"]["proto"])
            elif section["_name"] == "v100":
                self.assertEqual("interface", section["_type"])
                self.assertEqual(4, len(section["options"]))
                self.assertEqual(ap.uplink_port + ".100", section["options"]["ifname"])
                self.assertEqual("1", section["options"]["auto"])
                self.assertEqual("none", section["options"]["proto"])
            elif section["_name"] == "v10":
                self.assertEqual("interface", section["_type"])
                self.assertEqual(4, len(section["options"]))
                self.assertEqual(ap.uplink_port + ".10", section["options"]["ifname"])
                self.assertEqual("1", section["options"]["auto"])
                self.assertEqual("none", section["options"]["proto"])
            elif section["_name"] == "mgmt4_0":
                self.assertEqual("interface", section["_type"])
                self.assertEqual(7, len(section["options"]))
                self.assertEqual("static", section["options"]["proto"])
                self.assertEqual("1", section["options"]["auto"])
                self.assertEqual("192.168.1.1", section["options"]["dns"])
                self.assertEqual("192.168.1.1", section["options"]["gateway"])
                self.assertEqual("192.168.1.10", section["options"]["ipaddr"])
                self.assertEqual("255.255.255.0", section["options"]["netmask"])
                self.assertEqual("br-v10", section["options"]["ifname"])
            elif section["_name"] == "mgmt6_0":
                self.assertEqual("interface", section["_type"])
                self.assertEqual(6, len(section["options"]))
                self.assertEqual("static", section["options"]["proto"])
                self.assertEqual("1", section["options"]["auto"])
                self.assertEqual("fd00::1", section["options"]["dns"])
                self.assertEqual("fd00::1", section["options"]["ip6gw"])
                self.assertEqual("fd00::2/64", section["options"]["ip6addr"])
                self.assertEqual("br-v10", section["options"]["ifname"])
            else:
                self.fail("Unknown section " + section["_name"])
        uci = generate_uci_file(network_configuration)
        print(uci)