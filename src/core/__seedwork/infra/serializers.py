from rest_framework import serializers


class UUIDSerializer(serializers.Serializer):  # pylint: disable=abstract-method
    id = serializers.UUIDField(required=True)
