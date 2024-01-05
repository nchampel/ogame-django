"""
URL configuration for ogame_django project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from ogame.views.views_planet import GetResourcesAPIView, SaveResourcesAPIView, GetBuildingsAPIView, \
GetBuildingsResourcesAPIView, SaveLevelAPIView, GetBoosterCostAPIView, SaveBoosterCoefficientAPIView, \
ReinitializationAPIView, SaveSearchLevelAPIView

from ogame.views.views_planets import GetPlanetsDataAPIView, CreatePlanetsAPIView, SaveResourcesPlanetsAPIView

from ogame.views.views_planets_multiverse import GetPlanetsMultiverseDataAPIView, CreatePlanetsMultiverseAPIView,\
SaveResourcesPlanetsMultiverseAPIView, GetResultsAttackAPIView

from ogame.views.views_starship import GetStarshipDataAPIView, BuildStarshipAPIView, DestroyStarshipAPIView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('resources/get/', GetResourcesAPIView.as_view()),
    path('buildings/get/', GetBuildingsAPIView.as_view()),
    # pas utilisé
    path('buildings-resources/get/', GetBuildingsResourcesAPIView.as_view()),
    path('resources/save/', SaveResourcesAPIView.as_view()),
    path('level/save/', SaveLevelAPIView.as_view()),
    path('search/level/save/', SaveSearchLevelAPIView.as_view()),
    path('booster/cost/get/', GetBoosterCostAPIView.as_view()),
    path('booster/coefficient/save/', SaveBoosterCoefficientAPIView.as_view()),
    path('planets/get/', GetPlanetsDataAPIView.as_view()),
    path('planets/resources/save/', SaveResourcesPlanetsAPIView.as_view()),
    path('planets/multiverse/get/', GetPlanetsMultiverseDataAPIView.as_view()),
    path('planets/multiverse/resources/save/', SaveResourcesPlanetsMultiverseAPIView.as_view()),
    path('planets/multiverse/attack/results/get/', GetResultsAttackAPIView.as_view()),
    path('starship/get/', GetStarshipDataAPIView.as_view()),
    path('starship/build/', BuildStarshipAPIView.as_view()),
    path('starship/destroy/', DestroyStarshipAPIView.as_view()),

    path('planets/create/', CreatePlanetsAPIView.as_view()),
    path('planets/multiverse/create/', CreatePlanetsMultiverseAPIView.as_view()),
    path('reinitialization/', ReinitializationAPIView.as_view()),

]
