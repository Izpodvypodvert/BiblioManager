from django.urls import path, include, re_path
from rest_framework.permissions import AllowAny
from rest_framework.routers import DefaultRouter
from drf_yasg import openapi
from drf_yasg.views import get_schema_view

from .views import BookViewSet, UserRegistrationView


app_name = 'api'


router_v1 = DefaultRouter()
router_v1.register(r'books', BookViewSet)

urlpatterns = [
    path('v1/', include([
        path('', include(router_v1.urls)),
        path('register/', UserRegistrationView.as_view(), name='user-register'),
    ])),
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
