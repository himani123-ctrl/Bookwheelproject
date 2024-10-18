from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import (
    author_registration,
    author_login,
    author_dashboard,
    enquiry_form,
    payment_view,
    story_list,
    rate_story,
    story_detail,
)

urlpatterns = [
    path('register/', author_registration, name='author_registration'),
    path('login/', author_login, name='author_login'),
    path('dashboard/', author_dashboard, name='author_dashboard'),
    path('enquiry/', enquiry_form, name='enquiry_form'),
    path('payment/', payment_view, name='payment_view'),
    path('', story_list, name='story_list'),
    path('rate_story/<int:story_id>/', rate_story, name='rate_story'),
    path('story/<int:story_id>/', story_detail, name='story_detail'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)