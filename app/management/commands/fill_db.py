from django.core.management.base import BaseCommand, CommandParser
from app.models import Question
from app.models import Answer
from app.models import Tag
from app.models import AnswerLike
from app.models import QuestionLike
from django.contrib.auth.models import User


class Command(BaseCommand):

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument('ratio', type=int)

    def handle(self, *args, **options):
        ratio = options['ratio']
        print(ratio)
        
        users = [User.objects.create_user(f"User {i}", f"{i}_user@gmail.com", f"{i}_user_password") for i in range(1, ratio + 1)]
        

        print("end user block")
            

        tags = [Tag(name=f'Тег номер {i}') for i in range(ratio)]
        print('created list tag')
        Tag.objects.bulk_create(tags)
        print('saved in db tags') 
        
        questions = [Question(title=f'Вопрос номер {i}', text=f'Текст вопроса номер {i}') for i in range(1, ratio*10 + 1)]
        Question.objects.bulk_create(questions)
        print('created questions')

        for question in questions:
            for i in range(6):
                question.tags.add(tags[(i * question.id) % ratio])
            answers = [Answer(title=f'Ответ номер {i}', text=f'Текст ответа номер {i}', truth_checkbox=False, question_id = question.id) for i in range(1, 11)]
            Answer.objects.bulk_create(answers)
            for answer in answers:
                answerLike = [AnswerLike(user_id = i, answer_id = answer.id) for i in range(1, ratio + 1)]
                AnswerLike.objects.bulk_create(answerLike)
            questionLike = [QuestionLike(user_id = i, question_id = question.id) for i in range(1, ratio + 1)]
            QuestionLike.objects.bulk_create(questionLike)


