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

from ogame.models import Users, Token

env = Env()
env.read_env()
SECRET_KEY = env("SECRET_KEY")
CRON_KEY = env("CRON_KEY")

class RegisterAPIView(APIView):
    def post(self, request):
        pseudo = escape(request.data['values']['pseudo'])
        email = escape(request.data['values']['email'])
        password = escape(request.data['values']['password'])

    # on encrypte le mot de passe
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
        password_hashed = hashed.decode('utf-8')

        # data = {
        #     'pseudo': pseudo,
        #     'email': email,
        #     'password': password_hashed,
        # }
        try:
            Users.objects.create(pseudo=pseudo, email=email, password=password_hashed, 
                                 created_at=timezone.now())
            
            return Response('Enregistré')
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

                    password_checked = bcrypt.checkpw(pass_bytes, user.password.encode('utf-8'))
                    if not password_checked:
                        Users.objects.filter(pseudo=pseudo).update(attempts_connection=user.attempts_connection + 1)
                        # saveActivity(user.id, "connexion", "Connexion échouée sur l'application", request)
                        raise AuthenticationFailed('Identifiant ou mot de passe incorrect BDD', 400)
                    payload = {
                        'id': user.id,
                        'pseudo': pseudo,
                        'exp': dt.datetime.utcnow() + dt.timedelta(days=30),
                        'iat': dt.datetime.utcnow()
                    }
                    token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
                    # sauvegarder le token en bdd
                    Token.objects.create(user_id=user.id, token=token, created_at=timezone.now())

                    Users.objects.filter(pseudo=pseudo).update(last_login=timezone.now(), attempts_connection=user.attempts_connection + 1)

                    reponseJWT = Response()

                    reponseJWT.data = {
                        'jwt': token,
                        'authenticated': True
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
        print(token)
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            return Response('Jeton expiré')
        except:
            return Response("Pas de token")
        user_id_jwt = payload['id']

        
        try:
            token = Token.objects.filter(user_id=user_id_jwt, token=token).first()
            # token = Token.objects.filter(user_id=1, token=token).first()

            if token:
            
                return Response('Authentifié')
            else:
                return Response('Pas authentifié')
        except:
            content = {
                'msg': 'Erreur lors de la vérification de l\'authentification de l\'utilisateur'
            }
            return Response(content, status=status.HTTP_400_BAD_REQUEST)