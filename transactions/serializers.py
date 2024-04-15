from rest_framework import serializers
from .models import Transaction, PeerToPeer


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ['id', 'name', 'payment_type', 'transaction_type', 'amount', 'description', 'date', 'category']
        read_only_fields = ['id', 'date']  # 'date' is auto-added


class PeerToPeerSerializer(serializers.ModelSerializer):
    class Meta:
        model = PeerToPeer
        fields = '__all__'  # Include all model fields in the serializer
