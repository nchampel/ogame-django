from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

from random import randrange

from ogame.models import Planets

from ogame.serializers import PlanetsSerializer

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