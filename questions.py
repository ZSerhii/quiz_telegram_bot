from random   import randint
from json     import loads
from telegram import InlineKeyboardButton, InlineKeyboardMarkup


CHOICE_EMOJI = [u'\U00000031\U0000FE0F\U000020E3',
                u'\U00000032\U0000FE0F\U000020E3',
                u'\U00000033\U0000FE0F\U000020E3',
                u'\U00000034\U0000FE0F\U000020E3',
                u'\U00000035\U0000FE0F\U000020E3']


def from_file(file_path):
    with open(file_path) as json_file:
        json_data = json_file.read()

        return loads(json_data)


class Choice():
    def __init__(self, choice, index_mode=1):
        self.id         = choice['id']
        self.content    = choice['content']
        self.is_correct = choice['is_correct']
        self.index_mode = index_mode

        item = choice['content'].split(':', 1)

        if self.index_mode:
            self.key = str(self.id + 1)
        else:
            self.key = item[0].replace('*', '').lower()

        self.value = item[1].strip()

    def display(self):
        if self.index_mode:
            key = CHOICE_EMOJI[self.id]  # str(int(self.id) + 1)
        else:
            key = self.key  + ')'

        return (key + ' ' + str(self.is_correct) + ' ' + self.value)


class Choices(list):
    def __init__(self, choices):
        super().__init__(choices)
        self.index_mode = randint(0, 1)

        for index, item in enumerate(self):
            self[index] = Choice(item, self.index_mode)

    def display(self):
        choices = ''

        for choice in self:
            choices += choice.display() + '\n'

        return choices

    def get_keys(self):
        result = []

        for choice in self:
            result.append(choice.key)

        return tuple(result)


class Question():
    def __init__(self, question):
        self.id      = question['id']
        self.choices = Choices(question['choices'])
        self.content = question['content']

    def display(self):
        result = f'Question №{self.id}\n{self.content}?\n\nPossible answers:\n{self.choices.display()}'

        return result


class Questions():
    def __init__(self, questions_path):
        self.list  = from_file(questions_path)
        self.count = len(self.list)

    def get_random_question(self):
        # questions_id = tuple([id for id, status in available_questions.items() if status == 1])
        questions_id = tuple([item['id'] for item in self.list])

        question_id = questions_id[randint(0, len(questions_id) - 1)]

        # available_questions[question_id] = 0

        return self.get_question_by_id(question_id)

    def get_question_by_id(self, id):
        result = None

        for question in self.list:
            if question['id'] == id:
                result = question
                break

        return Question(result)


def render_question(update, question):
    keyboard = [[], [InlineKeyboardButton("Next", callback_data='/next')]]

    for choice in question.choices:
        answer = str(question.id) + '#' + str(choice.id)
        keyboard[0].append(InlineKeyboardButton(choice.key, callback_data=answer))

    reply_markup = InlineKeyboardMarkup(keyboard)

    update.message.reply_text(question.display())
    update.message.reply_text('Please choose:', reply_markup=reply_markup)
