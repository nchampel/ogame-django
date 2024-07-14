from rest_framework.views import APIView
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone

from ogame.models import Logs

from ogame.functions import authenticate

class SaveLogPowerGeneratorBuiltAPIView(APIView):
    def post(self, request):
        user_id = authenticate(request)
        try :
            number = request.data['number']

            description = str(number) + " groupe(s) électrogène créé(s)"

            Logs.objects.create(type='atelier', category='fabrication', users_id=user_id, description=description, target=user_id, created_at=timezone.now())
        
            return JsonResponse({'msg': "Sauvegarde du log de la création de groupes éclectrogène réussie"})
        except:
            content = {
                'msg': "Erreur lors de la sauvegarde du log de la création de groupes éclectrogène"
            }
            return Response(content, status=status.HTTP_400_BAD_REQUEST)