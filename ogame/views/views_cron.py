from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from django.utils import timezone
from django.utils.html import escape
# from itertools import chain
from django.db.models import Case, When, Value, IntegerField, F
from environ import Env

from ogame.models import Resources, Planets, PlanetsMultiverse, Users, Buildings

# from ogame.functions import saveResources

env = Env()
env.read_env()
CRON_KEY = env("CRON_KEY")

class CronAddResourcesAPIView(APIView):
    def get(self, request):
            key = escape(request.GET['key'])
            if key == CRON_KEY:
                resources_to_update = []
                types = ['metal', 'crystal', 'deuterium']
                users = Users.objects.all()
                for user in users:
                    
                    resources = Resources.objects.filter(users=user).values_list('resource_type', 'resource_value', 'id')
                    resources_player = [{rp[0]: rp[1], 'id': rp[2]} for rp in resources]
                    for resource in resources_player:
                        if 'booster' in resource:
                            booster = resource['booster']
                    # if user.id == 1:
                    #     print(resources_player)
                    buildings = Buildings.objects.filter(users=user).values_list('building_type', 'building_level')
                    buildings_player = {bp[0]: bp[1] for bp in buildings}
                    for resource in resources_player:
                        if 'metal' in resource:
                            resource['metal'] += 2 + 8 * booster * round(30 * buildings_player['metal'] * 1.1 ** buildings_player['metal'] / 60)
                        if 'crystal' in resource:
                            resource['crystal'] += 1 + 8 * booster * round(20 * buildings_player['crystal'] * 1.1 ** buildings_player['crystal'] / 60)
                        if 'deuterium' in resource:
                            resource['deuterium'] += 0 + 8 * booster * round(10 * buildings_player['deuterium'] * 1.1 ** buildings_player['deuterium'] / 60)
                    
                    for resource_player in resources_player:
                        for r_type in types:
                            resource_type, _ = resource_player
                            if r_type == resource_type:
                                    valeur_ressource = resource_player[r_type]
                                    update_condition = When(resource_type=r_type, then=Value(valeur_ressource))

                                    # Créer une instance mise à jour pour chaque utilisateur
                                    updated_instance = Resources(
                                        id=resource_player['id'],
                                        resource_value=Case(update_condition, default=F('resource_value'), output_field=IntegerField())
                                    ) 
                        resources_to_update.append(updated_instance)

                Resources.objects.bulk_update(resources_to_update, ['resource_value'], batch_size=len(resources_to_update))
                # partie planets
                # partie planets multiverse
                          
            return JsonResponse({'msg': 'Ressources ajoutées'})