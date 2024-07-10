from otree.api import (
    BaseConstants,
    BaseGroup,
    BasePlayer,
    BaseSubsession,
    Page,
    WaitPage,
)

doc = """
A simple Tullock contest game with possibly different costs of effort.
"""


class C(BaseConstants):
    NAME_IN_URL = "contest"
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    pass


# PAGES
class Intro(Page):
    pass


class SetupRound(WaitPage):
    pass


class Decision(Page):
    pass


class WaitForDecisions(WaitPage):
    pass


class Results(Page):
    pass


class EndBlock(Page):
    pass


page_sequence = [
    Intro,
    SetupRound,
    Decision,
    WaitForDecisions,
    Results,
    EndBlock,
]
