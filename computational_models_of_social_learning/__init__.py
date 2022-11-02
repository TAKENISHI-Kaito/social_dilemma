from otree.api import *


doc = """
Your app description
"""


class C(BaseConstants):
    NAME_IN_URL = 'computatioal_models_of_social_learning'
    PLAYERS_PER_GROUP = 4
    NUM_ROUNDS = 1
    ENDOWMENT = cu(10)
    MULTIPLIER = 1.5


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    print("group")
    total_contribution = models.CurrencyField()
    individual_share = models.CurrencyField()


class Player(BasePlayer):
    print("player")
    cooperate = models.BooleanField(
        label="Will you cooperate?"
    )


# FUNCTIONS
def set_payoffs(group: Group):
    players = group.get_players()
    contributions = []
    for p in players:
        if p.cooperate == "yes":
            contributions.append(10)
    # contributions = [p.contribution for p in players]
    print(contributions)
    group.total_contribution = sum(contributions)
    group.individual_share = group.total_contribution * C.MULTIPLIER / C.PLAYERS_PER_GROUP
    for player in players:
        player.payoff = C.ENDOWMENT - player.contribution + group.individual_share
    return contributions


# PAGES
class Contribute(Page):
    form_model = "player"
    form_fields = ["contribution"]


class ResultsWaitPage(WaitPage):
    after_all_players_arrive = set_payoffs


class Results(Page):
    @staticmethod
    def vars_for_template(player: Player):
        group = player.group
        players = group.get_players()
        contributions = [p.contribution for p in players]
        return dict(
            contributions=contributions
        )


page_sequence = [Contribute, ResultsWaitPage, Results]
