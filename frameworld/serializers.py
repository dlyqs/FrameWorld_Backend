from rest_framework import serializers
from .models import Entry, GlobalComment, FrameComment, Subtitle, LikeRecord


class EntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Entry
        fields = '__all__'


class GlobalCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = GlobalComment
        fields = '__all__'


class FrameCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = FrameComment
        fields = '__all__'


class SubtitleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subtitle
        fields = '__all__'


class LikeRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = LikeRecord
        fields = ['id', 'user', 'comment', 'status']
