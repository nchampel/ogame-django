from rest_framework.views import APIView
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone

from ogame.models import Users, Config

from ogame.functions import authenticate

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
                'msg': 'Erreur lors de la sauvegarde de l\'alignement BGZ'
            }
            return Response(content, status=status.HTTP_400_BAD_REQUEST)