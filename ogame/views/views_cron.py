from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from django.utils import timezone
from django.utils.html import escape
from environ import Env

from ogame.models import Resources, Planets, PlanetsMultiverse, Users, Buildings

env = Env()
env.read_env()
CRON_KEY = int(env("CRON_KEY"))

class CronAddResourcesAPIView(APIView):
    def get(self, request):
            key = escape(request.GET['key'])
            if key == CRON_KEY:
                types = ['metal', 'crystal', 'deuterium']
                users = Users.objects.all()
                for user in users:
                    resources = Resources.objects.filter(user=user).values('resource_type', 'resource_value')
                    resources_player = list(resources)
                    # resources_player = []
                    # for resource in resources:
                    #      resources_player.append({resource.resource_type: resource.resource_value})
                    buildings = Buildings.objects.filter(user=user).values('building_type', 'building_level')
                    buildings_player = list(buildings)
                    for type in types:
                        if type == resources_player['resource_type']
                        resource_value_player = Resources.objects.filter(user=user, resource_type=type).first().resource_value
                # partie planets
                # partie planets multiverse
                          
            return JsonResponse({'msg': 'Ressources ajoutées'})