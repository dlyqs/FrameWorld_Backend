from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from .models import Entry, FrameComment, Subtitle, GlobalComment, LikeRecord
from .serializers import EntrySerializer, FrameCommentSerializer, SubtitleSerializer, LikeRecordSerializer
from .serializers import GlobalCommentSerializer
from rest_framework import viewsets, status
from rest_framework.response import Response


class CommentByIdView(generics.RetrieveAPIView):
    queryset = GlobalComment.objects.all()
    serializer_class = GlobalCommentSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        comment_id = self.kwargs.get('comment_id')
        return get_object_or_404(GlobalComment, id=comment_id)


class EntryViewSet(viewsets.ModelViewSet):
    queryset = Entry.objects.all()
    serializer_class = EntrySerializer

    def retrieve(self, request, *args, **kwargs):
        entry = get_object_or_404(Entry, pk=kwargs.get('pk'))
        serializer = self.get_serializer(entry)
        return Response(serializer.data)


class GlobalCommentViewSet(viewsets.ModelViewSet):
    queryset = GlobalComment.objects.all()
    serializer_class = GlobalCommentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = super().get_queryset()
        comment_id = self.request.query_params.get('id')
        if comment_id:
            queryset = queryset.filter(id=comment_id)
        return queryset

    @action(detail=True, methods=['delete'])
    def delete_with_likes(self, request, pk=None):
        """
        This function handles the deletion of comments and their associated like records.
        """
        comment = self.get_object()
        if comment.user != request.user:
            return Response({"detail": "You do not have permission to delete this comment."},
                            status=status.HTTP_403_FORBIDDEN)

        LikeRecord.objects.filter(comment=comment).delete()  # Delete associated like records
        comment.delete()  # Delete the comment
        return Response(status=status.HTTP_204_NO_CONTENT)


class FrameCommentViewSet(viewsets.ModelViewSet):
    queryset = FrameComment.objects.all()
    serializer_class = FrameCommentSerializer

    @action(detail=True, methods=['get'], url_path='comments_for_entry')
    def comments_for_entry(self, request, pk=None):
        """Retrieve all comments for a specific entry."""
        entry = get_object_or_404(Entry, pk=pk)
        comments = FrameComment.objects.filter(entry=entry)
        serializer = self.get_serializer(comments, many=True)
        return Response(serializer.data)


class SubtitleViewSet(viewsets.ModelViewSet):
    queryset = Subtitle.objects.all()
    serializer_class = SubtitleSerializer


class LikeRecordViewSet(viewsets.ModelViewSet):
    queryset = LikeRecord.objects.all()
    serializer_class = LikeRecordSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        comment_id = self.request.query_params.get('comment')
        user_id = self.request.query_params.get('user')
        if comment_id and user_id:
            queryset = queryset.filter(comment_id=comment_id, user_id=user_id)
        return queryset

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(serializer.data)