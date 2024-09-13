# import uuid
# from collections.abc import Iterable

# from common.utils.file_upload_paths import return_request_files_path
# from common.validators.image_video_extension_validator import \
#     image_video_extension_validator
# from django.contrib.auth import get_user_model
# from django.db import models
# from django.utils.translation import gettext_lazy as _
# from product.models import Product,Color,Size

# User = get_user_model()


# class OrderItem(models.Model):
#     class SHIPPING_STATUS_CHOICES(models.TextChoices):
#         ORDERED = "OR", _("Ordered")
#         PREPARING = "P", _("Shipping is being prepared")
#         OTW = "OTW", _("On the way")
#         DE = "DE", _("Delivered")

#     user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_("Buyer"))
#     product = models.ForeignKey(Product, on_delete=models.CASCADE)
#     color=models.ForeignKey(Color,related_name="order_item",on_delete=models.SET_NULL,null=True,blank=True)
#     size=models.ForeignKey(Size,related_name="order_item",on_delete=models.SET_NULL,null=True,blank=True)
#     quantity = models.IntegerField(_("Quantity"), default=1)
#     total_price = models.DecimalField(
#         max_digits=15, decimal_places=2, default=0.0, null=True, blank=True
#     )
#     shipping_status = models.CharField(
#         _("Shipping Status"),
#         max_length=15,
#         choices=SHIPPING_STATUS_CHOICES.choices,
#         default=SHIPPING_STATUS_CHOICES.ORDERED,
#     )
#     created = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f"{self.quantity} of {self.product.name}"

#     def get_total_product_price(self):
#         return self.quantity * self.product.price

#     def get_total_discount_product_price(self):
#         return self.quantity * self.product.sale_price

#     def get_amount_saved(self):
#         return self.get_total_product_price() - self.get_total_discount_product_price()

#     def get_final_price(self):
#         if self.product.sale_price > 0:
#             return self.get_total_discount_product_price()
#         return self.get_total_product_price()

#     def save(self, *args, **kwargs):
#         self.total_price = self.get_total_product_price()
#         super().save(*args, **kwargs)


# class Order(models.Model):
#     class PAYMENT_CHOICES(models.TextChoices):
#         CASH = ("CASH", _("Cash"))

#     # id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

#     user = models.ForeignKey(
#         User, on_delete=models.CASCADE, verbose_name=_("Buyer"), related_name="orders"
#     )

#     products = models.ManyToManyField(OrderItem, verbose_name=_("Products"), blank=True)

#     created = models.DateTimeField(_("Ordered Date"), auto_now_add=True)

#     is_paid = models.BooleanField(_("Is Paid"), default=False)

#     payment_method = models.CharField(
#         _("Payment Method"), max_length=55, choices=PAYMENT_CHOICES.choices
#     )

#     def __str__(self):
#         return self.user.full_name

#     def get_total(self):
#         total = 0

#         for order_item in self.products.all():
#             total += order_item.get_final_price()

#         return total


# class ReturnRequest(models.Model):
#     class RETURN_STATUS_CHOICES(models.TextChoices):
#         NOT = "NOT", _("Not Requested")
#         APPLIED = "AP", _("Applied")
#         DECLINED = "DEC", _("Declined by Supplier")
#         APPROVED = "APR", _("Approved by Supplier")
#         OTW = "OTW", _("On the way")
#         COMPLETED = "CMP", _("Return Completed")

#     class RETURN_REASON_CHOICES(models.TextChoices):
#         POOR = "POO", _("Poor quality")
#         WRONG = "WRO", _("Wrong materials")
#         ADDRESS = "ADD", _("Shipped to a wrong address")

#     id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

#     user = models.ForeignKey(
#         User, on_delete=models.CASCADE, verbose_name=_("Buyer"), null=True, blank=True
#     )

#     product = models.ForeignKey(OrderItem, on_delete=models.CASCADE, null=True, blank=True)

#     tracking_number = models.CharField(_("Tracking Number"), unique=True, max_length=50)

#     status = models.CharField(
#         _("Return Status"),
#         max_length=15,
#         choices=RETURN_STATUS_CHOICES.choices,
#         default=RETURN_STATUS_CHOICES.NOT,
#     )

#     reason = models.CharField(
#         _("Return Reason"),
#         max_length=15,
#         choices=RETURN_REASON_CHOICES.choices,
#     )

#     description = models.TextField()

#     created = models.DateTimeField(auto_now_add=True)

#     decline_reason = models.TextField(null=True, blank=True)

#     def __str__(self):
#         return f"Return Request #{self.id}"


# class ReturnRequestFile(models.Model):
#     return_request = models.ForeignKey(ReturnRequest, on_delete=models.CASCADE)
#     evidence_file = models.FileField(
#         null=True,
#         blank=True,
#         upload_to=return_request_files_path,
#         validators=[
#             image_video_extension_validator,
#         ],
#     )
