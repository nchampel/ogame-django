from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from django.utils import timezone
from django.db.models import Q

from ogame.models import Buildings, Users

from ogame.functions import authenticate

class GetRankingAPIView(APIView):
    def post(self, request):
        authenticate(request)
        try :
            buildings = Buildings.objects.values_list('users_id', 'building_level').order_by('users_id')
            users = Users.objects.exclude(Q(nature=None) | Q(is_admin=True)).values_list('id', 'nature', 'pseudo')
            levels = [{'users_id': b[0], 'level': b[1]} for b in buildings]
            natures = {u[0]: u[1] for u in users}
            pseudos = {u[0]: u[2] for u in users}
            users_ids = [u[0] for u in users]
            
            # print(users)
            # print(natures)
            # pour supprimer doublons
            # users_id_clean = list(set(users_id))
            ranking_total = []
            for user_id in users_ids:
                points = 0
                for level in levels:
                    if level['users_id'] == user_id:
                        points += level['level']
                nature = natures.get(user_id, None)
                pseudo = pseudos.get(user_id, None)
                ranking_total.append({'points': points, 'nature': nature, 'pseudo': pseudo})
                # triage de la liste par points décroissant
            ranking_total_sorted = sorted(ranking_total, key=lambda x: x["points"], reverse=True)
            # classement par alignement
            ranking_sotoc = [rs for rs in ranking_total if rs['nature'] == 'sotoc']
            ranking_flumia = [rf for rf in ranking_total if rf['nature'] == 'flumia']
            ranking_nano = [rn for rn in ranking_total if rn['nature'] == 'nano']
            ranking_altheron = [ra for ra in ranking_total if ra['nature'] == 'altheron']
            ranking_sora = [rs for rs in ranking_total if rs['nature'] == 'sora']
            ranking_sotoc_sorted = sorted(ranking_sotoc, key=lambda x: x["points"], reverse=True)
            ranking_flumia_sorted = sorted(ranking_flumia, key=lambda x: x["points"], reverse=True)
            ranking_nano_sorted = sorted(ranking_nano, key=lambda x: x["points"], reverse=True)
            ranking_sora_sorted = sorted(ranking_sora, key=lambda x: x["points"], reverse=True)
            ranking_altheron_sorted = sorted(ranking_altheron, key=lambda x: x["points"], reverse=True)
            # ranking_sotoc_sorted.insert(0, {'points': 'name', 'pseudo': '', 'nature': 'Sotoc'})
            # print(ranking_sotoc)
            return JsonResponse({"ranking_total": ranking_total_sorted[:10],
                                 "ranking_sotoc": ranking_sotoc_sorted[:10],
                                 "ranking_flumia": ranking_flumia_sorted[:10],
                                 "ranking_sora": ranking_sora_sorted[:10],
                                 "ranking_nano": ranking_nano_sorted[:10],
                                 "ranking_altheron": ranking_altheron_sorted[:10],
                                 })
        except:
            content = {
                'msg': 'Erreur lors de la récupération des données du vaisseau'
            }
            return Response(content, status=status.HTTP_400_BAD_REQUEST)