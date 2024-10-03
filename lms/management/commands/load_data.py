from django.core.management.base import BaseCommand

from lms.models import Course, Lesson
from .utils import generate_courses_and_lessons


class Command(BaseCommand):
    help = 'Load sample data for courses and lessons'

    def add_arguments(self, parser):
        # Добавляем два аргумента: количество курсов и количество уроков
        parser.add_argument(
            '--num_courses',
            type=int,
            default=3,  # Значение по умолчанию
            help='Number of courses to create (default: 3)'
        )
        parser.add_argument(
            '--num_lessons',
            type=int,
            default=3,  # Значение по умолчанию
            help='Number of lessons per course to create (default: 3)'
        )

    def handle(self, *args, **kwargs):
        num_courses = kwargs['num_courses']
        num_lessons_per_course = kwargs['num_lessons']

        # Генерируем курсы и уроки
        courses_data, lessons_data = generate_courses_and_lessons(num_courses=num_courses,
                                                                  num_lessons_per_course=num_lessons_per_course)

        # Сохраняем курсы
        for course_data in courses_data:
            course = Course.objects.create(**course_data)

            # Сохраняем уроки для текущего курса
            for lesson_data in lessons_data:
                # Проверяем, к какому курсу относится урок
                if lesson_data['course'] == course_data['title']:
                    # Создаём урок, указывая объект курса
                    Lesson.objects.create(
                        title=lesson_data['title'],
                        description=lesson_data['description'],
                        course=course,  # Используем объект курса
                        avatar=lesson_data['avatar'],
                        video_link=lesson_data['video_link']
                    )

        self.stdout.write(self.style.SUCCESS('Successfully loaded courses and lessons!'))
