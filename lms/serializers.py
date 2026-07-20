from rest_framework import serializers
from .models import (
    Course,
    VideoLesson,
    Quiz,
    Question,
    Answer,
     StudentProgress,
)


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = "__all__"


class VideoLessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = VideoLesson
        fields = "__all__"


class QuizSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quiz
        fields = "__all__"


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = "__all__"


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = "__all__"

class StudentProgressSerializer(serializers.ModelSerializer):

    class Meta:
        model = StudentProgress
        fields = "__all__"        