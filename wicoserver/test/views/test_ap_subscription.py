from django.test import TestCase

from wicoserver import models


class APSubscriptionTestCase(TestCase):
    VALID_TEST_DATA = {
        "mac_address": "AA:BB:CC:DD:EE:FF",
        "model": "OCEDO Koala",
        "token": "d0d70149369b5bef6819c3e58ce5ac3db0978a930786370d06fbf2d3333d398d"
    }

    def test_ap_subscription_should_succeed_on_correct_request(self):
        response = self.client.post("/ap/subscribe", self.VALID_TEST_DATA)
        self.assertEqual(201, response.status_code)
        self.assertEqual(1, len(models.AccessPoint.objects.all()))
        self.assertEqual(self.VALID_TEST_DATA["mac_address"], models.AccessPoint.objects.first().mac_address)
        self.assertEqual(self.VALID_TEST_DATA["model"], models.AccessPoint.objects.first().model)
        self.assertEqual(self.VALID_TEST_DATA["token"], models.AccessPoint.objects.first().token)

    def test_ap_subscription_should_allow_resubscription_if_not_subscribed(self):
        response = self.client.post("/ap/subscribe", self.VALID_TEST_DATA)
        self.assertEqual(201, response.status_code)
        self.assertEqual(1, len(models.AccessPoint.objects.all()))
        self.assertEqual(self.VALID_TEST_DATA["mac_address"], models.AccessPoint.objects.first().mac_address)
        self.assertEqual(self.VALID_TEST_DATA["model"], models.AccessPoint.objects.first().model)
        self.assertEqual(self.VALID_TEST_DATA["token"], models.AccessPoint.objects.first().token)

        new_data = self.VALID_TEST_DATA
        new_data["token"] = "NEW_TOKEN"

        response2 = self.client.post("/ap/subscribe", new_data)
        self.assertEqual(201, response2.status_code)
        self.assertEqual(1, len(models.AccessPoint.objects.all()))
        self.assertEqual(new_data["mac_address"], models.AccessPoint.objects.first().mac_address)
        self.assertEqual(new_data["model"], models.AccessPoint.objects.first().model)
        self.assertEqual(new_data["token"], models.AccessPoint.objects.first().token)


    def test_ap_subscription_should_allow_resubscription_if_not_subscribed(self):
        response = self.client.post("/ap/subscribe", self.VALID_TEST_DATA)
        self.assertEqual(201, response.status_code)
        self.assertEqual(1, len(models.AccessPoint.objects.all()))
        self.assertEqual(self.VALID_TEST_DATA["mac_address"], models.AccessPoint.objects.first().mac_address)
        self.assertEqual(self.VALID_TEST_DATA["model"], models.AccessPoint.objects.first().model)
        self.assertEqual(self.VALID_TEST_DATA["token"], models.AccessPoint.objects.first().token)

        ap = models.AccessPoint.objects.first()
        ap.subscribed = True
        ap.save()

        response2 = self.client.post("/ap/subscribe", self.VALID_TEST_DATA)
        self.assertEqual(409, response2.status_code)
