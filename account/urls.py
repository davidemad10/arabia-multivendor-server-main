from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from . import views

app_name = "account"

urlpatterns = [
    path("login/", views.CustomTokenObtainPairView.as_view(), name="login"),
    path("token/refresh/", TokenRefreshView.as_view(), name="refresh"),
    path("buyer/register/", views.BuyerRegisterView.as_view(), name="buyer-register"),
    path("supplier/register/", views.SupplierRegisterView.as_view(), name="supplier-register"),
    path('verify-otp/',  views.VerifyOTPView.as_view(), name='verify-otp'),
    # path("supplier/list/", views.SupplierListView.as_view(), name="supplier-list"),
    # path("buyer/email-verify/", views.VerifyEmail.as_view(), name="activate"),
    # path(
    #     "buyer/email-verify-refresh/",
    #     views.RefreshBuyerActivationLink.as_view(),
    #     name="activate-refresh",
    # ),
    # path("password/reset/", views.PasswordResetView.as_view(), name="reset"),
    # path(
    #     "password/reset/confirm", views.PasswordResetConfirmView.as_view(), name="reset-confirm"
    # ),
    # path("show_user_stats/", views.ShowUserStatsView.as_view()),
    # path("profile/", views.ProfileView.as_view(), name="profile"),
    # path("profile/<id>/", views.GetProfileView.as_view()),
    # path("update-password/", views.UpdatePasswordAPIView.as_view(), name="update-password"),
    # path(
    #     "supplier/employee/",
    #     views.SupplierEmployeeView.as_view(),
    #     name="supplier_employee",
    # ),
    # path(
    #     "buyer/employee/",
    #     views.BuyerEmployeeView.as_view(),
    #     name="buyer_employee",
    # ),
]
