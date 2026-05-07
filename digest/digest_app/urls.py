from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('auth/', views.auth, name='auth'),
    path('reg/', views.reg, name='reg'),
    path('logout/', views.logout_view, name='logout'),
    path('confirm/', views.confirm, name='confirm'),
    path('account/', views.account, name='account'),
    path('digest_desktop/', views.digest_desktop, name='digest_desktop'),
    path('digest/all-news/', views.all_news, name='all_news'),
    path('digest/important-news/', views.important_news, name='important_news'),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
