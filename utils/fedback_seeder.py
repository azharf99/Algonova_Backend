from utils.level import get_course_level
from utils.topic import get_competency, get_result, get_topic
from utils.tutor_feedback import get_tutor_feedback


def feedback_seeder(Lesson, Feedback, group=False, group_id=None, all=False):
    if group and group_id:
        lessons = Lesson.objects.prefetch_related('group__students', 'students_attended').select_related('group').filter(is_active=True, group_id=group_id)
    elif not group and all:
        lessons = Lesson.objects.prefetch_related('group__students', 'students_attended').select_related('group').filter(is_active=True)
    else:
        return False
    updated_count = 0
    created_count = 0
    counter = 1
    for lesson in lessons:
        # Create monthly feedback
        if lesson.level == "M1L1":
            counter = 1
        if counter % 4 == 0:
            for student in lesson.group.students.all():
                feedback, is_created = Feedback.objects.select_related('student').update_or_create(
                    student = student,
                    number = counter // 4,
                    defaults={
                        'topic': get_topic(lesson.module, counter // 4),
                        'result': get_result(lesson.module, counter // 4),
                        'competency': get_competency(lesson.module, counter // 4),
                        'tutor_feedback': get_tutor_feedback(student.fullname),
                        'lesson_date': lesson.date_start,
                        'lesson_time': lesson.time_start,
                        'is_sent': False,
                        'level' : get_course_level(lesson.module),
                        'course' : lesson.module,
                        'project_link' : lesson.group.recordings_link,
                    }
                )
                
                if is_created:
                    created_count += 1
                else:
                    updated_count += 1
        counter += 1

    print(f"Created feedbacks: {created_count}, Updated feedbacks: {updated_count}")
    return True