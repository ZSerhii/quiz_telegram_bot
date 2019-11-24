ANSWER_EMOJI = [u'\U0000274C', u'\U00002705', u'\U0001F62D', u'\U0001F389']


class Answer():

    def __init__(self, question, user_answer):
        self.choices     = question.choices
        self.user_answer = user_answer
        self.user_choice = self.__get_user_choice()
        self.is_correct  = self.user_choice.is_correct

    def __get_user_choice(self):
        return self.choices[self.user_answer]

    def display(self):
        result = f'Your answer:\n{self.user_choice.key}) {self.user_choice.value}'

        if self.is_correct:
            result = result + f'\n{ANSWER_EMOJI[1]} Congratulations! {ANSWER_EMOJI[3]}\n'
        else:
            result = result + f'\n{ANSWER_EMOJI[0]} Sorry {ANSWER_EMOJI[2]} You are wrong...\n'

        return result
