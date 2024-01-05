from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from django.utils import timezone
from random import randrange, shuffle, uniform
from environ import Env

from ogame.models import PlanetsMultiverse, Resources

from ogame.serializers import PlanetsMultiverseSerializer

env = Env()
env.read_env()
USER_ID = int(env("USER_ID"))
class CreatePlanetsMultiverseAPIView(APIView):
    def get(self, request):
        try :
            planets_to_create = []
            user_id = 2
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

            # booster = Boosters.objects.filter(coefficient=coefficient).first()

            return JsonResponse({'coefficient': 'ok'})
        except:
            content = {
                'msg': 'Erreur lors de la création des planètes'
            }
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
        
class GetPlanetsMultiverseDataAPIView(APIView):
    def post(self, request):
        try :
            planets = PlanetsMultiverse.objects.filter(user_id=USER_ID).all()
            serializer = PlanetsMultiverseSerializer(planets, many=True).data

            # for idx, planet in enumerate(serializer):
            #     resources_on_planet = planet['metal'] + planet['crystal'] + planet['deuterium']
            #     serializer[idx]['cost'] = round(resources_on_planet / 10)

            shuffle(serializer)

            return Response(serializer)
        except:
            content = {
                'msg': 'Erreur lors de la récupération des données des planètes multivers'
            }
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
        
class SaveResourcesPlanetsMultiverseAPIView(APIView):
    def post(self, request):
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
        try :
            planet = request.data['planet']
            starship_levels = request.data['starshipLevels']
            resources = request.data['resources']
            
            results = [{'winner': '', 'round': 1, 'life_points_starship': 10, 'life_points_enemy': 10,
                        'shield_starship': 10, 'fire_starship': 10, 'shield_enemy': 10, 'fire_enemy': 10},
                        {'winner': 'Player', 'round': 1, 'life_points_starship': 10, 'life_points_enemy': 10,
                        'shield_starship': 10, 'fire_starship': 10, 'shield_enemy': 10, 'fire_enemy': 10}]
            
            winner = ''
            round = 1
            results = []

            while winner == '':
                
                if round == 1:
                    life_starship = int(10 * 1.7 ** (starship_levels['life_level'] - 1))
                    life_enemy = int(10 * 1.7 ** (planet['life_level'] - 1))
                fire_starship = int(8 * uniform(0.9, 1.5) ** (starship_levels['fire_level'] - 1))
                shield_starship = int(5 * uniform(1.1, 1.5) ** (starship_levels['shield_level'] - 1))
                fire_enemy = int(8 * uniform(0.9, 1.5) ** (planet['fire_level'] - 1))
                shield_enemy = int(5 * uniform(1.1, 1.5) ** (planet['shield_level'] - 1))   

                if shield_starship <= fire_enemy:
                    life_starship = life_starship - (fire_enemy - shield_starship)
                if shield_enemy <= fire_starship:
                    life_enemy = life_enemy - (fire_starship - shield_enemy)
                
                if life_enemy <= 0:
                    life_enemy = 0
                    winner = 'Player'
                    resources['metal'] += planet['metal']
                    resources['crystal'] += planet['crystal']
                    resources['deuterium'] += planet['deuterium']
                    # Resources.objects.filter(id=1).update(metal=resources['metal'],
                    #                     crystal=resources['crystal'], deuterium=resources['deuterium'])


                if life_starship <= 0:
                    life_starship = 0
                    winner = 'Enemy'
                    # détruire le vaisseau

                results.append({'winner': winner, 'round': round, 'life_points_starship': life_starship, 'life_points_enemy': life_enemy,
                        'shield_starship': shield_starship, 'fire_starship': fire_starship, 'shield_enemy': shield_enemy, 'fire_enemy': fire_enemy})

                round += 1

            return Response(results)
        except:
            content = {
                'msg': 'Erreur lors de l\'attaque de la planète multivers'
            }
            return Response(content, status=status.HTTP_400_BAD_REQUEST)