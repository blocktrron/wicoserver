from django.test import TestCase

from wicoserver import models
from wicoserver.ucigenerator import network


class NetworkUCIGeneratorTestCase(TestCase):
    def test_generate_network_configuration(self):
        site = models.Site(name="TestSite", legacy_rates=0, country="DE")
        site.save()

        ap = models.AccessPoint(name="Koala", model="OCEDO Koala", site=site, uplink_port="eth0")
        ap.save()

        radio0 = models.Radio(access_point=ap, radio_idx=0, htmode=models.Radio.HTModes.HT20, min_channel=1,
                              max_channel=13, channel=11, path="pcie1")
        radio0.save()

        radio1 = models.Radio(access_point=ap, radio_idx=1, htmode=models.Radio.HTModes.VHT80, min_channel=36,
                              max_channel=64, channel=40, path="pcie0")
        radio1.save()

        ssid = models.SSID(name="WirelessVAP", encryption=models.SSID.EncryptionMethods.WPA2_PSK, psk="psk2psk2")
        ssid.save()
        ssid.sites.add(site)
        ssid.save()

        network_configuration = network.generate_network_configuration(ap)

        self.assertEqual(1, len(network_configuration["sections"]))
        unencap = network_configuration["sections"][0]
        self.assertEqual("bridge", unencap["_type"])
        self.assertEqual("unencap", unencap["_name"])
        self.assertEqual(3, len(unencap["options"]))
        self.assertEqual(ap.uplink_port, unencap["options"]["ifname"])
        self.assertEqual("1", unencap["options"]["auto"])
