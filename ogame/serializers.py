from rest_framework.serializers import ModelSerializer

from ogame.models import Planets, PlanetsMultiverse

class PlanetsSerializer(ModelSerializer):
    class Meta:
        model = Planets
        fields = '__all__'

class PlanetsMultiverseSerializer(ModelSerializer):
    class Meta:
        model = PlanetsMultiverse
        fields = '__all__'