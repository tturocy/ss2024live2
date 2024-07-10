import random

from otree.api import (
    BaseConstants,
    BaseGroup,
    BasePlayer,
    BaseSubsession,
    Currency,
    Page,
    models,
)

doc = """
Encryption task
"""


class C(BaseConstants):
    NAME_IN_URL = "encrypt"
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 2
    PAYMENT_PER_CORRECT = Currency(0.10)


class Subsession(BaseSubsession):
    payment_per_correct = models.CurrencyField()

    def setup(self):
        self.payment_per_correct = C.PAYMENT_PER_CORRECT
        word = random.choice("AB")
        for player in self.get_players():
            player.word = word


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    word = models.StringField()
    response = models.IntegerField()
    is_correct = models.BooleanField()

    def compute_outcome(self):
        self.is_correct = (
                (self.word == "A" and self.response == 1) or
                (self.word == "B" and self.response == 2)
        )
        if self.is_correct:
            self.payoff = self.subsession.payment_per_correct


def creating_session(subsession):
    subsession.setup()


# PAGES
class Intro(Page):
    @staticmethod
    def is_displayed(player: Player) -> bool:
        return player.round_number == 1


class Decision(Page):
    form_model = "player"

    @staticmethod
    def get_form_fields(player):
        return ["response"]

    @staticmethod
    def before_next_page(player, timeout_happened):
        player.compute_outcome()


class Outcome(Page):
    @staticmethod
    def is_displayed(player: Player) -> bool:
        return player.round_number == C.NUM_ROUNDS


page_sequence = [
    Intro,
    Decision,
    Outcome,
]
