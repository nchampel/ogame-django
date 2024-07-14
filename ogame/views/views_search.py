from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from django.utils import timezone
from environ import Env

from ogame.models import Searches, Logs

from ogame.functions import authenticate


env = Env()
env.read_env()
USER_ID = int(env("USER_ID"))
        
class GetSearchLevelsAPIView(APIView):
    def post(self, request):
        user_id = authenticate(request)
        try :
            
            searches = Searches.objects.filter(users_id=user_id)

            search_levels = {'life': 0, 'fire': 0, 'shield': 0, 'energy': 0, 'electricity': 0}

            for search in searches:
                resources_needed = {'carbon': 0, 'diamond': 0, 'magic': 0}

                for resource in resources_needed:
                    resources_needed[resource] = getattr(search, resource)
                search_levels[search.search_type] = {'level': search.search_level, 
                                                     'carbon': search.carbon,
                                                     'diamond': search.diamond,
                                                     'magic': search.magic}
            # print(search_levels)
            return JsonResponse(search_levels)
                

            search_levels = {'life_level': search_levels['life'], 'fire_level': search_levels['fire'],
                                'shield_level': search_levels['shield'], 'metal': search_levels['metal'],
                                'crystal': search_levels['crystal'], 'tritium': search_levels['tritium']}

            
            return JsonResponse(search_levels)
        except:
            content = {
                'msg': 'Erreur lors de la récupération des niveaux de la recherche'
            }
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
        
class SaveSearchLevelAPIView(APIView):
    def post(self, request):
        user_id = authenticate(request)
        try :
            type = request.data['type']
            level = request.data['level']
            Searches.objects.filter(users_id=user_id, search_type=type).update(search_level=level)
            # resources_values = {'metal': resource.metal}

            searches_names = {
                'energy': "Energie",
                'electricity': "Electricité",
                "life": "Vie",
                'shield': "Bouclier",
                'fire': "Armes",
                'time': 'Accélération de temps'
            }

            description = searches_names[type] + " niveau " + str(level) + " obtenu"

            Logs.objects.create(type='recherche', category='recherche', users_id=user_id, description=description, target=user_id, created_at=timezone.now())

            return JsonResponse({'msg': 'Niveau de recherche sauvegardé'})
        except:
            content = {
                'msg': 'Erreur lors de la sauvegarde du niveau de recherche'
            }
            return Response(content, status=status.HTTP_400_BAD_REQUEST)