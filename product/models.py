import uuid
from common.utils.create_slug import create_slug
from common.utils.file_upload_paths import (
    brands_images_path,
    categories_images_path,
    product_images_path,
)
from common.utils.generate_sku import generate_sku
from common.validators.image_extension_validator import image_extension_validator
from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _
from mptt.models import MPTTModel, TreeForeignKey
from parler.models import TranslatableModel,TranslatedFields
from .managers import CategoryManager


User = get_user_model()


class Category(MPTTModel, TranslatableModel):
    translations=TranslatedFields(
    name = models.CharField(_("Category Name"), max_length=255, unique=True)
    )
    image = models.ImageField(
        _("Category Image"),
        upload_to=categories_images_path,
        validators=[image_extension_validator],
        
    )
    slug = models.SlugField(unique=True, null=True, blank=True)
    parent = TreeForeignKey(
        "self", on_delete=models.PROTECT, null=True, blank=True, related_name="children"
    )
    is_featured = models.BooleanField(default=False)

    objects = CategoryManager()


    def __str__(self):
        return self.name

    class MPTTMeta:
        order_insertion_by = ["slug"]

    class Meta:
        verbose_name_plural = "Categories"
        indexes = [
            models.Index(fields=['slug']),  
        ]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = create_slug(self.name)
        super().save(*args, **kwargs)

    @property
    def parent_name(self):
        if self.parent:
            return self.parent.name
        return None




class Brand(TranslatableModel):
    translations=TranslatedFields(
    name = models.CharField(_("Brand Name"), max_length=255, unique=True),
    )
    slug = models.SlugField(unique=True, null=True, blank=True)
    image = models.ImageField(
        _("Brand Image"),
        upload_to=brands_images_path,
        validators=[image_extension_validator],
    )

    class Meta:
        indexes = [
            models.Index(fields=['slug']),  
        ]
    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = create_slug(self.name)
        super().save(*args, **kwargs)




class Size(TranslatableModel):
    translations=TranslatedFields(
    name = models.CharField(_("Size Name"), max_length=10, unique=True),
    )
    def __str__(self):
        return self.name
    

class Color(TranslatableModel):
    translations=TranslatedFields(
    name = models.CharField(_("Color Name"), max_length=100, unique=True),
    )
    code = models.CharField(_("Color Code"), max_length=100, unique=True)

    def __str__(self):
        return self.name




class Product(TranslatableModel):
    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    translations=TranslatedFields(
    name=models.CharField(_("Product Name"), max_length=255),
    description=models.TextField(_("Description"))
    )

    color=models.ManyToManyField(Color,related_name="products",blank=True)
    size=models.ManyToManyField(Size,related_name="products",blank=True)

    sku = models.CharField( max_length=255, unique=True, blank=True)
    supplier = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_("Supplier"))
    slug = models.SlugField(unique=True, null=True, blank=True)
    price_before_discount = models.DecimalField(
        _("Price before discount"), max_digits=10, decimal_places=2, null=True, blank=True
    )
    price_after_discount = models.DecimalField(
        _("Price after discount"),
        max_digits=10,
        decimal_places=2,
        default=0.0,
    )

    category = TreeForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="products",
        verbose_name=_("Category"),
    )
    brand = models.ForeignKey(
        Brand, on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_("Brand")
    )
    stock_quantity = models.IntegerField(_("Stock Quantity"), default=0)
    total_sold = models.IntegerField(_("Total Sold"), default=0)
    total_views = models.IntegerField(_("Total Views"), default=0)
    is_available = models.BooleanField(_("Is Available ?"), default=True)
    specifications = models.JSONField(_("Specifications"), blank=True, null=True)
    created = models.DateTimeField(_("Added On"), auto_now_add=True)
    updated = models.DateTimeField(_("Edited On"), auto_now=True)

    def get_average_rating(self):
        reviews = self.reviews.all()
        if reviews.exists():
            return sum([reviews.rating for review in reviews])/reviews.count()
        return 0

    def save(self, *args, **kwargs):
        if not self.sku:
            self.sku = generate_sku(self)
        if not self.slug:
            self.slug = create_slug(self.sku)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
    

    class Meta:
        indexes = [
            models.Index(fields=['slug']),  # فهرس على حقل slug
            models.Index(fields=['price_before_discount']),  # فهرس على حقل price_before_discount
            models.Index(fields=['price_after_discount']),  # فهرس على حقل price_after_discount
            models.Index(fields=['category']),  # فهرس على حقل category
            models.Index(fields=['brand']),  # فهرس على حقل brand
            models.Index(fields=['supplier']),  # فهرس على حقل supplier
            models.Index(fields=['created']),  # فهرس على حقل created
            models.Index(fields=['updated']),  # فهرس على حقل updated
            models.Index(fields=['price_before_discount', 'price_after_discount']),  # فهرس مركب على حقلين
        ]
    
class ProductImage(models.Model):
    product=models.ForeignKey(Product, related_name='images',on_delete=models.CASCADE)
    image= models.ImageField(
        _("Image"),
        upload_to=product_images_path,
        blank=True,
        null=True,
        validators=[image_extension_validator]
    )
    alt_text=models.CharField(_('Alternative Text'), max_length=255,blank=True,null=True)

    def __str__(self):
        return f"Image for {self.product.sku}"

class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product,related_name="reviews", on_delete=models.CASCADE)
    rating = models.FloatField() 
    review_text = models.TextField(_("Review Text"),max_length=250, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'Review for {self.product.slug} by {self.user.full_name}'

    class Meta:
        unique_together = ('user', 'product')  
        indexes = [
            models.Index(fields=['rating']),  
        ]





