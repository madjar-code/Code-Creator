from rest_framework.serializers import ListSerializer


class ActiveListSerializer(ListSerializer):
    def to_representation(self, data):
        data = data.filter(is_active=True)
        return super().to_representation(data)
