from django.urls import path

from apps.tickets.views import VerifyEventTicketView



urlpatterns = [
    path(
        "tickets/verify/",
        VerifyEventTicketView.as_view(),
        name="verify-event-ticket",
    ),
] 