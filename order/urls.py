from django.contrib import admin
from django.urls import path, include

from . import views

app_name = "order"

urlpatterns = [
    # path("checkout/", views.CheckoutView.as_view()),
    # path("orders/", views.OrderItemListView.as_view()),
    # path("advance/", views.OrderItemShippingAdvanceView.as_view()),
    # path("return/list/", views.OrderReturnListView.as_view()),
    # path("return/<id>/", views.OrderReturnView.as_view()),
    # path("return/<id>/approve/", views.OrderReturnApproveView.as_view()),
    # path("return/<id>/decline/", views.OrderReturnDeclineView.as_view()),
    # path("<id>/", views.OrderItemDetailView.as_view()),
]
