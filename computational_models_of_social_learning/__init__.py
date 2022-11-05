from otree.api import *


doc = """
Your app description
"""

# "indID"：player.id_in_subsession
# "round_number"
# "groupID"：player.group_id
# "action"：player.contribute
# "othersCoop"：player.get_others_in_group()[n].action
# "payoff"：player.payoff
# "othersCoop_past"：


class C(BaseConstants):
    NAME_IN_URL = 'computatioal_models_of_social_learning'
    PLAYERS_PER_GROUP = 4
    NUM_ROUNDS = 3
    ENDOWMENT = cu(10)


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    total_contribution = models.CurrencyField()
    individual_share = models.CurrencyField()


class Player(BasePlayer):
    indID = models.IntegerField(label="以下にID番号を入力してください")
    groupID = models.IntegerField()
    action = models.IntegerField()
    othersCoop = models.IntegerField(initial=0)
    othersCoop_past = models.IntegerField()
    contribute = models.BooleanField(
        label="10ポイントを",
        choices=[[True, "提供する"], [False, "提供しない"]]
    )


# FUNCTIONS
def creating_session(subsession: Subsession):
    subsession.group_randomly(fixed_id_in_group=True)
    print(subsession.get_group_matrix())


def set_info(player: Player):
    player.indID = player.id_in_subsession
    player.groupID = player.group_id
    player.payoff = C.ENDOWMENT
    player.action = int(player.contribute)
    if player.round_number >= 2:
        player.othersCoop_past = player.in_round(
            player.round_number - 1).othersCoop
    else:
        player.othersCoop_past = None


def set_payoffs(group: Group):
    players = group.get_players()
    for player in players:
        if player.action == 1:
            player.payoff = C.ENDOWMENT - 10
        player.othersCoop = 0
        for i in range(3):
            if player.get_others_in_group()[i].action == 1:
                player.othersCoop += 1
        player.payoff += player.othersCoop * 5


# PAGES
class Input_ID(Page):
    form_model = "player"
    form_fields = ["indID"]
    @staticmethod
    def is_displayed(player):
        return player.round_number == 1


class Contribute(Page):
    form_model = "player"
    form_fields = ["contribute"]

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        set_info(player)


class ResultsWaitPage(WaitPage):
    after_all_players_arrive = set_payoffs


class Results(Page):
    @staticmethod
    def vars_for_template(player: Player):
        group = player.group
        players = group.get_players()
        return dict(
            players=players
        )


page_sequence = [Input_ID, Contribute, ResultsWaitPage, Results]


def custom_export(players):
    yield[
        "indID",
        "round",
        "groupID",
        "action",
        "othersCoop",
        "payoff",
        "othersCoop_past"
    ]
    for player in players:
        yield[
            player.indID,
            player.round_number,
            player.groupID,
            player.action,
            player.othersCoop,
            player.payoff,
            player.othersCoop_past
        ]
