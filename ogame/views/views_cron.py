from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from django.utils.html import escape
# from itertools import chain
from django.db.models import Case, When, Value, IntegerField, F
from environ import Env
# from datetime import datetime as dt
from django.utils import timezone
from decimal import Decimal

from ogame.models import Resources, Planets, PlanetsMultiverse, Users, Buildings

from ogame.functions import saveResourcesPlayer, saveResourcesPlanets, saveResourcesPlanetsMultiverse

env = Env()
env.read_env()
CRON_KEY = env("CRON_KEY")

class CronAddResourcesAPIView(APIView):
    def get(self, request):
            key = escape(request.GET['key'])
            if key == CRON_KEY:
                types = ['carbon', 'diamond', 'magic']
                users = Users.objects.all()
                resources_to_update_players = []
                for user in users:
                    if user.nature is not None:
                        resources = Resources.objects.filter(users=user).values_list('resource_type', 'resource_value', 'id', 'updated_at')
                        # print(resources)
                        resources_player = [{rp[0]: rp[1], 'id': rp[2]} for rp in resources]
                        updated_at = resources[0][3]
                        # print('updtaed', dt.fromisoformat(updated_at))

                        # print('updtaed', updated_at)
                        # print('tz', timezone.now())

                        # timezone.activate('Europe/Paris')

                        # Obtient l'heure locale actuelle
                        # local_time = timezone.localtime(timezone.now())
                        # print('lt', local_time)
                        # print((timezone.now() - updated_at).total_seconds())
                        # print((local_time - updated_at).total_seconds() > 60.0)
                        if updated_at is not None and (timezone.now() - updated_at).total_seconds() >= 60.0:
                            for resource in resources_player:
                                # print('resource', resource)
                                if 'booster' in resource:
                                    booster = resource['booster']
                            buildings = Buildings.objects.filter(users=user).values_list('building_type', 'building_level')
                            buildings_player = {bp[0]: bp[1] for bp in buildings}
                            for resource in resources_player:
                                if 'carbon' in resource:
                                    resource['carbon'] += 1.2 + 8 * booster * 30 * buildings_player['carbon'] * 1.1 ** buildings_player['carbon'] / 60
                                    # arrondir à 2 décimales
                                    decimal_number = Decimal(resource['carbon'])
                                    resource['carbon'] = '{:.2f}'.format(decimal_number)
                                if 'diamond' in resource:
                                    resource['diamond'] += 0.6 + 8 * booster * 20 * buildings_player['diamond'] * 1.1 ** buildings_player['diamond'] / 60
                                    decimal_number = Decimal(resource['diamond'])
                                    resource['diamond'] = '{:.2f}'.format(decimal_number)
                                if 'magic' in resource:
                                    resource['magic'] += 0 + 8 * booster * 10 * buildings_player['magic'] * 1.1 ** buildings_player['magic'] / 60
                                    decimal_number = Decimal(resource['magic'])
                                    resource['magic'] = '{:.2f}'.format(decimal_number)
                            # print(10 * buildings_player['tritium'] * 1.1 ** buildings_player['tritium'] / 60)
                            # print(booster)
                            resources_to_update = saveResourcesPlayer(types, resources_player)
                            # print('resources_to_update', resources_to_update)
                            for rtu in resources_to_update:
                                resources_to_update_players.append(rtu)
                # print('resources_to_update_players', resources_to_update_players)
                if len(resources_to_update_players) > 0:
                    Resources.objects.bulk_update(resources_to_update_players, ['resource_value'], batch_size=len(resources_to_update_players))
                
                # partie planets
                planets = Planets.objects.all()
                types_planet = [('carbon', 'carbon_level'), ('diamond', 'diamond_level'), ('magic', 'magic_level')]
                for planet in planets:
                    
                    for tp in types_planet:
                        type_resource, level = tp
                        resource_planet_type = getattr(planet, type_resource)
                        level_planet_type = getattr(planet, level)
                        if type_resource == 'carbon':
                            resource_planet_type += round(30 * level_planet_type * 1.1 ** level_planet_type / 60)
                        if type_resource == 'diamond':
                            resource_planet_type += round(20 * level_planet_type * 1.1 ** level_planet_type / 60)
                        if type_resource == 'magic':
                            resource_planet_type += round(10 * level_planet_type * 1.1 ** level_planet_type / 60)
                        setattr(planet, type_resource, resource_planet_type) 
                for _ in types:
                    resources_planets = [{'carbon': rp.carbon, 'diamond': rp.diamond, 'magic': rp.magic, 'id': rp.id} for rp in planets]

                resources_planets_to_update = saveResourcesPlanets(resources_planets)

                Planets.objects.bulk_update(resources_planets_to_update, ['carbon', 'diamond', 'magic'], batch_size=len(resources_planets_to_update))
                

                # partie planets multiverse
                planets_multiverse = PlanetsMultiverse.objects.all()
                types_planet_multiverse = [('carbon', 'carbon_level'), ('diamond', 'diamond_level'), ('magic', 'magic_level')]
                for planet_multiverse in planets_multiverse:
                    
                    for tpm in types_planet_multiverse:
                        type_resource, level = tpm
                        resource_planet_multiverse_type = getattr(planet_multiverse, type_resource)
                        level_planet_multiverse_type = getattr(planet_multiverse, level)
                        if type_resource == 'carbon':
                            resource_planet_multiverse_type += round(30 * level_planet_multiverse_type * 1.1 ** level_planet_multiverse_type / 60)
                        if type_resource == 'diamond':
                            resource_planet_multiverse_type += round(20 * level_planet_multiverse_type * 1.1 ** level_planet_multiverse_type / 60)
                        if type_resource == 'magic':
                            resource_planet_multiverse_type += round(10 * level_planet_multiverse_type * 1.1 ** level_planet_multiverse_type / 60)
                        setattr(planet_multiverse, type_resource, resource_planet_multiverse_type) 
                for _ in types:
                    resources_planets_multiverse = [{'carbon': rpm.carbon, 'diamond': rpm.diamond, 'magic': rpm.magic, 'id': rpm.id} for rpm in planets_multiverse]

                resources_planets_multiverse_to_update = saveResourcesPlanetsMultiverse(resources_planets_multiverse)

                PlanetsMultiverse.objects.bulk_update(resources_planets_multiverse_to_update, ['carbon', 'diamond', 'magic'], batch_size=len(resources_planets_multiverse_to_update))
                
                          
            return JsonResponse({'msg': 'Ressources ajoutées'})