from django.db import models
from django.utils.crypto import get_random_string
import string
import random

def generate_shared_secret():
    # Generate a random shared secret
    chars = string.ascii_letters + string.digits
    return ''.join(random.choice(chars) for _ in range(20))



class Shop(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=200, default="unknown")
    phone_number = models.CharField(max_length=20)
    email = models.EmailField()
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    class Meta:
        verbose_name = "Shop"

    def __str__(self):
        return self.name

class EndUser(models.Model):
    first_name = models.CharField(max_length=100, default="unknown")
    last_name = models.CharField(max_length=100, default="unknown")
    rfid_tag = models.CharField(max_length=100, unique=True)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    phone_number = models.CharField(max_length=20)
    email = models.EmailField()

    class Meta:
        verbose_name = "End User"

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class ESP32Controller(models.Model):
    mac_address = models.CharField(unique=True, max_length=17)
    shared_secret = models.CharField(max_length=100)
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "ESP32 Controller"

    def __str__(self):
        return self.mac_address

    def save(self, *args, **kwargs):
        if not self.shared_secret:
            # Generate a random shared secret if it doesn't exist
            self.shared_secret = generate_shared_secret()

        super().save(*args, **kwargs)

class Transaction(models.Model):
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE)
    end_user = models.ForeignKey(EndUser, on_delete=models.CASCADE)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Transaction"

    def __str__(self):
        return f"Transaction #{self.id}"