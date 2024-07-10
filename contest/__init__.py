import random

from otree.api import (
    BaseConstants,
    BaseGroup,
    BasePlayer,
    BaseSubsession,
    Page,
    WaitPage,
    models,
)

doc = """
A simple Tullock contest game with possibly different costs of effort.
"""


class C(BaseConstants):
    NAME_IN_URL = "contest"
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 2
    ENDOWMENT = 20
    PRIZE = 20
    COST_PER_TICKET = 1


class Subsession(BaseSubsession):
    is_paid = models.BooleanField()

    def setup(self):
        self.is_paid = (self.round_number == 1)
        for group in self.get_groups():
            group.setup()


class Group(BaseGroup):
    def setup(self):
        for player in self.get_players():
            player.setup()

    def determine_outcome(self):
        tickets = []
        for player in self.get_players():
            for _ in range(player.tickets_purchased):
                tickets.append(player.id_in_group)
        if not tickets:
            for player in self.get_players():
                tickets.append(player.id_in_group)
        winning_id = random.choice(tickets)
        for player in self.get_players():
            player.is_winner = (player.id_in_group == winning_id)
            player.earnings = (
                    player.endowment - player.cost_per_ticket*player.tickets_purchased
                    + player.is_winner * C.PRIZE
            )
            if self.subsession.is_paid:
                player.payoff = player.earnings


class Player(BasePlayer):
    endowment = models.IntegerField()
    cost_per_ticket = models.IntegerField()
    tickets_purchased = models.IntegerField()
    is_winner = models.BooleanField()
    earnings = models.IntegerField()

    def setup(self):
        self.endowment = C.ENDOWMENT
        self.cost_per_ticket = C.COST_PER_TICKET


# PAGES
class Intro(Page):
    pass


class SetupRound(WaitPage):
    wait_for_all_groups = True

    @staticmethod
    def after_all_players_arrive(subsession):
        subsession.setup()


class Decision(Page):
    form_model = "player"

    @staticmethod
    def get_form_fields(player):
        return ["tickets_purchased"]


class WaitForDecisions(WaitPage):
    wait_for_all_groups = True

    @staticmethod
    def after_all_players_arrive(subsession):
        for group in subsession.get_groups():
            group.determine_outcome()


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
