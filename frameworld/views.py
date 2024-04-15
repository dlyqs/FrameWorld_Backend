from rest_framework import viewsets
from .models import Entry, GlobalComment, FrameComment, Subtitle
from .serializers import EntrySerializer, GlobalCommentSerializer, FrameCommentSerializer, SubtitleSerializer


class EntryViewSet(viewsets.ModelViewSet):
    queryset = Entry.objects.all()
    serializer_class = EntrySerializer


class GlobalCommentViewSet(viewsets.ModelViewSet):
    queryset = GlobalComment.objects.all()
    serializer_class = GlobalCommentSerializer


class FrameCommentViewSet(viewsets.ModelViewSet):
    queryset = FrameComment.objects.all()
    serializer_class = FrameCommentSerializer


class SubtitleViewSet(viewsets.ModelViewSet):
    queryset = Subtitle.objects.all()
    serializer_class = SubtitleSerializer
