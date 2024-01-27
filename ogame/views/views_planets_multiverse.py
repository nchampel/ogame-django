from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from django.utils import timezone
from random import randrange, shuffle, uniform
from environ import Env

from ogame.models import PlanetsMultiverse, Resources, Starship

from ogame.serializers import PlanetsMultiverseSerializer

from ogame.functions import handleResourcesAttackedPlanet, authenticate

env = Env()
env.read_env()
USER_ID = int(env("USER_ID"))
class CreatePlanetsMultiverseAPIView(APIView):
    def post(self, request):
        user_id = authenticate(request)
        try :
            planets_to_create = []
            user_id = 3
            for i in range(10):
                for t in range(50):
                    name = str(i) + '.' + str(t + 1)
                    metal_level = randrange(40, 100)
                    crystal_level = randrange(40, 90)
                    deuterium_level = randrange(40, 80)
                    has_headquarter = randrange(0, 2)
                    type = 'ressources' if has_headquarter == 0 else 'ennemi'

                    # planets_to_create.append(name)
                    # if i == 0:
                    if has_headquarter == 0:
                        planets_to_create.append(
                            PlanetsMultiverse(user_id=user_id, name=name, metal_level=metal_level, type=type,
                                            crystal_level=crystal_level, deuterium_level=deuterium_level,
                                            has_headquarter=has_headquarter, created_at=timezone.now()))
                    else:
                        planets_to_create.append(
                            PlanetsMultiverse(user_id=user_id, name=name, metal_level=metal_level, type=type,
                                            crystal_level=crystal_level, deuterium_level=deuterium_level,
                                            has_headquarter=has_headquarter,
                                            life_level=randrange(1, 50), fire_level=randrange(1, 50),
                                            shield_level=randrange(1, 50), created_at=timezone.now()))
            # création du boss
            planets_to_create.append(PlanetsMultiverse(user_id=user_id, name=str(randrange(0, 10)) + '.' + str(randrange(0, 51)), type='boss',
                                            crystal_level=randrange(80, 250), deuterium_level=randrange(80, 250),
                                            has_headquarter=1, metal_level=randrange(80, 250), 
                                            life_level=randrange(50, 70), fire_level=randrange(50, 70),
                                            shield_level=randrange(50, 70), created_at=timezone.now()))     
            #         planets_to_create.append(PlanetsMultiverse(name=name, metal_level=metal_level, crystal_level=crystal_level, deuterium_level=deuterium_level))
            PlanetsMultiverse.objects.bulk_create(planets_to_create)


            return JsonResponse({'coefficient': 'ok'})
        except:
            content = {
                'msg': 'Erreur lors de la création des planètes'
            }
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
        
class GetPlanetsMultiverseDataAPIView(APIView):
    def post(self, request):
        user_id = authenticate(request)
        try :
            planets = PlanetsMultiverse.objects.filter(users_id=user_id).all()
            serializer_all = PlanetsMultiverseSerializer(planets, many=True).data
            shuffle(serializer_all)
            
            planets = PlanetsMultiverse.objects.filter(users_id=user_id, is_discovered=1).order_by('updated_at')
            serializer_discovered = PlanetsMultiverseSerializer(planets, many=True).data
            # shuffle(serializer_discovered)
            
            planets = PlanetsMultiverse.objects.filter(users_id=user_id,  is_discovered=0)
            serializer_not_discovered = PlanetsMultiverseSerializer(planets, many=True).data
            shuffle(serializer_not_discovered)

            return JsonResponse({'all': serializer_all, 'discovered': serializer_discovered,
                                 'not_discovered': serializer_not_discovered})
        except:
            content = {
                'msg': 'Erreur lors de la récupération des données des planètes multivers'
            }
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
        
class SaveResourcesPlanetsMultiverseAPIView(APIView):
    def post(self, request):
        user_id = authenticate(request)
        try :
            planets = request.data['planets']
            for planet in planets:

                PlanetsMultiverse.objects.filter(id=planet['id']).update(metal=planet['metal'],
                                        crystal=planet['crystal'], deuterium=planet['deuterium'])
            # resources_values = {'metal': resource.metal}

            return JsonResponse({'msg': 'Ressources des planètes multivers sauvegardées'})
        except:
            content = {
                'msg': 'Erreur lors de la sauvegarde des ressources des planètes multivers'
            }
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
class GetResultsAttackAPIView(APIView):
    def post(self, request):
        user_id = authenticate(request)
        try :
            planet = request.data['planet']
            starship_levels = request.data['starshipLevels']
            resources = request.data['resources']
            user_id = request.data['user_id']
            
            # results = [{'winner': '', 'round': 1, 'life_points_starship': 10, 'life_points_enemy': 10,
            #             'shield_starship': 10, 'fire_starship': 10, 'shield_enemy': 10, 'fire_enemy': 10},
            #             {'winner': 'Player', 'round': 1, 'life_points_starship': 10, 'life_points_enemy': 10,
            #             'shield_starship': 10, 'fire_starship': 10, 'shield_enemy': 10, 'fire_enemy': 10}]
            
            winner = ''
            round = 1
            results = []
            metal = 0
            crystal = 0
            deuterium = 0

            while winner == '':
                
                if round == 1:
                    life_starship = int(10 * 1.7 ** (starship_levels['life_level'] - 1))
                    life_enemy = int(10 * 1.7 ** (planet['life_level'] - 1))
                    if planet['type'] == 'boss':
                        boss_life = life_enemy
                fire_starship = int(8 * uniform(0.9, 1.5) ** (starship_levels['fire_level'] - 1))
                shield_starship = int(5 * uniform(1.1, 1.5) ** (starship_levels['shield_level'] - 1))
                fire_enemy = int(8 * uniform(0.9, 1.5) ** (planet['fire_level'] - 1))
                shield_enemy = int(5 * uniform(1.1, 1.5) ** (planet['shield_level'] - 1))   

                if shield_starship <= fire_enemy:
                    life_starship = life_starship - (fire_enemy - shield_starship)
                if shield_enemy <= fire_starship:
                    life_enemy = life_enemy - (fire_starship - shield_enemy)

                has_exploded = False
                if planet['type'] == 'boss':
                    if life_enemy < boss_life / 2 and life_enemy >= boss_life / 4 and randrange(0, 6) == 0:
                        life_enemy = 0
                        has_exploded = True
                    if life_enemy < boss_life / 4 and life_enemy >= boss_life / 10 and randrange(0, 5) == 0:
                        life_enemy = 0
                        has_exploded = True
                    if life_enemy < boss_life / 10 and randrange(0, 4) == 0:
                        life_enemy = 0
                        has_exploded = True
                
                if life_enemy <= 0:
                    life_enemy = 0
                    winner = 'Player'
                    handleResourcesAttackedPlanet(planet, resources, user_id)
                    metal = 0
                    crystal = 0
                    deuterium = 0

                if life_starship <= 0:
                    life_starship = 0
                    winner = 'Enemy'
                    # détruire le vaisseau
                    Starship.objects.filter(users_id=user_id).update(is_built=0)
                    

                results.append({'winner': winner, 'round': round, 'life_points_starship': life_starship, 'life_points_enemy': life_enemy,
                        'shield_starship': shield_starship, 'fire_starship': fire_starship, 'shield_enemy': shield_enemy, 'fire_enemy': fire_enemy,
                        'exploded': has_exploded, 'metal': metal, 'crystal': crystal, 'deuterium': deuterium})

                round += 1

            return Response(results)
        except:
            content = {
                'msg': 'Erreur lors de l\'attaque de la planète multivers'
            }
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
        
class SaveDiscoveredPlanetAPIView(APIView):
    def post(self, request):
        user_id = authenticate(request)
        try :
            planet_id = request.data['planet_id']

            PlanetsMultiverse.objects.filter(id=planet_id).update(is_discovered=1, updated_at=timezone.now())

            return JsonResponse({'msg': 'Découverte de la planète multivers sauvegardée'})
        except:
            content = {
                'msg': 'Erreur lors de la sauvegarde de la planète multivers'
            }
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
        
# class GetResourcesAttackAPIView(APIView):
#     def post(self, request):
#          user_id = authenticate(request)
#         try :
#             planet = request.data['planet']
#             resources = request.data['resources']

#             handleResourcesAttackedPlanet(planet, resources)

#             return JsonResponse({'msg': 'Ressources volées de la planète multivers attaquée sauvegardée'})
#         except:
#             content = {
#                 'msg': 'Erreur lors de la sauvegarde de la planète multivers ressource'
#             }
#             return Response(content, status=status.HTTP_400_BAD_REQUEST)