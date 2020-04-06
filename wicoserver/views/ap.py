from rest_framework.decorators import api_view
from rest_framework.response import Response

from wicoserver import models


@api_view(["POST"])
def subscribe_access_point(request):
    token = request.data["token"]
    model = request.data["model"]
    mac_address = request.data["mac_address"]

    existing_ap = models.AccessPoint.objects.filter(mac_address=mac_address).first()
    if existing_ap is not None:
        if existing_ap.subscribed == True:
            return Response(status=409)
        existing_ap.delete()

    models.AccessPoint.create_from_subscription_request(model=model, mac_address=mac_address, token=token)
    return Response(status=201)


@api_view()
def get_access_point_subscription_state(request, token):
    existing_ap = models.AccessPoint.objects.filter(token=token).first()

    if existing_ap is None:
        return Response(status=404)

    return Response({"subscribed": existing_ap.subscribed})