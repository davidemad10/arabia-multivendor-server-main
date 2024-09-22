from django.contrib import admin
from parler.admin import TranslatableAdmin,TranslatableModelForm
from.models import Brand,Category,Product,Review,Color,Size
from mptt.admin import MPTTModelAdmin
from mptt.forms import MPTTAdminForm

# Register your models here.




class CategoryAdminForm(MPTTAdminForm, TranslatableModelForm):
    pass


class CategoryAdmin(TranslatableAdmin, MPTTModelAdmin):
    form = CategoryAdminForm

    def get_prepopulated_fields(self, request, obj=None):
        return {'slug': ('name',)}  


class ReviewAdmin(admin.ModelAdmin):
    list_display = ('id','product','user','rating','created_at')
    readonly_fields=['created_at']


admin.site.register(Brand,TranslatableAdmin)
admin.site.register(Product,TranslatableAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Review , ReviewAdmin)
admin.site.register(Color,TranslatableAdmin)
admin.site.register(Size,TranslatableAdmin)