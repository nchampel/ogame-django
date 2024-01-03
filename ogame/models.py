from django.db import models

class Resources(models.Model):
    # users = models.ForeignKey(Users, on_delete=models.CASCADE)
    metal = models.fields.IntegerField(default=0, blank=True, null=True)
    crystal = models.fields.IntegerField(default=0, blank=True, null=True)
    deuterium = models.fields.IntegerField(default=0, blank=True, null=True)
    energy = models.fields.IntegerField(default=0, blank=True, null=True)
    created_at = models.fields.DateTimeField(max_length=0)
    class Meta:
        db_table = "resources"

class Buildings(models.Model):
    # users = models.ForeignKey(Users, on_delete=models.CASCADE)
    metal = models.fields.IntegerField(default=0, blank=True, null=True)
    crystal = models.fields.IntegerField(default=0, blank=True, null=True)
    deuterium = models.fields.IntegerField(default=0, blank=True, null=True)
    energy = models.fields.IntegerField(default=0, blank=True, null=True)
    booster = models.fields.IntegerField(default=1, blank=True, null=True)
    life_level = models.fields.IntegerField(default=1, blank=True, null=True)
    fire_level = models.fields.IntegerField(default=1, blank=True, null=True)
    shield_level = models.fields.IntegerField(default=1, blank=True, null=True)
    created_at = models.fields.DateTimeField(max_length=0)
    class Meta:
        db_table = "buildings"

class BuildingsResources(models.Model):
    # users = models.ForeignKey(Users, on_delete=models.CASCADE)
    type = models.fields.CharField(max_length=50)
    metal = models.fields.IntegerField(default=0, blank=True, null=True)
    crystal = models.fields.IntegerField(default=0, blank=True, null=True)
    deuterium = models.fields.IntegerField(default=0, blank=True, null=True)
    energy = models.fields.IntegerField(default=0, blank=True, null=True)
    resource_to_add = models.fields.IntegerField(default=0, blank=True, null=True)
    created_at = models.fields.DateTimeField(max_length=0)
    class Meta:
        db_table = "buildings_resources"

class Boosters(models.Model):
    # users = models.ForeignKey(Users, on_delete=models.CASCADE)
    coefficient = models.fields.IntegerField(default=0, blank=True, null=True)
    cost = models.fields.IntegerField(default=0, blank=True, null=True)

    class Meta:
        db_table = "boosters"

class Planets(models.Model):
    # users = models.ForeignKey(Users, on_delete=models.CASCADE)
    name = models.fields.CharField(max_length=50)
    metal = models.fields.IntegerField(default=0, blank=True, null=True)
    crystal = models.fields.IntegerField(default=0, blank=True, null=True)
    deuterium = models.fields.IntegerField(default=0, blank=True, null=True)
    metal_level = models.fields.IntegerField(default=0, blank=True, null=True)
    crystal_level = models.fields.IntegerField(default=0, blank=True, null=True)
    deuterium_level = models.fields.IntegerField(default=0, blank=True, null=True)

    class Meta:
        db_table = "planets"

class PlanetsMultiverse(models.Model):
    # users = models.ForeignKey(Users, on_delete=models.CASCADE)
    name = models.fields.CharField(max_length=50)
    type = models.fields.CharField(max_length=50)
    metal = models.fields.IntegerField(default=0, blank=True, null=True)
    crystal = models.fields.IntegerField(default=0, blank=True, null=True)
    deuterium = models.fields.IntegerField(default=0, blank=True, null=True)
    metal_level = models.fields.IntegerField(default=0, blank=True, null=True)
    crystal_level = models.fields.IntegerField(default=0, blank=True, null=True)
    deuterium_level = models.fields.IntegerField(default=0, blank=True, null=True)
    has_headquarter = models.fields.BooleanField(default=0, blank=True, null=True)
    life_level = models.fields.IntegerField(default=0, blank=True, null=True)
    fire_level = models.fields.IntegerField(default=0, blank=True, null=True)
    shield_level = models.fields.IntegerField(default=0, blank=True, null=True)
    is_discovered = models.fields.BooleanField(default=0, blank=True, null=True)

    class Meta:
        db_table = "planets_multiverse"
