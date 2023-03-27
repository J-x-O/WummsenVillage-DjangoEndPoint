from rest_framework import serializers


class PlayerDefinition:
    def __init__(self, name: str, tag: int, local: bool, access_token: str):
        self.name = name
        self.tag = tag
        self.local = local
        self.access_token = access_token


class PlayerDefinitionSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=32, required=True)
    tag = serializers.IntegerField(required=True)
    local = serializers.BooleanField(default=True)
    access_token = serializers.CharField(max_length=10, default=None)

    def create(self, validated_data):
        return PlayerDefinition(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get("name", instance.name)
        instance.tag = validated_data.get("tag", instance.tag)
        instance.local = validated_data.get("local", instance.local)
        instance.access_token = validated_data.get("access_token", instance.access_token)
        return instance
