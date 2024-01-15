from rest_framework.exceptions import AuthenticationFailed, APIException
import jwt
from environ import Env
from django.utils.html import escape

from ogame.models import Token, Resources, PlanetsMultiverse

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