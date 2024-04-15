from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import EntryViewSet, GlobalCommentViewSet, FrameCommentViewSet, SubtitleViewSet

router = DefaultRouter()
router.register(r'entries', EntryViewSet)
router.register(r'global_comments', GlobalCommentViewSet)
router.register(r'frame_comments', FrameCommentViewSet)
router.register(r'subtitles', SubtitleViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
