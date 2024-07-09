from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from django.utils import timezone
from datetime import date
from environ import Env

from ogame.models import Resources, ShopItems, Buildings

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
            level = request.data['level']
            unity_link_player = Resources.objects.filter(users_id=user_id, resource_type='unity-link').first()
            try:
                Resources.objects.filter(users_id=user_id, resource_type='unity-link').update(resource_value=DAILY_REWARD + 100 * level + unity_link_player.resource_value, harvested_at=timezone.now())
                return JsonResponse({
                    'msg': 'récompense sauvegardée',
                    'unityLink': DAILY_REWARD + 100 * level + unity_link_player.resource_value,
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
        

class GetDisplayBuildingsShopLevelsAPIView(APIView):
    def post(self, request):
        user_id = authenticate(request)
        try :
            shop_buildings_names = ['unity-link_generator', 'ticket_generator']
            shop_buildings = [
                {'unity-link_generator' : {
                    'rules': [
                        {'type': 'metal', 'level': 20, 'order': 1},
                        {'type': 'crystal', 'level': 20, 'order': 2},
                        {'type': 'tritium', 'level': 20, 'order': 3},
                        {'type': 'metal', 'level': 40, 'order': 4},
                        {'type': 'crystal', 'level': 30, 'order': 5},
                        {'type': 'tritium', 'level': 30, 'order': 6},
                    ],
                    'is_next_level_buildable': False, 
                    'next_level_data' : 
                        {'type': 'metal', 'level': 20, 'level_building': 1},
                    }
                 },
                {'ticket_generator' : {
                    'rules': [
                        {'type': 'metal', 'level': 25, 'order': 1},
                        {'type': 'crystal', 'level': 60, 'order': 2},
                        {'type': 'tritium', 'level': 60, 'order': 3},
                        {'type': 'metal', 'level': 60, 'order': 4},
                        {'type': 'crystal', 'level': 60, 'order': 5},
                        {'type': 'tritium', 'level': 60, 'order': 6},
                    ],
                    'is_next_level_buildable': False,
                    'next_level_data' : 
                        {'type': 'metal', 'level': 25, 'level_building': 1},
                    }
                 },
            ]
            # on récupère les niveaux des bâtiments de la boutique
            buildings_shop = Buildings.objects.filter(users_id=user_id).values('building_type', 'building_level')
            # buildings_shop_player = []
            # buildings_shop = Buildings.objects.filter(users_id=6)
            # for building_name in shop_buildings_names:

            #     for bs in buildings_shop:
            #         if bs.building_type == building_name:
            #             buildings_shop_player.append({building_name: bs.building_level})

            buildings_dict = {bs['building_type']: bs['building_level'] for bs in buildings_shop}

            buildings_shop_player = {name: buildings_dict[name] for name in shop_buildings_names if name in buildings_dict}
            # retourne {'unity-link_generator': 0}
            buildings = request.data['buildings']
            # buildings_names = ['metal', 'crystal', 'tritium']
            # buildings sous la forme {'metal': 60, 'crystal': 10 ...}

            for building in shop_buildings:
                for shop_building_key, shop_building_value in building.items():
                    building_shop_level_player = buildings_shop_player[shop_building_key]
                    # print(building_shop_level_player)
                    for key_building_data, building_data_value in shop_building_value.items():
                        # print(building_data_value)
                        if key_building_data == 'rules':
                            for value_in_rules in building_data_value:
                                # print(value_in_rules)
                                for key_building_player, value_building in buildings.items():
                                    if value_in_rules['order'] == building_shop_level_player + 1 and key_building_player == value_in_rules['type'] and value_building >= value_in_rules['level']:
                                        shop_building_value['is_next_level_buildable'] = True
                                        # donner infos que niveau suivant constructible
                                        for search_next_rule in shop_building_value['rules']:
                                            if search_next_rule['order'] == building_shop_level_player + 2:
                                                shop_building_value['next_level_data'] = {'type': search_next_rule['type'], 'level': search_next_rule['level'], 'level_building': building_shop_level_player + 2}
                                                # print(f"niveau {building_shop_level_player + 2} : {search_next_rule['type']} niv {search_next_rule['level']}")
                                    elif value_in_rules['order'] == building_shop_level_player + 1 and key_building_player == value_in_rules['type'] and value_building < value_in_rules['level']:
                                        for search_next_rule_buildable_false in shop_building_value['rules']:
                                            if search_next_rule_buildable_false['order'] == building_shop_level_player + 1:
                                                shop_building_value['next_level_data'] = {'type': search_next_rule_buildable_false['type'], 'level': search_next_rule_buildable_false['level'], 'level_building': building_shop_level_player + 1}
                                          
            print(shop_buildings)            

            return Response(shop_buildings)
        except:
            content = {
                'msg': "Erreur lors de la sauvegarde de l'utilisation de l'objet de la boutique"
            }
            return Response(content, status=status.HTTP_400_BAD_REQUEST)