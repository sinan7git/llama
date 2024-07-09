from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from llama import views
from llama.views import qa_bot

urlpatterns = [
                  path('admin/', admin.site.urls),
                  path('qa/', qa_bot, name='qa_bot'),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
