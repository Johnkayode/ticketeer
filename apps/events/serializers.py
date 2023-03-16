from rest_framework import serializers

from apps.events.models import Event


class EventSerializer(serializers.ModelSerializer):
    from_date = serializers.DateTimeField(format="iso-8601")
    is_expired = serializers.SerializerMethodField()
    class Meta:
        model = Event
        fields = (
            "uid",
            "name",
            "venue",
            "from_date",
            "to_date",
            "max_participants",
            "is_expired",
            "is_cancelled",
            "is_free",
            "created_at",
        )
        read_only_fields = (
            "uid",
            "is_expired",
            "is_cancelled",
            "created_at",
        )

    def get_is_expired(self, instance: Event) -> bool:
        return instance.is_expired