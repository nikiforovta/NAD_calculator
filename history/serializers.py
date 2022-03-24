import uuid

from rest_framework import serializers

from history.models import Entry


class HistoryEntrySerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    id = serializers.HiddenField(default=uuid.uuid4())

    class Meta:
        model = Entry
        fields = '__all__'


class HistoryEntriesSerializer(serializers.ModelSerializer):
    def getUsername(self, obj):
        return obj.user.username

    username = serializers.SerializerMethodField("getUsername")

    class Meta:
        model = Entry
        username = serializers.CharField(source="owner.username", read_only=True)
        fields = ('id', 'username', 'operation_type', 'operands')
