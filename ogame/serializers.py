from rest_framework.serializers import ModelSerializer

from ogame.models import Planets, PlanetsMultiverse, Buildings, Resources, Starship, ShopItems

class PlanetsSerializer(ModelSerializer):
    class Meta:
        model = Planets
        fields = '__all__'

class PlanetsMultiverseSerializer(ModelSerializer):
    class Meta:
        model = PlanetsMultiverse
        fields = '__all__'

class ResourcesSerializer(ModelSerializer):
    class Meta:
        model = Resources
        exclude = ['id', 'created_at']

class StarshipSerializer(ModelSerializer):
    class Meta:
        model = Starship
        exclude = ['id', 'created_at']
class ShopItemsSerializer(ModelSerializer):
    class Meta:
        model = ShopItems
        exclude = ['id', 'created_at', 'users']