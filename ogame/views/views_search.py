from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from django.utils import timezone
from environ import Env

from ogame.models import Searches


env = Env()
env.read_env()
USER_ID = int(env("USER_ID"))
        
class GetSearchLevelsAPIView(APIView):
    def post(self, request):
        # try :
            
            searches = Searches.objects.filter(user_id=USER_ID)

            search_levels = {'life': 0, 'fire': 0, 'shield': 0, }

            for search in searches:
                resources_needed = {'metal': 0, 'crystal': 0, 'deuterium': 0}

                for resource in resources_needed:
                    # print(resource)
                    # print(search[resource])
                    resources_needed[resource] = getattr(search, resource)
                search_levels[search.search_type] = {'level': search.search_level, 
                                                     'metal': search.metal,
                                                     'crystal': search.crystal,
                                                     'deuterium': search.deuterium}
            print(search_levels)
            return JsonResponse(search_levels)
                

            search_levels = {'life_level': search_levels['life'], 'fire_level': search_levels['fire'],
                                'shield_level': search_levels['shield'], 'metal': search_levels['metal'],
                                'crystal': search_levels['crystal'], 'deuterium': search_levels['deuterium']}

            
            return JsonResponse(search_levels)
        # except:
        #     content = {
        #         'msg': 'Erreur lors de la récupération des niveaux de la recherche'
        #     }
        #     return Response(content, status=status.HTTP_400_BAD_REQUEST)
        
class SaveSearchLevelAPIView(APIView):
    def post(self, request):
        try :
            type = request.data['type']
            level = request.data['level']
            Searches.objects.filter(user_id=USER_ID, search_type=type).update(search_level=level)
            # resources_values = {'metal': resource.metal}

            return JsonResponse({'msg': 'Niveau de recherche sauvegardé'})
        except:
            content = {
                'msg': 'Erreur lors de la sauvegarde du niveau de recherche'
            }
            return Response(content, status=status.HTTP_400_BAD_REQUEST)