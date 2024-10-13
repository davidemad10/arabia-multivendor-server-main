from django.contrib import admin
from .models import Address, BuyerProfile, SupplierProfile, User,SupplierDocuments,Favorite

admin.site.register(Address)
admin.site.register(User)
admin.site.register(SupplierProfile)
admin.site.register(BuyerProfile)
admin.site.register(SupplierDocuments)
admin.site.register(Favorite)






