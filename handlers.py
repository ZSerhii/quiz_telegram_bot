from questions import Questions, render_question
from answers   import Answer
from users     import User


QUESTIONS_PATH = 'C:\\Projects\\Beetroot.Academy\\Lessons\\questions.json'

questions = Questions(QUESTIONS_PATH)


def handle_start(update, context):
    user = User(update.message.from_user, questions)

    update.message.reply_text(f'Hello, {user.name}. Let the game begin!')

    handle_next(update, context)


def handle_button(update, context):
    query = update.callback_query

    if query.data.count('#') > 0:
        user_answer = query.data.split('#')

        question_id = int(user_answer[0])
        choice_id   = int(user_answer[1])

        question = questions.get_question_by_id(question_id)

        answer = Answer(question, choice_id)

        response = answer.display()
    else:
        response = f'Input /next to get next random question'

    query.edit_message_text(response)


def handle_help(update, context):
    update.message.reply_text('''Input:
/start to start new game;
/next to get next question;
/get <number> to get question number <number>;
/finish to finish game and get results;
/result to get current results''')


def handle_next(update, context):
    question = questions.get_random_question()

    render_question(update, question)


def handle_get(update, context):
    if len(context.args) == 1 and context.args[0].isdigit():
        question = questions.get_question_by_id(int(context.args[0]))
    else:
        question = questions.get_random_question()

        comment = 'Use /get # to get question with ID = #,\n' \
                  'for example /get 120.\n' \
                  'Random question by default'

        update.message.reply_text(comment)

    render_question(update, question)


def handle_finish(update, context):
    update.message.reply_text('The End')


def handle_result(update, context):
    update.message.reply_text('Results!')


def echo(update, context):
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f'You wrote:\n{update.message.text}\nInput /help to get a list of available commands.'
    )
