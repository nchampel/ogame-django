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
ReinitializationAPIView, SalutAPIView

from ogame.views.views_shop import DetermineDailyHarvestableAPIView, SaveDailyClaimedAPIView, \
SaveLinkUnityAPIView, GetLinkUnityTicketAPIView, GetShopItemsDataAPIView, SaveItemUsingAPIView, \
SaveItemBoughtAPIView, GetDisplayBuildingsShopLevelsAPIView, SaveTicketAPIView, GetPriceWonAPIView, \
SaveItemWonAPIView, SaveUnityLinkInvestedAPIView

from ogame.views.views_planets import GetPlanetsDataAPIView, CreatePlanetsAPIView, SaveResourcesPlanetsAPIView

from ogame.views.views_planets_multiverse import GetPlanetsMultiverseDataAPIView, CreatePlanetsMultiverseAPIView,\
SaveResourcesPlanetsMultiverseAPIView, GetResultsAttackAPIView, SaveDiscoveredPlanetAPIView

from ogame.views.views_starship import GetStarshipDataAPIView, BuildStarshipAPIView, DestroyStarshipAPIView

from ogame.views.views_search import SaveSearchLevelAPIView, GetSearchLevelsAPIView

from ogame.views.views_users import RegisterAPIView, LoginAPIView, ReinitializeAttemptsAPIView,\
VerifyJWTAPIView, DetermineNatureAPIView, SaveNatureAPIView

from ogame.views.views_cron import CronAddResourcesAPIView

from ogame.views.views_ranking import GetRankingAPIView

from ogame.views.views_workshop import SaveLogPowerGeneratorBuiltAPIView

from ogame.views.views_player import SaveResourcesInvestedAPIView, GetIsWebsiteUnderMaintenanceAPIView, \
GetSuccessPlayerAPIView, SaveSuccessPlayerAPIView


from ogame.views.views_test import testAPIView

urlpatterns = [
    path('admin/', admin.site.urls),

    path('salut/', SalutAPIView.as_view()),

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
    # path('planets/multiverse/attack/resources/get/', GetResourcesAttackAPIView.as_view()),
    path('planets/multiverse/discovered/save/', SaveDiscoveredPlanetAPIView.as_view()),
    path('starship/get/', GetStarshipDataAPIView.as_view()),
    path('starship/build/', BuildStarshipAPIView.as_view()),
    path('starship/destroy/', DestroyStarshipAPIView.as_view()),
    path('search/levels/get/', GetSearchLevelsAPIView.as_view()),

    path('planets/create/', CreatePlanetsAPIView.as_view()),
    path('planets/multiverse/create/', CreatePlanetsMultiverseAPIView.as_view()),
    path('reinitialization/', ReinitializationAPIView.as_view()),
    path('subscribe/', RegisterAPIView.as_view()),
    path('login/', LoginAPIView.as_view()),
    path('attempts/reinitialize/', ReinitializeAttemptsAPIView.as_view()),
    path('jwt/verify/', VerifyJWTAPIView.as_view()),
    path('nature/determine/', DetermineNatureAPIView.as_view()),
    path('nature/save/', SaveNatureAPIView.as_view()),
    path('ranking/get/', GetRankingAPIView.as_view()),

    path('unity-link/get/', GetLinkUnityTicketAPIView.as_view()),
    path('unity-link/save/', SaveLinkUnityAPIView.as_view()),
    path('unity-link/invested/save/', SaveUnityLinkInvestedAPIView.as_view()),
    path('ticket/save/', SaveTicketAPIView.as_view()),
    path('unity-link/daily/get/', DetermineDailyHarvestableAPIView.as_view()),
    path('unity-link/daily/save/', SaveDailyClaimedAPIView.as_view()),
    path('shop-items/get/', GetShopItemsDataAPIView.as_view()),
    path('shop-items/using/save/', SaveItemUsingAPIView.as_view()),
    path('shop-items/bought/save/', SaveItemBoughtAPIView.as_view()),
    path('shop-buildings/display/get/', GetDisplayBuildingsShopLevelsAPIView.as_view()),
    path('shop/price/won/get/', GetPriceWonAPIView.as_view()),
    path('shop/item/won/save/', SaveItemWonAPIView.as_view()),

    path('workshop/power/generator/log/save/', SaveLogPowerGeneratorBuiltAPIView.as_view()),

    path('player/resources/invested/save/', SaveResourcesInvestedAPIView.as_view()),
    path('website/maintenance/get/', GetIsWebsiteUnderMaintenanceAPIView.as_view()),
    path('player/success/get/', GetSuccessPlayerAPIView.as_view()),
    path('player/success/save/', SaveSuccessPlayerAPIView.as_view()),
    
    path('cron/resources/add/', CronAddResourcesAPIView.as_view()),
    # path('cron/unity-link/daily/', CronUnityLinkDailyAPIView.as_view()),

    path('test/', testAPIView.as_view()),

]
