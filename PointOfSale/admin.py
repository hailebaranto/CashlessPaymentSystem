from django.contrib import admin
from django.contrib.auth.models import Group
from .models import EndUser, Shop, ESP32Controller, Transaction, generate_shared_secret

# Unregister the Group model from the default admin site
# admin.site.unregister(Group) 

# Create a custom AdminSite
class CustomAdminSite(admin.AdminSite):
    site_header = 'Cashless Payment System Administration'  # Customize the site header
    site_title = 'Cashless Payment System'  # Customize the site title
    index_title = 'Welcome to the Cashless Payment System'  # Customize the index page title
    
custom_admin_site = CustomAdminSite(name='customadmin')

# Register your models with the custom admin site
@admin.register(EndUser, site=custom_admin_site)
class EndUserAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'rfid_tag', 'balance', 'phone_number', 'email')
    list_filter = ('balance',)
    search_fields = ('first_name', 'last_name', 'rfid_tag', 'phone_number', 'email')

@admin.register(Shop, site=custom_admin_site)
class ShopAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'phone_number', 'email', 'balance')
    list_filter = ('balance',)
    search_fields = ('name', 'address', 'phone_number', 'email')

@admin.register(Transaction, site=custom_admin_site)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('id', 'shop', 'end_user', 'total_price', 'timestamp')
    list_filter = ('shop', 'end_user', 'timestamp')
    search_fields = ('id', 'shop__name', 'end_user__first_name', 'end_user__last_name')

@admin.register(ESP32Controller, site=custom_admin_site)
class ESP32ControllerAdmin(admin.ModelAdmin):
    list_display = ('mac_address', 'shared_secret', 'shop')
    search_fields = ('mac_address', 'shared_secret', 'shop__name')

    def save_model(self, request, obj, form, change):
        if not obj.shared_secret:
            # Generate a random shared secret if it doesn't exist
            obj.shared_secret = generate_shared_secret()
        super().save_model(request, obj, form, change)

    # def get_actions(self, request):
    #     actions = super().get_actions(request)
    #     if 'delete_selected' in actions:
    #         del actions['delete_selected']
    #     return actions

    # def has_delete_permission(self, request, obj=None):
    #     return False


# Replace the default admin site with the custom admin site
admin.site.__class__ = custom_admin_site.__class__
admin.site.__dict__.update(custom_admin_site.__dict__)