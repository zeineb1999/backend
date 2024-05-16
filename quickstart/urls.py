from django.contrib import admin
from django.urls import path
from django.urls import include, path
from rest_framework import routers
from rest_framework.urlpatterns import format_suffix_patterns
from .views import CustomTokenObtainPairView,excel_data_api, EquipementsTotalConsommation, zonesTotalConsommation
from .views import *
from quickstart import views
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.urls import re_path
from .views import AlertConsumer  # Importez votre consommateur WebSocket
websocket_urlpatterns = [
 re_path(r'ws/chat/notification_test/$', AlertConsumer.as_asgi() ),
 re_path(r'ws/user-id-change/$', UserIDChangeConsumer.as_asgi()),
 #re_path(r'ws/dataminute/$', LocalConsumer.as_asgi()),
]

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'profileUser', views.ProfileUserViewSet)
router.register(r'zones', views.ZoneViewSet)
router.register(r'equipement', views.EquipementViewSet)
router.register(r'etage', views.EtageViewSet)
router.register(r'batiment', views.BatimentViewSet)
router.register(r'alerte', views.AlerteViewSet)
router.register(r'periode-activite', views.PeriodeActiviteViewSet)
router.register(r'rapport', views.RapportViewSet)
# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.

urlpatterns = [
    path('profile/', views.ProfileView.as_view()),
    path('deleteUser/<int:user_Id>', views.deleteUser, name='delete_user'),
    path('Allusers/', views.Allusers.as_view()),
    path('hopital_consommation_pendant_mois', HopitalConsommationPendantMois.as_view(), name='hopital_consommation'),
    path('equipement-consommation-p/<int:equipement_id>/', EquipementConsommationParPeriode.as_view(), name='equipement_consommation'),
    path('', include(router.urls)),
    path('getRole/<int:user_Id>/', views.get_role, name='get_role'),
    path('api/token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('getId/<str:username>/', views.get_id, name='get_id'),
    path('zones/<int:zone_id>/equipements/', views.equipements_by_zone, name='equipements_by_zone'),
    path('etage/<int:etage_id>/zones/', views.zones_by_etage, name='zones_by_etage'),
    path('read-csv/<str:file_path>/', views.read_csv, name='read_csv'),
    path('excel-data/', excel_data_api, name='excel_data_api'),
    path('equipements/consommation_totale/', EquipementsTotalConsommation.as_view(), name='tous_equipements_consommation'),
    path('batiment/<int:batiment_id>/etages/', views.etages_by_batiment, name='etages_by_batiment'),
    path('batiment-id/<str:nom_batiment>/', get_batiment_id, name='get_batiment_id'),
    path('etage-id/<str:nom_etage>/', get_etage_id, name='get_etage_details'),
    path('zone_consommation_totale/', zonesTotalConsommation.as_view(), name='tous_zones_consommation'),
    path('batiment_consommation_totale/', batimentsTotalConsommation.as_view(), name='tous_batiments_consommation'),
    path('etage_consommation_totale/<int:batiment_id>', etagesTotalConsommation.as_view(), name='tous_etages_consommation'),
    path('equipement-consommation-p/', EquipementsConsommationParPeriode.as_view(), name='equipement_consommation'),
    path('equipement-consommation-seulement-p/', EquipementsOnlyConsommationParPeriode.as_view(), name='equipement_consommation'),
    path('zone-consommation-p/', localConsommationParPeriode.as_view(), name='zone_consommation'),
    path('batiment-consommation-p/', batimentConsommationParPeriode.as_view(), name='zone_consommation'),
    path('etage-consommation-p/<int:batiment_id>/', etagesConsommationParPeriode.as_view(), name='zone_consommation'),
    path('hopital_consommation_par_mois', hopitalConsommationParMois.as_view(), name='zone_consommation'),
    path('send-reset-password-email/',ChangePasswordEmail.as_view(),name="send_reset_password_email"),
    path('reset_password_avec_uid/<uidb64>/<token>/', reset_password_avec_uid, name='reset_password'),
    path('send-reset-password-email/',ChangePasswordEmail.as_view(),name="send_reset_password_email"),
    #path('ChangePassword/', ChangePassword.as_view(), name="ChangePassword"),
    path('modificationProfile/',UpdateEmail.as_view(),name="send_reset_password_email"),
    path('genererDATA/', generateExcel.as_view(), name="genererDATA"),
    path('rechercher_donnees/', rechercher_donnees.as_view(), name="rechercher_donnees"),
    #path('batiment-details/', batiment_details.as_view(), name="batiment_details"),
    path('batimentsList/', get_batiments_with_etages_zones, name='batiment-list'),
    path('recuperer/',get_json,  name='etages-list'),
    path('avg_TH_par_heure/',get_TH_par_heure,  name='avg_TH_par_heure'),
    path('avg_TH_par_jour/',get_TH_par_jour,  name='avg_TH_par_jour'),
    path('avg_TH_par_instant/',get_TH_par_instant,  name='avg_TH_par_instant'),
    path('alerteById',get_alerte_by_id.as_view(),  name='get_alerte_by_id'),
    path('alerteSansId',get_alerte_sans_id.as_view(),  name='get_alerte_sans_id'),
    
    path('addUserAlerte',add_user_alerte.as_view(),  name='add_user_alerte'),
    path('notifierAlerte',notifier_alerte.as_view(),  name='notifier_alerte'),
   
    path('get_alerte_non_notifie/', GetAlerteNonNotifie.as_view(), name='get_alerte_non_notifie'),
    path('getTenAlertes', views.getTenAlertes, name='getTenAlertes'),
   
    path('rapportByEquipement/<int:equipementId>/', views.getRapportByEquipement, name='getAlertes'),
    path('stop-method/', stop_method_view, name='stop-method'),
    path('start-method/', start_method_view, name='start-method'),
    path('rapportByAlerte/<int:alerteId>/', views.getRapportByAlerte, name='getRapports'),
    path('initialData/', initialData.as_view(), name='initialData'),
   
  ]

urlpatterns += router.urls