from . import views
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('', views.Home , name ="home"),
    path('next', views.loadcontent, name="Loadcontent")
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
