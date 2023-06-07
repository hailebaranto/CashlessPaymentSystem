"""
Serializer module for the Transaction model.

This module provides the TransactionSerializer class, which serializes Transaction objects
and handles their deserialization.
"""

from rest_framework import serializers
from .models import Transaction
from .views import EndUser, Shop
from datetime import datetime

class TransactionSerializer(serializers.ModelSerializer):
    """
    Serializer class for the Transaction model.

    Serializes Transaction objects and handles their deserialization.
    """

    class Meta:
        model = Transaction
        fields = ['shop', 'end_user', 'total_price', 'timestamp']
        read_only_fields = ['timestamp']

    def create(self, validated_data):
        """
        Creates a new Transaction object based on the validated data.

        Args:
            validated_data (dict): Validated data from the deserialization process.

        Returns:
            Transaction: The created Transaction object.
        """

        shop_id = validated_data['shop']
        end_user_id = validated_data['end_user']
        shop = Shop.objects.get(id=shop_id)
        end_user = EndUser.objects.get(id=end_user_id)
        transaction = Transaction.objects.create(
            shop=shop,
            end_user=end_user,
            total_price=validated_data['total_price'],
            timestamp=datetime.now()
        )
        return transaction