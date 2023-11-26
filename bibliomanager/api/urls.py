from django.urls import path, include, re_path
from rest_framework.permissions import AllowAny
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView
from drf_yasg import openapi
from drf_yasg.views import get_schema_view

from .views import BookViewSet, BorrowBookView, MeView, ReturnBookView, UserBookLoansView, UserRegistrationView


app_name = 'api'


router_v1 = DefaultRouter()
router_v1.register(r'books', BookViewSet)

urlpatterns = [
    path('v1/', include(router_v1.urls)),
    path('v1/register/', UserRegistrationView.as_view(), name='user-register'),
    path('v1/me/', MeView.as_view(), name='user-me'),
    path('v1/borrow-book/<int:book_id>/',
         BorrowBookView.as_view(), name='borrow-book'),
    path('v1/return-book/<int:book_id>/',
         ReturnBookView.as_view(), name='return-book'),
    path('v1/user-book-loans/', UserBookLoansView.as_view(), name='user-book-loans'),
    path('v1/token/', TokenObtainPairView.as_view(), name='token_obtain'),
]

schema_view = get_schema_view(
    openapi.Info(
        title="BiblioManager API",
        default_version='v1',
        description="Документация для api проекта BiblioManager",
        contact=openapi.Contact(email="izalbu@yandex.ru"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[AllowAny],
)

urlpatterns += [
    re_path(r'^swagger(?P<format>\.json|\.yaml)$',
            schema_view.without_ui(cache_timeout=0), name='schema-json'),
    re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0),
            name='schema-swagger-ui'),
    re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0),
            name='schema-redoc'),
]
