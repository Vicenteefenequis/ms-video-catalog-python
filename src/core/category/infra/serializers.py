from rest_framework import ISO_8601, serializers



class CategorySerializer(serializers.Serializer):  # pylint: disable=abstract-method
    id = serializers.UUIDField(read_only=True)
    name = serializers.CharField()
    description = serializers.CharField(required=False, allow_null=True)
    is_active = serializers.BooleanField(required=False)
    created_at = serializers.DateTimeField(
        read_only=True, format=ISO_8601  # type: ignore
    )
