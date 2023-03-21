from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from apps.events.models import Event
from apps.events.serializers import EventSerializer
from apps.tickets.models import EventTicket
from apps.tickets.serializers import EventTicketSerializer, VerifyEventTicketSerializer
from apps.tickets.tasks import generate_pdf_and_send_ticket_to_mail
from apps.tickets.utils import get_data_from_qrcode


class EventView(ModelViewSet):
    serializer_class = EventSerializer
    serializer_action_classes = {
        "tickets": EventTicketSerializer,
        "verify_ticket": VerifyEventTicketSerializer
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

            # generate qrcode, pdf and send mail to attendee
            generate_pdf_and_send_ticket_to_mail.delay(
                ticket_uid=_ticket.uid
            )

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

    @action(detail=True, methods=["POST"])
    def verify_ticket(self, request, *args, **kwargs):
        instance: Event = self.get_object()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        _qrcode = serializer.validated_data["qrcode"]
        _data, msg = get_data_from_qrcode(_qrcode)
        if _data is not None:   
            _ticket, msg = EventTicket.verify_ticket(data=_data, event=instance)
            if _ticket:
                return Response(
                    {
                        "status_code": status.HTTP_200_OK,
                        "message": msg,
                        "data": EventTicketSerializer(_ticket).data
                    },
                    status.HTTP_200_OK,
                )
        
        return Response(
            {
                "status_code": status.HTTP_204_NO_CONTENT,
                "message":msg,
                "data": None
            },
            status.HTTP_204_NO_CONTENT
        )
        

    def get_serializer_class(self):
        try:
            return self.serializer_action_classes[self.action]
        except (KeyError, AttributeError):
            return super().get_serializer_class()

    def get_queryset(self):
        return Event.objects.all()
