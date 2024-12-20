from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('automobiliai/', views.automobiliu_sarasas, name='automobiliu_sarasas'),
    path('automobiliai/<int:modelis_id>/', views.automobilis_klientai, name='automobilis_klientai'),
    path('uzsakymai/', views.UzsakymaiListView.as_view(), name='uzsakymai'),
    path('uzsakymai/<int:pk>/', views.UzsakymasDetailView.as_view(), name='uzsakymas_detail'),
    path('search/', views.search, name='search'),
    path('manoservisas/', views.ServiceByUserListView.as_view(), name='mano_servisas'),
    path('register/', views.register, name='register'),
    path('profilis/', views.profilis, name='profilis')
]

