from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

from random import randrange, shuffle

from ogame.models import PlanetsMultiverse

from ogame.serializers import PlanetsMultiverseSerializer

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