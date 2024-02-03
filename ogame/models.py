from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser


# from users.managers import CustomUserManager

# class Users(models.Model):
#     pseudo = models.fields.CharField(max_length=50, blank=True, null=False)
#     email = models.fields.EmailField(max_length=100, blank=True, null=False)
#     password = models.fields.CharField(max_length=100, blank=True, null=False)
#     attempts_connection = models.fields.IntegerField(default=0, blank=True, null=True)
#     nature = models.fields.CharField(max_length=50, default=None, blank=True, null=True)
#     created_at = models.fields.DateTimeField(max_length=0)
#     last_login = models.fields.DateTimeField(max_length=0, default=None, blank=True, null=True)
#     class Meta:
#         db_table = "users"

class Users(AbstractBaseUser):
    password = models.fields.CharField(max_length=255, default=None, blank=True, null=True)
    pseudo = models.fields.CharField(max_length=50, blank=True, null=False, unique=True)
    email = models.fields.EmailField(max_length=100, blank=True, null=False)
    attempts_connection = models.fields.IntegerField(default=0, blank=True, null=True)
    nature = models.fields.CharField(max_length=50, default=None, blank=True, null=True)
    created_at = models.fields.DateTimeField(max_length=0)
    username = None

    USERNAME_FIELD = 'pseudo'
    REQUIRED_FIELDS = []

    # test enregistrement user en BDD
    # objects = CustomUserManager()
    class Meta:
        db_table = "users"

class Token(models.Model):
    token = models.fields.TextField()
    user_id = models.fields.IntegerField()
    created_at = models.fields.DateTimeField(default=timezone.now, blank=True, null=True, max_length=0)
    class Meta:
        db_table = "token"

class Resources(models.Model):
    # users = models.ForeignKey(Users, on_delete=models.CASCADE)
    # metal = models.fields.BigIntegerField(default=0, blank=True, null=True)
    # crystal = models.fields.BigIntegerField(default=0, blank=True, null=True)
    # tritium = models.fields.BigIntegerField(default=0, blank=True, null=True)
    # satellites = models.fields.IntegerField(default=0, blank=True, null=True)
    # booster = models.fields.IntegerField(default=1, blank=True, null=True)
    resource_type = models.fields.CharField(max_length=50, default=None, blank=True, null=True)
    resource_value = models.fields.BigIntegerField(default=0, blank=True, null=True)
    harvestable = models.fields.BooleanField(default=0, blank=True, null=True)
    # user_id = models.fields.IntegerField(default=1, blank=True, null=True)
    users = models.ForeignKey(Users, on_delete=models.CASCADE, default=None, blank=True, null=True)
    updated_at = models.fields.DateTimeField(max_length=0, default=None, blank=True, null=True)
    harvested_at = models.fields.DateTimeField(max_length=0, default=None, blank=True, null=True)
    created_at = models.fields.DateTimeField(max_length=0)
    class Meta:
        db_table = "resources"

class Buildings(models.Model):
    # users = models.ForeignKey(Users, on_delete=models.CASCADE)
    building_type = models.fields.CharField(max_length=50, default=None, blank=True, null=True)
    building_level = models.fields.IntegerField(default=0, blank=True, null=True)
    # metal = models.fields.IntegerField(default=0, blank=True, null=True)
    # crystal = models.fields.IntegerField(default=0, blank=True, null=True)
    # tritium = models.fields.IntegerField(default=0, blank=True, null=True)
    # energy = models.fields.IntegerField(default=0, blank=True, null=True)
    # booster = models.fields.IntegerField(default=1, blank=True, null=True)
    # life_level = models.fields.IntegerField(default=0, blank=True, null=True)
    # fire_level = models.fields.IntegerField(default=0, blank=True, null=True)
    # shield_level = models.fields.IntegerField(default=0, blank=True, null=True)
    # user_id = models.fields.IntegerField(default=1, blank=True, null=True)
    users = models.ForeignKey(Users, on_delete=models.CASCADE, default=None, blank=True, null=True)
    created_at = models.fields.DateTimeField(max_length=0)
    class Meta:
        db_table = "buildings"

# pas utilisé
class BuildingsResources(models.Model):
    # users = models.ForeignKey(Users, on_delete=models.CASCADE)
    type = models.fields.CharField(max_length=50)
    metal = models.fields.IntegerField(default=0, blank=True, null=True)
    crystal = models.fields.IntegerField(default=0, blank=True, null=True)
    tritium = models.fields.IntegerField(default=0, blank=True, null=True)
    energy = models.fields.IntegerField(default=0, blank=True, null=True)
    resource_to_add = models.fields.IntegerField(default=0, blank=True, null=True)
    created_at = models.fields.DateTimeField(max_length=0)
    class Meta:
        db_table = "buildings_resources"

class Boosters(models.Model):
    # users = models.ForeignKey(Users, on_delete=models.CASCADE)
    coefficient = models.fields.IntegerField(default=0, blank=True, null=True)
    cost = models.fields.BigIntegerField(default=0, blank=True, null=True)

    class Meta:
        db_table = "boosters"

class Planets(models.Model):
    # users = models.ForeignKey(Users, on_delete=models.CASCADE)
    name = models.fields.CharField(max_length=50)
    metal = models.fields.BigIntegerField(default=0, blank=True, null=True)
    crystal = models.fields.BigIntegerField(default=0, blank=True, null=True)
    tritium = models.fields.BigIntegerField(default=0, blank=True, null=True)
    metal_level = models.fields.IntegerField(default=0, blank=True, null=True)
    crystal_level = models.fields.IntegerField(default=0, blank=True, null=True)
    tritium_level = models.fields.IntegerField(default=0, blank=True, null=True)
    # user_id = models.fields.IntegerField(default=1, blank=True, null=True)
    users = models.ForeignKey(Users, on_delete=models.CASCADE,default=None, blank=True, null=True)
    created_at = models.fields.DateTimeField(max_length=0, default=None, blank=True, null=True)
    updated_at = models.fields.DateTimeField(max_length=0, default=None, blank=True, null=True)

    class Meta:
        db_table = "planets"

class PlanetsMultiverse(models.Model):
    # users = models.ForeignKey(Users, on_delete=models.CASCADE)
    name = models.fields.CharField(max_length=50)
    type = models.fields.CharField(max_length=50)
    metal = models.fields.BigIntegerField(default=0, blank=True, null=True)
    crystal = models.fields.BigIntegerField(default=0, blank=True, null=True)
    tritium = models.fields.BigIntegerField(default=0, blank=True, null=True)
    metal_level = models.fields.IntegerField(default=0, blank=True, null=True)
    crystal_level = models.fields.IntegerField(default=0, blank=True, null=True)
    tritium_level = models.fields.IntegerField(default=0, blank=True, null=True)
    # has_headquarter = models.fields.BooleanField(default=0, blank=True, null=True)
    life_level = models.fields.IntegerField(default=0, blank=True, null=True)
    fire_level = models.fields.IntegerField(default=0, blank=True, null=True)
    shield_level = models.fields.IntegerField(default=0, blank=True, null=True)
    # user_id = models.fields.IntegerField(default=1, blank=True, null=True)
    # users = models.ForeignKey(Users, on_delete=models.CASCADE)
    is_discovered = models.fields.BooleanField(default=0, blank=True, null=True)
    updated_at = models.fields.DateTimeField(max_length=0, default=None, blank=True, null=True)
    created_at = models.fields.DateTimeField(max_length=0, default=None, blank=True, null=True)

    class Meta:
        db_table = "planets_multiverse"

# class Fight(models.Model):
#     round = models.fields.IntegerField(default=0, blank=True, null=True)
#     life_points_starship = models.fields.IntegerField(default=0, blank=True, null=True)
#     life_points_enemy = models.fields.IntegerField(default=0, blank=True, null=True)
#     fire_starship = models.fields.IntegerField(default=0, blank=True, null=True)
#     fire_enemy = models.fields.IntegerField(default=0, blank=True, null=True)
#     shield_starship = models.fields.IntegerField(default=0, blank=True, null=True)
#     shield_enemy = models.fields.IntegerField(default=0, blank=True, null=True)
#     winner = models.fields.CharField(max_length=50, default=None, blank=True, null=True)

#     class Meta:
#         db_table = "fight"

class Starship(models.Model):
    is_built = models.fields.BooleanField(default=0, blank=True, null=True)
    # life_level = models.fields.IntegerField(default=0, blank=True, null=True)
    # fire_level = models.fields.IntegerField(default=0, blank=True, null=True)
    # shield_level = models.fields.IntegerField(default=0, blank=True, null=True)
    # search_type = models.fields.CharField(max_length=50, default=None, blank=True, null=True)
    # search_level = models.fields.IntegerField(default=0, blank=True, null=True)
    fight_exp = models.fields.IntegerField(default=0, blank=True, null=True)
    # user_id = models.fields.IntegerField(default=1, blank=True, null=True)
    users = models.ForeignKey(Users, on_delete=models.CASCADE, default=None, blank=True, null=True)
    created_at = models.fields.DateTimeField(max_length=0)
    class Meta:
        db_table = "starship"

class Searches(models.Model):
    # users = models.ForeignKey(Users, on_delete=models.CASCADE)
    search_type = models.fields.CharField(max_length=50, default=None, blank=True, null=True)
    search_level = models.fields.IntegerField(default=0, blank=True, null=True)
    metal = models.fields.BigIntegerField(default=0, blank=True, null=True)
    crystal = models.fields.BigIntegerField(default=0, blank=True, null=True)
    tritium = models.fields.BigIntegerField(default=0, blank=True, null=True)
    # user_id = models.fields.IntegerField(default=1, blank=True, null=True)
    users = models.ForeignKey(Users, on_delete=models.CASCADE,default=None, blank=True, null=True)
    created_at = models.fields.DateTimeField(max_length=0)
    class Meta:
        db_table = "searches"

class Logs(models.Model):
    description = models.fields.TextField(default=None, blank=True, null=True)
    target = models.fields.IntegerField(default=None, blank=True, null=True)
    users = models.ForeignKey(Users, on_delete=models.RESTRICT, default=None, blank=True, null=True)
    type = models.fields.CharField(max_length=50)
    category = models.fields.CharField(max_length=50)
    created_at = models.fields.DateTimeField(default=None, blank=True, null=True, max_length=0)
    class Meta:
        db_table = "logs"
