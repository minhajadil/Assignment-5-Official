from django.contrib import admin
from django.urls import path,include
from .import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('user/', include('User.urls')),
    path('book/', include('Books.urls')),
    path('wallet/', include('Wallet.urls')),
    path('', views.home,name='homepage'),
    path('category/<slug:category_slug>', views.home,name='categoryfilter'),
]

urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
