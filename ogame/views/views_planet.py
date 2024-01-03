from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

from ogame.models import Resources, Buildings, BuildingsResources, Boosters

from ogame.serializers import BuildingsSerializer, ResourcesSerializer

class GetResourcesAPIView(APIView):
    def post(self, request):
        try :
            # courses_id = escape(request.data['courses_id'])
            resource = Resources.objects.filter(id=1).first()
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
            resource = Resources.objects.filter(id=1).update(metal=resources['metal'],
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
            building = Buildings.objects.filter(id=1).first()
            serializer = BuildingsSerializer(building).data
            return JsonResponse(serializer)
        except:
            content = {
                'msg': 'Erreur lors de la récupération des ressources'
            }
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
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
            Buildings.objects.filter(id=1).update(**{type: level})
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
            Buildings.objects.filter(id=1).update(booster=coefficient)

            booster = Boosters.objects.filter(coefficient=coefficient).first()

            return JsonResponse({'coefficient': coefficient, 'cost': booster.cost})
        except:
            content = {
                'msg': 'Erreur lors de la sauvegarde du niveau du booster'
            }
            return Response(content, status=status.HTTP_400_BAD_REQUEST)