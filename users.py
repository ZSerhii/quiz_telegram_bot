class User():

    def __init__(self, user, questions):
        self.id = user.id

        if len(user.first_name.strip()) == 0:
            self.name = user.username
        else:
            self.name = user.first_name

        self.progress = {question['id']: 0 for question in questions.list}

    def render_user_progress(self):
        remain = tuple([id for id, status in self.progress.items() if status == 0])
        passed = len(self.progress) - remain

        successes = len([id for id, status in self.progress.items() if status > 0])
        mistakes  = len([id for id, status in self.progress.items() if status < 0])

        return f'Questions: {passed} passed, {successes} correct answers, {mistakes} mistakes, {remain} remain.'
