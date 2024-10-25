from django.contrib import admin
from .models import Address, BuyerProfile, SupplierProfile, User,SupplierDocuments,Favorite

admin.site.site_header= "Arabia Admin Panel"
admin.site.site_title="Arabia AdminPanel"





class IsActiveSupplierFilter(admin.SimpleListFilter):
    title = 'Active Supplier'
    parameter_name = 'is_active_supplier'

    def lookups(self, request, model_admin):
        return (
            ('True', 'Active'),
            ('False', 'Inactive'),
        )

    def queryset(self, request, queryset):
        if self.value() == 'True':
            return queryset.filter(user__is_active=True)
        elif self.value() == 'False':
            return queryset.filter(user__is_active=False)
        return queryset

class SupplierDocumentsAdmin(admin.ModelAdmin):
    list_display = ['user']
    list_filter = (IsActiveSupplierFilter,) 







class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'full_name', 'is_supplier', 'is_active', 'is_staff')
    list_filter = ('is_supplier', 'is_active','is_buyer')



admin.site.register(Address)
admin.site.register(User ,UserAdmin)
admin.site.register(SupplierProfile)
admin.site.register(BuyerProfile)
admin.site.register(SupplierDocuments,SupplierDocumentsAdmin)
admin.site.register(Favorite)



