from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from django.utils import timezone
from collections import defaultdict
from environ import Env

from ogame.models import Resources, Buildings, BuildingsResources, Boosters, \
Planets, PlanetsMultiverse, Starship

from ogame.serializers import ResourcesSerializer

env = Env()
env.read_env()
USER_ID = int(env("USER_ID"))

class GetResourcesAPIView(APIView):
    def post(self, request):
        try :
            # courses_id = escape(request.data['courses_id'])
            resource = Resources.objects.filter(user_id=USER_ID).first()
            serializer = ResourcesSerializer(resource).data

            return JsonResponse(serializer)
        except:
            content = {
                'msg': 'Erreur lors de la récupération des ressources'
            }
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
        
class SaveResourcesAPIView(APIView):
    def post(self, request):
        try :
            resources = request.data['resources']
            resource = Resources.objects.filter(user_id=USER_ID).update(metal=resources['metal'],
                                        crystal=resources['crystal'], deuterium=resources['deuterium'],
                                        satellites=resources['satellites'])
            # resources_values = {'metal': resource.metal}

            return JsonResponse({'msg': 'Ressources sauvegardées'})
        except:
            content = {
                'msg': 'Erreur lors de la sauvegarde des ressources'
            }
            return Response(content, status=status.HTTP_400_BAD_REQUEST)

class GetBuildingsAPIView(APIView):
    def post(self, request):
        try :
            # courses_id = escape(request.data['courses_id'])
            buildings = Buildings.objects.filter(user_id=USER_ID)
           
            building_levels = {'metal': 0, 'crystal': 0, 'deuterium': 0, 'energy': 0}

            for building in buildings:
                building_levels[building.building_type] = building.building_level
            return JsonResponse({'metal': building_levels['metal'],
                                 'crystal': building_levels['crystal'],
                                 'deuterium': building_levels['deuterium'],
                                 'energy': building_levels['energy'],})
        
            buildings = Buildings.objects.filter(user_id=USER_ID).values('building_type', 'building_level')
            

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
        try :
            # courses_id = escape(request.data['courses_id'])
            types = ['metal', 'crystal', 'deuterium', 'energy']

            # Obtenez toutes les valeurs des ressources pour les types spécifiés en une seule requête
            buildings_resources_values = BuildingsResources.objects.filter(type__in=types)

            # Initialisez la liste résultante
            buildings_resources_values_all = []

            # Parcourez les types et les valeurs des ressources correspondantes
            for t in types:
                # Trouvez la valeur correspondante dans la liste filtrée
                building_resources_values = next((brv for brv in buildings_resources_values if brv.type == t), None)
                
                # Ajoutez la valeur à la liste résultante
                buildings_resources_values_all.append({t: {'metal': building_resources_values.metal,
                                'crystal': building_resources_values.crystal,
                                'deuterium': building_resources_values.deuterium,
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
        try :
            type = request.data['type']
            level = request.data['level']
            Buildings.objects.filter(user_id=USER_ID, building_type=type).update(building_level=level)
            # resources_values = {'metal': resource.metal}

            return JsonResponse({'msg': 'Ressources ajoutées'})
        except:
            content = {
                'msg': 'Erreur lors de l\'ajout des ressources'
            }
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
        
class GetBoosterCostAPIView(APIView):
    def post(self, request):
        try :
            coefficient = request.data['coefficient']
            cost = Boosters.objects.filter(coefficient=coefficient).first().cost

            return Response(cost)
        except:
            content = {
                'msg': 'Erreur lors de la récupération du coût du booster'
            }

class SaveBoosterCoefficientAPIView(APIView):
    def post(self, request):
        try :
            coefficient = request.data['coefficient']
            Resources.objects.filter(user_id=USER_ID).update(booster=coefficient)

            booster = Boosters.objects.filter(coefficient=coefficient).first()

            return JsonResponse({'coefficient': coefficient, 'cost': booster.cost})
        except:
            content = {
                'msg': 'Erreur lors de la sauvegarde du niveau du booster'
            }
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
        
class ReinitializationAPIView(APIView):
    def post(self, request):
        try :
            user_id = request.data['user_id']
            Buildings.objects.filter(user_id=user_id).update(metal=0, crystal=0, deuterium=0, energy=0,
                                                            created_at=timezone.now())
            Resources.objects.filter(user_id=user_id).update(metal=1000, crystal=1000, deuterium=0,
                                                             satellites=0, booster=1, created_at=timezone.now())
            Planets.objects.filter(user_id=user_id).update(metal=0, crystal=0, deuterium=0)
            PlanetsMultiverse.objects.filter(user_id=user_id).update(metal=0, crystal=0, deuterium=0,
                                                                     is_discovered=0)
            Starship.objects.filter(user_id=user_id).update(is_built=0, life_level=0, fire_level=0, shield_level=0)
            

            return JsonResponse({'msg': 'Réinitialisation réussie'})
        except:
            content = {
                'msg': 'Erreur lors de la réinitialisation'
            }
            return Response(content, status=status.HTTP_400_BAD_REQUEST)