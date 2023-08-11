
from django.urls import path
from . import views
app_name = 'revision'
urlpatterns = [
    path('', views.index, name='index'),
    path('promote/<int:id>/', views.promote, name='promote'),
    path('pr/<int:id>/', views.demote, name='demote'),


    # path('arnaba_create', views.arnaba_create, name='arnaba_create'),
    # path('arnab_create', views.arnab_create, name='arnab_create'),
    # path('arnaba_list', views.arnaba_list, name='arnaba_list'),
    # path('arnab_list', views.arnab_list, name='arnab_list'),
    # path('update/<int:id>/', views.arnaba_update, name='arnaba_update'),
    # path('gass/<int:id>/', views.arnaba_gass, name='arnaba_gass'),
    # path('males/update/<int:id>/', views.arnab_update, name='arnab_update'),
    # path('delete/<int:id>/', views.arnaba_delete, name='arnaba_delete'),
    # path('males/delete/<int:id>/', views.arnab_delete, name='arnab_delete'),
    # path('<int:id>/', views.detail, name='detail'),
    # path('males/<int:id>/', views.arnab_detail, name='arnab_detail')



]