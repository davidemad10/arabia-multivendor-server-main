from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path,re_path
from django.conf.urls.i18n import i18n_patterns

# from drf_yasg import openapi
# from drf_yasg.views import get_schema_view
# from rest_framework import permissions

# schema_view = get_schema_view(
#     openapi.Info(
#         title="Medex API",
#         default_version="v1",
#     ),
#     public=True,
#     permission_classes=(permissions.AllowAny,),
# )

urlpatterns = i18n_patterns(
    path("api/admin/", admin.site.urls),
    path('rosetta/', include('rosetta.urls')),
    path("api/account/", include("account.urls", namespace="account")),
    path("api/product/", include("product.urls", namespace="product")),
    path("api/advertisement/", include("advertisement.urls", namespace="advertisement")),
    path("api/order/", include("order.urls", namespace="order")),
    # path("api/contact/", include("contact.urls", namespace="contact")),
    # path("api/quote/", include("quote.urls", namespace="quote")),
    # path("api/wishlist/", include("wishlist.urls", namespace="wishlist")),
    # path("api/opportunity/", include("opportunity.urls", namespace="opportunity")),
    # path("api/chat/", include("chat.urls", namespace="chat")),
    # path("api/stats/", include("stats.urls", namespace="stats")),
    # path("api/company/", include("company.urls", namespace="company")),
    # path("api/wallet/", include("wallet.urls", namespace="wallet")),
    # path("swagger/", schema_view.with_ui("swagger", cache_timeout=0), name="schema-swagger-ui"),
    # path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),

)
urlpatterns+= static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

