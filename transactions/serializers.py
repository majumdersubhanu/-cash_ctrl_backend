from rest_framework import serializers
from .models import Transaction


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ['id', 'name', 'payment_type', 'transaction_type', 'amount', 'description', 'date', 'category']
        read_only_fields = ['id', 'date']  # 'date' is auto-added
