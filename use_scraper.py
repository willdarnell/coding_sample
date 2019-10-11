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
    for team in stats:
        field_goal = team['made_field_goals'] / team['attempted_field_goals']
        if field_goal > max_field_goal[1]:
            max_field_goal[0] = team['team']
            max_field_goal[1] = field_goal
        else:
            max_field_goal
    return max_field_goal


print(daily_leaders(25, 12, 2018))
