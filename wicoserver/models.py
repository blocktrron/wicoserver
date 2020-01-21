from django.db import models
from django.utils.translation import gettext_lazy


class Site(models.Model):
    name = models.CharField(max_length=100)
    # Encapsulation for management traffic
    mgmt_vxlan = models.CharField(null=True, max_length=128)
    mgmt_vlan = models.IntegerField(null=True)
    country = models.CharField(max_length=2)
    legacy_rates = models.BooleanField(default=True)


class Location(models.Model):
    latitude = models.FloatField()
    longitude = models.FloatField()


class AccessPoint(models.Model):
    name = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    location = models.ForeignKey(to=Location, on_delete=models.SET_NULL, null=True)
    site = models.ForeignKey(to=Site, on_delete=models.SET_NULL, null=True)
    uplink_port = models.CharField(max_length=16)


class Radio(models.Model):
    class HTModes(models.TextChoices):
        HT20 = 'H2', gettext_lazy('HT20')
        HT40 = 'H4', gettext_lazy('HT40')
        VHT20 = 'V2', gettext_lazy('VHT20')
        VHT40 = 'V4', gettext_lazy('VHT40')
        VHT80 = 'V8', gettext_lazy('VHT80')

    access_point = models.ForeignKey(to=AccessPoint, on_delete=models.CASCADE)
    radio_idx = models.IntegerField()
    htmode = models.CharField(max_length=2, choices=HTModes.choices)
    channel = models.IntegerField()
    path = models.CharField(max_length=32)
    min_channel = models.IntegerField()
    max_channel = models.IntegerField()


class SSID(models.Model):
    class EncryptionMethods(models.TextChoices):
        WPA2_PSK = 'P2', gettext_lazy('psk2')
        WPA3_PSK = 'P3', gettext_lazy('psk3')

    name = models.CharField(max_length=32)
    vxlan = models.CharField(null=True, max_length=128)
    vlan = models.IntegerField(null=True)
    sites = models.ManyToManyField(Site)
    encryption = models.CharField(max_length=2, choices=EncryptionMethods.choices)
    psk = models.CharField(max_length=64)


class SSHKey(models.Model):
    name = models.CharField(max_length=128)
    key = models.CharField(max_length=1024)
