from django.urls import path
from rest_framework.routers import DefaultRouter

from apps.events.views import EventView

router = DefaultRouter(trailing_slash=True)
router.register("", EventView, "event")

urlpatterns = [
] + router.urls