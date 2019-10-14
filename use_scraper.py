from basketball_reference_web_scraper import client
from basketball_reference_web_scraper.data import Team
from basketball_reference_web_scraper.data import OutputType
from collections import defaultdict


# this class is comprised of get methods that access client methods of the basketball reference web scraper
class use_scraper:
    def __init__(self, name):
        self.name = name

    def get_box_scores_date(self, day, month, year, output_type):
        player_scores = client.player_box_scores(day, month, year, output_type)
        return player_scores

    def get_team_scores(self, day, month, year):
        team_scores = client.team_box_scores(day, month, year)
        return team_scores

    def get_player_totals(self, season_year):
        player_totals = client.players_season_totals(season_year)
        return player_totals

    def get_advanced_totals(self, season_year):
        advanced_totals = client.players_advanced_season_totals(season_year)
        return advanced_totals


# this function calls the scraper and gets box scores by team from a specific date
def parse_team_stats(day, month, year):
    scraper = use_scraper("team_stats_scraper")
    team_stats_payload = scraper.get_team_scores(day, month, year)
    return team_stats_payload


# this function returns leaders in several categories including: field goal percentage
# three point field goal percentage, assist to turnover ratio, rebounds, fouls
def daily_leaders(day, month, year):
    stats = parse_team_stats(day, month, year)
    max_field_goal = [None, float('-inf')]
    max_3pt = [None, float('-inf')]
    top_rebounders = [None, float('-inf')]
    best_atot = [None, float('-inf')]
    fouls_list = sorted(stats, key=lambda team: team['personal_fouls'], reverse=True)
    most_fouls = [fouls_list[0]['team'], fouls_list[0]['personal_fouls']]
    for team in stats:
        field_goal = team['made_field_goals'] / team['attempted_field_goals']
        three_point = team['made_three_point_field_goals'] / team['attempted_three_point_field_goals']
        rebound = team['offensive_rebounds'] + team['defensive_rebounds']
        ass_to_turn = team['assists'] / team['turnovers']


        if field_goal > max_field_goal[1]:
            max_field_goal[0] = team['team']
            max_field_goal[1] = field_goal
        else:
            max_field_goal
        if three_point > max_3pt[1]:
            max_3pt[0] = team['team']
            max_3pt[1] = three_point
        else:
            max_3pt
        if rebound > top_rebounders[1]:
            top_rebounders[0] = team['team']
            top_rebounders[1] = rebound
        else:
            top_rebounders
        if ass_to_turn > best_atot[1]:
            best_atot[0] = team['team']
            best_atot[1] = ass_to_turn
        else:
            best_atot

    return max_field_goal, max_3pt, top_rebounders, best_atot, most_fouls


# this function does a variety of sorting operations using lambda functions to compute the best player in a
# variety of categories including field goals, three point field goals, and box plus minus.

def best_players(season_year):
    scraper = use_scraper("player_stats_scraper")
    player_stats = scraper.get_player_totals(season_year)
    sorted_points = sorted(player_stats, key=lambda player: player['made_field_goals'], reverse=True)
    sorted_three_points = sorted(player_stats, key=lambda player: player['made_three_point_field_goals'], reverse=True)
    statement = "The player with the most field goals and three point field" \
                "goals were: ", sorted_points[0]['name'], sorted_three_points[0]['name']
    advanced_stats = scraper.get_advanced_totals(season_year)
    sorted_box = sorted(advanced_stats, key=lambda player: player['box_plus_minus'], reverse=True)
    i = 0

    while sorted_box[i]['games_played'] < 60:
        i += 1
    else:
        return sorted_box[i], statement


print(daily_leaders(25, 12, 2017))
print(best_players(season_year=2018))
