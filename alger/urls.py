# urls.py
from django.urls import path
from .views import QuestionListView, AnswerView

urlpatterns = [
    path('api/questions/', QuestionListView.as_view(), name='question-list-api'),
    path('api/answer/<int:question_id>/', AnswerView.as_view(), name='answer-api'),
]
