from rest_framework import serializers
from materials.models import Course, Lesson, Subscription
from materials.validators import ProhibitedUrlValidator


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = '__all__'
        validators = [ProhibitedUrlValidator(field='url')]


class CourseSerializer(serializers.ModelSerializer):
    lessons_count = serializers.SerializerMethodField()
    lessons = LessonSerializer(source='lesson_set', many=True, read_only=True)
    subscription = serializers.SerializerMethodField()

    def get_lessons_count(self, instance):
        return instance.lesson_set.count()

    def get_subscription(self, instance):
        user = self.context['request'].user
        if user.is_authenticated:
            subscription = Subscription.objects.filter(user=user, course=instance).first()
            if subscription:
                return subscription.status_subscrip
        return 0

    class Meta:
        model = Course
        fields = '__all__'


class SubscriptionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Subscription
        fields = '__all__'
