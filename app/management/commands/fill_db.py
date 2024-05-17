from django.core.management.base import BaseCommand, CommandError, CommandParser
from app.models import Question
from app.models import Answer
from app.models import Tag
# from app.models import Status
from app.models import QuestionLike, Answer, AnswerLike, Profile, Tag
from django.contrib.auth.models import User




class Command(BaseCommand):

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument('ratio', type=int)



    def handle(self, *args, **options):
        Profile.objects.all().delete()
        Tag.objects.all().delete()
        Question.objects.all().delete()
        Answer.objects.all().delete()
        User.objects.all().delete()
        User.objects.create_superuser(username='andreykarganov', password='111')
        print('FINISHED DELETING')
        ratio = options['ratio']
        print(ratio)
        users_to_create = [
            User(
                username="user_{}".format(i),
                password="{}".format(i),
                email="email_{}@mail.ru".format(i),
                first_name="First_{}_name".format(i),
                last_name="Last_{}_name".format(i),
            )
            for i in range(1, ratio + 1)
        ]
        User.objects.bulk_create(users_to_create)
        print('Created Users')

        profiles_to_create = [
            Profile(
                user=users_to_create[i]
            )
            for i in range(ratio)
        ]
        Profile.objects.bulk_create(profiles_to_create)
        print('Created Profiles')

        tags_to_create = [
            Tag(
                name="Tag_{}".format(i),
                id=i,
            )
            for i in range(ratio)
        ]
        Tag.objects.bulk_create(tags_to_create)
        print('Created Tags')

        questions_to_create = [
            Question(
                question_id=i,
                title=f"Question #{i}",
                text=f"this question is {i} times better then the prev",
                creator=profiles_to_create[i % ratio],
                carma=(((i + 191) * 7) % 257),
                answer_count=(i * 29) % ratio,
            )
            for i in range(ratio * 10)
        ]
        Question.objects.bulk_create(questions_to_create)
        print('Created Questions')

        answers_to_create = [
            Answer(
                title=f"Answer #{i}",
                text=f"This is text answer #{i}",
                creator=profiles_to_create[i % ratio],
                question=questions_to_create[i % (ratio * 10)],
                truth_checkbox=True,
                carma=(((i + 91) * 51) % 41),
            )
            for i in range(ratio * 100)
        ]
        Answer.objects.bulk_create(answers_to_create)
        print('Created Answers')

        print('ALL CREATED SUCCESSFULY')



