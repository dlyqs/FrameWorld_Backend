from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import EntryViewSet, GlobalCommentViewSet, FrameCommentViewSet, SubtitleViewSet, LikeRecordViewSet, FrameLikeRecordViewSet
from .views import CommentByIdView

router = DefaultRouter()
router.register(r'entries', EntryViewSet)
router.register(r'global_comments', GlobalCommentViewSet)
router.register(r'frame_comments', FrameCommentViewSet)
router.register(r'subtitles', SubtitleViewSet)
router.register(r'like_records', LikeRecordViewSet)
router.register(r'frame_like_records', FrameLikeRecordViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('global_comments/<int:comment_id>/', CommentByIdView.as_view(), name='comment_by_id'),
]
