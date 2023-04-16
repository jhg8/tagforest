from django.urls import path, include
from rest_framework.routers import DefaultRouter, SimpleRouter
from . import views

router = SimpleRouter()
router.register(r'trees', views.TreeViewSet, basename='tree')
router.register(r'tags', views.TagViewSet, basename='tag')
router.register(r'extendedtags', views.ExtendedTagViewSet, basename='extendedtag')
router.register(r'tagcategories', views.TagCategoryViewSet, basename='tagcategory')

trees_patterns = [
    path('graph/', views.graph_view, name='graph'),
    path('import/', views.import_data, name='import'),
    path('export/', views.export_data, name='export'),
]

urlpatterns = [
    path(r'', include(router.urls)),
    path(r'', views.root_view),
    path('trees/<int:tree_pk>/', include(trees_patterns)),
    path('api-auth/', include('rest_framework.urls')),
]
