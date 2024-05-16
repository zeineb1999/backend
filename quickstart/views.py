from django.contrib.auth.models import  User
from rest_framework import permissions, viewsets
from rest_framework.response import Response
from .serializers import *
from .models import *
from rest_framework import status
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404, render
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import EquipementSerializer
from rest_framework import generics
class RapportViewSet(viewsets.ModelViewSet):
    queryset = Rapport.objects.all()
    serializer_class = RapportSerializer

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer

class Allusers(APIView):

    def get(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)

        return Response(serializer.data)

class ProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        profile_data = {
            'id': user.id,
            'username': user.username,
            'firstname': user.first_name,
            'lastname': user.last_name,
           'password': user.password.encode('utf-8'),
            'email': user.email,
        }
        #print("profile_data : ", profile_data)
        return Response(profile_data)
    def put(self, request):

        user = request.user
        """print("username : ", request.data.get('username'))
        print("firstname : ", request.data.get('firstname'))
        print("lastname : ", request.data.get('lastname')) """

        new_username = request.data.get('username')
        new_firstname = request.data.get('firstname')
        new_lastname = request.data.get('lastname')
        new_email = request.data.get('email')
        #if(new_username != None):
            #user.username = new_username
        user.username = new_username
        user.first_name = new_firstname

        user.last_name = new_lastname
        user.email =new_email
        user.save()
        return Response({'message': 'Profil mis à jour avec succès'})
    

from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import User

@api_view(['DELETE'])
def deleteUser(request, user_Id):
    try:
        # Récupérer le profil de l'utilisateur par user_id
        user = get_object_or_404(User, id=user_Id)
        user.delete()
        return Response(status=204)  # No Content
    except User.DoesNotExist:
        return Response(status=404)  # Not Found


class CustomAuthToken(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'username': user.username,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'user_id': user.pk,
            'email': user.email
        })

#               ******************************************* Models views *******************************************

class ZoneViewSet(viewsets.ModelViewSet):
    queryset = Zone.objects.all()
    serializer_class = ZoneSerializer

    def list(self, request, *args, **kwargs):
        zones = Zone.objects.all()
        serializer = ZoneSerializer(zones, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            # Récupérer l'ID de l'élément ajouté
            zone_id = serializer.data.get('id')
            return Response({'id': zone_id}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class EquipementViewSet(viewsets.ModelViewSet):
    queryset = Equipement.objects.all()
    serializer_class = EquipementSerializer
    def list(self, request, *args, **kwargs):
        equipements = Equipement.objects.all()
        serializer =EquipementSerializer(equipements, many=True)
        return Response(serializer.data)


class BatimentViewSet(viewsets.ModelViewSet):
    queryset = Batiment.objects.all()
    serializer_class = BatimentSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            batiment_id = serializer.data.get('id')
            return Response({'id': batiment_id}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def list(self, request, *args, **kwargs):
        batiments = Batiment.objects.all()
        serializer = BatimentSerializer(batiments, many=True)
        return Response(serializer.data)
''' ************************************* webbbbbbbbbbbbbbbbbbbb socket ************************************* '''
from channels.generic.websocket import AsyncWebsocketConsumer
import json
import asyncio
from channels.generic.websocket import AsyncWebsocketConsumer

from channels.generic.websocket import AsyncWebsocketConsumer
import json
from django.db.models.signals import post_save
from django.dispatch import receiver
from channels.layers import get_channel_layer
from .models import Alerte
import json

from channels.generic.websocket import WebsocketConsumer
import json
""" class AlertConsumer(WebsocketConsumer):
  def connect(self):
    self.room_name = 'test'
    self.room_group_name = self.room_name
    async_to_sync(self.channel_layer.group_add)(
    self.room_group_name, self.channel_name)
    self.accept()
  def disconnect(self, close_code):
  # Leave room group
    async_to_sync(self.channel_layer.group_discard)(
    self.room_group_name,
    self.channel_name
    )
  # broadcast Notification; Individual + community
  def broadcast_notification_message(self, event):
    print('event  envoi', event)
    message = event['message']
    self.send(text_data=json.dumps({ 
    'message': message
    }))

@receiver(post_save, sender=Alerte)
def notification_post_save(sender, instance, created, **kwargs):
  if created:
    serailize = AlerteSerializer(instance)
    channel_layer = get_channel_layer()
    group_name = 'test'
    async_to_sync(channel_layer.group_send)(
      group_name, {
      'type': 'broadcast_notification_message',
      'message': serailize.data
      }
    )
    print('group_name', group_name)
 """
class AlertConsumer(WebsocketConsumer):
  def connect(self):
    self.room_name = 'test'
    self.room_group_name = self.room_name
    async_to_sync(self.channel_layer.group_add)(
    self.room_group_name, self.channel_name)
    self.accept()
    self.is_running = True
    self.send_data()
  def disconnect(self, close_code):
  # Leave room group
    self.is_running = False
    async_to_sync(self.channel_layer.group_discard)(
    self.room_group_name,
    self.channel_name
    )
  def send_data(self):
        #print('send_data')
    if self.is_running:
            #print('send_data running')
      self.check_conditions_and_create_alerts()

      Timer(60, self.send_data).start()
  def check_conditions_and_create_alerts(self):
        print('check_conditions_and_create_alerts chaque minute')
        locaux = Zone.objects.all()
        date_recherchee = datetime.now().strftime('%Y-%m-%d %H:%M:00')
        for local in locaux:
            nom_fichier_json = f"{local.id}"
            chemin_fichier = os.path.join('media', 'donnees' + str(nom_fichier_json) + '.json')
            if os.path.exists(chemin_fichier):
                with open(chemin_fichier, 'r') as fichier:
                    contenu_json = json.load(fichier)
                if date_recherchee in contenu_json:
                    temperature = contenu_json[date_recherchee]["temperature"]
                    humidite = contenu_json[date_recherchee]["humidite"]
                    if temperature < local.minT or temperature > local.maxT :
                        print('cas temperature : ', temperature, 'local : ', local)
                        self.create_alert(local, temperature, "temperature")
                    if humidite < local.minH or humidite > local.maxH:
                        print('cas humidite : ', humidite, 'local : ', local)
                        self.create_alert(local,humidite, "humidite" )

  def create_alert(self, local, temperature, type):
        if type == "temperature":
          alert = Alerte(
              type='temperature',

              localId=local,
              valeur=temperature,
             
              text=f"Alert! Temperature: {temperature}  out of range."
          )
        elif type == "humidite":
          alert = Alerte(
              type='humidite',

              localId=local,
              valeur=temperature,
             
              text=f"Alert! humidité: {temperature}  out of range."
          )
        alert.save() 
  # broadcast Notification; Individual + community
  def broadcast_notification_message(self, event):
    print('event  envoi', event)
    message = event['message']
    self.send(text_data=json.dumps({ 
    'message': message
    }))

@receiver(post_save, sender=Alerte)
def notification_post_save(sender, instance, created, **kwargs):
  if created:
    serailize = AlerteSerializer(instance)
    channel_layer = get_channel_layer()
    group_name = 'test'
    async_to_sync(channel_layer.group_send)(
      group_name, {
      'type': 'broadcast_notification_message',
      'message': serailize.data
      }
    )
    print('group_name', group_name)
#------------------------------------------------------- alerte to maintenance ---------------------------
class UserIDChangeConsumer(WebsocketConsumer):
  def connect(self):
    self.room_name = 'user_id_change'
    self.room_group_name = self.room_name
    async_to_sync(self.channel_layer.group_add)(
    self.room_group_name, self.channel_name)
    self.accept()
  def disconnect(self, close_code):
  # Leave room group
    async_to_sync(self.channel_layer.group_discard)(
    self.room_group_name,
    self.channel_name
    )
  def user_id_change_message(self, event):
    print('event  envoi', event)
    message = event['message']
    self.send(text_data=json.dumps({ 
    'message': message
    }))
from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import Alerte
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from .serializers import AlerteSerializer  # Assurez-vous d'importer votre serializer

@receiver(pre_save, sender=Alerte)
def notify_user_id_change(sender, instance, **kwargs):
    if instance.pk:
        previous = Alerte.objects.get(pk=instance.pk)
        if previous.userID != instance.userID:
            serialize = AlerteSerializer(instance)
            channel_layer = get_channel_layer()
            group_name = 'user_id_change'
            async_to_sync(channel_layer.group_send)(
                group_name, {
                    'type': 'user_id_change_message',
                    'message': serialize.data
                }
            )
            print('userID modified, notification sent')
#------------------------------------------------------- FIN alerte to maintenance ---------------------------
  # broadcast Notification; Individual + community
#************************************** fin web socket *****************************


#************************************ web socket 1min *************************************
import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
from threading import Timer
from datetime import datetime
import os

""" 
class LocalConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = 'test'
        self.room_group_name = self.room_name
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        self.accept()
        self.is_running = True
        self.send_data()

    def disconnect(self, close_code):
        self.is_running = False
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    def send_data(self):
        #print('send_data')
        if self.is_running:
            #print('send_data running')
            self.check_conditions_and_create_alerts()
            '''
            data = self.get_TH_par_instant()  # Remplacez par votre fonction pour obtenir les données`
            print('data ----------> : ', data)
            self.send(text_data=json.dumps(data)) `
            '''
            Timer(60, self.send_data).start()
    def check_conditions_and_create_alerts(self):
        locaux = Zone.objects.all()
        date_recherchee = datetime.now().strftime('%Y-%m-%d %H:%M:00')
        for local in locaux:
            nom_fichier_json = f"{local.id}"
            chemin_fichier = os.path.join('media', 'donnees' + str(nom_fichier_json) + '.json')
            if os.path.exists(chemin_fichier):
                with open(chemin_fichier, 'r') as fichier:
                    contenu_json = json.load(fichier)
                if date_recherchee in contenu_json:
                    temperature = contenu_json[date_recherchee]["temperature"]
                    humidite = contenu_json[date_recherchee]["humidite"]
                    if temperature < local.minT or temperature > local.maxT :
                        self.create_alert(local, temperature, "temperature")
                    if humidite < local.minH or humidite > local.maxH:
                        self.create_alert(local,humidite, "humidite" )

    def create_alert(self, local, temperature, type):
        if type == "temperature":
          alert = Alerte(
              type='temperature',

              localId=local.id,
              valeur=temperature,
             
              text=f"Alert! Temperature: {temperature}  out of range."
          )
        elif type == "humidite":
          alert = Alerte(
              type='humidite',

              localId=local.id,
              valeur=temperature,
             
              message=f"Alert! humidité: {temperature}  out of range."
          )
        alert.save() 
    def get_TH_par_instant(self):
        #print('get_TH_par_instant')
        # Exemple de récupération de plusieurs locaux
        locaux = Zone.objects.all()
        #print('locaux : ', locaux)
        date_recherchee = datetime.now().strftime('%Y-%m-%d %H:%M:00')
        #print('date_recherchee : ', date_recherchee)
        results = []

        for local in locaux:
            nom_fichier_json = f"{local.id}"  # Assurez-vous que le nom du fichier correspond à l'ID du local
            chemin_fichier = os.path.join('media', 'donnees' + str(nom_fichier_json) + '.json')
            #print('chemin_fichier : ', chemin_fichier)
            if os.path.exists(chemin_fichier):
                with open(chemin_fichier, 'r') as fichier:
                    contenu_json = json.load(fichier)
                    
                    
                if date_recherchee in contenu_json:
                    #print('contenu_json : ', contenu_json)
                    temperature = contenu_json[date_recherchee]["temperature"]
                    humidite = contenu_json[date_recherchee]["humidite"]
                    
                    # Utiliser l'identifiant de la zone plutôt que l'objet lui-même
                    results.append({"id": local.id, "T": temperature, "H": humidite})
                    #print('result : ', results)

        return results
 """
#***********************************  fin web socket 1min *************************************
from rest_framework import viewsets
from rest_framework.response import Response
from .models import Alerte
from .serializers import AlerteSerializer
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync


from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Alerte

from asgiref.sync import async_to_sync
import json

import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import Alerte


from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
class AlerteViewSet(viewsets.ModelViewSet):
    queryset = Alerte.objects.all()
    serializer_class = AlerteSerializer

    
class EtageViewSet(viewsets.ModelViewSet):
    queryset = Etage.objects.all()
    serializer_class = EtageSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            # Récupérer l'ID de l'étage ajouté
            etage_id = serializer.data.get('id')
            return Response({'id': etage_id}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def list(self, request, *args, **kwargs):
        etages = Etage.objects.all()
        serializer = EtageSerializer(etages, many=True)
        return Response(serializer.data)

class PeriodeActiviteViewSet(viewsets.ModelViewSet):
    queryset = PeriodeActivite.objects.all()
    serializer_class = PeriodeActiviteSerializer
    def list(self, request, *args, **kwargs):
        periodes = PeriodeActivite.objects.all()
        serializer = PeriodeActiviteSerializer(periodes, many=True)
        return Response(serializer.data)

class BatimentList(generics.ListAPIView):
    queryset = Batiment.objects.all()
    serializer_class = BatimentTSerializer


def get_batiments_with_etages_zones(request):
    #date = request.GET.get('date')
    # Récupérer tous les bâtiments
    batiments = Batiment.objects.all()

    # Serializer les données des bâtiments avec leurs étages et zones associées
    data = []
    for batiment in batiments:
        batiment_data = {
            'id': batiment.id,
            'nomBatiment': batiment.nomBatiment,
            'etages': [],
        }
        etages = Etage.objects.filter(batimentId=batiment.id)
        for etage in etages:
            etage_data = {
                'id': etage.id,
                'nomEtage': etage.nomEtage,
                'zones': [],
            }
            zones = Zone.objects.filter(etageZ=etage.id)
            for zone in zones:
                zone_data = {
                    'id': zone.id,
                    'nomLocal': zone.nomLocal,
                    'typeLocal': zone.typeLocal,
                    'surface': zone.surface,
                    'minT': zone.minT,
                    'maxT': zone.maxT,
                    'minH': zone.minH,
                    'maxH': zone.maxH,
                    'T': 0,
                    'H': 0,
                }
                etage_data['zones'].append(zone_data)
            batiment_data['etages'].append(etage_data)
        data.append(batiment_data)

    # Renvoyer les données au format JSON
    return JsonResponse(data, safe=False)


#       ******************************************* GET API views *******************************************
@api_view(['GET'])
def getRapportByAlerte(request, alerteId):
    try:
        # Récupérer tous les rapports associés à l'equipement spécifique
        rapports = Rapport.objects.filter(alerte=alerteId)
        for rapport in rapports:
            rapport.vu = True
            rapport.notifie = True
            rapport.save()
        print(rapports)
        # Sérialiser les données des rapports
        serializer = RapportSerializer(rapports, many=True)

        # Retourner la réponse avec les rapports sérialisés
        return Response(serializer.data)
    except Rapport.DoesNotExist:
        # Si l'equipement spécifiée n'existe pas, retourner une erreur 404
        return Response(status=status.HTTP_404_NOT_FOUND)

from django.http import JsonResponse
is_get_TH_par_heure_running = True

# Variable de contrôle globale pour la méthode get_TH_par_jour
is_get_TH_par_jour_running = True

# Variable de contrôle globale pour la méthode get_TH_par_instant
is_get_TH_par_instant_running = True

def stop_method_view(request):
    print("**************************************************stop_method_view")
    global is_get_TH_par_heure_running, is_get_TH_par_jour_running, is_get_TH_par_instant_running
    
    # Modifier les variables de contrôle pour arrêter les méthodes correspondantes
    is_get_TH_par_heure_running = False
    is_get_TH_par_jour_running = False
    is_get_TH_par_instant_running = False
    
    return JsonResponse({'message': 'Méthodes arrêtées avec succès'}, status=200)

def start_method_view(request):
    print("**************************************************start_method_view")
    
    global is_get_TH_par_heure_running, is_get_TH_par_jour_running, is_get_TH_par_instant_running
    
    # Modifier les variables de contrôle pour arrêter les méthodes correspondantes
    is_get_TH_par_heure_running = True
    is_get_TH_par_jour_running = True
    is_get_TH_par_instant_running = True
    
    return JsonResponse({'message': 'Méthodes arrêtées avec succès'}, status=200)

@api_view(['GET'])
def equipements_by_zone(request, zone_id):
    try:
        # Récupérer tous les équipements associés à la zone spécifique
        equipements = Equipement.objects.filter(zoneE=zone_id)
        # Sérialiser les données des équipements
        serializer = EquipementSerializer(equipements, many=True)
        # Retourner la réponse avec les équipements sérialisés
        return Response(serializer.data)
    except Equipement.DoesNotExist:
        # Si la zone spécifiée n'existe pas, retourner une erreur 404
        return Response(status=status.HTTP_404_NOT_FOUND)
@api_view(['GET'])
def getRapportByEquipement(request, equipementId):
    try:
        # Récupérer tous les rapports associés à l'equipement spécifique
        rapports = Rapport.objects.filter(equipement=equipementId)
        print(rapports)
        # Sérialiser les données des rapports
        serializer = RapportSerializer(rapports, many=True)
        
        # Retourner la réponse avec les rapports sérialisés
        return Response(serializer.data)
    except Rapport.DoesNotExist:
        # Si l'equipement spécifiée n'existe pas, retourner une erreur 404
        return Response(status=status.HTTP_404_NOT_FOUND)
@api_view(['GET'])
def zones_by_etage(request, etage_id):
    try:
        # Récupérer tous les équipements associés à la zone spécifique
        zones = Zone.objects.filter(etageZ=etage_id)
        # Sérialiser les données des équipements
        serializer = ZoneSerializer(zones, many=True)
        # Retourner la réponse avec les équipements sérialisés
        return Response(serializer.data)
    except Zone.DoesNotExist:
        # Si la zone spécifiée n'existe pas, retourner une erreur 404
        return Response(status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
def etages_by_batiment(request, batiment_id):
    try:
        # Récupérer tous les équipements associés à la zone spécifique
        etages = Etage.objects.filter(batimentId=batiment_id)
        # Sérialiser les données des équipements
        serializer = EtageSerializer(etages, many=True)
        # Retourner la réponse avec les équipements sérialisés
        return Response(serializer.data)
    except Etage.DoesNotExist:
        # Si la zone spécifiée n'existe pas, retourner une erreur 404
        return Response(status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
def get_batiment_id(request, nom_batiment):
    try:
        batiment = Batiment.objects.get(nomBatiment=nom_batiment)
        return Response({'idBatiment': batiment.id})
    except Batiment.DoesNotExist:
        return Response({'error': 'Le batiment spécifié n\'existe pas'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
def get_etage_id(request, nom_etage):
    try:
        etage =  Etage.objects.get(nomEtage=nom_etage)
        return Response({'idEtage': etage.id})
    except Batiment.DoesNotExist:
        return Response({'error': 'L etage spécifié n\'existe pas'}, status=status.HTTP_404_NOT_FOUND)

def get_etage_details(request, nom_etage):
    try:
        # Récupérer les détails de l'étage à partir du nom d'étage fourni
        etage = Etage.objects.get(nomEtage=nom_etage)
        # Vous pouvez maintenant sérialiser les détails de l'étage et les renvoyer dans la réponse
        # Ici, nous supposons que vous utilisez Django Rest Framework pour la sérialisation
        serializer = EtageSerializer(etage)
        return JsonResponse(serializer.data)
    except Etage.DoesNotExist:
        return JsonResponse({'detail': 'Étage non trouvé'}, status=404)


#               ******************************************* CSV views *******************************************


import os
import csv
from django.http import JsonResponse

def read_csv(request, file_path):
    # Construire le chemin complet du fichier CSV en fonction du chemin fourni
    full_file_path = os.path.join('C:\\Users\\zeine\\OneDrive\\Desktop\\PFE MASTER2\\dataset', file_path)

    # Lire le fichier CSV et récupérer les données
    data = []
    with open(full_file_path, 'r') as file:
        csv_reader = csv.reader(file)
        for row in csv_reader:
            data.append(row)

    # Retourner les données dans une réponse JSON
    return JsonResponse({'data': data})


#               ******************************************* Excel data views *******************************************


import openpyxl
from django.http import JsonResponse

def excel_data_api(request):
    # Chemin vers le fichier Excel
    excel_file = r'C:\Users\zeine\OneDrive\Desktop\gitIslem\backend\crud\src\assets\DataSensor.xlsx'

    # Charger le fichier Excel
    wb = openpyxl.load_workbook(excel_file)
    sheet = wb.active  # Utilisez la première feuille du classeur

    # Lire les données de chaque ligne du fichier Excel à partir de la deuxième ligne
    data = []
    for row in sheet.iter_rows(min_row=2, values_only=True):
        # Ajoutez les données de chaque ligne à une liste
        data.append({
            'column1': row[2],
            'column2': row[3],
            # Ajoutez d'autres champs en fonction de votre fichier Excel
        })

    # Renvoyer toutes les données sous forme de JSON
    return JsonResponse(data, safe=False)


#               ******************************************* traslation views *******************************************


from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from googletrans import Translator

@csrf_exempt
def translate(request):
    if request.method == 'POST':
        # Obtenir les données JSON de la requête POST
        data = request.POST.get('data', '')
        # Initialiser le traducteur
        translator = Translator()
        try:
            # Traduire du français vers l'anglais
            translation_fr_to_en = translator.translate(data, src='fr', dest='en').text
            # Traduire de l'anglais vers le français
            translation_en_to_fr = translator.translate(data, src='en', dest='fr').text
            # Retourner les traductions
            return JsonResponse({'translation_fr_to_en': translation_fr_to_en,
                                 'translation_en_to_fr': translation_en_to_fr})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)


#               ******************************************* Consumtion calculate views *******************************************


from rest_framework.response import Response
from rest_framework import status
from .models import Equipement
from operator import itemgetter

class EquipementsTotalConsommation(APIView):
    def get(self, request):
        try:
            equipements = Equipement.objects.all()
            equipements_consommation = []
            for equipement in equipements:
                consommation_totale = equipement.calculerConsommationTotale()
                equipements_consommation.append({
                    'id': equipement.id,
                    'nom': equipement.nom,
                    'etat': equipement.etat,
                    'consommation_W': consommation_totale,
                    'consommation_kW': consommation_totale/1000,
                    'localId': equipement.zoneE.id,
                    'nomLocal': equipement.zoneE.nomLocal,
                    'typeLocal': equipement.zoneE.typeLocal,
                    'numEtage': equipement.zoneE.etageZ.id,
                    'nomEtage': equipement.zoneE.etageZ.nomEtage,
                    'batimentId': equipement.zoneE.etageZ.batimentId.id,
                    'batiment': equipement.zoneE.etageZ.batimentId.nomBatiment,
                })
            # Trier les équipements par consommation totale décroissante
            equipements_consommation = sorted(equipements_consommation, key=itemgetter('consommation_kW'), reverse=True)
            return Response(equipements_consommation, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class zonesTotalConsommation(APIView):
    def get(self, request):
        try:
            #print('zzzzzzzzzzzzzzzzzzzzzz')
            zones_consommation = []
            zones = Zone.objects.all()
            for zone in zones:
                consommation_totale = zone.calculerConsommationTotaleZone()
                zones_consommation.append({
                    'id': zone.id,
                    'nomLocal': zone.nomLocal,
                    'typeLocal': zone.typeLocal,
                    'surface': zone.surface,
                    'numEtage': zone.etageZ.id,
                    'nomEtage': zone.etageZ.nomEtage,
                    'batiment': zone.etageZ.batimentId.nomBatiment,
                    'consommation_W': consommation_totale,
                    'consommation_kW': consommation_totale/1000
                })
                #print('Zone_cons: ', zones_consommation, '\n')

            zones_consommation = sorted(zones_consommation, key=itemgetter('consommation_W'), reverse=True)
            return Response(zones_consommation, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class etagesTotalConsommation(APIView):
    def get(self, request, batiment_id):
        try:
            etages_consommation = []
            batiment = get_object_or_404(Batiment, id=batiment_id)

            # Récupérer les étages associés à ce batiment
            etages = Etage.objects.filter(batimentId=batiment)

            for etage in etages:
                consommation_totale = etage.calculerConsommationTotaleEtage()
                etages_consommation.append({
                    'id': etage.id,
                    'nomEtage': etage.nomEtage,
                    'batimentId': etage.batimentId.id,
                    'nomBatiment': etage.batimentId.nomBatiment,
                    'consommation_W': consommation_totale,
                    'consommation_kW': consommation_totale / 1000
                })

            #etages_consommation = sorted(etages_consommation, key=itemgetter('consommation_W'), reverse=True)
            return Response(etages_consommation, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class batimentsTotalConsommation(APIView):
    def get(self, request):
        try:
            batiments_consommation = []
            batiments = Batiment.objects.all()
            for batiment in batiments:
                consommation_totale = batiment.calculerConsommationTotaleBatiment()
                batiments_consommation.append({
                    'id': batiment.id,
                    'nomBatiment': batiment.nomBatiment,
                    'consommation_W': consommation_totale,
                    'consommation_kW': consommation_totale/1000
                })
                #print('Zone_cons: ', batiments_consommation, '\n')

            #batiments_consommation = sorted(batiments_consommation, key=itemgetter('consommation_W'), reverse=True)
            return Response(batiments_consommation, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class hopitalTotalConsommation(APIView):
    def get(self, request):
        try:
            batiments = Batiment.objects.all()
            consommation_totale = 0
            for batiment in batiments:
              consommation_totale += batiment.calculerConsommationTotaleBatiment()
              #print('Zone_cons: ', batiments_consommation, '\n')

            return Response(consommation_totale, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


#               ******************************************* Consumtion calculate views (#               ******************************************* Consumtion calculate views (Periods)  *******************************************) *******************************************

class EquipementsOnlyConsommationParPeriode(APIView):
    def get(self, request):
        try:
            # Récupérez les paramètres de la requête GET
            date_debut = request.GET.get('dateDebut')
            date_fin = request.GET.get('dateFin')
            #print(date_debut, ' -> ', date_fin)
            #print('*******************debut ', date_debut, 'fin ', date_fin)
            equipements = Equipement.objects.all()
            equipements_consommation = []
            for equipement in equipements:
                consommation= equipement.calculerConsommationParPeriode(date_debut, date_fin)
                equipements_consommation.append({
                    'id': equipement.id,
                    'consommation_W': consommation,
                    'consommation_kW': consommation/1000
                })
                #print('* ', equipements_consommation[-1], '\n\n**')
            # Trier les équipements par consommation totale décroissante
            equipements_consommation = sorted(equipements_consommation, key=itemgetter('consommation_kW'), reverse=True)
            return Response(equipements_consommation, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class EquipementsConsommationParPeriode(APIView):
    def get(self, request):
        try:
            # Récupérez les paramètres de la requête GET
            date_debut = request.GET.get('dateDebut')
            date_fin = request.GET.get('dateFin')
            #print(date_debut, ' -> ', date_fin)
            #print('*******************debut ', date_debut, 'fin ', date_fin)
            equipements = Equipement.objects.all()
            equipements_consommation = []
            for equipement in equipements:
                consommation= equipement.calculerConsommationParPeriode(date_debut, date_fin)
                equipements_consommation.append({
                    'id': equipement.id,
                    'nom': equipement.nom,
                    'etat': equipement.etat,
                    'localId': equipement.zoneE.id,
                    'nomLocal': equipement.zoneE.nomLocal,
                    'typeLocal': equipement.zoneE.typeLocal,
                    'numEtage': equipement.zoneE.etageZ.id,
                    'nomEtage': equipement.zoneE.etageZ.nomEtage,
                    'batiment': equipement.zoneE.etageZ.batimentId.nomBatiment,
                    'batimentId': equipement.zoneE.etageZ.batimentId.id,
                    'dateDebut': date_debut,
                    'dateFin': date_fin,
                    'consommation_W': consommation,
                    'consommation_kW': consommation/1000
                })
                #print('* ', equipements_consommation[-1], '\n\n**')
            # Trier les équipements par consommation totale décroissante
            equipements_consommation = sorted(equipements_consommation, key=itemgetter('consommation_kW'), reverse=True)
            return Response(equipements_consommation, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class EquipementConsommationParPeriode(APIView):
    def get(self, request, equipement_id):
        try:
            # Récupérez les paramètres de la requête GET
            date_debut = request.GET.get('dateDebut')
            date_fin = request.GET.get('dateFin')
            this_equipement = get_object_or_404(Equipement, id=equipement_id)
            equipements = Equipement.objects.filter(id=this_equipement.id)

            for equipement in equipements:
                consommation= equipement.calculerConsommationParPeriode(date_debut, date_fin)
                equipements_consommation = {
                    'id': equipement.id,
                    'nom': equipement.nom,
                    'etat': equipement.etat,
                    'localId': equipement.zoneE.id,
                    'nomLocal': equipement.zoneE.nomLocal,
                    'typeLocal': equipement.zoneE.typeLocal,
                    'numEtage': equipement.zoneE.etageZ.id,
                    'nomEtage': equipement.zoneE.etageZ.nomEtage,
                    'batiment': equipement.zoneE.etageZ.batimentId.nomBatiment,
                    'batimentId': equipement.zoneE.etageZ.batimentId.id,
                    'dateDebut': date_debut,
                    'dateFin': date_fin,
                    'consommation_W': consommation,
                    'consommation_kW': consommation/1000
                }
            return Response(equipements_consommation, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class localConsommationParPeriode(APIView):
    def get(self, request, zone_id):
        date_debut = request.GET.get('dateDebut')
        date_fin = request.GET.get('dateFin')

        try:
            zones_consommation = []
            zones = Zone.objects.all()
            for zone in zones:
                consommation = zone.calculerConsommationLocalParPeriode(date_debut, date_fin)
                zones_consommation.append({
                    'id': zone.id,
                    'nomLocal': zone.nomLocal,
                    'typeLocal': zone.typeLocal,
                    'surface': zone.surface,
                    'numEtage': zone.etageZ.id,
                    'nomEtage': zone.etageZ.nomEtage,
                    'batiment': zone.etageZ.batimentId.nomBatiment,
                    'dateDebut': date_debut,
                    'dateFin': date_fin,
                    'consommation_W': consommation,
                    'consommation_kW': consommation/1000
                })
                #print('Zone_cons: ', zones_consommation, '\n')

            #zones_consommation = sorted(zones_consommation, key=itemgetter('consommation_W'), reverse=True)
            return Response(zones_consommation, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class etagesConsommationParPeriode(APIView):
    def get(self, request, batiment_id):
        date_debut = request.GET.get('dateDebut')
        date_fin = request.GET.get('dateFin')
        try:
            etages_consommation = []
            batiment = get_object_or_404(Batiment, id=batiment_id)

            # Récupérer les étages associés à ce batiment
            etages = Etage.objects.filter(batimentId=batiment)

            for etage in etages:
                consommation = etage.calculerConsommationEtageParPeriode(date_debut, date_fin)
                etages_consommation.append({
                    'id': etage.id,
                    'nomEtage': etage.nomEtage,
                    'batimentId': etage.batimentId.id,
                    'nomBatiment': etage.batimentId.nomBatiment,
                    'consommation_W': consommation,
                    'consommation_kW': consommation / 1000
                })

            #etages_consommation = sorted(etages_consommation, key=itemgetter('consommation_W'), reverse=True)
            return Response(etages_consommation, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class batimentConsommationParPeriode(APIView):
    def get(self, request):
        date_debut = request.GET.get('dateDebut')
        date_fin = request.GET.get('dateFin')
        try:
            batiments_consommation = []
            batiments = Batiment.objects.all()
            for batiment in batiments:
                consommation = batiment.calculerConsommationBatimentParPeriode(date_debut, date_fin)
                batiments_consommation.append({
                    'id': batiment.id,
                    'nomBatiment': batiment.nomBatiment,
                    'consommation_W': consommation,
                    'consommation_kW': consommation/1000
                })
            #batiments_consommation = sorted(batiments_consommation, key=itemgetter('consommation_W'), reverse=True)
            return Response(batiments_consommation, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class hopitalTotalConsommation(APIView):
    def get(self, request):
        date_debut = request.GET.get('dateDebut')
        date_fin = request.GET.get('dateFin')
        try:
            batiments = Batiment.objects.all()
            consommation = 0
            for batiment in batiments:
              consommation += batiment.calculerConsommationBatimentParPeriode(date_debut, date_fin)

            return Response(consommation, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class hopitalConsommationParMois(APIView):
    def get(self, request):
        """  date_debut = request.GET.get('dateDebut')
        date_fin = request.GET.get('dateFin') """
        try:
            derniers_jours_de_mois = ['31', '29', '31', '30', '31', '30', '31', '31', '30', '31', '30', '31']
            consommations_mois = []
            for i in ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12'] :
              batiments = Batiment.objects.all()
              consommation = 0
              for batiment in batiments:
                #print('2024-'+i+'-01 00:00:00 -> '+'2024-'+i+'-'+derniers_jours_de_mois[int(i)-1])
                consommation += batiment.calculerConsommationBatimentParPeriode('2024-'+i+'-01 00:00:00', '2024-'+i+'-'+derniers_jours_de_mois[int(i)-1]+' 00:00:00')
              consommations_mois.append(consommation)
            #print('Consommations mois : ', consommations_mois)
            return Response(consommations_mois, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class HopitalConsommationPendantMois(APIView):
    def get(self, request):
        try:
            date_debut = request.GET.get('dateDebut')
            date_fin = request.GET.get('dateFin')

            equipements = Equipement.objects.all()
            consommation = 0

            for equipement in equipements:
                consommation += equipement.calculerConsommationParPeriode(date_debut, date_fin)

            return Response(consommation, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# Reset password:


from rest_framework.response import Response
from rest_framework.views import APIView
from django.core.mail import send_mail
from rest_framework import status
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core.mail import send_mail
from django.utils.encoding import force_bytes, force_str  # Modifier l'importation ici
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User

class ChangePasswordEmail(APIView):
    @csrf_exempt
    def post(self, request, *args, **kwargs):
        data = request.data  # Utilisez request.data pour récupérer les données du corps de la requête
        email = data.get('email')
        #print("email ,"+email)
        user = User.objects.filter(email=email).first()
        if user:
            # Générer un token unique
            token_generator = PasswordResetTokenGenerator()
            uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
            token = token_generator.make_token(user)

            # Créer l'URL de réinitialisation de mot de passe
            reset_url = f'http://localhost:4200/changerPassword/{uidb64}/{token}/'

            # Envoyer l'e-mail de réinitialisation de mot de passe
            send_mail(
                'Réinitialisation de mot de passe',
                f'Voici le lien pour réinitialiser votre mot de passe : {reset_url}',
                'from@example.com',
                [email],
                fail_silently=False,
            )
            return JsonResponse({'message': f'Un e-mail de réinitialisation de mot de passe a été envoyé à {email}'})
        else:
            return JsonResponse({'error': 'Aucun utilisateur trouvé avec cet e-mail'}, status=400)

from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

class ChangePassword(APIView):
    def post(self, request, *args, **kwargs):
        # Récupérer l'e-mail et le nouveau mot de passe du corps de la requête POST
        email = request.data.get('email')
        new_password = request.data.get('new_password')

        # Vérifier si l'utilisateur existe
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({'error': 'Utilisateur non trouvé.'}, status=status.HTTP_404_NOT_FOUND)

        # Changer le mot de passe de l'utilisateur
        user.set_password(new_password)
        user.save()

        return Response({'message': 'Mot de passe changé avec succès.'}, status=status.HTTP_200_OK)



from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response

@api_view(['POST'])
def reset_password_avec_uid(request, uidb64, token):
    UserModel = get_user_model()

    # Décoder l'UIDB64
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = UserModel._default_manager.get(pk=uid)
    except (TypeError, ValueError, OverflowError, UserModel.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        # Réinitialiser le mot de passe
        new_password = request.data.get('newPassword')
        #print('le nouveau mot de passe', new_password)
        user.set_password(new_password)
        user.save()
        return Response({'message': 'Mot de passe réinitialisé avec succès.'}, status=status.HTTP_200_OK)
    else:
        return Response({'error': 'Lien de réinitialisation de mot de passe non valide.'}, status=status.HTTP_400_BAD_REQUEST)

class UpdateEmail(APIView):

    def post(self, request, *args, **kwargs):
        data = request.data  # Utilisez request.data pour récupérer les données du corps de la requête
        email = data.get('email')
        #print("email ,"+email)

        code = data.get('code')
        send_mail(
            'Modification d`email ',
            f'Voici le code pour modifier votre email : '+str(code),
            'from@example.com',
            [email],
            fail_silently=False,
        )
        return JsonResponse({'message': f'Un e-mail de modification a été envoyé à {email}'})

@api_view(['GET'])
def get_role(request, user_Id):
    try:
        # Récupérer le profil de l'utilisateur par user_id
        profile = ProfileUser.objects.get(userId=user_Id)
        if profile:
            # Retourner la propriété role du profil
            return Response({'role': profile.role})
        else:
            # Si le profil n'existe pas, retourner une erreur 404
            return Response(status=status.HTTP_404_NOT_FOUND)
    except ProfileUser.DoesNotExist:
        # Si le profil n'existe pas, retourner une erreur 404
        return Response(status=status.HTTP_404_NOT_FOUND)
@api_view(['GET'])
def get_id(request, username):
    try:
        user = User.objects.get(username=username)
        # Récupérer le profil de l'utilisateur par user_id
        profile = ProfileUser.objects.get(userId=user.id)
        if profile:
            # Retourner la propriété role du profil
            return Response({'role': profile.role})
        else:
            # Si le profil n'existe pas, retourner une erreur 404
            return Response(status=status.HTTP_404_NOT_FOUND)
    except ProfileUser.DoesNotExist:
        # Si le profil n'existe pas, retourner une erreur 404
        return Response(status=status.HTTP_404_NOT_FOUND)

class ProfileUserViewSet(viewsets.ModelViewSet):
    queryset = ProfileUser.objects.all()
    serializer_class = ProfileUserSerializer
    def get_role(self, request, pk=None):
        profile = self.get_object()
        role = profile.role
        return Response({'role': role}, status=status.HTTP_200_OK)
    def list(self, request, *args, **kwargs):
        profiles = ProfileUser.objects.all()
        serializer =ProfileUserSerializer(profiles, many=True)
        return Response(serializer.data)


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import User, ProfileUser
from .serializers import UserSerializer

class Allusers(APIView):
    def get(self, request):
        users = User.objects.all()
        data = []
        for user in users:
            try:
                profile = ProfileUser.objects.get(userId=user)
                role = profile.role
            except ProfileUser.DoesNotExist:
                role = None
            serializer = UserSerializer(user)
            data.append({**serializer.data, 'role': role})
        return Response(data)
import os
""" 
def traiter_chauffage(equi):
    tempsDebut=None
    verif = False
    chemin_fichier = os.path.join('media', 'data' + str(equi.zoneE.id) + '.csv')
    if os.path.exists(chemin_fichier):
        with open(chemin_fichier, 'r') as fichier:
            for ligne in fichier:
                temperature= float(ligne.strip().split(';')[2])
                #print('**************************temperature :  ',temperature)
                #print('**************************la ligne complete :  ',ligne)
                # Ajoutez ici la logique pour vérifier la température et contrôler le chauffage/climatisation

                if temperature < equi.zoneE.maxT:

                    #print('Le chauffage est actif')
                    puissance = equi.puissance  # Supposons que le champ pour la puissance soit 'puissance'

            # Calculer la consommation

                    #print('************************** DEBUT :  ',datetime.strptime(ligne.strip().split(';')[0]+' '+ ligne.strip().split(';')[1], '%d/%m/%Y %H:%M'))  # Convertir la première colonne en datetime
                    tempsDebut = datetime.strptime(ligne.strip().split(';')[0]+' '+ ligne.strip().split(';')[1], '%d/%m/%Y %H:%M')
                    if(verif==False):
                      # Créer une nouvelle période d'activité
                      periode_activite = PeriodeActivite.objects.create(
                          tempsDebut=datetime.strptime(ligne.strip().split(';')[0]+' '+ ligne.strip().split(';')[1], '%d/%m/%Y %H:%M'),  # Convertir la première colonne en datetime
                          tempsFin=None,
                          Equipement=equi,

                      )
                      verif=True
                else :
                    if(tempsDebut!=None):
                      #print('************************** FIN :  ',PeriodeActivite.objects.filter(Equipement=equi).latest('tempsDebut'))  # Convertir la première colonne en datetime
                      verif=False
                      derniere_periode = PeriodeActivite.objects.filter(Equipement=equi).latest('tempsDebut')
                      derniere_periode.tempsFin = datetime.strptime(ligne.strip().split(';')[0]+' '+ ligne.strip().split(';')[1], '%d/%m/%Y %H:%M')
                      derniere_periode.calculer_consommation()
                      derniere_periode.save()
                      tempsDebut=None
                      #print('--------------------------------------------------------------------------------------------------------------------')



    else:
        #print("Le fichier de données pour le local", equi.id, "n'existe pas.")¸
        pass """
"""
def traiter_climatiseur(equi):
    tempsDebut=None
    verif = False
    chemin_fichier = os.path.join('media', 'data' + str(equi.zoneE.id) + '.csv')
    if os.path.exists(chemin_fichier):
        with open(chemin_fichier, 'r') as fichier:
            for ligne in fichier:
                temperature= float(ligne.strip().split(';')[2])
                #print('**************************temperature :  ',temperature)
                #print('**************************la ligne complete :  ',ligne)
                # Ajoutez ici la logique pour vérifier la température et contrôler le chauffage/climatisation

                if temperature > equi.zoneE.maxT:

                    #print('Le chauffage est actif')
                    puissance = equi.puissance  # Supposons que le champ pour la puissance soit 'puissance'

            # Calculer la consommation

                    #print('************************** DEBUT :  ',datetime.strptime(ligne.strip().split(';')[0]+' '+ ligne.strip().split(';')[1], '%d/%m/%Y %H:%M'))  # Convertir la première colonne en datetime
                    tempsDebut = datetime.strptime(ligne.strip().split(';')[0]+' '+ ligne.strip().split(';')[1], '%d/%m/%Y %H:%M')
                    if(verif==False):
                      # Créer une nouvelle période d'activité
                      periode_activite = PeriodeActivite.objects.create(
                          tempsDebut=datetime.strptime(ligne.strip().split(';')[0]+' '+ ligne.strip().split(';')[1], '%d/%m/%Y %H:%M'),  # Convertir la première colonne en datetime
                          tempsFin=None,
                          Equipement=equi,

                      )
                      verif=True
                else :
                    if(tempsDebut!=None):
                      #print('************************** FIN :  ',PeriodeActivite.objects.filter(Equipement=equi).latest('tempsDebut'))  # Convertir la première colonne en datetime
                      verif=False
                      derniere_periode = PeriodeActivite.objects.filter(Equipement=equi).latest('tempsDebut')
                      derniere_periode.tempsFin = datetime.strptime(ligne.strip().split(';')[0]+' '+ ligne.strip().split(';')[1], '%d/%m/%Y %H:%M')
                      derniere_periode.calculer_consommation()
                      derniere_periode.save()
                      tempsDebut=None
                      #print('--------------------------------------------------------------------------------------------------------------------')



    else:
        print("Le fichier de données pour le local", equi.id, "n'existe pas.")

def traiter_lampe(equi):
    tempsDebut=None
    verif = False
    chemin_fichier = os.path.join('media', 'data' + str(equi.zoneE.id) + '.csv')
    if os.path.exists(chemin_fichier):
        with open(chemin_fichier, 'r') as fichier:
            for ligne in fichier:
                temperature= float(ligne.strip().split(';')[4])
                # Ajoutez ici la logique pour vérifier la température et contrôler le chauffage/climatisation

                if temperature ==1:

                    #print('Lampe actif')
                    puissance = equi.puissance  # Supposons que le champ pour la puissance soit 'puissance'

            # Calculer la consommation

                    #print('************************** DEBUT :  ',datetime.strptime(ligne.strip().split(';')[0]+' '+ ligne.strip().split(';')[1], '%d/%m/%Y %H:%M'))  # Convertir la première colonne en datetime
                    tempsDebut = datetime.strptime(ligne.strip().split(';')[0]+' '+ ligne.strip().split(';')[1], '%d/%m/%Y %H:%M')
                    if(verif==False):
                      # Créer une nouvelle période d'activité
                      periode_activite = PeriodeActivite.objects.create(
                          tempsDebut=datetime.strptime(ligne.strip().split(';')[0]+' '+ ligne.strip().split(';')[1], '%d/%m/%Y %H:%M'),  # Convertir la première colonne en datetime
                          tempsFin=None,
                          Equipement=equi,

                      )
                      verif=True
                else :
                    if(tempsDebut!=None):
                      #print('************************** FIN :  ',PeriodeActivite.objects.filter(Equipement=equi).latest('tempsDebut'))  # Convertir la première colonne en datetime
                      verif=False
                      derniere_periode = PeriodeActivite.objects.filter(Equipement=equi).latest('tempsDebut')
                      derniere_periode.tempsFin = datetime.strptime(ligne.strip().split(';')[0]+' '+ ligne.strip().split(';')[1], '%d/%m/%Y %H:%M')
                      derniere_periode.calculer_consommation()
                      derniere_periode.save()
                      tempsDebut=None
                      #print('--------------------------------------------------------------------------------------------------------------------')



    else:
        #print("Le fichier de données pour le local", equi.id, "n'existe pas.")
        pass

def traiter_humidificateur(equi):
    tempsDebut=None
    verif = False
    chemin_fichier = os.path.join('media', 'data' + str(equi.zoneE.id) + '.csv')
    if os.path.exists(chemin_fichier):
        with open(chemin_fichier, 'r') as fichier:
            for ligne in fichier:
                temperature= float(ligne.strip().split(';')[3])
                #print('**************************temperature :  ',temperature)
                #print('**************************la ligne complete :  ',ligne)
                # Ajoutez ici la logique pour vérifier la température et contrôler le chauffage/climatisation

                if temperature > equi.zoneE.maxH:

                    #print('Le chauffage est actif')
                    puissance = equi.puissance  # Supposons que le champ pour la puissance soit 'puissance'

            # Calculer la consommation
                    #print('************************** DEBUT :  ',datetime.strptime(ligne.strip().split(';')[0]+' '+ ligne.strip().split(';')[1], '%d/%m/%Y %H:%M'))  # Convertir la première colonne en datetime
                    tempsDebut = datetime.strptime(ligne.strip().split(';')[0]+' '+ ligne.strip().split(';')[1], '%d/%m/%Y %H:%M')
                    if(verif==False):
                      # Créer une nouvelle période d'activité
                      periode_activite = PeriodeActivite.objects.create(
                          tempsDebut=datetime.strptime(ligne.strip().split(';')[0]+' '+ ligne.strip().split(';')[1], '%d/%m/%Y %H:%M'),  # Convertir la première colonne en datetime
                          tempsFin=None,
                          Equipement=equi
                      )
                      verif=True
                else :
                    if(tempsDebut!=None):

                      #print('************************** FIN :  ',PeriodeActivite.objects.filter(Equipement=equi).latest('tempsDebut'))  # Convertir la première colonne en datetime
                      verif=False
                      derniere_periode = PeriodeActivite.objects.filter(Equipement=equi).latest('tempsDebut')
                      derniere_periode.tempsFin = datetime.strptime(ligne.strip().split(';')[0]+' '+ ligne.strip().split(';')[1], '%d/%m/%Y %H:%M')

                      derniere_periode.calculer_consommation()

                      derniere_periode.save()
                      tempsDebut=None
                      #print('--------------------------------------------------------------------------------------------------------------------')



    else:
        #print("Le fichier de données pour le local", equi.id, "n'existe pas.")
        pass


import random
from datetime import datetime, timedelta
from .models import PeriodeActivite, Equipement
PeriodeActivite.objects.all().delete()
#Liste des équipements disponibles
equipements = Equipement.objects.all()

#Fonction pour générer une heure aléatoire dans une journée

def randomtime():
    return timedelta(hours=random.randint(0, 23), minutes=random.randint(0, 59), seconds=random.randint(0, 59))

#Définir la plage de dates
start_date = datetime(2024, 1, 1)
end_date = datetime(2024, 12, 31)

#Boucle à travers chaque jour
current_date = start_date
while current_date <= end_date:
    # Boucle à travers chaque équipement
    for equipement in equipements:
        if 'chauffage'  in equipement.nom.lower():
            print('dkhel fel cas********************************************************')
            traiter_chauffage(equipement)
        elif 'climatiseur' in equipement.nom:
            traiter_climatiseur(equipement)
        elif 'lampe' in equipement.nom or 'led' in equipement.nom:
            traiter_lampe(equipement)
        elif 'humidificateur' in equipement.nom:
            traiter_humidificateur(equipement)
        else :
        # Générer un nombre aléatoire de périodes d'activité pour chaque équipement et chaque jour
          num_activites = random.randint(1, 5)

          for i in range(num_activites):
              # Générer des dates de début et de fin aléatoires pour la journée
              debut = current_date + randomtime()
              fin = debut + timedelta(minutes=random.randint(30, 240))  # Durée aléatoire entre 30 minutes et 4 heures

              # Calculer la durée de la période
              duree = (fin - debut).total_seconds() / 3600  # Convertir en heures

              # Récupérer la puissance de l'équipement
              puissance = equipement.puissance  # Supposons que le champ pour la puissance soit 'puissance'

              # Calculer la consommation
              consommation = duree * puissance

              # Créer une nouvelle période d'activité
              periode_activite = PeriodeActivite.objects.create(
                  tempsDebut=debut,
                  tempsFin=fin,
                  Equipement=equipement,
                  consommation=consommation
              )

    # Passer au jour suivant
    current_date += timedelta(days=1)

 """
import json
import os
from datetime import datetime
from .models import PeriodeActivite  # Assurez-vous d'importer votre modèle PeriodeActivite ici

def traiter_chauffage(equi):
    tempsDebut = None
    verif = False
    chemin_fichier = os.path.join('media', 'donnees' + str(equi.zoneE.id) + '.json') 
    #print('chemin_fichier ',chemin_fichier) # Assurez-vous que votre fichier est au format JSON
    if os.path.exists(chemin_fichier):
        with open(chemin_fichier, 'r') as fichier:
            data = json.load(fichier)
            for timestamp, values in data.items():
                temperature = values['temperature']
                humidite = values['humidite']
                # Ajoutez ici la logique pour vérifier la température et l'humidité et contrôler le chauffage/climatisation
                #print('--------------------la temperature :  ', temperature, 'maxT :  ', equi.zoneE.maxT)
                
                if temperature < equi.zoneE.maxT:
                    # Le chauffage est actif
                    puissance = equi.puissance  # Supposons que le champ pour la puissance soit 'puissance'

                    # Calculer la consommation
                    tempsDebut = datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S')  # Convertir le timestamp en datetime
                    if not verif:
                        # Créer une nouvelle période d'activité
                        periode_activite = PeriodeActivite.objects.create(
                            tempsDebut=tempsDebut,
                            tempsFin=None,
                            Equipement=equi,
                        )
                        verif = True
                else:
                    if tempsDebut is not None:
                        verif = False
                        derniere_periode = PeriodeActivite.objects.filter(Equipement=equi).latest('tempsDebut')
                        derniere_periode.tempsFin = datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S')
                        derniere_periode.calculer_consommation()
                        derniere_periode.save()
                        tempsDebut = None
    else:
        # Le fichier de données pour le local n'existe pas.
      pass

import json
import os
from datetime import datetime
from .models import PeriodeActivite  # Assurez-vous d'importer votre modèle PeriodeActivite ici

def traiter_climatiseur(equi):
    tempsDebut = None
    verif = False
    chemin_fichier = os.path.join('media', 'donnees' + str(equi.zoneE.id) + '.json') 
    #print('chemin_fichier ',chemin_fichier) # Assurez-vous que votre fichier est au format JSON
    if os.path.exists(chemin_fichier):
        with open(chemin_fichier, 'r') as fichier:
            data = json.load(fichier)
            for timestamp, values in data.items():
                temperature = values['temperature']
                humidite = values['humidite']
                # Ajoutez ici la logique pour vérifier la température et l'humidité et contrôler le chauffage/climatisation
                #print('--------------------la temperature :  ', temperature, 'maxT :  ', equi.zoneE.maxT)
                
                if temperature > equi.zoneE.maxT:
                    # Le chauffage est actif
                    puissance = equi.puissance  # Supposons que le champ pour la puissance soit 'puissance'

                    # Calculer la consommation
                    tempsDebut = datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S')  # Convertir le timestamp en datetime
                    if not verif:
                        # Créer une nouvelle période d'activité
                        periode_activite = PeriodeActivite.objects.create(
                            tempsDebut=tempsDebut,
                            tempsFin=None,
                            Equipement=equi,
                        )
                        verif = True
                else:
                    if tempsDebut is not None:
                        verif = False
                        derniere_periode = PeriodeActivite.objects.filter(Equipement=equi).latest('tempsDebut')
                        derniere_periode.tempsFin = datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S')
                        derniere_periode.calculer_consommation()
                        derniere_periode.save()
                        tempsDebut = None
    else:
        # Le fichier de données pour le local n'existe pas.
      pass

import os
import json
from datetime import datetime
from .models import PeriodeActivite

def traiter_lampe(equi):
    tempsDebut = None
    verif = False
    chemin_fichier = os.path.join('media', 'donnees' + str(equi.zoneE.id) + '.json')
    
    if os.path.exists(chemin_fichier):
        with open(chemin_fichier, 'r') as fichier:
            data = json.load(fichier)
            for timestamp, values in data.items():
                presence = values['presence']
                if presence == 1:
                    puissance = equi.puissance
                    tempsDebut = datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S')
                    if not verif:
                        periode_activite = PeriodeActivite.objects.create(
                            tempsDebut=tempsDebut,
                            tempsFin=None,
                            Equipement=equi
                        )
                        verif = True
                else:
                    if tempsDebut is not None:
                        verif = False
                        derniere_periode = PeriodeActivite.objects.filter(Equipement=equi).latest('tempsDebut')
                        derniere_periode.tempsFin = datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S')
                        derniere_periode.calculer_consommation()
                        derniere_periode.save()
                        tempsDebut = None
    else:
        # Le fichier de données pour le local n'existe pas.
        pass
def traiter_humidificateur(equi):
    tempsDebut = None
    verif = False
    chemin_fichier = os.path.join('media', 'donnees' + str(equi.zoneE.id) + '.json') 
    #print('chemin_fichier ',chemin_fichier) # Assurez-vous que votre fichier est au format JSON
    if os.path.exists(chemin_fichier):
        with open(chemin_fichier, 'r') as fichier:
            data = json.load(fichier)
            for timestamp, values in data.items():
                
                humidite = values['humidite']
                # Ajoutez ici la logique pour vérifier la température et l'humidité et contrôler le chauffage/climatisation
                #print('--------------------la temperature :  ', temperature, 'maxT :  ', equi.zoneE.maxT)
                
                if  humidite > equi.zoneE.maxT:
                    # Le chauffage est actif
                    puissance = equi.puissance  # Supposons que le champ pour la puissance soit 'puissance'

                    # Calculer la consommation
                    tempsDebut = datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S')  # Convertir le timestamp en datetime
                    if not verif:
                        # Créer une nouvelle période d'activité
                        periode_activite = PeriodeActivite.objects.create(
                            tempsDebut=tempsDebut,
                            tempsFin=None,
                            Equipement=equi,
                        )
                        verif = True
                else:
                    if tempsDebut is not None:
                        verif = False
                        derniere_periode = PeriodeActivite.objects.filter(Equipement=equi).latest('tempsDebut')
                        derniere_periode.tempsFin = datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S')
                        derniere_periode.calculer_consommation()
                        derniere_periode.save()
                        tempsDebut = None
    else:
        # Le fichier de données pour le local n'existe pas.
      pass

import random
from datetime import datetime, timedelta
from .models import PeriodeActivite, Equipement
#PeriodeActivite.objects.all().delete()
#Liste des équipements disponibles
from django.db.models import Q
from .models import Equipement

# Filtrer les équipements dont le nom contient "lampe" ou "led"
from django.db.models import Q
""" 
equipements = Equipement.objects.exclude(
    Q(nom__icontains='humidificateur') |
    Q(nom__icontains='chauffage') |
    Q(nom__icontains='climatiseur') |
    Q(nom__icontains='lampe') |
    Q(nom__icontains='led')
)

equipements = Equipement.objects.all()

#Fonction pour générer une heure aléatoire dans une journée

def randomtime():
    return timedelta(hours=random.randint(0, 23), minutes=random.randint(0, 59), seconds=random.randint(0, 59))

#Définir la plage de dates
start_date = datetime(2024, 1, 1)
end_date = datetime(2024, 6, 30)

#Boucle à travers chaque jour
current_date = start_date
while current_date <= end_date:
    # Boucle à travers chaque équipement
    for equipement in equipements:
       
        # Générer un nombre aléatoire de périodes d'activité pour chaque équipement et chaque jour
          num_activites = random.randint(1, 3)

          for i in range(num_activites):
              # Générer des dates de début et de fin aléatoires pour la journée
              debut = current_date + randomtime()
              fin = debut + timedelta(minutes=random.randint(30, 240))  # Durée aléatoire entre 30 minutes et 4 heures

              # Calculer la durée de la période
              duree = (fin - debut).total_seconds() / 3600  # Convertir en heures

              # Récupérer la puissance de l'équipement
              puissance = equipement.puissance  # Supposons que le champ pour la puissance soit 'puissance'

              # Calculer la consommation
              consommation = duree * puissance

              # Créer une nouvelle période d'activité
              periode_activite = PeriodeActivite.objects.create(
                  tempsDebut=debut,
                  tempsFin=fin,
                  Equipement=equipement,
                  consommation=consommation
              )

    # Passer au jour suivant
    current_date += timedelta(days=1)
 """

import random
from datetime import datetime, timedelta
import csv
mois_chauds = [6, 7, 8]
mois_froids = [1, 2, 11, 12]
mois_frais = [3, 4, 5, 9, 10]

matin = [6, 7, 8, 9, 10]
midi = [11, 12, 13, 14]
soir = [15, 16, 17, 18, 19]
jour = matin + midi + soir
nuit = [0, 1, 2, 3, 4, 5, 20, 21, 22, 23]


#Fonction pour générer une heure aléatoire dans une journée


def générerT1(date, prec):
  #Possibilité de réécrire la valeur précédente
  panne_probabilite = 0.05

    # Vérifier si une panne se produit
  
  if round(random.uniform(0, 1), 0)==1 :
    return prec

  T='0'
  i=1 # il tente maximum 10 fois pour avoir une valeur proche à la précédente
  if int(date.strftime('%m')) in mois_chauds:

    if int(date.strftime('%H')) in matin :
      T =(round(random.uniform(18.0, 20.0), 1))
      while(i<10 and prec!=0 and (float(T)>prec+0.5 or float(T)<prec-0.5)):
        T =(round(random.uniform(18.0, 20.0), 1))
        i=i+1

    elif int(date.strftime('%H')) in midi :
      T =(round(random.uniform(17.0, 18.0), 1))
      while(i<10 and prec!=0 and float(T)>prec+0.5 and float(T)<prec+0.5):
        T =(round(random.uniform(17.0, 18.0), 1))
        i=i+1

    elif int(date.strftime('%H')) in soir :
      T =(round(random.uniform(18.0, 20.0), 1))
      while(i<10 and prec!=0 and float(T)>prec+0.5 and float(T)<prec+0.5):
        T =(round(random.uniform(18.0, 20.0), 1))
        i=i+1

    elif int(date.strftime('%H')) in nuit :
      T =(round(random.uniform(17.0, 18.0), 1))
      while(i<10 and prec!=0 and float(T)>prec+0.5 and float(T)<prec+0.5):
        T =(round(random.uniform(17.0, 20.0), 1))
        i=i+1


  elif int(date.strftime('%m')) in mois_froids:

    if int(date.strftime('%H')) in jour :
      T =(round(random.uniform(22.0, 24.0), 1))
      while(i<10 and prec!=0 and float(T)>prec+0.5 and float(T)<prec-0.5):
        T =(round(random.uniform(18.0, 20.0), 1))
        i=i+1

    elif int(date.strftime('%H')) in nuit :
      T =(round(random.uniform(24.0, 26.0), 1))
      while(i<10 and prec!=0 and float(T)>prec+0.5 and float(T)<prec+0.5):
        T =(round(random.uniform(17.0, 20.0), 1))
        i=i+1


  elif int(date.strftime('%m')) in mois_frais:

    if int(date.strftime('%H')) in matin :
      T =(round(random.uniform(20.0, 22.0), 1))
      while(i<10 and prec!=0 and float(T)>prec+0.5 and float(T)<prec-0.5):
        T =(round(random.uniform(18.0, 20.0), 1))
        i=i+1

    elif int(date.strftime('%H')) in midi :
      T =(round(random.uniform(19.0, 21.0), 1))
      while(i<10 and prec!=0 and float(T)>prec+0.5 and float(T)<prec+0.5):
        T =(round(random.uniform(17.0, 18.0), 1))
        i=i+1

    elif int(date.strftime('%H')) in soir :
      T =(round(random.uniform(20.0, 22.0), 1))
      while(i<10 and prec!=0 and float(T)>prec+0.5 and float(T)<prec+0.5):
        T =(round(random.uniform(18.0, 20.0), 1))
        i=i+1

    elif int(date.strftime('%H')) in nuit :
      T =(round(random.uniform(20.0, 22.0), 1))
      while(i<10 and prec!=0 and float(T)>prec+0.5 and float(T)<prec+0.5):
        T =(round(random.uniform(17.0, 20.0), 1))
        i=i+1

  return T
def générerH1(date, prec):
  panne_probabilite = 0.05

    # Vérifier si une panne se produit
  
  #Possibilité de réécrire la valeur précédente
  if round(random.uniform(0, 1), 0)==1 :
    return prec

  T='0'
  i=1 # il tente maximum 10 fois pour avoir une valeur proche à la précédente
  if int(date.strftime('%m')) in mois_chauds:

    if int(date.strftime('%H')) in matin :
      T =(round(random.uniform(50.0, 60.0), 1))
      while(i<10 and prec!=0 and (float(T)>prec+0.5 or float(T)<prec-0.5)):
        T =(round(random.uniform(50.0, 60.0), 1))
        i=i+1

    elif int(date.strftime('%H')) in midi :
      T =(round(random.uniform(40.0, 50.0), 1))
      while(i<10 and prec!=0 and float(T)>prec+0.5 and float(T)<prec+0.5):
        T =(round(random.uniform(40.0, 50.0), 1))
        i=i+1

    elif int(date.strftime('%H')) in soir :
      T =(round(random.uniform(40.0, 50.0), 1))
      while(i<10 and prec!=0 and float(T)>prec+0.5 and float(T)<prec+0.5):
        T =(round(random.uniform(40.0, 50.0), 1))
        i=i+1

    elif int(date.strftime('%H')) in nuit :
      T =(round(random.uniform(50.0, 60.0), 1))
      while(i<10 and prec!=0 and float(T)>prec+0.5 and float(T)<prec+0.5):
        T =(round(random.uniform(50.0, 60.0), 1))
        i=i+1


  elif int(date.strftime('%m')) in mois_froids:

    if int(date.strftime('%H')) in jour :
      T =(round(random.uniform(45.0, 55.0), 1))
      while(i<10 and prec!=0 and float(T)>prec+0.5 and float(T)<prec-0.5):
        T =(round(random.uniform(45.0, 55.0), 1))
        i=i+1

    elif int(date.strftime('%H')) in nuit :
      T =(round(random.uniform(45.0, 55.0), 1))
      while(i<10 and prec!=0 and float(T)>prec+0.5 and float(T)<prec+0.5):
        T =(round(random.uniform(45.0, 55.0), 1))
        i=i+1


  elif int(date.strftime('%m')) in mois_frais:

    if int(date.strftime('%H')) in matin :
      T =(round(random.uniform(50.0, 60.0), 1))
      while(i<10 and prec!=0 and float(T)>prec+0.5 and float(T)<prec-0.5):
        T =(round(random.uniform(50.0, 60.0), 1))
        i=i+1

    elif int(date.strftime('%H')) in midi :
      T =(round(random.uniform(50.0, 60.0), 1))
      while(i<10 and prec!=0 and float(T)>prec+0.5 and float(T)<prec+0.5):
        T =(round(random.uniform(50.0, 60.0), 1))
        i=i+1

    elif int(date.strftime('%H')) in soir :
      T =(round(random.uniform(45.0, 55.0), 1))
      while(i<10 and prec!=0 and float(T)>prec+0.5 and float(T)<prec+0.5):
        T =(round(random.uniform(45.0, 55.0), 1))
        i=i+1

    elif int(date.strftime('%H')) in nuit :
      T =(round(random.uniform(45.0, 55.0), 1))
      while(i<10 and prec!=0 and float(T)>prec+0.5 and float(T)<prec+0.5):
        T =(round(random.uniform(45.0, 55.0), 1))
        i=i+1

  return T
def générerT2(date, prec):
  panne_probabilite = 0.05

    # Vérifier si une panne se produit
  
  #Possibilité de réécrire la valeur précédente

  if round(random.uniform(0, 1), 0)==1 :
    return prec

  T='0'
  i=1 # il tente maximum 10 fois pour avoir une valeur proche à la précédente
  if int(date.strftime('%m')) in mois_chauds:

    if int(date.strftime('%H')) in matin :
      T =(round(random.uniform(15.0, 25.0), 1))
      while(i<10 and prec!=0 and (float(T)>prec+0.5 or float(T)<prec-0.5)):
        T =(round(random.uniform(15.0, 25.0), 1))
        i=i+1

    elif int(date.strftime('%H')) in midi :
      T =(round(random.uniform(15.0, 25.0), 1))
      while(i<10 and prec!=0 and float(T)>prec+0.5 and float(T)<prec+0.5):
        T =(round(random.uniform(15.0, 25.0), 1))
        i=i+1

    elif int(date.strftime('%H')) in soir :
      T =(round(random.uniform(15.0, 25.0), 1))
      while(i<10 and prec!=0 and float(T)>prec+0.5 and float(T)<prec+0.5):
        T =(round(random.uniform(15.0, 25.0), 1))
        i=i+1

    elif int(date.strftime('%H')) in nuit :
      T =(round(random.uniform(15.0, 25.0), 1))
      while(i<10 and prec!=0 and float(T)>prec+0.5 and float(T)<prec+0.5):
        T =(round(random.uniform(15.0, 25.0), 1))
        i=i+1


  elif int(date.strftime('%m')) in mois_froids:

    if int(date.strftime('%H')) in jour :
      T =(round(random.uniform(15.0, 25.0), 1))
      while(i<10 and prec!=0 and float(T)>prec+0.5 and float(T)<prec-0.5):
        T =(round(random.uniform(15.0, 25.0), 1))
        i=i+1

    elif int(date.strftime('%H')) in nuit :
      T =(round(random.uniform(15.0, 25.0), 1))
      while(i<10 and prec!=0 and float(T)>prec+0.5 and float(T)<prec+0.5):
        T =(round(random.uniform(15.0, 25.0), 1))
        i=i+1


  elif int(date.strftime('%m')) in mois_frais:

    if int(date.strftime('%H')) in matin :
      T =(round(random.uniform(15.0, 25.0), 1))
      while(i<10 and prec!=0 and float(T)>prec+0.5 and float(T)<prec-0.5):
        T =(round(random.uniform(15.0, 25.0), 1))
        i=i+1

    elif int(date.strftime('%H')) in midi :
      T =(round(random.uniform(15.0, 25.0), 1))
      while(i<10 and prec!=0 and float(T)>prec+0.5 and float(T)<prec+0.5):
        T =(round(random.uniform(15.0, 25.0), 1))
        i=i+1

    elif int(date.strftime('%H')) in soir :
      T =(round(random.uniform(15.0, 25.0), 1))
      while(i<10 and prec!=0 and float(T)>prec+0.5 and float(T)<prec+0.5):
        T =(round(random.uniform(15.0, 25.0), 1))
        i=i+1

    elif int(date.strftime('%H')) in nuit :
      T =(round(random.uniform(15.0, 25.0), 1))
      while(i<10 and prec!=0 and float(T)>prec+0.5 and float(T)<prec+0.5):
        T =(round(random.uniform(15.0, 25.0), 1))
        i=i+1

  return T
def générerH2(date, prec):
  panne_probabilite = 0.05

    # Vérifier si une panne se produit

  #Possibilité de réécrire la valeur précédente
  if round(random.uniform(0, 1), 0)==1 :
    return prec

  T='0'
  i=1 # il tente maximum 10 fois pour avoir une valeur proche à la précédente
  if int(date.strftime('%m')) in mois_chauds:

    if int(date.strftime('%H')) in matin :
      T =(round(random.uniform(50.0, 60.0), 1))
      while(i<10 and prec!=0 and (float(T)>prec+0.5 or float(T)<prec-0.5)):
        T =(round(random.uniform(50.0, 60.0), 1))
        i=i+1

    elif int(date.strftime('%H')) in midi :
      T =(round(random.uniform(30.0, 40.0), 1))
      while(i<10 and prec!=0 and float(T)>prec+0.5 and float(T)<prec+0.5):
        T =(round(random.uniform(30.0, 40.0), 1))
        i=i+1

    elif int(date.strftime('%H')) in soir :
      T =(round(random.uniform(30.0, 40.0), 1))
      while(i<10 and prec!=0 and float(T)>prec+0.5 and float(T)<prec+0.5):
        T =(round(random.uniform(30.0, 40.0), 1))
        i=i+1

    elif int(date.strftime('%H')) in nuit :
      T =(round(random.uniform(50.0, 60.0), 1))
      while(i<10 and prec!=0 and float(T)>prec+0.5 and float(T)<prec+0.5):
        T =(round(random.uniform(50.0, 60.0), 1))
        i=i+1


  elif int(date.strftime('%m')) in mois_froids:

    if int(date.strftime('%H')) in jour :
      T =(round(random.uniform(35.0, 45.0), 1))
      while(i<10 and prec!=0 and float(T)>prec+0.5 and float(T)<prec-0.5):
        T =(round(random.uniform(35.0, 45.0), 1))
        i=i+1

    elif int(date.strftime('%H')) in nuit :
      T =(round(random.uniform(35.0, 45.0), 1))
      while(i<10 and prec!=0 and float(T)>prec+0.5 and float(T)<prec+0.5):
        T =(round(random.uniform(35.0, 45.0), 1))
        i=i+1


  elif int(date.strftime('%m')) in mois_frais:

    if int(date.strftime('%H')) in matin :
      T =(round(random.uniform(50.0, 60.0), 1))
      while(i<10 and prec!=0 and float(T)>prec+0.5 and float(T)<prec-0.5):
        T =(round(random.uniform(50.0, 60.0), 1))
        i=i+1

    elif int(date.strftime('%H')) in midi :
      T =(round(random.uniform(50.0, 60.0), 1))
      while(i<10 and prec!=0 and float(T)>prec+0.5 and float(T)<prec+0.5):
        T =(round(random.uniform(50.0, 60.0), 1))
        i=i+1

    elif int(date.strftime('%H')) in soir :
      T =(round(random.uniform(35.0, 45.0), 1))
      while(i<10 and prec!=0 and float(T)>prec+0.5 and float(T)<prec+0.5):
        T =(round(random.uniform(35.0, 45.0), 1))
        i=i+1

    elif int(date.strftime('%H')) in nuit :
      T =(round(random.uniform(35.0, 45.0), 1))
      while(i<10 and prec!=0 and float(T)>prec+0.5 and float(T)<prec+0.5):
        T =(round(random.uniform(35.0, 45.0), 1))
        i=i+1

  return T
def générerT3(date, prec):
  panne_probabilite = 0.05

    # Vérifier si une panne se produit
 
  #Possibilité de réécrire la valeur précédente
  if round(random.uniform(0, 1), 0)==1 :
    return prec

  T='0'
  i=1 # il tente maximum 10 fois pour avoir une valeur proche à la précédente
  if int(date.strftime('%m')) in mois_chauds:

    if int(date.strftime('%H')) in matin :
      T =(round(random.uniform(5.0, 8.0), 1))
      while(i<10 and prec!=0 and (float(T)>prec+0.5 or float(T)<prec-0.5)):
        T =(round(random.uniform(5.0, 8.0), 1))
        i=i+1

    elif int(date.strftime('%H')) in midi :
      T =(round(random.uniform(5.0, 8.0), 1))
      while(i<10 and prec!=0 and float(T)>prec+0.5 and float(T)<prec+0.5):
        T =(round(random.uniform(5.0, 8.0), 1))
        i=i+1

    elif int(date.strftime('%H')) in soir :
      T =(round(random.uniform(5.0, 8.0), 1))
      while(i<10 and prec!=0 and float(T)>prec+0.5 and float(T)<prec+0.5):
        T =(round(random.uniform(5.0, 8.0), 1))
        i=i+1

    elif int(date.strftime('%H')) in nuit :
      T =(round(random.uniform(5.0, 8.0), 1))
      while(i<10 and prec!=0 and float(T)>prec+0.5 and float(T)<prec+0.5):
        T =(round(random.uniform(5.0, 8.0), 1))
        i=i+1


  elif int(date.strftime('%m')) in mois_froids:

    if int(date.strftime('%H')) in jour :
      T =(round(random.uniform(5.0, 8.0), 1))
      while(i<10 and prec!=0 and float(T)>prec+0.5 and float(T)<prec-0.5):
        T =(round(random.uniform(5.0, 8.0), 1))
        i=i+1

    elif int(date.strftime('%H')) in nuit :
      T =(round(random.uniform(5.0, 8.0), 1))
      while(i<10 and prec!=0 and float(T)>prec+0.5 and float(T)<prec+0.5):
        T =(round(random.uniform(5.0, 8.0), 1))
        i=i+1


  elif int(date.strftime('%m')) in mois_frais:

    if int(date.strftime('%H')) in matin :
      T =(round(random.uniform(5.0, 8.0), 1))
      while(i<10 and prec!=0 and float(T)>prec+0.5 and float(T)<prec-0.5):
        T =(round(random.uniform(5.0, 8.0), 1))
        i=i+1

    elif int(date.strftime('%H')) in midi :
      T =(round(random.uniform(5.0, 8.0), 1))
      while(i<10 and prec!=0 and float(T)>prec+0.5 and float(T)<prec+0.5):
        T =(round(random.uniform(5.0, 8.0), 1))
        i=i+1

    elif int(date.strftime('%H')) in soir :
      T =(round(random.uniform(5.0, 8.0), 1))
      while(i<10 and prec!=0 and float(T)>prec+0.5 and float(T)<prec+0.5):
        T =(round(random.uniform(5.0, 8.0), 1))
        i=i+1

    elif int(date.strftime('%H')) in nuit :
      T =(round(random.uniform(5.0, 8.0), 1))
      while(i<10 and prec!=0 and float(T)>prec+0.5 and float(T)<prec+0.5):
        T =(round(random.uniform(5.0, 8.0), 1))
        i=i+1

  return T
def générerH3(date, prec):
  panne_probabilite = 0.05

    # Vérifier si une panne se produit
 
  #Possibilité de réécrire la valeur précédente
  if round(random.uniform(0, 1), 0)==1 :
    return prec

  T='0'
  i=1 # il tente maximum 10 fois pour avoir une valeur proche à la précédente
  if int(date.strftime('%m')) in mois_chauds:

    if int(date.strftime('%H')) in matin :
      T =(round(random.uniform(50.0, 60.0), 1))
      while(i<10 and prec!=0 and (float(T)>prec+0.5 or float(T)<prec-0.5)):
        T =(round(random.uniform(50.0, 60.0), 1))
        i=i+1

    elif int(date.strftime('%H')) in midi :
      T =(round(random.uniform(50.0, 60.0), 1))
      while(i<10 and prec!=0 and float(T)>prec+0.5 and float(T)<prec+0.5):
        T =(round(random.uniform(50.0, 60.0), 1))
        i=i+1

    elif int(date.strftime('%H')) in soir :
      T =(round(random.uniform(50.0, 60.0), 1))
      while(i<10 and prec!=0 and float(T)>prec+0.5 and float(T)<prec+0.5):
        T =(round(random.uniform(50.0, 60.0), 1))
        i=i+1

    elif int(date.strftime('%H')) in nuit :
      T =(round(random.uniform(50.0, 60.0), 1))
      while(i<10 and prec!=0 and float(T)>prec+0.5 and float(T)<prec+0.5):
        T =(round(random.uniform(50.0, 60.0), 1))
        i=i+1


  elif int(date.strftime('%m')) in mois_froids:

    if int(date.strftime('%H')) in jour :
      T =(round(random.uniform(50.0, 60.0), 1))
      while(i<10 and prec!=0 and float(T)>prec+0.5 and float(T)<prec-0.5):
        T =(round(random.uniform(50.0, 60.0), 1))
        i=i+1

    elif int(date.strftime('%H')) in nuit :
      T =(round(random.uniform(50.0, 60.0), 1))
      while(i<10 and prec!=0 and float(T)>prec+0.5 and float(T)<prec+0.5):
        T =(round(random.uniform(50.0, 60.0), 1))
        i=i+1


  elif int(date.strftime('%m')) in mois_frais:

    if int(date.strftime('%H')) in matin :
      T =(round(random.uniform(50.0, 60.0), 1))
      while(i<10 and prec!=0 and float(T)>prec+0.5 and float(T)<prec-0.5):
        T =(round(random.uniform(50.0, 60.0), 1))
        i=i+1

    elif int(date.strftime('%H')) in midi :
      T =(round(random.uniform(50.0, 60.0), 1))
      while(i<10 and prec!=0 and float(T)>prec+0.5 and float(T)<prec+0.5):
        T =(round(random.uniform(50.0, 60.0), 1))
        i=i+1

    elif int(date.strftime('%H')) in soir :
      T =(round(random.uniform(50.0, 60.0), 1))
      while(i<10 and prec!=0 and float(T)>prec+0.5 and float(T)<prec+0.5):
        T =(round(random.uniform(50.0, 60.0), 1))
        i=i+1

    elif int(date.strftime('%H')) in nuit :
      T =(round(random.uniform(50.0, 60.0), 1))
      while(i<10 and prec!=0 and float(T)>prec+0.5 and float(T)<prec+0.5):
        T =(round(random.uniform(50.0, 60.0), 1))
        i=i+1

  return T
def générerT4(date, prec):
  panne_probabilite = 0.05

    # Vérifier si une panne se produit
  
  #Possibilité de réécrire la valeur précédente
  if round(random.uniform(0, 1), 0)==1 :
    return prec

  T='0'
  i=1 # il tente maximum 10 fois pour avoir une valeur proche à la précédente
  if int(date.strftime('%m')) in mois_chauds:

    if int(date.strftime('%H')) in matin :
      T =(round(random.uniform(-18.0,-15.0), 1))
      while(i<10 and prec!=0 and (float(T)>prec+0.5 or float(T)<prec-0.5)):
        T =(round(random.uniform(-18.0,-15.0), 1))
        i=i+1

    elif int(date.strftime('%H')) in midi :
      T =(round(random.uniform(-18.0,-15.0), 1))
      while(i<10 and prec!=0 and float(T)>prec+0.5 and float(T)<prec+0.5):
        T =(round(random.uniform(-18.0,-15.0), 1))
        i=i+1

    elif int(date.strftime('%H')) in soir :
      T =(round(random.uniform(-18.0,-15.0), 1))
      while(i<10 and prec!=0 and float(T)>prec+0.5 and float(T)<prec+0.5):
        T =(round(random.uniform(-18.0,-15.0), 1))
        i=i+1

    elif int(date.strftime('%H')) in nuit :
      T =(round(random.uniform(-18.0,-15.0), 1))
      while(i<10 and prec!=0 and float(T)>prec+0.5 and float(T)<prec+0.5):
        T =(round(random.uniform(-18.0,-15.0), 1))
        i=i+1


  elif int(date.strftime('%m')) in mois_froids:

    if int(date.strftime('%H')) in jour :
      T =(round(random.uniform(-18.0,-15.0), 1))
      while(i<10 and prec!=0 and float(T)>prec+0.5 and float(T)<prec-0.5):
        T =(round(random.uniform(-18.0,-15.0), 1))
        i=i+1

    elif int(date.strftime('%H')) in nuit :
      T =(round(random.uniform(-18.0,-15.0), 1))
      while(i<10 and prec!=0 and float(T)>prec+0.5 and float(T)<prec+0.5):
        T =(round(random.uniform(-18.0,-15.0), 1))
        i=i+1


  elif int(date.strftime('%m')) in mois_frais:

    if int(date.strftime('%H')) in matin :
      T =(round(random.uniform(-18.0,-15.0), 1))
      while(i<10 and prec!=0 and float(T)>prec+0.5 and float(T)<prec-0.5):
        T =(round(random.uniform(-18.0,-15.0), 1))
        i=i+1

    elif int(date.strftime('%H')) in midi :
      T =(round(random.uniform(-18.0,-15.0), 1))
      while(i<10 and prec!=0 and float(T)>prec+0.5 and float(T)<prec+0.5):
        T =(round(random.uniform(-18.0,-15.0), 1))
        i=i+1

    elif int(date.strftime('%H')) in soir :
      T =(round(random.uniform(-18.0,-15.0), 1))
      while(i<10 and prec!=0 and float(T)>prec+0.5 and float(T)<prec+0.5):
        T =(round(random.uniform(-18.0,-15.0), 1))
        i=i+1

    elif int(date.strftime('%H')) in nuit :
      T =(round(random.uniform(-18.0,-15.0), 1))
      while(i<10 and prec!=0 and float(T)>prec+0.5 and float(T)<prec+0.5):
        T =(round(random.uniform(-18.0,-15.00), 1))
        i=i+1

  return T
def générerH4(date, prec):
  panne_probabilite = 0.05

    # Vérifier si une panne se produit
  
  #Possibilité de réécrire la valeur précédente
  if round(random.uniform(0, 1), 0)==1 :
    return prec

  T='0'
  i=1 # il tente maximum 10 fois pour avoir une valeur proche à la précédente
  if int(date.strftime('%m')) in mois_chauds:

    if int(date.strftime('%H')) in matin :
      T =(round(random.uniform(50.0, 60.0), 1))
      while(i<10 and prec!=0 and (float(T)>prec+0.5 or float(T)<prec-0.5)):
        T =(round(random.uniform(50.0, 60.0), 1))
        i=i+1

    elif int(date.strftime('%H')) in midi :
      T =(round(random.uniform(50.0, 60.0), 1))
      while(i<10 and prec!=0 and float(T)>prec+0.5 and float(T)<prec+0.5):
        T =(round(random.uniform(50.0, 60.0), 1))
        i=i+1

    elif int(date.strftime('%H')) in soir :
      T =(round(random.uniform(50.0, 60.0), 1))
      while(i<10 and prec!=0 and float(T)>prec+0.5 and float(T)<prec+0.5):
        T =(round(random.uniform(50.0, 60.0), 1))
        i=i+1

    elif int(date.strftime('%H')) in nuit :
      T =(round(random.uniform(50.0, 60.0), 1))
      while(i<10 and prec!=0 and float(T)>prec+0.5 and float(T)<prec+0.5):
        T =(round(random.uniform(50.0, 60.0), 1))
        i=i+1


  elif int(date.strftime('%m')) in mois_froids:

    if int(date.strftime('%H')) in jour :
      T =(round(random.uniform(50.0, 60.0), 1))
      while(i<10 and prec!=0 and float(T)>prec+0.5 and float(T)<prec-0.5):
        T =(round(random.uniform(50.0, 60.0), 1))
        i=i+1

    elif int(date.strftime('%H')) in nuit :
      T =(round(random.uniform(50.0, 60.0), 1))
      while(i<10 and prec!=0 and float(T)>prec+0.5 and float(T)<prec+0.5):
        T =(round(random.uniform(50.0, 60.0), 1))
        i=i+1


  elif int(date.strftime('%m')) in mois_frais:

    if int(date.strftime('%H')) in matin :
      T =(round(random.uniform(50.0, 60.0), 1))
      while(i<10 and prec!=0 and float(T)>prec+0.5 and float(T)<prec-0.5):
        T =(round(random.uniform(50.0, 60.0), 1))
        i=i+1

    elif int(date.strftime('%H')) in midi :
      T =(round(random.uniform(50.0, 60.0), 1))
      while(i<10 and prec!=0 and float(T)>prec+0.5 and float(T)<prec+0.5):
        T =(round(random.uniform(50.0, 60.0), 1))
        i=i+1

    elif int(date.strftime('%H')) in soir :
      T =(round(random.uniform(50.0, 60.0), 1))
      while(i<10 and prec!=0 and float(T)>prec+0.5 and float(T)<prec+0.5):
        T =(round(random.uniform(50.0, 60.0), 1))
        i=i+1

    elif int(date.strftime('%H')) in nuit :
      T =(round(random.uniform(50.0, 60.0), 1))
      while(i<10 and prec!=0 and float(T)>prec+0.5 and float(T)<prec+0.5):
        T =(round(random.uniform(50.0, 60.0), 1))
        i=i+1

  return T

def générerT5(date, prec):
  panne_probabilite = 0.05

    # Vérifier si une panne se produit
  
  #Possibilité de réécrire la valeur précédente
  if round(random.uniform(0, 1), 0)==1 :
    return prec

  T='0'
  i=1 # il tente maximum 10 fois pour avoir une valeur proche à la précédente
  if int(date.strftime('%m')) in mois_chauds:

    if int(date.strftime('%H')) in matin :
      T =(round(random.uniform(21.0, 23.0), 1))
      while(i<10 and prec!=0 and (float(T)>prec+0.5 or float(T)<prec-0.5)):
        T =(round(random.uniform(21.0, 23.0), 1))
        i=i+1

    elif int(date.strftime('%H')) in midi :
      T =(round(random.uniform(20.0, 21.0), 1))
      while(i<10 and prec!=0 and float(T)>prec+0.5 and float(T)<prec+0.5):
        T =(round(random.uniform(20.0, 21.0), 1))
        i=i+1

    elif int(date.strftime('%H')) in soir :
      T =(round(random.uniform(21.0, 23.0), 1))
      while(i<10 and prec!=0 and float(T)>prec+0.5 and float(T)<prec+0.5):
        T =(round(random.uniform(21.0, 23.0), 1))
        i=i+1

    elif int(date.strftime('%H')) in nuit :
      T =(round(random.uniform(20.0, 21.0), 1))
      while(i<10 and prec!=0 and float(T)>prec+0.5 and float(T)<prec+0.5):
        T =(round(random.uniform(20.0, 21.0), 1))
        i=i+1


  elif int(date.strftime('%m')) in mois_froids:

    if int(date.strftime('%H')) in jour :
      T =(round(random.uniform(23.0, 25.0), 1))
      while(i<10 and prec!=0 and float(T)>prec+0.5 and float(T)<prec-0.5):
        T =(round(random.uniform(23.0, 25.0), 1))
        i=i+1

    elif int(date.strftime('%H')) in nuit :
      T =(round(random.uniform(20.0, 21.0), 1))
      while(i<10 and prec!=0 and float(T)>prec+0.5 and float(T)<prec+0.5):
        T =(round(random.uniform(20.0, 21.0), 1))
        i=i+1


  elif int(date.strftime('%m')) in mois_frais:

    if int(date.strftime('%H')) in matin :
      T =(round(random.uniform(20.0, 22.0), 1))
      while(i<10 and prec!=0 and float(T)>prec+0.5 and float(T)<prec-0.5):
        T =(round(random.uniform(20.0, 22.0), 1))
        i=i+1

    elif int(date.strftime('%H')) in midi :
      T =(round(random.uniform(21.0, 23.0), 1))
      while(i<10 and prec!=0 and float(T)>prec+0.5 and float(T)<prec+0.5):
        T =(round(random.uniform(21.0, 23.0), 1))
        i=i+1

    elif int(date.strftime('%H')) in soir :
      T =(round(random.uniform(20.0, 22.0), 1))
      while(i<10 and prec!=0 and float(T)>prec+0.5 and float(T)<prec+0.5):
        T =(round(random.uniform(20.0, 22.0), 1))
        i=i+1

    elif int(date.strftime('%H')) in nuit :
      T =(round(random.uniform(20.0, 22.0), 1))
      while(i<10 and prec!=0 and float(T)>prec+0.5 and float(T)<prec+0.5):
        T =(round(random.uniform(20.0, 22.0), 1))
        i=i+1

  return T
def générerH5(date, prec):
  panne_probabilite = 0.05

    # Vérifier si une panne se produit
 
  #Possibilité de réécrire la valeur précédente
  if round(random.uniform(0, 1), 0)==1 :
    return prec

  T='0'
  i=1 # il tente maximum 10 fois pour avoir une valeur proche à la précédente
  if int(date.strftime('%m')) in mois_chauds:

    if int(date.strftime('%H')) in matin :
      T =(round(random.uniform(50.0, 60.0), 1))
      while(i<10 and prec!=0 and (float(T)>prec+0.5 or float(T)<prec-0.5)):
        T =(round(random.uniform(50.0, 60.0), 1))
        i=i+1

    elif int(date.strftime('%H')) in midi :
      T =(round(random.uniform(30.0, 40.0), 1))
      while(i<10 and prec!=0 and float(T)>prec+0.5 and float(T)<prec+0.5):
        T =(round(random.uniform(30.0, 40.0), 1))
        i=i+1

    elif int(date.strftime('%H')) in soir :
      T =(round(random.uniform(30.0, 40.0), 1))
      while(i<10 and prec!=0 and float(T)>prec+0.5 and float(T)<prec+0.5):
        T =(round(random.uniform(30.0, 40.0), 1))
        i=i+1

    elif int(date.strftime('%H')) in nuit :
      T =(round(random.uniform(50.0, 60.0), 1))
      while(i<10 and prec!=0 and float(T)>prec+0.5 and float(T)<prec+0.5):
        T =(round(random.uniform(50.0, 60.0), 1))
        i=i+1


  elif int(date.strftime('%m')) in mois_froids:

    if int(date.strftime('%H')) in jour :
      T =(round(random.uniform(35.0, 45.0), 1))
      while(i<10 and prec!=0 and float(T)>prec+0.5 and float(T)<prec-0.5):
        T =(round(random.uniform(35.0, 45.0), 1))
        i=i+1

    elif int(date.strftime('%H')) in nuit :
      T =(round(random.uniform(35.0, 45.0), 1))
      while(i<10 and prec!=0 and float(T)>prec+0.5 and float(T)<prec+0.5):
        T =(round(random.uniform(35.0, 45.0), 1))
        i=i+1


  elif int(date.strftime('%m')) in mois_frais:

    if int(date.strftime('%H')) in matin :
      T =(round(random.uniform(50.0, 60.0), 1))
      while(i<10 and prec!=0 and float(T)>prec+0.5 and float(T)<prec-0.5):
        T =(round(random.uniform(50.0, 60.0), 1))
        i=i+1

    elif int(date.strftime('%H')) in midi :
      T =(round(random.uniform(50.0, 60.0), 1))
      while(i<10 and prec!=0 and float(T)>prec+0.5 and float(T)<prec+0.5):
        T =(round(random.uniform(50.0, 60.0), 1))
        i=i+1

    elif int(date.strftime('%H')) in soir :
      T =(round(random.uniform(35.0, 45.0), 1))
      while(i<10 and prec!=0 and float(T)>prec+0.5 and float(T)<prec+0.5):
        T =(round(random.uniform(35.0, 45.0), 1))
        i=i+1

    elif int(date.strftime('%H')) in nuit :
      T =(round(random.uniform(35.0, 45.0), 1))
      while(i<10 and prec!=0 and float(T)>prec+0.5 and float(T)<prec+0.5):
        T =(round(random.uniform(35.0, 45.0), 1))
        i=i+1

  return T
"""
################################## generate json file for new zone 
from django.http import JsonResponse
from django.core.files import File
import json
import os
from datetime import datetime, timedelta
import random

def generateJSON(minT):
      data = {}

      # Définir la période de temps
      date1 = datetime(2024, 1, 1, 0, 0, 0)
      date2 = datetime(2024, 6, 30, 23, 59, 0)
      delta = timedelta(minutes=1)

      c=1
      # Générer des données pour chaque jour
       # Utilisez request.data pour récupérer les données du corps de la requête
     
      param2 = minT
      if param2 =='17':
        T_func = générerT1
        H_func = générerH1

      elif param2 == '15':
        T_func = générerT2
        H_func = générerH2

      elif param2 == '5':
        T_func = générerT3
        H_func = générerH3

      elif param2 == '-18':
        T_func = générerT4
        H_func = générerH4

      else:
        T_func = générerT5
        H_func = générerH5     

      while date1 <= date2:
        if(c==1):
          prec1=22
          prec2=40
          c=c+1

        prec1 = float(T_func(date1, prec1))
        prec2 = float(H_func(date1,prec2))
                  
                  

        data[date1.strftime('%Y-%m-%d %H:%M:%S')] = {
            'temperature': T_func(date1, prec1),
            'humidite': H_func(date1, prec2),
            'presence': random.randint(0,1)
                      
                    
        }

        date1 += delta

      return data
""" 
class generateExcel(APIView):

    def post(self, request, *args, **kwargs):
        data = request.data  # Utilisez request.data pour récupérer les données du corps de la requête
        param1 = data.get('id')
        param2 = data.get('minT')
        param3 = data.get('maxT')
        param4 = data.get('maxH')
        param5 = data.get('minH')

        donnees_aleatoires = generateJSON(param2,param3,param5,param4)
        json_data = json.dumps(donnees_aleatoires, indent=2)

    # Définir le chemin du fichier dans le dossier media
        chemin_fichier = os.path.join('media', 'donnees' + str(param1) + '.json')

    # Écrire les données JSON dans le fichier
        with open(chemin_fichier, 'w') as fichier:
          fichier.write(json_data)

        
        return Response('done', status=status.HTTP_200_OK)



############################## fin call and generate file JSON FOR NEW ZONE

import pandas as pd



""" class rechercher_donnees(APIView):
    def get(self, request):
        try:
            date_heure_recherchee = request.GET.get('date')
            nom_fichier = request.GET.get('nom_fichier')
            fichier_csv = 'media/data' + str(nom_fichier) + '.csv'
            df = pd.read_csv(fichier_csv, delimiter=';', header=None)
            df[0] = pd.to_datetime(df[0] + ' ' + df[1], format='%d/%m/%Y %H:%M')
            resultat = df[df[0] == pd.to_datetime(date_heure_recherchee, format='%d/%m/%Y %H:%M:%S')]

#Vérifier si des données correspondent à la date et à l'heure spécifiées
            if resultat.empty:
                return Response({'error': 'Aucune donnée correspondant à la date et l\'heure spécifiées'}, status=status.HTTP_404_NOT_FOUND)

#Sélectionner uniquement les valeurs de température et d'humidité de la 2ème et 3ème colonnes
            valeurs_colonnes = resultat.iloc[:, 2:4].values.tolist()

            # Renvoyer les valeurs des colonnes avec une clé 'data'
            return Response({'data': valeurs_colonnes}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR) """


class rechercher_donnees(APIView):
    def get(self, request):
        try:
            date_heure_recherchee = request.GET.get('date')
            nom_fichier = request.GET.get('nom_fichier')
            fichier_csv = 'media/data' + str(nom_fichier) + '.csv'
            df = pd.read_csv(fichier_csv, delimiter=';', nrows=43200,header=None)
            df[0] = pd.to_datetime(df[0] + ' ' + df[1], format='%d/%m/%Y %H:%M')
            resultat = df[df[0] == pd.to_datetime(date_heure_recherchee, format='%d/%m/%Y %H:%M:%S')]

            if resultat.empty:
                return Response({'error': 'Aucune donnée correspondant à la date et l\'heure spécifiées'}, status=status.HTTP_404_NOT_FOUND)

            valeurs_colonnes = resultat.iloc[:, 2:4].values.tolist()

            # Renvoyer les valeurs des colonnes avec une clé 'data'
            return Response({'data': valeurs_colonnes}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# pour l utiliser avec des args
def rechercher_donnees2(date_heure_recherchee, nom_fichier):
        fichier_csv = 'media/data' + str(nom_fichier) + '.csv'
        df = pd.read_csv(fichier_csv, delimiter=';', header=None)
        df[0] = pd.to_datetime(df[0] + ' ' + df[1], format='%d/%m/%Y %H:%M')
        resultat = df[df[0] == pd.to_datetime(date_heure_recherchee, format='%d/%m/%Y %H:%M:%S')]

        if resultat.empty:
            raise ValueError('Aucune donnée correspondant à la date et l\'heure spécifiées')

        valeurs_colonnes = resultat.iloc[:, 2:4].values.tolist()

        return valeurs_colonnes


import time

import csv, datetime
import time, random

mois_chauds = [6, 7, 8]
mois_froids = [1, 2, 11, 12]
mois_frais = [3, 4, 5, 9, 10]

matin = [6, 7, 8, 9, 10]
midi = [11, 12, 13, 14]
soir = [15, 16, 17, 18, 19]
jour = matin + midi + soir
nuit = [0, 1, 2, 3, 4, 5, 20, 21, 22, 23]
j=0
j1=0
k=False
k1=False
T=20.0

m=False
m1=False
compteur=0
compteur1=0
def genererTemp(date, prec):
  #Possibilité de réécrire la valeur précédente
  panne_probabilite = 0.001
  global k1
  global j1
  global m1
  global compteur1
  global k

  global j
  global T
  global m
  global compteur

  #time.sleep(1)
  #print('********* date',date,'********* prec',prec)
    # Augmenter progressivement la température jusqu'à 30 si prec > 26
  if random.random() < panne_probabilite and k1==False and j1==0 and random.randint(0, 1)==0:
      k1=True  # Générer une valeur spécifique pour indiquer une panne (par exemple, -999)
      T = prec-random.uniform(0.4, 0.8)
      #print('panne   k',k1,'      j',j1,'             T',T)
      
  elif(k1==True):
    if(prec>10.0 and  j1==0): 
        T=prec-random.uniform(0.4, 0.8)
        k1=True
        #print('cas >10    k',k1,'      j',j1,'             T',T)
    
   
       
    elif(compteur1<5 and (prec <10 or prec ==10) ) :
      T =prec 
      k1=True
      j1=1
      compteur1=compteur1+1
      #print('cas =10    k',k1,'      j',j1,'             T',T,'              compteur',compteur1)
      
    
    elif compteur1==5:
      T=prec-random.uniform(0.4, 0.8)
      compteur1=compteur1+1
    elif(prec<17.0 and j1==1 and compteur1>5):

      T=prec+random.uniform(0.4, 0.8)
      k1=True
      #print('cas >26    k',k,'      j',j,'             T',T)
      
    elif(prec<16.0 and prec>17.0  or prec==17.0  or prec==16.0 and j1==1 ):
      k1=False
      j1=0
      compteur1=0
      #print('cas =26    k',k,'      j',j,'             T',T)
  if random.random() < panne_probabilite and k==False and j==0 and random.randint(0, 1)==1:
      k=True  # Générer une valeur spécifique pour indiquer une panne (par exemple, -999)
      T = prec+random.uniform(0.4, 0.8)
      #print('panne   k',k,'      j',j,'             T',T)
      
  elif(k==True):
    if(prec<30.0 and  j==0): 
        T=prec+random.uniform(0.4, 0.8)
        k=True
        #print('cas <30    k',k,'      j',j,'             T',T)
    
   
       
    elif(compteur<5 and (prec >30 or prec ==30) ) :
      T =prec 
      k=True
      j=1
      compteur=compteur+1
      #print('cas =30    k',k,'      j',j,'             T',T,'              compteur',compteur)
      
    
    elif compteur==5:
      T=prec-random.uniform(0.4, 0.8)
      compteur=compteur+1
    elif(prec>26.0 and j==1 and compteur>5):

      T=prec-random.uniform(0.4, 0.8)
      k=True
      #print('cas >26    k',k,'      j',j,'             T',T)
      
    elif(prec>25.0 and prec<26.0  or prec==25.0  or prec==26.0 and j==1 ):
      k=False
      j=0
      compteur=0
      #print('cas =26    k',k,'      j',j,'             T',T)
  elif( k==False and j==0 and k1==False and j1==0 ):
    #print('cas ordinaire    k',k,'      j',j,'             T',T)
    
    if round(random.uniform(0.2, 0.9), 0)==1 :
      return (prec) 

    T='0'
    i=1 # il tente maximum 10 fois pour avoir une valeur proche à la précédente
    if int(date.strftime('%m')) in mois_chauds:

      if int(date.strftime('%H')) in matin :
        T = (round(random.uniform(18.0, 20.0), 1))
        while(i<10 and prec!=0 and (float(T)>prec+0.5 or float(T)<prec-0.5)):
          T =(round(random.uniform(18.0, 20.0), 1))
          i=i+1

      elif int(date.strftime('%H')) in midi :
        T = (round(random.uniform(17.0, 18.0), 1))
        while(i<10 and prec!=0 and float(T)>prec+0.5 and float(T)<prec+0.5):
          T = (round(random.uniform(17.0, 18.0), 1))
          i=i+1

      elif int(date.strftime('%H')) in soir :
        T = (round(random.uniform(18.0, 20.0), 1))
        while(i<10 and prec!=0 and float(T)>prec+0.5 and float(T)<prec+0.5):
          T = (round(random.uniform(18.0, 20.0), 1))
          i=i+1

      elif int(date.strftime('%H')) in nuit :
        T = (round(random.uniform(17.0, 18.0), 1))
        while(i<10 and prec!=0 and float(T)>prec+0.5 and float(T)<prec+0.5):
          T = (round(random.uniform(17.0, 20.0), 1))
          i=i+1


    elif int(date.strftime('%m')) in mois_froids:

      if int(date.strftime('%H')) in jour :
        T = (round(random.uniform(22.0, 24.0), 1))
        while(i<10 and prec!=0 and float(T)>prec+0.5 and float(T)<prec-0.5):
          T = (round(random.uniform(18.0, 20.0), 1))
          i=i+1

      elif int(date.strftime('%H')) in nuit :
        T = (round(random.uniform(24.0, 26.0), 1))
        while(i<10 and prec!=0 and float(T)>prec+0.5 and float(T)<prec+0.5):
          T = (round(random.uniform(17.0, 20.0), 1))
          i=i+1


    elif int(date.strftime('%m')) in mois_frais:

      if int(date.strftime('%H')) in matin :
        T = (round(random.uniform(20.0, 22.0), 1))
        while(i<10 and prec!=0 and float(T)>prec+0.5 and float(T)<prec-0.5):
          T = (round(random.uniform(18.0, 20.0), 1))
          i=i+1

      elif int(date.strftime('%H')) in midi :
        T = (round(random.uniform(19.0, 21.0), 1))
        while(i<10 and prec!=0 and float(T)>prec+0.5 and float(T)<prec+0.5):
          T = (round(random.uniform(17.0, 18.0), 1))
          i=i+1

      elif int(date.strftime('%H')) in soir :
        T = (round(random.uniform(20.0, 22.0), 1))
        while(i<10 and prec!=0 and float(T)>prec+0.5 and float(T)<prec+0.5):
          T = (round(random.uniform(18.0, 20.0), 1))
          i=i+1

      elif int(date.strftime('%H')) in nuit :
        T = (round(random.uniform(20.0, 22.0), 1))
        while(i<10 and prec!=0 and float(T)>prec+0.5 and float(T)<prec+0.5):
          T = (round(random.uniform(17.0, 20.0), 1))
          i=i+1

  return T




from django.http import JsonResponse
from django.core.files import File
import json
import os
from datetime import datetime, timedelta
import random
'''class generateJSON(APIView):

    def post(self, request, *args, **kwargs):
      data = {}

      # Définir la période de temps
      date1 = datetime(2024, 1, 1, 0, 0, 0)
      date2 = datetime(2024, 6, 30, 23, 59, 0)
      delta = timedelta(minutes=1)

      c=1
      # Générer des données pour chaque jour
      data1 = request.data  # Utilisez request.data pour récupérer les données du corps de la requête
     
      param2 = data1.get('minT')
      if param2 =='17':
        T_func = générerT1
        H_func = générerH1

      elif param2 == '15':
        T_func = générerT2
        H_func = générerH2

      elif param2 == '5':
        T_func = générerT3
        H_func = générerH3

      elif param2 == '-18':
        T_func = générerT4
        H_func = générerH4

      else:
        T_func = générerT5
        H_func = générerH5     

      while date1 <= date2:
        if(c==1):
          prec1=22
          prec2=40
          c=c+1

        prec1 = float(T_func(date1, prec1))
        prec2 = float(H_func(date1,prec2))
                  
                  

        data[date1.strftime('%Y-%m-%d %H:%M:%S')] = {
            'temperature': T_func(date1, prec1),
            'humidite': H_func(date1, prec2),
            'presence': random.randint(0,1)
                      
                    
        }

        date1 += delta

      return data 

'''
### debut generer json sur views
from random import randint

from django.http import JsonResponse
from django.core.files import File
import json
import os
from datetime import datetime, timedelta
import random
from random import uniform

def generateJSON(minT, maxT, minH, maxH):
    data = {}
    date1 = datetime.now().replace(second=0)
    date2 = datetime(2024, 6, 30, 23, 59, 0)
    delta = timedelta(minutes=1)

    while date1 <= date2:
        data[date1.strftime('%Y-%m-%d %H:%M:%S')] = {
            'temperature': uniform(float(minT), float(maxT)),
            'humidite': uniform(float(minH), float(maxH)),
            'presence': randint(0, 1)
        }
        date1 += delta

    return data


""" def generateJSON(minT,maxT,minH,maxH):
      data = {}

      # Définir la période de temps
      #date1 = datetime(2024, 1, 1, 0, 0, 0)
      date1 = datetime.now()
      print(date1)
      date2 = datetime(2024, 6, 30, 23, 59, 0)
      print(date2)
      delta = timedelta(minutes=1)

      c=1
      # Générer des données pour chaque jour
       # Utilisez request.data pour récupérer les données du corps de la requête
     
      param2 = minT
      if param2 =='17':
        T_func = générerT1
        H_func = générerH1

      elif param2 == '15':
        T_func = générerT2
        H_func = générerH2

      elif param2 == '5':
        T_func = générerT3
        H_func = générerH3

      elif param2 == '-18':
        T_func = générerT4
        H_func = générerH4

      else:
        T_func = générerT5
        H_func = générerH5     

      while date1 <= date2:
        if(c==1):
          prec1=22
          prec2=40
          c=c+1

        prec1 = float(T_func(date1, prec1))
        prec2 = float(H_func(date1,prec2))
                  
                  

        data[date1.strftime('%Y-%m-%d %H:%M:%S')] = {
            'temperature': T_func(date1, prec1),
            'humidite': H_func(date1, prec2),
            'presence': random.randint(0,1)
                      
                    
        }

        date1 += delta

      return data """
"""
zones = Zone.objects.all()
for zone in zones:
    minT = zone.minT
    # Générer les données aléatoires avec la valeur minT de la zone actuelle
    donnees_aleatoires = generateJSON(minT)
    
    # Convertir les données en format JSON
    json_data = json.dumps(donnees_aleatoires, indent=2)

    # Définir le chemin du fichier dans le dossier media
    chemin_fichier = os.path.join('media', 'donnees' + str(zone.id) + '.json')

    # Écrire les données JSON dans le fichier
    with open(chemin_fichier, 'w') as fichier:
        fichier.write(json_data)


 """
### fin generer json sur views
""" for i in range(52,53):
  donnees_aleatoires = generer_donnees()

      # Convertir les données en format JSON
  json_data = json.dumps(donnees_aleatoires, indent=2)

      # Définir le chemin du fichier dans le dossier media
  chemin_fichier = os.path.join('media', 'donnees' + str(i) + '.json')

      # Écrire les données JSON dans le fichier
  with open(chemin_fichier, 'w') as fichier:
          fichier.write(json_data)
 """

""" def generer_donnees():
    data = {}

    # Définir la période de temps
    start_date = datetime(2024, 1, 1)
    end_date = datetime(2024, 6, 30)

    # Générer des données pour chaque jour
    current_date = start_date
    while current_date <= end_date:
        for hour in range(24):
            for minute in range(60):  # Une boucle pour chaque minute
                date_time_key = current_date.replace(hour=hour, minute=minute).strftime('%Y-%m-%d %H:%M:00')

                temperature = random.randint(20, 30)
                humidite = random.randint(40, 60)
                presence = random.choice([0, 1])

                data[date_time_key] = {
                    'temperature': temperature,
                    'humidite': humidite,
                    'presence': presence
                }

        current_date += timedelta(days=1)

    return data
 """


 
def get_json(request):
    # Chemin du fichier JSON
    nom_fichier_json = request.GET.get('nom_fichier')
    date_recherchee = request.GET.get('date')
    chemin_fichier = os.path.join('media', 'donnees'+str(nom_fichier_json)+'.json')
    #print('*************** date ',date_recherchee)
    # Vérifier si le fichier existe
    if os.path.exists(chemin_fichier):
        # Lire le contenu du fichier JSON
        with open(chemin_fichier, 'r') as fichier:
            contenu_json = json.load(fichier)

        # Clé de recherche basée sur la date et l'heure spécifiées
        cle_recherchee = date_recherchee  # Format: 'YYYY-MM-DD HH:MM:SS'

        # Récupérer les données correspondantes à la clé spécifiée
        donnees = contenu_json.get(cle_recherchee, None)

        if donnees:
            return JsonResponse(donnees)
        else:
            return JsonResponse({'message': 'Aucune donnée trouvée pour la date et l\'heure spécifiées.'}, status=404)
    else:
        return JsonResponse({'message': 'Le fichier spécifié n\'existe pas.'}, status=404)

# Une fois que les données ont été écrites dans le fichier, vous pouvez accéder à ce fichier en utilisant le chemin chemin_fichier

'''
def genererCsvLocal():
    # Charger le fichier CSV en tant que DataFrame
    zones = Zone.objects.all()
    for zone in zones:
        generateExcel(zone.id, zone.minT)


genererCsvLocal()

'''

""" import concurrent.futures

class rechercher_donnees(APIView):
    def get(self, request):
        try:
            valeurs_zones = []
            zones = Zone.objects.all()  # Récupérez toutes les zones depuis la base de données
            date_heure_recherchee = request.GET.get('date')
            
            # Définir une fonction pour lire les données de chaque zone en parallèle
            def read_zone_data(zone, date_heure_recherchee):
                fichier_csv = 'media/data' + str(zone.id) + '.csv'
                df = pd.read_csv(fichier_csv, delimiter=';', header=None)
                if not df.empty:
                    df[0] = pd.to_datetime(df[0] + ' ' + df[1], format='%d/%m/%Y %H:%M')
                    resultat = df[df[0] == pd.to_datetime(date_heure_recherchee, format='%d/%m/%Y %H:%M:%S')]
                
                    temperature = resultat.iloc[0, 2]
                    humidite = resultat.iloc[0, 3]
                   
                    return {'zone_id': zone.id, 'temperature': temperature, 'humidite': humidite}
                else:
                    # Gérez le cas où le DataFrame est vide
                    return {'zone_id': zone.id, 'temperature': None, 'humidite': None}
                            
                            
       
            # Utiliser des processus parallèles pour lire les données de chaque zone
            with concurrent.futures.ThreadPoolExecutor() as executor:
                futures = [executor.submit(read_zone_data, zone, date_heure_recherchee) for zone in zones]
                for future in concurrent.futures.as_completed(futures):
                    valeurs_zones.append(future.result())

            return Response({'data': valeurs_zones}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
 """

class get_alerte_by_id(APIView):
    def get(self, request):
        try:
            user_Id = request.GET.get('id')
            alertes = Alerte.objects.filter(userID=user_Id)
        
            serializer = AlerteSerializer(alertes, many=True)
       
            return Response(serializer.data)
        except Alerte.DoesNotExist:
        # Si la zone spécifiée n'existe pas, retourner une erreur 404
          return Response(status=status.HTTP_404_NOT_FOUND)

class get_alerte_sans_id(APIView):
    def get(self, request):
        try:
            
            alertes = Alerte.objects.filter(userID=None)
        
            serializer = AlerteSerializer(alertes, many=True)
       
            return Response(serializer.data)
        except Alerte.DoesNotExist:
        # Si la zone spécifiée n'existe pas, retourner une erreur 404
          return Response(status=status.HTTP_404_NOT_FOUND)

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Alerte

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Alerte
from django.contrib.auth.models import User

class add_user_alerte(APIView):
    def post(self, request):
        try:
            user_id = request.data.get('idUser')
            alerte_id = request.data.get('idAlerte')
            
            # Assurez-vous que l'utilisateur et l'alerte existent
            user = User.objects.get(id=user_id)
            alerte = Alerte.objects.get(id=alerte_id)
            
            # Associez l'utilisateur à l'alerte
            alerte.userID = user
            alerte.save()
            
            return Response(status=status.HTTP_200_OK)
        
        except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND, data={'message': 'User not found'})
        
        except Alerte.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND, data={'message': 'Alerte not found'})
class notifier_alerte(APIView):
    def post(self, request):
        try:
          
            alerte_id = request.data.get('alerteId')
            
            # Assurez-vous que l'utilisateur et l'alerte existent
         
            alerte = Alerte.objects.get(id=alerte_id)
            
            # Associez l'utilisateur à l'alerte
            alerte.notifie = True
            alerte.save()
            
            return Response(status=status.HTTP_200_OK)
        
        except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND, data={'message': 'User not found'})
        
        except Alerte.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND, data={'message': 'Alerte not found'})

def get_TH_par_heure(request):
    global is_get_TH_par_heure_running
    
    # Vérifier si la méthode doit continuer à s'exécuter
    if not is_get_TH_par_heure_running:
        return JsonResponse({'message': 'Méthode arrêtée'}, status=200)
    
    # Chemin du fichier JSON
    #print(' *****************nom_fichier ',request.GET.get('nom_fichier'), ' date ',request.GET.get('date'))
    
    nom_fichier_json = request.GET.get('nom_fichier')
    date_recherchee = request.GET.get('date')
    chemin_fichier = os.path.join('media', 'donnees'+str(nom_fichier_json)+'.json')
    #print('*************** date ',date_recherchee)
    # Vérifier si le fichier existe
    if os.path.exists(chemin_fichier):
        # Lire le contenu du fichier JSON
        with open(chemin_fichier, 'r') as fichier:
            contenu_json = json.load(fichier)

        data = {
          "T": 0,
          "H": 0,
        }
        i=0
        while not '60' in date_recherchee : # Format: 'YYYY-MM-DD HH:MM:SS'
          data["T"] = data["T"]+contenu_json.get(date_recherchee, None)["temperature"]
          data["H"] = data["H"]+contenu_json.get(date_recherchee, None)["humidite"]
          
          if(contenu_json.get(date_recherchee, None)):
            i=i+1
            if(int(date_recherchee.split(' ')[1].split(':')[1])+1 <10):
              date_recherchee = date_recherchee.split(' ')[0] + ' '+ date_recherchee.split(' ')[1].split(':')[0] +':0'+ str(int(date_recherchee.split(' ')[1].split(':')[1])+1) +':'+ date_recherchee.split(' ')[1].split(':')[2]
            else :
              date_recherchee = date_recherchee.split(' ')[0] + ' '+ date_recherchee.split(' ')[1].split(':')[0] +':'+ str(int(date_recherchee.split(' ')[1].split(':')[1])+1) +':'+ date_recherchee.split(' ')[1].split(':')[2]

        data["T"] = data["T"]/i
        data["H"] = data["H"]/i
        if data:
            return JsonResponse(data)
        else:
            return JsonResponse({'message': 'Aucune donnée trouvée'}, status=404)
    else:
        return JsonResponse({'message': 'Le fichier spécifié n\'existe pas.'}, status=404)

from datetime import datetime, timedelta

def get_TH_par_jour(request):
    global is_get_TH_par_jour_running
    
    # Vérifier si la méthode doit continuer à s'exécuter
    if not is_get_TH_par_jour_running:
        return JsonResponse({'message': 'Méthode arrêtée'}, status=200)
    
    nom_fichier_json = request.GET.get('nom_fichier')
    date_recherchee = request.GET.get('date')
    chemin_fichier = os.path.join('media', 'donnees' + str(nom_fichier_json) + '.json')

    if os.path.exists(chemin_fichier):
        with open(chemin_fichier, 'r') as fichier:
            contenu_json = json.load(fichier)

        data = {
            "T": 0,
            "H": 0,
        }
        count = 0
        # Récupérer la date du jour suivant pour délimiter la fin de la journée
        date_limite = datetime.strptime(date_recherchee[:10], '%Y-%m-%d') + timedelta(days=1)

        for key, value in contenu_json.items():
            # Vérifier si la clé correspond à la journée spécifiée
            if key.startswith(date_recherchee[:10]):
                data["T"] += value["temperature"]
                data["H"] += value["humidite"]
                count += 1

        if count > 0:
            data["T"] /= count
            data["H"] /= count
            return JsonResponse(data)
        else:
            return JsonResponse({'message': 'Aucune donnée trouvée pour cette date'}, status=404)
    else:
        return JsonResponse({'message': 'Le fichier spécifié n\'existe pas.'}, status=404)



def get_TH_par_instant(request):
    global is_get_TH_par_instant_running
    
    # Vérifier si la méthode doit continuer à s'exécuter
    if not is_get_TH_par_instant_running:
        return JsonResponse({'message': 'Méthode arrêtée'}, status=200)
    
    nom_fichier_json = request.GET.get('nom_fichier')
    date_recherchee = request.GET.get('date')
    chemin_fichier = os.path.join('media', 'donnees' + str(nom_fichier_json) + '.json')

    if os.path.exists(chemin_fichier):
        with open(chemin_fichier, 'r') as fichier:
            contenu_json = json.load(fichier)

        data = {
            "T": 0,
            "H": 0,
        }

        if date_recherchee in contenu_json:
            data["T"] = contenu_json[date_recherchee]["temperature"]
            data["H"] = contenu_json[date_recherchee]["humidite"]
            return JsonResponse(data)
        else:
            return JsonResponse({'message': 'Aucune donnée trouvée pour cet instant'}, status=404)
    else:
        return JsonResponse({'message': 'Le fichier spécifié n\'existe pas.'}, status=404)


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Alerte
from .serializers import AlerteSerializer

from django.http import HttpRequest
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .models import Alerte
from .serializers import AlerteSerializer

class GetAlerteNonNotifie(APIView):
    def get(self, request):  # Utilisez HttpRequest ici
       try:
        userId = request.GET.get('userID')
        role = ProfileUser.objects.get(userId=userId).role
        print("role ",role)
        if role == 'Responsable de maintenance':
            alertes = Alerte.objects.filter(userID=userId, notifie=False)
        else:
            alertes = Alerte.objects.filter(notifie=False, userID=None)
        serializer = AlerteSerializer(alertes, many=True)
        return Response(serializer.data)
       except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


        
@api_view(['GET'])
def getTenAlertes(request):
    try:
        alertes = Alerte.objects.order_by('-id')[:10]
        serializer = AlerteSerializer(alertes, many=True)
        return Response(serializer.data)
    except Alerte.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    

""" def setAlertesText() :
  try:
    alertes = Alerte.objects.all()
    for alerte in alertes :
        print(alerte.id)
        if alerte.type == 'temperature' :
          alerte.text = alerte.localId.nomLocal + ' enregistre une température moyenne inhabituelle'
        elif alerte.type == 'humidite':
          alerte.text = alerte.localId.nomLocal + ' enregistre une humidité moyenne inhabituelle'
        elif alerte.type == 'maintenance':
          text = 'Vous avez une tâche de maintenance dans '+ alerte.localId.nomLocal ;
        alerte.save() 
  except Alerte.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

setAlertesText() """


from rest_framework.views import APIView
from rest_framework.response import Response

class initialData(APIView):
    def get(self, request):
        
        initialdata = [
            { 'name': 'critique', 'data': [1, 1, 1, 1, 1, 1] },
            { 'name': 'non critique', 'data': [2, 3, 5, 7, 6, 3] },
            { 'name': 'tous', 'data': [4, 3, 3, 9, 0, 5] }
        ]
        formatted_data = " [\n"
        for item in initialdata:
            formatted_data += "  { name: '" + item['name'] + "', data: " + str(item['data']) + " },\n"
        formatted_data += "];"
        return Response(formatted_data)
        
