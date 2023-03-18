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
            "pdf",
            "created_at",
            "is_expired",
        )
        read_only_fields = (
            "uid",
            "event",
            "reference",
            "qrcode",
            "pdf",
            "created_at",
            "is_expired",
        )

class VerifyEventTicketSerializer(serializers.Serializer):

    qrcode = serializers.ImageField()
