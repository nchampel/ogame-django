from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from random import randrange, shuffle

from ogame.models import Resources, Buildings, BuildingsResources, Boosters, \
Planets, PlanetsMultiverse

from ogame.serializers import PlanetsSerializer, PlanetsMultiverseSerializer

class GetResourcesAPIView(APIView):
    def post(self, request):
        try :
            # courses_id = escape(request.data['courses_id'])
            resource = Resources.objects.filter(id=1).first()
            resources_values = {'metal': resource.metal,
                                'crystal': resource.crystal,
                                'deuterium': resource.deuterium,
                                'energy': resource.energy,}

            return JsonResponse(resources_values)
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
                                        crystal=resources['crystal'], deuterium=resources['deuterium'])
            # resources_values = {'metal': resource.metal}

            return JsonResponse({'msg': 'Ressources ajoutées'})
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
            building_values = {'metal': building.metal,
                                'crystal': building.crystal,
                                'deuterium': building.deuterium,
                                'energy': building.energy,
                                'booster': building.booster,
                                'life_level': building.life_level,
                                'fire_level': building.fire_level,
                                'shield_level': building.shield_level}

            return JsonResponse(building_values)
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
        
class CreatePlanetsAPIView(APIView):
    def get(self, request):
        try :
            planets_to_create = []
            for i in range(10):
                for t in range(10):
                    name = str(i) + '.' + str(t + 1)
                    metal_level = randrange(1 * (i + 1), 10 * (i + 1))
                    crystal_level = randrange(1 * (i + 1), 10 * (i + 1))
                    deuterium_level = randrange(1 * (i + 1), 10 * (i + 1))
                    # if i == 0:
                    # print(name)
                    # print(metal_level)
                    planets_to_create.append(Planets(name=name, metal_level=metal_level, crystal_level=crystal_level, deuterium_level=deuterium_level))
            Planets.objects.bulk_create(planets_to_create)

            # booster = Boosters.objects.filter(coefficient=coefficient).first()

            return JsonResponse({'coefficient': 'ok'})
        except:
            content = {
                'msg': 'Erreur lors de la création des planètes'
            }
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
        
class GetPlanetsDataAPIView(APIView):
    def post(self, request):
        try :
            planets = Planets.objects.all()
            serializer = PlanetsSerializer(planets, many=True).data

            for idx, planet in enumerate(serializer):
                resources_on_planet = planet['metal'] + planet['crystal'] + planet['deuterium']
                serializer[idx]['cost'] = round(resources_on_planet / 10)

            return Response(serializer)
        except:
            content = {
                'msg': 'Erreur lors de la récupération des données des planètes'
            }
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
        
class SaveResourcesPlanetsAPIView(APIView):
    def post(self, request):
        try :
            planets = request.data['planets']
            for planet in planets:

                Planets.objects.filter(id=planet['id']).update(metal=planet['metal'],
                                        crystal=planet['crystal'], deuterium=planet['deuterium'])
            # resources_values = {'metal': resource.metal}

            return JsonResponse({'msg': 'Ressources des planètes sauvegardées'})
        except:
            content = {
                'msg': 'Erreur lors de la sauvegarde des ressources des planètes'
            }
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
        
class CreatePlanetsMultiverseAPIView(APIView):
    def get(self, request):
        try :
            planets_to_create = []
            for i in range(10):
                for t in range(50):
                    name = str(i) + '.' + str(t + 1)
                    metal_level = randrange(40, 100)
                    crystal_level = randrange(40, 90)
                    deuterium_level = randrange(40, 80)
                    has_headquarter = randrange(0, 2)
                    type = 'ressources' if has_headquarter == 0 else 'ennemi'

                    # planets_to_create.append(name)
                    # if i == 0:
                    if has_headquarter == 0:
                        planets_to_create.append(
                            PlanetsMultiverse(name=name, metal_level=metal_level, type=type,
                                            crystal_level=crystal_level, deuterium_level=deuterium_level,
                                            has_headquarter=has_headquarter))
                    else:
                        planets_to_create.append(
                            PlanetsMultiverse(name=name, metal_level=metal_level, type=type,
                                            crystal_level=crystal_level, deuterium_level=deuterium_level,
                                            has_headquarter=has_headquarter,
                                            life_level=randrange(1, 50), fire_level=randrange(1, 50),
                                            shield_level=randrange(1, 50)))
            # création du boss
            planets_to_create.append(PlanetsMultiverse(name=str(randrange(0, 10)) + '.' + str(randrange(0, 51)), type='boss',
                                            crystal_level=randrange(80, 250), deuterium_level=randrange(80, 250),
                                            has_headquarter=1, metal_level=randrange(80, 250), 
                                            life_level=randrange(50, 70), fire_level=randrange(50, 70),
                                            shield_level=randrange(50, 70)))     
            #         planets_to_create.append(PlanetsMultiverse(name=name, metal_level=metal_level, crystal_level=crystal_level, deuterium_level=deuterium_level))
            PlanetsMultiverse.objects.bulk_create(planets_to_create)

            # booster = Boosters.objects.filter(coefficient=coefficient).first()

            return JsonResponse({'coefficient': 'ok'})
        except:
            content = {
                'msg': 'Erreur lors de la création des planètes'
            }
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
        
class GetPlanetsMultiverseDataAPIView(APIView):
    def post(self, request):
        try :
            planets = PlanetsMultiverse.objects.all()
            serializer = PlanetsMultiverseSerializer(planets, many=True).data

            # for idx, planet in enumerate(serializer):
            #     resources_on_planet = planet['metal'] + planet['crystal'] + planet['deuterium']
            #     serializer[idx]['cost'] = round(resources_on_planet / 10)

            shuffle(serializer)

            return Response(serializer)
        except:
            content = {
                'msg': 'Erreur lors de la récupération des données des planètes multivers'
            }
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
        
class SaveResourcesPlanetsMultiverseAPIView(APIView):
    def post(self, request):
        try :
            planets = request.data['planets']
            for planet in planets:

                PlanetsMultiverse.objects.filter(id=planet['id']).update(metal=planet['metal'],
                                        crystal=planet['crystal'], deuterium=planet['deuterium'])
            # resources_values = {'metal': resource.metal}

            return JsonResponse({'msg': 'Ressources des planètes multivers sauvegardées'})
        except:
            content = {
                'msg': 'Erreur lors de la sauvegarde des ressources des planètes multivers'
            }
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
      