from rest_framework import serializers
from .models import UserProfile, EnergyTransaction, BlockchainBlock
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']

class UserProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = UserProfile
        fields = ['user', 'role', 'energy_tokens']

class EnergyTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = EnergyTransaction
        fields = '__all__'

class BlockchainBlockSerializer(serializers.ModelSerializer):
    transaction = EnergyTransactionSerializer()
    class Meta:
        model = BlockchainBlock
        fields = '__all__'
