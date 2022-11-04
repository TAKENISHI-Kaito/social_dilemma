from otree.api import *


doc = """
Your app description
"""

# "indID"：player.id_in_subsession
# "round_num"：player.round_number
# "groupID"：player.group_id
# "action"：player.contribute
# "othersCoop"：player.get_others_in_group()[n].action
# "payoff"：player.payoff
# "othersCoop.past"：


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
    contributer = models.IntegerField(initial=0)


class Player(BasePlayer):
    indID = models.IntegerField(label="ID番号入力欄")
    round_num = models.IntegerField()
    groupID = models.IntegerField()
    action = models.IntegerField()
    othersCoop = models.IntegerField()
    othersCoop.past = models.IntegerField()
    contribute = models.BooleanField(
        label="10ポイントを?",
        choices=[[True, "提供する"], [False, "提供しない"]]
    )


# FUNCTIONS
def creating_session(subsession: Subsession):
    subsession.group_randomly(fixed_id_in_group=True)
    print(subsession.get_group_matrix())


def set_info(player: Player):
    player.indID = player.id_in_subsession
    player.round_num = player.round_number
    player.groupID = player.group_id
    player.payoff = C.ENDOWMENT
    if player.contribute == True:
        player.action = 1
    else:
        player.action = 0


def set_payoffs(group: Group):
    players = group.get_players()
    for player in players:
        print("player is ", player)
        print("player_action is ", player.action)
        print("player_payoff_before is ", player.payoff)
        group.contributer = 0
        if player.action == 1:
            player.payoff = C.ENDOWMENT - 10
        print("player_payoff is ", player.payoff)
        for i in range(3):
            print("i", i)
            print("player.get_others_in_group()[i]", player.get_others_in_group()[i])
            print("player.get_others_in_group()[i].action", player.get_others_in_group()[i].action)
            if player.get_others_in_group()[i].action == 1:
                group.contributer += 1
        print("group_contributer is ", group.contributer)
        print("***************************************")
        player.payoff += group.contributer * 5



# def set_payoffs(group: Group):
#     players = group.get_players()
#     # subsession = group.subsession
#     contributions = []
#     for p in players:
#         print(p.contribute)
#         print(p.id_in_subsession)
#         print(p.in_round)
#         print(p.in_rounds)
#         print(p.get_others_in_group()[0].id_in_subsession)
#         print(p.get_others_in_group()[1].id_in_subsession)
#         print(p.get_others_in_group()[2].id_in_subsession)
#         if p.contribute == True:
#             contributions.append(10)
#     # contributions = [p.contribution for p in players]
#     print(contributions)
#     group.total_contribution = sum(contributions)
#     group.individual_share = group.total_contribution * 1.5
#     for player in players:
#         player.payoff = C.ENDOWMENT - player.contribute + group.individual_share
#
    # return contributions


# PAGES
# class Input_ID(Page):
#     form_model: "player"
#     form_fields: ["indID"]


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
        contributions = [p.contribute for p in players]
        return dict(
            contributions=contributions
        )


page_sequence = [Contribute, ResultsWaitPage, Results]


def custom_export(players):
    yield[
        "indID",
        "round_num",
        "groupID",
        "action",
        "othersCoop",
        "payoff",
        # "othersCoop.past"
    ]
    for player in players:
        yield[
            "player.indID",
            "player.round_num",
            "player.groupID",
            "player.action",
            "player.othersCoop",
            "player.payoff",
            # "player.othersCoop.past"
        ]
