from rest_framework.views import APIView
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from collections import defaultdict

from ogame.models import Users, Config, Success, Logs

from ogame.functions import authenticate

from ogame.names import resources_names

class SaveResourcesInvestedAPIView(APIView):
    def post(self, request):
        user_id = authenticate(request)
        try :
            resources = request.data['resources']

            user = Users.objects.filter(id=user_id).first()

            Users.objects.filter(id=user_id).update(resources_invested=user.resources_invested + resources)

            return JsonResponse({'msg': "Sauvegarde des ressources investies réussie"})
        except:
            content = {
                'msg': "Erreur lors de la sauvegarde des ressources investies"
            }
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
        
class GetIsWebsiteUnderMaintenanceAPIView(APIView):
    def post(self, request):
        user_id = authenticate(request)
        try:

            config = Config.objects.filter(name="maintenance").first()

            maintenance = True if config.value == 'true' else False
            
            return JsonResponse({'isWebsiteUnderMaintenance': maintenance})
            
        except:
            content = {
                'msg': "Erreur lors de la récupération de l'information du site en maintenance"
            }
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
        
class GetSuccessPlayerAPIView(APIView):
    def post(self, request):
        user_id = authenticate(request)
        try:

            success = Success.objects.filter(users_id=user_id).values_list("success_resource_type", "success_value", "is_won")

            success_player = [{'resource': sp[0], 'value': sp[1], 'is_won': sp[2]} for sp in success]

            # print(success_player) 

            return JsonResponse({'successPlayer': success_player})
            
        except:
            content = {
                'msg': 'Erreur lors de la récupération des succès'
            }
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
class SaveSuccessPlayerAPIView(APIView):
    def post(self, request):
        user_id = authenticate(request)
        try:
            success_to_save = request.data["success_to_save"]
            success = Success.objects.filter(users_id=user_id).values_list("success_resource_type", "success_value", "is_won")

            success_player_in_DB = [{'resource': sp[0], 'value': sp[1], 'is_won': sp[2]} for sp in success]

            logs_to_save = []
            for s_t_s in success_to_save:
                for data_in_DB in success_player_in_DB:
                    # print(data_in_DB)
                    if s_t_s['is_won'] and not data_in_DB['is_won'] and data_in_DB['resource'] == s_t_s['resource'] and data_in_DB['value'] == s_t_s['value']:
                        # print(s_t_s['resource'])
                        # print(s_t_s['value'])
                        Success.objects.filter(users_id=user_id, 
                                            success_resource_type=s_t_s['resource'], 
                                            success_value=s_t_s['value']).update(is_won=True)
                        
                        description = 'Récompense pour ' + str(s_t_s['value']) + ' ' + resources_names[s_t_s['resource']] + ' obtenue'
                        logs_to_save.append(Logs(type='succès', category='ressources', users_id=user_id, description=description, target=user_id, created_at=timezone.now()))
            Logs.objects.bulk_create(logs_to_save)
            # print(success_player) 

            return JsonResponse({'msg': 'Sauvegarde des succès réussie'})
            
        except:
            content = {
                'msg': 'Erreur lors de la sauvegarde des succès'
            }
            return Response(content, status=status.HTTP_400_BAD_REQUEST)