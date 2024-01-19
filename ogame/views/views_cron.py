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

from ogame.functions import saveResourcesPlayer, saveResourcesPlanets, saveResourcesPlanetsMultiverse

env = Env()
env.read_env()
CRON_KEY = env("CRON_KEY")

class CronAddResourcesAPIView(APIView):
    def get(self, request):
            key = escape(request.GET['key'])
            if key == CRON_KEY:
                types = ['metal', 'crystal', 'deuterium']
                users = Users.objects.all()
                for user in users:
                    
                    resources = Resources.objects.filter(users=user).values_list('resource_type', 'resource_value', 'id')
                    resources_player = [{rp[0]: rp[1], 'id': rp[2]} for rp in resources]
                    for resource in resources_player:
                        if 'booster' in resource:
                            booster = resource['booster']
                    buildings = Buildings.objects.filter(users=user).values_list('building_type', 'building_level')
                    buildings_player = {bp[0]: bp[1] for bp in buildings}
                    for resource in resources_player:
                        if 'metal' in resource:
                            resource['metal'] += 2 + 8 * booster * round(30 * buildings_player['metal'] * 1.1 ** buildings_player['metal'] / 60)
                        if 'crystal' in resource:
                            resource['crystal'] += 1 + 8 * booster * round(20 * buildings_player['crystal'] * 1.1 ** buildings_player['crystal'] / 60)
                        if 'deuterium' in resource:
                            resource['deuterium'] += 0 + 8 * booster * round(10 * buildings_player['deuterium'] * 1.1 ** buildings_player['deuterium'] / 60)
                    
                resources_to_update = saveResourcesPlayer(types, resources_player)

                Resources.objects.bulk_update(resources_to_update, ['resource_value'], batch_size=len(resources_to_update))
                
                # partie planets
                planets = Planets.objects.all()
                types_planet = [('metal', 'metal_level'), ('crystal', 'crystal_level'), ('deuterium', 'deuterium_level')]
                for planet in planets:
                    
                    for tp in types_planet:
                        type, level = tp
                        resource_planet_type = getattr(planet, type)
                        level_planet_type = getattr(planet, level)
                        if type == 'metal':
                            resource_planet_type += round(30 * level_planet_type * 1.1 ** level_planet_type / 60)
                        if type == 'crystal':
                            resource_planet_type += round(20 * level_planet_type * 1.1 ** level_planet_type / 60)
                        if type == 'deuterium':
                            resource_planet_type += round(10 * level_planet_type * 1.1 ** level_planet_type / 60)
                        setattr(planet, type, resource_planet_type) 
                for type in types:
                    resources_planets = [{'metal': rp.metal, 'crystal': rp.crystal, 'deuterium': rp.deuterium, 'id': rp.id} for rp in planets]

                resources_planets_to_update = saveResourcesPlanets(resources_planets)

                Planets.objects.bulk_update(resources_planets_to_update, ['metal', 'crystal', 'deuterium'], batch_size=len(resources_planets_to_update))
                

                # partie planets multiverse
                planets_multiverse = PlanetsMultiverse.objects.all()
                types_planet_multiverse = [('metal', 'metal_level'), ('crystal', 'crystal_level'), ('deuterium', 'deuterium_level')]
                for planet_multiverse in planets_multiverse:
                    
                    for tpm in types_planet_multiverse:
                        type, level = tpm
                        resource_planet_multiverse_type = getattr(planet_multiverse, type)
                        level_planet_multiverse_type = getattr(planet_multiverse, level)
                        if type == 'metal':
                            resource_planet_multiverse_type += round(30 * level_planet_multiverse_type * 1.1 ** level_planet_multiverse_type / 60)
                        if type == 'crystal':
                            resource_planet_multiverse_type += round(20 * level_planet_multiverse_type * 1.1 ** level_planet_multiverse_type / 60)
                        if type == 'deuterium':
                            resource_planet_multiverse_type += round(10 * level_planet_multiverse_type * 1.1 ** level_planet_multiverse_type / 60)
                        setattr(planet_multiverse, type, resource_planet_multiverse_type) 
                for type in types:
                    resources_planets_multiverse = [{'metal': rpm.metal, 'crystal': rpm.crystal, 'deuterium': rpm.deuterium, 'id': rpm.id} for rpm in planets_multiverse]

                resources_planets_multiverse_to_update = saveResourcesPlanetsMultiverse(resources_planets_multiverse)

                PlanetsMultiverse.objects.bulk_update(resources_planets_multiverse_to_update, ['metal', 'crystal', 'deuterium'], batch_size=len(resources_planets_multiverse_to_update))
                
                          
            return JsonResponse({'msg': 'Ressources ajoutées'})