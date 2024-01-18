from rest_framework.exceptions import AuthenticationFailed, APIException
import jwt
from environ import Env
from django.utils.html import escape
from django.db.models import Case, When, Value, IntegerField, F
from typing import Dict

from ogame.models import Token, Resources, PlanetsMultiverse, Users

# Get JWT secret key
env = Env()
env.read_env()
SECRET_KEY = env("SECRET_KEY")

def authenticate(request):
        
        jwt_token = request.headers.get('Authorization', None)

        if not jwt_token:
            raise AuthenticationFailed('Pas de jwt token !')

        token = jwt_token[7:]

        # if not "user_id" in request.data:
        #     raise AuthenticationFailed('Pas d\'id renseigné !')

        # user_id = escape(request.data['user_id'])
        jwt_token = request.headers.get('authorization', None)

        if not jwt_token:
            raise AuthenticationFailed('Non authentifié !')

                # soustraire le "Bearer " devant le jwt
        token = jwt_token[7:]

        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
            user_id = payload['id']
            # if int(user_id) != int(user_id_jwt):
            #     raise AuthenticationFailed('Ids différents !')
            isTokenInDB = False
            tokensInDB = Token.objects.filter(user_id=user_id)
            for tokenInDB in tokensInDB:
                if tokenInDB.token == token:
                    isTokenInDB = True
            if not isTokenInDB:
                raise AuthenticationFailed('Token absent de la BDD !')
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Jeton expiré !')
            # raise MyCustomExceptionCode401('Jeton expiré !')
        except (jwt.DecodeError, jwt.InvalidTokenError):
            raise AuthenticationFailed('JWT non valide !')
        
def handleResourcesAttackedPlanet(planet, resources, user_id):
    # print(resources)
    # à tester
    for key, _ in resources.items():
        # print(key, value)
        resources[key] += round(planet[key] / 2)
        Resources.objects.filter(user_id=user_id, resource_type=key).update(resource_value=resources[key])

    # resources['metal'] += planet['metal']
    # resources['crystal'] += planet['crystal']
    # resources['deuterium'] += planet['deuterium']
    # Resources.objects.filter(id=user_id).update(metal=resources['metal'],
    #                     crystal=resources['crystal'], deuterium=resources['deuterium'])
    PlanetsMultiverse.objects.filter(id=planet['id']).update(metal=round(planet['metal'] / 2), 
                                                             crystal=round(planet['crystal'] / 2), 
                                                             deuterium=round(planet['deuterium'] / 2))
    
def saveResources(user: Users, resources: Dict[str, int]):
    types = ['metal', 'crystal', 'deuterium']
    
    updates = []

    for resource in resources:
        for r_type in types:
            if r_type in resource:
                valeur_ressource = resource[r_type]
                update_condition = When(resource_type=r_type, then=Value(valeur_ressource))
                updates.append(update_condition)

    # Appliquer la mise à jour en une seule requête
    Resources.objects.filter(users=user.id).update(
        resource_value=Case(*updates, default=F('resource_value'), output_field=IntegerField())
    )