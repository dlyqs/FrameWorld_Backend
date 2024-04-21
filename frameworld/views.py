from django.db import transaction
from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Entry, FrameComment, Subtitle, GlobalComment, LikeRecord, FrameLikeRecord
from .serializers import EntrySerializer, FrameCommentSerializer, SubtitleSerializer, LikeRecordSerializer, \
    FrameLikeRecordSerializer
from .serializers import GlobalCommentSerializer


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
        entry_id = self.request.query_params.get('entry', None)
        if entry_id is not None:
            queryset = queryset.filter(entry=entry_id)
        return queryset

    @action(detail=True, methods=['delete'])
    def delete_global_comment(self, request, pk=None):
        """
        Deletes a comment and if it's a root comment, all its replies and associated like records.
        """
        comment = self.get_object()
        if comment.user != request.user:
            return Response({"detail": "You do not have permission to delete this comment."},
                            status=status.HTTP_403_FORBIDDEN)

        with transaction.atomic():
            # Check if the comment is a root comment
            replies = GlobalComment.objects.filter(parentID=comment.id)
            reply_ids = replies.values_list('id', flat=True)

            LikeRecord.objects.filter(comment__id__in=reply_ids).delete()  # Delete associated like records for replies
            replies.delete()  # Delete all replies

            LikeRecord.objects.filter(comment=comment).delete()  # Delete associated like records
            comment.delete()  # Delete the comment
        return Response(status=status.HTTP_204_NO_CONTENT)


class FrameCommentViewSet(viewsets.ModelViewSet):
    queryset = FrameComment.objects.all()
    serializer_class = FrameCommentSerializer

    def get_queryset(self):
        queryset = FrameComment.objects.all()
        entry_id = self.request.query_params.get('entry', None)
        if entry_id is not None:
            queryset = queryset.filter(entry=entry_id)
        return queryset

    @action(detail=True, methods=['get'], url_path='comments_for_entry')
    def comments_for_entry(self, request, pk=None):
        """Retrieve all comments for a specific entry."""
        entry = get_object_or_404(Entry, pk=pk)
        comments = FrameComment.objects.filter(entry=entry)
        serializer = self.get_serializer(comments, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='comments_for_timestamp')
    def comments_for_timestamp(self, request):
        """Retrieve comments for a specific entry and timestamp."""
        entry_id = request.query_params.get('entry_id')
        timestamp = request.query_params.get('timestamp')
        if entry_id is None or timestamp is None:
            return Response({'error': 'Entry ID and timestamp are required'}, status=400)

        comments = FrameComment.objects.filter(entry=entry_id, timestamp=timestamp)
        serializer = self.get_serializer(comments, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['delete'])
    def delete_frame_comment(self, request, pk=None):
        """
        Deletes a frame comment and all its replies, including their like records.
        """
        comment = self.get_object()
        if comment.user != request.user:
            return Response({"detail": "You do not have permission to delete this comment."},
                            status=status.HTTP_403_FORBIDDEN)

        with transaction.atomic():
            replies = FrameComment.objects.filter(replies=comment.id)
            reply_ids = replies.values_list('id', flat=True)

            FrameLikeRecord.objects.filter(comment__id__in=reply_ids).delete()
            replies.delete()

            FrameLikeRecord.objects.filter(comment=comment).delete()
            comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


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

    @action(detail=False, methods=['post'], url_path='handle-like')
    def handle_like(self, request, *args, **kwargs):
        user_id = request.data.get('user')
        comment_id = request.data.get('comment')
        status_wanted = request.data.get('status', True)

        like_record, created = LikeRecord.objects.get_or_create(
            user_id=user_id,
            comment_id=comment_id,
            defaults={'status': status_wanted}
        )

        if not created:
            like_record.status = status_wanted
            like_record.save()

        return Response(LikeRecordSerializer(like_record).data, status=status.HTTP_200_OK)


class FrameLikeRecordViewSet(viewsets.ModelViewSet):
    queryset = FrameLikeRecord.objects.all()
    serializer_class = FrameLikeRecordSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        comment_id = self.request.query_params.get('comment')
        user_id = self.request.query_params.get('user')
        if comment_id and user_id:
            queryset = queryset.filter(comment_id=comment_id, user_id=user_id)
        return queryset

    @action(detail=False, methods=['post'], url_path='handle-like')
    def handle_like(self, request, *args, **kwargs):
        user_id = request.data.get('user')
        comment_id = request.data.get('comment')
        status_wanted = request.data.get('status', True)

        like_record, created = FrameLikeRecord.objects.get_or_create(
            user_id=user_id,
            comment_id=comment_id,
            defaults={'status': status_wanted}
        )

        if not created:
            like_record.status = status_wanted
            like_record.save()

        return Response(FrameLikeRecordSerializer(like_record).data, status=status.HTTP_200_OK)
