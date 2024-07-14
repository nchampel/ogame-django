from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from django.utils import timezone
from collections import defaultdict
from environ import Env

from ogame.models import Resources, Buildings, BuildingsResources, Boosters, \
Planets, PlanetsMultiverse, Starship, Logs

from ogame.serializers import ResourcesSerializer, BuildingsSerializer

from ogame.functions import authenticate

env = Env()
env.read_env()
USER_ID = int(env("USER_ID"))

class SalutAPIView(APIView):
    def get(self, request):
        try :
            return JsonResponse({'msg': 'Hourra !!!!!!!!!'})
        except:
            content = {
                'msg': 'Erreur lors de la récupération des ressources'
            }
            return Response(content, status=status.HTTP_400_BAD_REQUEST)

class GetResourcesAPIView(APIView):
    def post(self, request):
        user_id = authenticate(request)
        try :
            # courses_id = escape(request.data['courses_id'])
            resources = Resources.objects.filter(users_id=user_id)

            resources_values = {'carbon': 0, 'diamond': 0, 'magic': 0, 'power_generator': 0, 'booster': 1}

            for resource in resources:
                resources_values[resource.resource_type] = resource.resource_value
            return JsonResponse({'carbon': resources_values['carbon'],
                                 'diamond': resources_values['diamond'],
                                 'magic': resources_values['magic'],
                                 'power_generator': resources_values['power_generator'],
                                 'booster': resources_values['booster'],
                                 })
            serializer = ResourcesSerializer(resource).data

            return JsonResponse(serializer)
        except:
            content = {
                'msg': 'Erreur lors de la récupération des ressources'
            }
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
        
class SaveResourcesAPIView(APIView):
    def post(self, request):
        user_id = authenticate(request)
        try :
            resources = request.data['resources']
            # print(resources)
            for key, value in resources.items():
                # print(key, value)
                Resources.objects.filter(users_id=user_id, resource_type=key).update(resource_value=value, updated_at=timezone.now())
            # Resources.objects.filter(users_id=user_id).update(metal=resources['metal'],
            #                             crystal=resources['crystal'], tritium=resources['tritium'],
            #                             satellites=resources['satellites'])
            # resources_values = {'metal': resource.metal}

            return JsonResponse({'msg': 'Ressources sauvegardées'})
        except:
            content = {
                'msg': 'Erreur lors de la sauvegarde des ressources'
            }
            return Response(content, status=status.HTTP_400_BAD_REQUEST)

class GetBuildingsAPIView(APIView):
    def post(self, request):
        user_id = authenticate(request)
        try :
            # courses_id = escape(request.data['courses_id'])
            buildings = Buildings.objects.filter(users_id=user_id)
            
            building_levels = {'carbon': 0, 'diamond': 0, 'magic': 0, 'energy': 0,
                               'unity-link_generator': 0, 'ticket_generator': 0,'protective_dome': 0}

            for building in buildings:
                building_levels[building.building_type] = building.building_level
            return JsonResponse({'carbon': building_levels['carbon'],
                                    'diamond': building_levels['diamond'],
                                    'magic': building_levels['magic'],
                                    'energy': building_levels['energy'],
                                    'unity-link_generator': building_levels['unity-link_generator'],
                                    'ticket_generator': building_levels['ticket_generator'],
                                    'protective_dome': building_levels['protective_dome'],
                                     })

            # buildings = Buildings.objects.filter(users_id=user_id)
            # serializer = BuildingsSerializer(buildings, many=True).data

            # return JsonResponse(serializer, safe=False)
        
            buildings = Buildings.objects.filter(users_id=user_id).values('building_type', 'building_level')
            

            building_levels = defaultdict(int)

            for building in buildings:
                building_levels[building['building_type']] = building['building_level']
            return JsonResponse(building_levels)
        except:
            content = {
                'msg': 'Erreur lors de la récupération des niveaux des bâtiments'
            }
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
        
# pas utilisé
class GetBuildingsResourcesAPIView(APIView):
    def post(self, request):
        user_id = authenticate(request)
        try :
            # courses_id = escape(request.data['courses_id'])
            types = ['carbon', 'diamond', 'magic', 'energy']

            # Obtenez toutes les valeurs des ressources pour les types spécifiés en une seule requête
            buildings_resources_values = BuildingsResources.objects.filter(type__in=types)

            # Initialisez la liste résultante
            buildings_resources_values_all = []

            # Parcourez les types et les valeurs des ressources correspondantes
            for t in types:
                # Trouvez la valeur correspondante dans la liste filtrée
                building_resources_values = next((brv for brv in buildings_resources_values if brv.type == t), None)
                
                # Ajoutez la valeur à la liste résultante
                buildings_resources_values_all.append({t: {'carbon': building_resources_values.carbon,
                                'diamond': building_resources_values.diamond,
                                'magic': building_resources_values.magic,
                                'energy': building_resources_values.energy,
                                'resource_to_add': building_resources_values.resource_to_add,}})


            return Response(buildings_resources_values_all)
        except:
            content = {
                'msg': 'Erreur lors de la récupération des ressources des bâtiments'
            }
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
        
class SaveLevelAPIView(APIView):
    def post(self, request):
        user_id = authenticate(request)
        try :
            type = request.data['type']
            level = request.data['level']
            Buildings.objects.filter(users_id=user_id, building_type=type).update(building_level=level)
            # resources_values = {'metal': resource.metal}

            buildings_names = {
                'carbon': "Synthétiseur de carbone",
                'diamond': "Raffinerie de diamants",
                'magic': "Extracteur de magie",
                'energy': "Génératrice d'énergie",
                'protective_dome': "Dôme protecteur"
            }

            description = "Bâtiment " + buildings_names[type] + " niveau " + str(level) + " obtenu"

            Logs.objects.create(type='planète', category='bâtiments', users_id=user_id, description=description, target=user_id, created_at=timezone.now())

            return JsonResponse({'msg': 'Ressources ajoutées'})
        except:
            content = {
                'msg': 'Erreur lors de l\'ajout des ressources'
            }
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
        
class GetBoosterCostAPIView(APIView):
    def post(self, request):
        user_id = authenticate(request)
        try :
            coefficient = request.data['coefficient']
            cost = Boosters.objects.filter(coefficient=coefficient).first().cost

            return Response(cost)
        except:
            content = {
                'msg': 'Erreur lors de la récupération du coût du booster'
            }
            return Response(content, status=status.HTTP_400_BAD_REQUEST)

class SaveBoosterCoefficientAPIView(APIView):
    def post(self, request):
        user_id = authenticate(request)
        try :
            coefficient = request.data['coefficient']
            t = Resources.objects.filter(users_id=user_id, resource_type='booster').update(resource_value=coefficient)
            booster = Boosters.objects.filter(coefficient=coefficient).first()

            description = "Booster niveau " + str(coefficient) + " obtenu"

            Logs.objects.create(type='planète', category='ressources', users_id=user_id, description=description, target=user_id, created_at=timezone.now())

            return JsonResponse({'coefficient': coefficient, 'cost': booster.cost})
        except:
            content = {
                'msg': 'Erreur lors de la sauvegarde du niveau du booster'
            }
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
        
class ReinitializationAPIView(APIView):
    def post(self, request):
        user_id = authenticate(request)
        try :
            user_id = request.data['user_id']
            Buildings.objects.filter(user_id=user_id).update(building_level=0,
                                                            created_at=timezone.now())
            # à tester
            resources_start = {'carbon': 1000, 'diamond': 1000, 'magic': 0,
                               'power_generator': 0, 'booster': 1}
            for key, value in resources_start.items():

                Resources.objects.filter(user_id=user_id, resource_type=key).update(resource_value=value, created_at=timezone.now())
            Planets.objects.filter(user_id=user_id).update(carbon=0, diamond=0, magic=0)
            PlanetsMultiverse.objects.filter(user_id=user_id).update(carbon=0, diamond=0, magic=0,
                                                                     is_discovered=0)
            Starship.objects.filter(user_id=user_id).update(is_built=0, fight_exp=0)
            

            return JsonResponse({'msg': 'Réinitialisation réussie'})
        except:
            content = {
                'msg': 'Erreur lors de la réinitialisation'
            }
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
        
