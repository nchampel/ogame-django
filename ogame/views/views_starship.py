from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from django.utils import timezone
from environ import Env

from ogame.models import Starship, Resources

from ogame.serializers import StarshipSerializer

env = Env()
env.read_env()
USER_ID = int(env("USER_ID"))

class GetStarshipDataAPIView(APIView):
    def post(self, request):
        try :
            # courses_id = escape(request.data['courses_id'])
            starship = Starship.objects.filter(user_id=USER_ID).first()
            serializer = StarshipSerializer(starship).data

            return JsonResponse(serializer)
        except:
            content = {
                'msg': 'Erreur lors de la récupération des données du vaisseau'
            }
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
        
class BuildStarshipAPIView(APIView):
    def post(self, request):
        try :
            # on récupère les données pour les ressources nécessaires à la construction du vaisseau
            starship = Starship.objects.filter(user_id=USER_ID).first()
            resources_needed = {'metal': 1000000 * starship.life_level, 'crystal': 1000000 * starship.fire_level,
                                'deuterium': 1000000 * starship.shield_level}
            resources = Resources.objects.filter(user_id=USER_ID).first()

            if not starship.is_built and resources_needed['metal'] <= resources.metal and resources_needed['crystal'] <= resources.crystal and resources_needed['deuterium'] <= resources.deuterium:
                Starship.objects.filter(user_id=USER_ID).update(is_built=1)
                remaining_metal = resources.metal - resources_needed['metal']
                remaining_crystal = resources.crystal - resources_needed['crystal']
                remaining_deuterium = resources.deuterium - resources_needed['deuterium']
                Resources.objects.filter(user_id=USER_ID).update(metal=remaining_metal,
                                        crystal=remaining_crystal, deuterium=remaining_deuterium)

            return JsonResponse({'msg': 'Vaisseau construit'})
        except:
            content = {
                'msg': 'Erreur lors de la construction du vaisseau'
            }
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
        
class DestroyStarshipAPIView(APIView):
    def post(self, request):
        try :
            Starship.objects.filter(user_id=USER_ID).update(is_built=0)

            return JsonResponse({'msg': 'Vaisseau détruit'})
        except:
            content = {
                'msg': 'Erreur lors de la destruction du vaisseau'
            }
            return Response(content, status=status.HTTP_400_BAD_REQUEST)