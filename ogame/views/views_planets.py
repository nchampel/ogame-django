from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from django.utils import timezone
from random import randrange
from environ import Env

from ogame.models import Planets

from ogame.serializers import PlanetsSerializer

from ogame.functions import authenticate

env = Env()
env.read_env()
USER_ID = int(env("USER_ID"))

class CreatePlanetsAPIView(APIView):
    def post(self, request):
        user_id = authenticate(request)
        try :
            planets_to_create = []
            user_id = 3
            for i in range(10):
                for t in range(10):
                    name = str(i) + '.' + str(t + 1)
                    metal_level = randrange(1 * (i + 1), 10 * (i + 1))
                    crystal_level = randrange(1 * (i + 1), 10 * (i + 1))
                    tritium_level = randrange(1 * (i + 1), 10 * (i + 1))
                    # if i == 0:
                    # print(name)
                    # print(metal_level)
                    planets_to_create.append(Planets(user_id=user_id, name=name, metal_level=metal_level, crystal_level=crystal_level, tritium_level=tritium_level, created_at=timezone.now()))
            Planets.objects.bulk_create(planets_to_create)

            return JsonResponse({'msg': 'Planètes créées'})
        except:
            content = {
                'msg': 'Erreur lors de la création des planètes'
            }
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
        
class GetPlanetsDataAPIView(APIView):
    def post(self, request):
        user_id = authenticate(request)
        try :
            planets = Planets.objects.filter(users_id=user_id).all()
            serializer = PlanetsSerializer(planets, many=True).data

            for idx, planet in enumerate(serializer):
                resources_on_planet = planet['metal'] + planet['crystal'] + planet['tritium']
                serializer[idx]['cost'] = round(resources_on_planet / 10)

            return Response(serializer)
        except:
            content = {
                'msg': 'Erreur lors de la récupération des données des planètes'
            }
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
        
class SaveResourcesPlanetsAPIView(APIView):
    def post(self, request):
        user_id = authenticate(request)
        try :
            planets = request.data['planets']
            for planet in planets:

                Planets.objects.filter(id=planet['id']).update(metal=planet['metal'],
                                        crystal=planet['crystal'], tritium=planet['tritium'])
            # resources_values = {'metal': resource.metal}

            return JsonResponse({'msg': 'Ressources des planètes sauvegardées'})
        except:
            content = {
                'msg': 'Erreur lors de la sauvegarde des ressources des planètes'
            }
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
        