from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from django.utils import timezone
from datetime import date
from random import randrange
from environ import Env

from ogame.models import Resources, ShopItems, Buildings, Users, Logs

from ogame.serializers import ShopItemsSerializer

from ogame.functions import authenticate

env = Env()
env.read_env()
DAILY_REWARD_UNITY_LINK = int(env("DAILY_REWARD_UNITY_LINK"))
DAILY_REWARD_TICKET = int(env("DAILY_REWARD_TICKET"))

class DetermineDailyHarvestableAPIView(APIView):
    def post(self, request):
        user_id = authenticate(request)
        try:
            today = date.today()
            resources = Resources.objects.filter(users_id=user_id, resource_type='unity-link').first()

            is_daily_harvestable = resources.harvested_at is None or resources.harvested_at.date() < today

                
            return JsonResponse({'isDailyHarvestable': is_daily_harvestable, 
                    'dailyReward': {
                        'unityLink': DAILY_REWARD_UNITY_LINK,
                        'ticket': DAILY_REWARD_TICKET
                        }})
        except:
            content = {
                'msg': 'Erreur lors de la récupération de la récompense journalière'
            }
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
class SaveDailyClaimedAPIView(APIView):
    def post(self, request):
        user_id = authenticate(request)
        try:
            levels = request.data['levels']
            unity_link_player = Resources.objects.filter(users_id=user_id, resource_type='unity-link').first()
            ticket_player = Resources.objects.filter(users_id=user_id, resource_type='ticket').first()
            try:
                Resources.objects.filter(users_id=user_id, resource_type='unity-link').update(resource_value=DAILY_REWARD_UNITY_LINK + 100 * levels['unityLink'] + unity_link_player.resource_value, harvested_at=timezone.now())
                Resources.objects.filter(users_id=user_id, resource_type='ticket').update(resource_value=DAILY_REWARD_TICKET + 2 * levels['ticket'] + ticket_player.resource_value, harvested_at=timezone.now())
                
                description = str(DAILY_REWARD_UNITY_LINK + levels['unityLink'] * 100) + " Lien-Unités et " + str(DAILY_REWARD_TICKET + levels['ticket'] * 2) + " tickets obtenus"

                Logs.objects.create(type='boutique', category='récompense journalière', users_id=user_id, description=description, target=user_id, created_at=timezone.now())
            

                return JsonResponse({
                    'msg': 'récompense sauvegardée',
                    'unityLink': DAILY_REWARD_UNITY_LINK + 100 * levels['unityLink'] + unity_link_player.resource_value,
                    'ticket': DAILY_REWARD_TICKET + 2 * levels['ticket'] + ticket_player.resource_value,
                    })
            except:
                return JsonResponse({'msg': 'souci lors de la sauvegarde de la récompense'})
                
        except:
            content = {
                'msg': 'Erreur lors de la sauvegarde de la récompense journalière'
            }
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
        
class GetLinkUnityTicketAPIView(APIView):
    def post(self, request):
        user_id = authenticate(request)
        try:
            # user = Users.objects.filter(id=user_id).first()
            # return JsonResponse({'unity_link': user.unity_link})
            resources_unity_link = Resources.objects.filter(users_id=user_id, resource_type='unity-link').first()
            resources_ticket = Resources.objects.filter(users_id=user_id, resource_type='ticket').first()
            return JsonResponse({'unity_link': resources_unity_link.resource_value, 'ticket': resources_ticket.resource_value})
            
        except:
            content = {
                'msg': 'Erreur lors de la récupération du Lien-Unité et des tickets'
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
class SaveTicketAPIView(APIView):
    def post(self, request):
        user_id = authenticate(request)
        try:
            ticket = request.data['ticket']
            Resources.objects.filter(users_id=user_id, resource_type='ticket').update(resource_value=ticket)
            return JsonResponse({'msg': "Ticket sauvegardé"})
            
        except:
            content = {
                'msg': 'Erreur lors de la sauvegarde du ticket'
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

items_names = {
                '1 hour': "1 heure",
                '2 hours': "2 heures",
                '1 day': "1 jour",
                '2 days': "2 jours",
                '1 week': "1 semaine",
            }
class SaveItemUsingAPIView(APIView):
    def post(self, request):
        user_id = authenticate(request)
        try :
            type = request.data['type']
            shop_item = ShopItems.objects.filter(users_id=user_id, item_type=type).first()
            ShopItems.objects.filter(users_id=user_id, item_type=type).update(item_quantity= shop_item.item_quantity - 1,
                                                                              item_used=shop_item.item_used + 1)
        

            description = 'Utilisation ' + items_names[type] 

            Logs.objects.create(type='boutique', category='utilisation objet', users_id=user_id, description=description, target=user_id, created_at=timezone.now())

            return JsonResponse({'msg': "sauvegarde de l'utilisation de l'objet de la boutique réussie"})
        except:
            content = {
                'msg': "Erreur lors de la sauvegarde de l'utilisation de l'objet de la boutique"
            }
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
class GetPriceWonAPIView(APIView):
    def post(self, request):
        user_id = authenticate(request)
        try :
            ticket = request.data['ticket']
            if (ticket > 0):
                Resources.objects.filter(users_id=user_id, resource_type="ticket").update(resource_value=ticket - 1)
                random = randrange(1, 100)
                if random >= 1 and random <= 55:
                    price_won = '1 hour'
                if random > 55 and random <= 75:
                    price_won = '2 hours'
                if random > 75 and random <= 89:
                    price_won = '1 day'
                if random > 89 and random <= 95:
                    price_won = '2 days'
                if random > 95 and random <= 98:
                    price_won = '1 week'
                if random > 98 and random <= 100:
                    price_won = 'unity-link_won'

                if price_won != 'unity-link_won':
                    shop_item = ShopItems.objects.filter(users_id=user_id, item_type=price_won).first()
                    ShopItems.objects.filter(users_id=user_id, item_type=price_won).update(item_won=shop_item.item_won + 1)
                    description = items_names[price_won] + " gagné"

                    Logs.objects.create(type='boutique', category='gain', users_id=user_id, description=description, target=user_id, created_at=timezone.now())

                else:
                    description = "500 Lien-Unités gagnés"

                    Logs.objects.create(type='boutique', category='gain', users_id=user_id, description=description, target=user_id, created_at=timezone.now())


                return JsonResponse({'msg': "OK", 'price_won': price_won})
            else:
                return JsonResponse({'msg': "erreur", 'price_won': 'erreur'})
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
            link_unity_used = request.data['link_unity_used']
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
            Resources.objects.filter(users_id=user_id, resource_type='unity-link').update(resource_value=resource.resource_value - link_unity_used)

            description = items_names[type] + " acheté"

            Logs.objects.create(type='boutique', category='achat', users_id=user_id, description=description, target=user_id, created_at=timezone.now())

            
            return JsonResponse({
                'msg': "sauvegarde de l'utilisation de l'objet de la boutique réussie",
                'purchasable': purchasable, 'quantity': shop_item.item_quantity + 1, 'type': type,
                'unityLink': resource.resource_value - link_unity_used})
        except:
            content = {
                'msg': "Erreur lors de la sauvegarde de l'utilisation de l'objet de la boutique"
            }
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
class SaveItemWonAPIView(APIView):
    def post(self, request):
        user_id = authenticate(request)
        try :
            type = request.data['type']
            # print(type)
            
            shop_item = ShopItems.objects.filter(users_id=user_id, item_type=type).first()
            
            ShopItems.objects.filter(users_id=user_id, item_type=type).update(item_quantity=shop_item.item_quantity + 1)

            # le log se fait dans GetPriceWon
                
            return JsonResponse({
                # 'msg': "sauvegarde du gain de l'objet de la boutique réussie",
                'quantity': shop_item.item_quantity + 1})
        except:
            content = {
                'msg': "Erreur lors de la sauvegarde du gain de l'objet de la boutique"
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
                        {'type': 'carbon', 'level': 20, 'order': 1},
                        {'type': 'diamond', 'level': 20, 'order': 2},
                        {'type': 'magic', 'level': 20, 'order': 3},
                        {'type': 'carbon', 'level': 40, 'order': 4},
                        {'type': 'diamond', 'level': 30, 'order': 5},
                        {'type': 'magic', 'level': 30, 'order': 6},
                        {'type': 'carbon', 'level': 50, 'order': 7},
                        {'type': 'diamond', 'level': 40, 'order': 8},
                        {'type': 'magic', 'level': 40, 'order': 9},
                        {'type': 'carbon', 'level': 60, 'order': 10},
                        {'type': 'diamond', 'level': 50, 'order': 11},
                        {'type': 'magic', 'level': 50, 'order': 12},
                    ],
                    'is_next_level_buildable': False, 
                    'next_level_data' : 
                        {'type': 'carbon', 'level': 20, 'level_building': 1},
                    }
                 },
                {'ticket_generator' : {
                    'rules': [
                        {'type': 'carbon', 'level': 30, 'order': 1},
                        {'type': 'diamond', 'level': 30, 'order': 2},
                        {'type': 'magic', 'level': 30, 'order': 3},
                        {'type': 'carbon', 'level': 40, 'order': 4},
                        {'type': 'diamond', 'level': 40, 'order': 5},
                        {'type': 'magic', 'level': 40, 'order': 6},
                        {'type': 'carbon', 'level': 50, 'order': 7},
                        {'type': 'diamond', 'level': 50, 'order': 8},
                        {'type': 'magic', 'level': 50, 'order': 9},
                        {'type': 'carbon', 'level': 60, 'order': 10},
                        {'type': 'diamond', 'level': 60, 'order': 11},
                        {'type': 'magic', 'level': 60, 'order': 12},
                    ],
                    'is_next_level_buildable': False,
                    'next_level_data' : 
                        {'type': 'carbon', 'level': 30, 'level_building': 1},
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
            # buildings_names = ['carbon', 'diamond', 'magic']
            # buildings sous la forme {'carbon': 60, 'diamond': 10 ...}

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
                                    # print(building_shop_level_player)
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
                                          
            # print(shop_buildings)            

            return Response(shop_buildings)
        except:
            content = {
                'msg': "Erreur lors de la sauvegarde de l'utilisation de l'objet de la boutique"
            }
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
        
class SaveUnityLinkInvestedAPIView(APIView):
    def post(self, request):
        user_id = authenticate(request)
        try :
            unity_link = request.data['unity_link']
            user = Users.objects.filter(id=user_id).first()
            Users.objects.filter(id=user_id).update(unity_link_invested=user.unity_link_invested + unity_link)
        
            return JsonResponse({'msg': "Sauvegarde des unité-liens investis réussie"})
        except:
            content = {
                'msg': "Erreur lors de la sauvegarde des unité-liens investis"
            }
            return Response(content, status=status.HTTP_400_BAD_REQUEST)