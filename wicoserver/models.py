from django.db import models
from django.utils.translation import gettext_lazy


class Site(models.Model):
    name = models.CharField(max_length=100)
    # Encapsulation for management traffic
    mgmt_vxlan = models.CharField(null=True, max_length=128)
    mgmt_vlan = models.IntegerField(null=True)


class Location(models.Model):
    latitude = models.FloatField()
    longitude = models.FloatField()


class AccessPoint(models.Model):
    name = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    location = models.ForeignKey(to=Location, on_delete=models.SET_NULL)
    site = models.ForeignKey(to=Site, on_delete=models.SET_NULL)
    uplink_port = models.CharField(max_length=16)


class Radio(models.Model):
    access_point = models.ForeignKey(to=AccessPoint, on_delete=models.SET_NULL)
    min_channel = models.IntegerField()
    max_channel = models.IntegerField()


class SSID(models.Model):
    class EncryptionMethods(models.TextChoices):
        WPA2_PSK = 'P2', gettext_lazy('psk2')

    name = models.CharField(max_length=32)
    vxlan = models.CharField(null=True, max_length=128)
    vlan = models.IntegerField(null=True)
    sites = models.ManyToManyField(Site)
    encryption = models.CharField(max_length=2, choices=EncryptionMethods.choices)
    psk = models.CharField(max_length=64)


class SSHKey(models.Model):
    name = models.CharField(max_length=128)
    key = models.CharField(max_length=1024)
