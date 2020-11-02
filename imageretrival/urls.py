from imageretrival.actions import do_login
from django.urls import path
from . import views, actions
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index),
    path('imagenes', views.images),
    path('subir-imagen', views.upload),
    path('duplicados', actions.find_duplicates),
    path('duplicados-auto', actions.find_automatic_duplicates, name='automatic-duplicates'),
    path('login', views.login),
    path('do_login', actions.do_login),
    path('logout', views.logout),
    path('registro', views.register),
    path('do_register', actions.do_register),
    path('eliminar/<int:image_id>', actions.delete, name='eliminar'),
    path('detalle/<int:image_id>', views.detail, name='detalle')
]

if settings.DEBUG:
    urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
