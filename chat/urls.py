from django.urls import include, path
from rest_framework import routers
from .views import ConversationViewSet, MessageViewSet, PromptViewSet, EmbeddingDocumentViewSet, SettingViewSet

router = routers.SimpleRouter()
router.register(r'conversations', ConversationViewSet, basename='conversationModel')
router.register(r'messages', MessageViewSet, basename='messageModel')
router.register(r'prompts', PromptViewSet, basename='promptModel')
router.register(r'embedding_document', EmbeddingDocumentViewSet, basename='embeddingDocumentModel')
router.register(r'settings', SettingViewSet, basename='settingModel')

urlpatterns = [
    path('', include(router.urls)),
]