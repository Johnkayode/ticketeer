from rest_framework.decorators import action
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from apps.tickets.models import EventTicket
from apps.tickets.serializers import EventTicketSerializer

