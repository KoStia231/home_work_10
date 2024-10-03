from faker import Faker

fake = Faker()


def generate_random_course_data():
    return {
        "title": fake.catch_phrase(),  # Генерирует случайный заголовок
        "description": fake.paragraph(nb_sentences=3),  # Генерирует случайное описание
        "avatar": f"course/{fake.word()}.jpg",  # Случайное имя файла
    }


def generate_random_lesson_data(course):
    return {
        "title": fake.sentence(nb_words=5),  # Генерирует случайное название урока
        "description": fake.paragraph(nb_sentences=2),  # Генерирует случайное описание
        "course": course,
        "avatar": f"lesson/{fake.word()}.jpg",  # Случайное имя файла
        "video_link": fake.url(),  # Генерирует случайную ссылку
    }


def generate_courses_and_lessons(num_courses=5, num_lessons_per_course=3):
    courses = []
    lessons = []

    for _ in range(num_courses):
        course_data = generate_random_course_data()
        course = {
            "title": course_data["title"],
            "description": course_data["description"],
            "avatar": course_data["avatar"]
        }
        courses.append(course)

        # Генерируем уроки для курса
        for _ in range(num_lessons_per_course):
            lesson_data = generate_random_lesson_data(course_data["title"])
            lessons.append(lesson_data)

    return courses, lessons
