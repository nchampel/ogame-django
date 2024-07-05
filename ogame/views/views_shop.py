from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from django.utils import timezone
from datetime import date
from environ import Env

from ogame.models import Resources, ShopItems

from ogame.serializers import ShopItemsSerializer

from ogame.functions import authenticate

env = Env()
env.read_env()
DAILY_REWARD = int(env("DAILY_REWARD"))

class DetermineDailyHarvestableAPIView(APIView):
    def post(self, request):
        user_id = authenticate(request)
        try:
            today = date.today()
            resources = Resources.objects.filter(users_id=user_id, resource_type='unity-link').first()

            is_daily_harvestable = resources.harvested_at is None or resources.harvested_at.date() < today
            
            return JsonResponse({'isDailyHarvestable': is_daily_harvestable, 
                    'dailyReward': DAILY_REWARD})
        except:
            content = {
                'msg': 'Erreur lors de la récupération de la récompense journalière'
            }
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
class SaveDailyClaimedAPIView(APIView):
    def post(self, request):
        user_id = authenticate(request)
        try:
            unity_link_player = Resources.objects.filter(users_id=user_id, resource_type='unity-link').first()
            try:
                Resources.objects.filter(users_id=user_id, resource_type='unity-link').update(resource_value=DAILY_REWARD + unity_link_player.resource_value, harvested_at=timezone.now())
                return JsonResponse({
                    'msg': 'récompense sauvegardée',
                    'unityLink': DAILY_REWARD + unity_link_player.resource_value,
                    })
            except:
                return JsonResponse({'msg': 'souci lors de la sauvegarde de la récompense'})
                
        except:
            content = {
                'msg': 'Erreur lors de la sauvegarde de la récompense journalière'
            }
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
        
class GetLinkUnityAPIView(APIView):
    def post(self, request):
        user_id = authenticate(request)
        try:
            # user = Users.objects.filter(id=user_id).first()
            # return JsonResponse({'unity_link': user.unity_link})
            resources = Resources.objects.filter(users_id=user_id, resource_type='unity-link').first()
            return JsonResponse({'unity_link': resources.resource_value})
            
        except:
            content = {
                'msg': 'Erreur lors de la récupération du Lien-Unité'
            }
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
        
class SaveLinkUnityAPIView(APIView):
    def post(self, request):
        user_id = authenticate(request)
        try:
            unity_link = request.data['unity_link']
            Resources.objects.filter(users_id=user_id, resource_type='unity-link').update(resource_value=unity_link)
            return JsonResponse({'msg': "Lien-Unité sauvegardé"})
            
        except:
            content = {
                'msg': 'Erreur lors de la sauvegarde du Lien-Unité'
            }
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
        
class GetShopItemsDataAPIView(APIView):
    def post(self, request):
        user_id = authenticate(request)
        try :
            shop_items = ShopItems.objects.filter(users_id=user_id)
            serializer = ShopItemsSerializer(shop_items, many=True).data

            return JsonResponse(serializer, safe=False)
        except:
            content = {
                'msg': 'Erreur lors de la récupération des données de la boutique'
            }
            return Response(content, status=status.HTTP_400_BAD_REQUEST)

class SaveItemUsingAPIView(APIView):
    def post(self, request):
        user_id = authenticate(request)
        try :
            type = request.data['type']
            shop_item = ShopItems.objects.filter(users_id=user_id, item_type=type).first()
            ShopItems.objects.filter(users_id=user_id, item_type=type).update(item_quantity= shop_item.item_quantity - 1,
                                                                              item_used=shop_item.item_used + 1)

            return JsonResponse({'msg': "sauvegarde de l'utilisation de l'objet de la boutique réussie"})
        except:
            content = {
                'msg': "Erreur lors de la sauvegarde de l'utilisation de l'objet de la boutique"
            }
            return Response(content, status=status.HTTP_400_BAD_REQUEST)

class SaveItemBoughtAPIView(APIView):
    def post(self, request):
        user_id = authenticate(request)
        try :
            type = request.data['type']
            next_item_purchasable = False
            purchasable = False
            shop_item = ShopItems.objects.filter(users_id=user_id, item_type=type).first()
            if type != '1 week':
                purchasable_rules = [
                    {'type': '1 hour', 'quantity': 5 - 1, 'order': 1},
                    {'type': '2 hours', 'quantity': 12 - 1, 'order': 2},
                    {'type': '1 day', 'quantity': 20 - 1, 'order': 3},
                    {'type': '2 days', 'quantity': 30 - 1, 'order': 4},
                    {'type': '1 week', 'quantity': 0, 'order': 5},
                    ]
                for rule in purchasable_rules:
                    if rule['type'] == type and rule['quantity'] <= shop_item.item_bought:
                        next_item_purchasable = rule['order'] + 1
                if next_item_purchasable:
                    for rule in purchasable_rules:
                        if rule['order'] == next_item_purchasable:
                            next_type = rule['type']
                            break
                    # print(next_type)
                    ShopItems.objects.filter(users_id=user_id, item_type=next_type).update(purchasable=True)
                    purchasable = next_type
            ShopItems.objects.filter(users_id=user_id,
                                     item_type=type).update(item_quantity= shop_item.item_quantity + 1,
                                                            item_bought=shop_item.item_bought + 1)

            resource = Resources.objects.filter(users_id=user_id, resource_type='unity-link').first()
            Resources.objects.filter(users_id=user_id, resource_type='unity-link').update(resource_value=resource.resource_value - 500)

            return JsonResponse({
                'msg': "sauvegarde de l'utilisation de l'objet de la boutique réussie",
                'purchasable': purchasable, 'quantity': shop_item.item_quantity + 1, 'type': type,
                'unityLink': resource.resource_value - 500})
        except:
            content = {
                'msg': "Erreur lors de la sauvegarde de l'utilisation de l'objet de la boutique"
            }
            return Response(content, status=status.HTTP_400_BAD_REQUEST)