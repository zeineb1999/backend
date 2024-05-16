from django.contrib.auth.models import Group, User
from rest_framework import serializers
from .models import *

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import AllowAny


from django.contrib.auth.models import User
from rest_framework import serializers
from django.contrib.auth.models import AbstractUser
from django.db import models



class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'password']
        extra_kwargs = { 'password': { 'write_only':True,  'required':True}}
    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user
    def update(self, instance, validated_data):
        instance.username = validated_data.get('username', instance.username)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.email = validated_data.get('email', instance.email)
        instance.password = validated_data.get('password', instance.password)
        instance.save()
        return instance
    def update_password(self, instance, validated_data):
        instance.password = validated_data.get('password', instance.password)
        instance.save()
        return instance


from django.contrib.auth.models import User

class ZoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Zone
        fields = ('id','nomLocal', 'typeLocal','surface', 'etageZ', 'minT', 'maxT', 'minH', 'maxH')

class EtageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Etage
        fields = ('id', 'nomEtage', 'surface', 'batimentId')

class BatimentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Batiment
        fields = ('id','nomBatiment','typeBatiment')



class EquipementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Equipement
        fields = ('id','nom', 'etat', 'categorie','type','puissance','zoneE')

class ProfileUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProfileUser
        fields = ('id','userId', 'role')

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import AllowAny

class CustomTokenObtainPairView(TokenObtainPairView):
    permission_classes = [AllowAny]


from rest_framework import serializers

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)


class PeriodeActiviteSerializer(serializers.ModelSerializer):
    class Meta:
        model = PeriodeActivite
        fields = ('id','tempsDebut', 'tempsFin', 'Equipement','consommation')

# pour recuperer tous:


class EtageTSerializer(serializers.ModelSerializer):
    zones = ZoneSerializer(many=True, read_only=True)

    class Meta:
        model = Etage
        fields = ['id', 'surface', 'nomEtage', 'zones']

class BatimentTSerializer(serializers.ModelSerializer):
    etages = EtageTSerializer(many=True, read_only=True)

    class Meta:
        model = Batiment
        fields = ['id', 'nomBatiment', 'typeBatiment', 'etages']
class AlerteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Alerte
        fields = ['id','type','text','localId', 'equipementId', 'dateAlerte', 'userID','valeur', 'notifie', 'vu']

class RapportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rapport
        fields = ['id','alerte','redacteur','causes', 'solutions', 'risques', 'equipementsDemandes', 'equipementsNecessites', 'equipement', 'dateRapport', 'vu', 'notifie']

