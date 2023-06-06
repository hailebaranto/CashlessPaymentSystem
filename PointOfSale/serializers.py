from rest_framework import serializers

from .models import Transaction
from .views import EndUser, Shop
class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ['shop', 'end_user', 'total_price', 'timestamp']
        read_only_fields = ['timestamp']

    def create(self, validated_data):
        # Retrieve the shop and end_user instances using the provided IDs
        shop_id = validated_data['shop']
        end_user_id = validated_data['end_user']
        shop = Shop.objects.get(id=shop_id)
        end_user = EndUser.objects.get(id=end_user_id)

        # Create the Transaction object
        transaction = Transaction.objects.create(
            shop=shop,
            end_user=end_user,
            total_price=validated_data['total_price']
        )

        return transaction