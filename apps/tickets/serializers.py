from rest_framework import serializers

from apps.tickets.models import EventTicket



class EventTicketSerializer(serializers.ModelSerializer):
   
    class Meta:
        model = EventTicket
        fields = (
            "uid",
            "event",
            "reference",
            "name",
            "email",
            "qrcode",
            "created_at",
        )
        read_only_fields = (
            "uid",
            "event",
            "reference",
            "qrcode",
            "created_at",
        )
