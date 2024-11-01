from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from django.utils import timezone
import bcrypt
from django.utils.html import escape
from rest_framework.exceptions import AuthenticationFailed
from environ import Env
import jwt, datetime as dt
from typing import Dict

from ogame.models import Users, Token, Buildings, Resources, Searches, Starship, Logs, ShopItems, \
Success

from ogame.functions import authenticate

env = Env()
env.read_env()
SECRET_KEY = env("SECRET_KEY")
CRON_KEY = env("CRON_KEY")

class RegisterAPIView(APIView):
    def post(self, request):
        pseudo = escape(request.data['values']['pseudo'])
        email = escape(request.data['values']['email'])
        password = escape(request.data['values']['password'])

        user_in_db = Users.objects.filter(pseudo=pseudo).first()
        if user_in_db:
            return JsonResponse({'msg': 'Pseudo déjà utilisé'})

    # on encrypte le mot de passe
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
        password_hashed = hashed.decode('utf-8')
        # password = b"super secret password"
        # password_hashed = bcrypt.hashpw(password, bcrypt.gensalt())

        try:
            Users.objects.create(pseudo=pseudo, email=email, password=password_hashed, 
                                    created_at=timezone.now())
            user = Users.objects.latest('id')
            buildings = ['carbon', 'diamond', 'magic', 'energy', 'unity-link_generator', 'ticket_generator', 'protective_dome']
            buildings_to_insert = []
            for building in buildings:
                buildings_to_insert.append(Buildings(building_type=building, building_level=0, users_id=user.id, created_at=timezone.now()))
            Buildings.objects.bulk_create(buildings_to_insert)
            shop_items = ['1 hour', '2 hours', '1 day', '2 days', '1 week']
            purchasable = False
            shop_items_to_insert = []
            for shop_item in shop_items:
                purchasable = False
                if shop_item == '1 hour':
                    purchasable = True
                shop_items_to_insert.append(ShopItems(item_type=shop_item, item_quantity=0, users_id=user.id, 
                                                    item_used=0, item_bought=0, purchasable=purchasable,
                                                    created_at=timezone.now()))
            ShopItems.objects.bulk_create(shop_items_to_insert)
            resources = ['carbon', 'diamond', 'magic', 'booster', 'power_generator', 'unity-link', 'ticket']
            resources_to_insert = []
            for resource in resources:
                value = 0
                if resource == 'carbon':
                    value = 500
                if resource == 'diamond':
                    value = 500
                if resource == 'booster':
                    value = 1
                if resource == 'unity-link':
                    value = 500
                if resource == 'ticket':
                    value = 5
                resources_to_insert.append(Resources(resource_type=resource, resource_value=value, users_id=user.id, created_at=timezone.now()))
            Resources.objects.bulk_create(resources_to_insert)
            searches = ['life', 'fire', 'shield', 'time', 'electricity', 'energy']
            searches_to_insert = []
            for search in searches:
                carbon_value = 0
                diamond_value = 0
                magic_value = 0
                if search == 'fire':
                    diamond_value = 50
                if search == 'life':
                    carbon_value = 100
                if search == 'shield':
                    magic_value = 20
                    diamond_value = 50
                if search == 'time':
                    carbon_value = 10000
                    magic_value = 1000
                    diamond_value = 5000
                if search == 'electricity':
                    carbon_value = 1000000
                    magic_value = 100000
                    diamond_value = 500000
                if search == 'energy':
                    carbon_value = 1000
                    magic_value = 100
                    diamond_value = 500
                searches_to_insert.append(Searches(search_type=search, search_level=0, users_id=user.id, 
                                                    carbon=carbon_value, diamond=diamond_value,
                                                    magic=magic_value, created_at=timezone.now()))
            Searches.objects.bulk_create(searches_to_insert)
            resources_for_success = ['carbon', 'diamond', 'magic']
            values_success = [1000, 10000, 100000, 1000000, 10000000, 100000000, 1000000000, 10000000000]
            resources_for_success_to_insert = []
            for resource_for_success in resources_for_success:
                for value_success in values_success:

                    resources_for_success_to_insert.append(Success(success_resource_type=resource_for_success, users_id=user.id, 
                                                        success_value=value_success, is_won=False,
                                                        created_at=timezone.now()))
            Success.objects.bulk_create(resources_for_success_to_insert)
            Starship.objects.create(is_built=0, fight_exp=0, users_id=user.id, created_at=timezone.now())
            
            return JsonResponse({'msg': 'Enregistré'})
        except:
            content = {
                'msg': 'Erreur lors de la création de l\'utilisateur'
            }
            return Response(content, status=status.HTTP_400_BAD_REQUEST)


class LoginAPIView(APIView):
    def post(self, request):
        pseudo = escape(request.data['values']['pseudo'])
        password = escape(request.data['values']['password'])
        # supprimer les espaces en trop dans l'email
        # email = email_not_treated.rstrip().lstrip().lower()

        if pseudo != "":
            # on regarde si l'utilisateur est déjà enregistré en bdd
            user = Users.objects.filter(pseudo=pseudo).first()
            # gérer le cas où il n'est pas en bdd
            if user:
                if user.attempts_connection <= 3:    
                    # vérifier la correspondance des mdp
                    pass_bytes = password.encode('utf-8')
                    # print(base64.b64encode(pass_bytes).decode('utf-8'))
                    

                    password_checked = bcrypt.checkpw(pass_bytes, user.password.encode('utf-8'))
                    if not password_checked:
                        Users.objects.filter(pseudo=pseudo).update(attempts_connection=user.attempts_connection + 1)
                        # saveActivity(user.id, "connexion", "Connexion échouée sur l'application", request)
                        raise AuthenticationFailed('Identifiant ou mot de passe incorrect BDD', 400)
                    payload = {
                        'id': user.id,
                        'pseudo': pseudo,
                        # 'nature': user.nature,
                        'exp': dt.datetime.utcnow() + dt.timedelta(days=30),
                        'iat': dt.datetime.utcnow()
                    }
                    token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
                    # sauvegarder le token en bdd
                    Token.objects.create(user_id=user.id, token=token, created_at=timezone.now())

                    Users.objects.filter(pseudo=pseudo).update(last_login=timezone.now())

                    reponseJWT = Response()

                    reponseJWT.data = {
                        'jwt': token,
                        'authenticated': True,
                        'nature': user.nature,
                    }
                    return reponseJWT
                else:
                    content = {
                    'msg': 'Trop de tentatives de connexion'
                }
                return Response(content, status=status.HTTP_403_FORBIDDEN)
            else:
                content = {
                    'msg': 'Utilisateur non trouvé'
                }
                return Response(content, status=status.HTTP_403_FORBIDDEN)
        else:
            content = {
                'msg': 'Pseudo vide'
            }
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
        
class ReinitializeAttemptsAPIView(APIView):
    def get(self, request):
        key = escape(request.GET['key'])
        if key == CRON_KEY:
            Users.objects.all().update(attempts_connection=0)
        return JsonResponse({'msg': 'nombres de connexion réinitialisé'})
    
class VerifyJWTAPIView(APIView):
    def post(self, request):
        token = request.data['jwt']
        # print(token)
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            return JsonResponse({'msg': 'Jeton expiré'})
            return Response('Jeton expiré')
        except:
            return JsonResponse({'msg': "Pas de token"})
            return Response("Pas de token")
        user_id_jwt = payload['id']
        user = Users.objects.filter(id=user_id_jwt).first()

        
        try:
            token = Token.objects.filter(user_id=user_id_jwt, token=token).first()
            # token = Token.objects.filter(user_id=1, token=token).first()

            if token:
                return JsonResponse({'msg': 'Authentifié', 'nature': user.nature, 'pseudo': user.pseudo,
                        "isAdmin": user.is_admin,})
                return Response('Authentifié')
            else:
                return JsonResponse({'msg': 'Pas authentifié', 'nature': None, "isAdmin": False})
                return Response('Pas authentifié')
        except:
            content = {
                'msg': 'Erreur lors de la vérification de l\'authentification de l\'utilisateur'
            }
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
        
class DetermineNatureAPIView(APIView):
    def post(self, request):
        user_id = authenticate(request)
        values = request.data['values']
        
        try:
            user = Users.objects.filter(id=user_id).first()
        
            sotoc_score = 0
            flumia_score = 0
            sora_score = 0
            nano_score = 0
            altheron_score = 0
            description = "Le joueur " + user.pseudo + " a répondu "
            for key, value in values.items():
                if value == 'rb' or value == 'rm':
                    sotoc_score += 1
                if value == 'eb' or value == 'em':
                    flumia_score += 1
                if value == 'ob' or value == 'om':
                    sora_score += 1
                if value == 'ab' or value == 'am':
                    nano_score += 1
                if value == 'sb' or value == 'sm':
                    altheron_score += 1
                description += key + ' : ' + value + ', '
            description = description[:-2]
            # sauvegarder le log des réponses données
            Logs.objects.create(type='joueur', category='alignement', users=user, description=description, target=user.id, created_at=timezone.now())

            score = [{'sotoc': sotoc_score}, {'flumia': flumia_score}, {'sora': sora_score}, 
                    {'nano': nano_score}, {'altheron': altheron_score}]

            # Trouver la valeur maximale
            value_max = max(dict[list(dict.keys())[0]] for dict in score)

            # Récupérer tous les dictionnaires avec la valeur maximale
            bgz_max = [dict for dict in score if dict[list(dict.keys())[0]] == value_max]

            if len(bgz_max) == 1:
                Users.objects.filter(id=user_id).update(nature=list(bgz_max[0].keys())[0])
                return JsonResponse({'bgz': list(bgz_max[0].keys())[0]})
            else:
                return JsonResponse({'bgz': bgz_max})
        except:
            content = {
                'msg': 'Erreur lors de la détermination de l\'alignement BGZ'
            }
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
class SaveNatureAPIView(APIView):
    def post(self, request):
        user_id = authenticate(request)
        try:
            values = request.data['values']
            Users.objects.filter(id=user_id).update(nature=values['choice'])

            user = Users.objects.filter(id=user_id).first()

            description = "Essence du joueur " + user.pseudo + " déterminée : " + values['choice']

            Logs.objects.create(type='joueur', category='alignement', users_id=user_id, description=description, target=user_id, created_at=timezone.now())

            return JsonResponse({'msg': 'alignement sauvegardé'})
            
        except:
            content = {
                'msg': 'Erreur lors de la sauvegarde de l\'alignement BGZ'
            }
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
    
        
