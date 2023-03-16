from django.urls import path

from apps.tickets.views import EventTicketView



urlpatterns = [
    path(
        "events/<slug:uid>/ticket/",
        EventTicketView.as_view(),
        name="create-event-ticket",
    ),
] 