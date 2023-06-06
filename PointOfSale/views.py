from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404

from .models import EndUser, Shop, ESP32Controller
from .serializers import TransactionSerializer
from .models import EndUser, Shop

@api_view(['GET', 'POST'])
@authentication_classes([])
@permission_classes([IsAuthenticated])
def transaction_view(request):
    if request.method == 'POST':
        try:
            # Validate and sanitize input data
            rfid_id = request.data.get('rfid_id')
            money_amount = request.data.get('money_amount')
            esp32_mac_address = request.data.get('esp32_mac_address')
            shared_secret = request.data.get('shared_secret')

            # Check if both ESP32 MAC address and shared secret match
            esp32_controller = get_object_or_404(
                ESP32Controller, mac_address=esp32_mac_address, shared_secret=shared_secret
            )
            shop = esp32_controller.shop

            # Check if the EndUser exists
            end_user = get_object_or_404(EndUser, rfid_tag=rfid_id)

            # Check if the EndUser has sufficient balance
            if end_user.balance >= money_amount:
                # Deduct money from EndUser's balance
                end_user.balance -= money_amount

                # Add money to Shop's balance
                shop.balance += money_amount

                # Save the changes
                end_user.save()
                shop.save()

                # Create a Transaction instance
                serializer = TransactionSerializer(data={
                    'shop': shop.id,
                    'end_user': end_user.id,
                    'total_price': money_amount
                })

                if serializer.is_valid():
                    serializer.save()

                    # Return a generic success message without revealing model names
                    return Response({'message': 'Transaction successful'}, status=status.HTTP_200_OK)
                else:
                    # Return a generic error message without revealing model names
                    return Response({'message': 'Transaction failed'}, status=status.HTTP_400_BAD_REQUEST)

            else:
                # Return a generic error message without revealing model names
                return Response({'message': 'Insufficient funds'}, status=status.HTTP_400_BAD_REQUEST)

        except EndUser.DoesNotExist:
            # Return a generic error message without revealing model names
            return Response({'message': 'Invalid RFID tag'}, status=status.HTTP_400_BAD_REQUEST)

        except ESP32Controller.DoesNotExist:
            # Return a generic error message without revealing model names
            return Response({'message': 'Invalid ESP32 MAC address or shared secret'}, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'GET':
        # Handle the GET request here
        # You can return any necessary data or render a template
        return Response({'message': 'GET request handled'})

    else:
        # Return a "405 Method Not Allowed" response for unsupported methods
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    


def index(request):
    return render(request, 'PointOfSale/index.html')

def shop_list(request):
    # Fetch the list of registered shops from your database and pass it to the template
    shops = Shop.objects.all()
    return render(request, 'PointOfSale/shop_list.html', {'shops': shops})

def user_list(request):
    # Fetch the list of registered users from your database and pass it to the template
    users = EndUser.objects.all()
    return render(request, 'PointOfSale/user_list.html', {'users': users})
