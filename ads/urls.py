from django.urls import path
from rest_framework import routers

from ads import views

router = routers.SimpleRouter()
router.register('categories', views.CategoriesViewSet)

urlpatterns = [
    path('', views.AdsListView.as_view()),
    path('<int:pk>/', views.AdDetailView.as_view()),
    path('<int:pk>/del/', views.AdDeleteApiView.as_view()),
    path('create/', views.AdCreateView.as_view()),
    path('<int:pk>/update/', views.AdUpdateApiView.as_view()),
    path('<int:pk>/upload_image', views.AdUpdateImageView.as_view()),

    path('selections/', views.SelectionView.as_view()),
    path('selections/<int:pk>/', views.SelectionDetailView.as_view()),
    path('selections/create/', views.SelectionCreateView.as_view()),
    path('selections/<int:pk>/update/', views.SelectionUpdateView.as_view()),
    path('selections/<int:pk>/del/', views.SelectionDeleteView.as_view()),
]

urlpatterns += router.urls
