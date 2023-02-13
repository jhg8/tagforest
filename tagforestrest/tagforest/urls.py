from django.urls import path, include
from rest_framework.routers import DefaultRouter, SimpleRouter
from . import views

#router = DefaultRouter()
router = SimpleRouter()
router.register(r'tags', views.TagViewSet, basename='tag')

urlpatterns = [
    path('', include(router.urls)),
    path('', views.root_view),
    path('graph/', views.graph_view, name='graph'),
    path('api-auth/', include('rest_framework.urls')),
]
