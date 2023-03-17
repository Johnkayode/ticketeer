from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from apps.events.models import Event
from apps.events.serializers import EventSerializer
from apps.tickets.models import EventTicket
from apps.tickets.serializers import EventTicketSerializer


class EventView(ModelViewSet):
    serializer_class = EventSerializer
    serializer_action_classes = {
        "tickets": EventTicketSerializer,
    }
    permission_classes = [AllowAny]
    lookup_field = "uid"
    

    @action(detail=True, methods=["GET", "POST"])
    def tickets(self, request, *args, **kwargs):
        instance: Event = self.get_object()
       
        if request.method == "POST":
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            _ticket: EventTicket = serializer.save(event=instance)
            _ticket.generate_qrcode()
            _ticket.generate_ticket_pdf()

            headers = self.get_success_headers(serializer.data)
            return Response(
                {
                    "status_code": status.HTTP_201_CREATED,
                    "message": "Event Ticket created successfully",
                    "data": self.get_serializer(_ticket).data,
                },
                status.HTTP_201_CREATED,
                headers=headers,
            )

        else:
            tickets = EventTicket.objects.filter(event=instance)
            data = self.get_serializer(tickets, many=True).data
            return Response(
                {
                    "status_code": status.HTTP_200_OK,
                    "message": "Event Tickets",
                    "data": data
                },
                status.HTTP_200_OK,
            )


    def get_serializer_class(self):
        try:
            return self.serializer_action_classes[self.action]
        except (KeyError, AttributeError):
            return super().get_serializer_class()

    def get_queryset(self):
        return Event.objects.all()
