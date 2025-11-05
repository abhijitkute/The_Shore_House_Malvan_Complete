from django.urls import path
from . import views
app_name = "payments"
urlpatterns = [
    path("<int:pk>/", views.payment_detail, name="detail"),
]
