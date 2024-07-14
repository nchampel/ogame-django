from rest_framework.exceptions import AuthenticationFailed, APIException
import jwt
from environ import Env
from django.utils.html import escape
from django.db.models import Case, When, Value, IntegerField, F
from typing import Dict, List

from ogame.models import Token, Resources, PlanetsMultiverse, Planets

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
            return user_id
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Jeton expiré !')
            # raise MyCustomExceptionCode401('Jeton expiré !')
        except (jwt.DecodeError, jwt.InvalidTokenError):
            raise AuthenticationFailed('JWT non valide !')
        
def handleResourcesAttackedPlanet(planet: Dict[str, int], resources: Dict[str, int], user_id: int):
    # print(resources)
    # à tester, vérifier le typage
    for key, _ in resources.items():
        # print(key, value)
        resources[key] += round(planet[key] / 2)
        Resources.objects.filter(user_id=user_id, resource_type=key).update(resource_value=resources[key])

    # resources['metal'] += planet['metal']
    # resources['crystal'] += planet['crystal']
    # resources['tritium'] += planet['tritium']
    # Resources.objects.filter(id=user_id).update(metal=resources['metal'],
    #                     crystal=resources['crystal'], tritium=resources['tritium'])
    PlanetsMultiverse.objects.filter(id=planet['id']).update(carbon=round(planet['carbon'] / 2), 
                                                             diamond=round(planet['diamond'] / 2), 
                                                             magic=round(planet['magic'] / 2))
    
def saveResourcesPlayer(types: List[str], resources_player: Dict[str, int]):

    resources_to_update = []
    # print('resources_player', resources_player)
    for resource_player in resources_player:
            # print('resource_player', resource_player)
            for r_type in types:
                resource_type, _ = resource_player
                # print('tz', resource_player[updated].replace(tzinfo=None, microsecond=0))
                # print('tzt', resource_player[updated])
                # print('tzs', (timezone.now().replace(tzinfo=None, microsecond=0).replace(tzinfo=None, microsecond=0)).total_seconds())
                # print('up', (resource_player[updated].replace(tzinfo=None, microsecond=0)).total_seconds())
                # print('seconds', (timezone.now().replace(tzinfo=None, microsecond=0) - resource_player[updated].replace(tzinfo=None, microsecond=0)).total_seconds())
                # print((timezone.now() - resource_player[updated]).total_seconds() > 60.0 )
                # print('resource_type', resource_type)
                updated_instance = None
                if r_type == resource_type:
                        # print('rtype')
                        valeur_ressource = resource_player[r_type]
                        update_condition = When(resource_type=r_type, then=Value(valeur_ressource))

                        # Créer une instance mise à jour pour chaque utilisateur
                        updated_instance = Resources(
                            id=resource_player['id'],
                            resource_value=Case(update_condition, default=F('resource_value'), output_field=IntegerField(),
                            # updated_at=timezone.now()
                            )
                        )
                if updated_instance is not None: 
                    resources_to_update.append(updated_instance)

    return resources_to_update

def saveResourcesPlanets(resources_planet: Dict[str, int]):

    resources_to_update = []
    
    for resource_planet in resources_planet:
        resource_planet_without_id = resource_planet.copy()
        del resource_planet_without_id['id']
        updated_instance = Planets(
            id=resource_planet['id'],
            **{key: value for key, value in resource_planet_without_id.items()}
        ) 
        resources_to_update.append(updated_instance)

    return resources_to_update

def saveResourcesPlanetsMultiverse(resources_planet: Dict[str, int]):

    resources_to_update = []
    
    for resource_planet in resources_planet:
        resource_planet_without_id = resource_planet.copy()
        del resource_planet_without_id['id']
        updated_instance = PlanetsMultiverse(
            id=resource_planet['id'],
            **{key: value for key, value in resource_planet_without_id.items()}
        ) 
        resources_to_update.append(updated_instance)

    return resources_to_update
                