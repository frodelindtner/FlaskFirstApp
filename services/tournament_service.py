from models.tournament import Tournament
from models.tournament_team import TournamentTeam
from storage.db_tournaments import Storage_Tournament


class TournamentService:
    def __init__(self):
        self.__storage = Storage_Tournament()

    def get_all_tournaments(self):
        return self.__storage.get_all_tournaments()

    def get_tournament_by_id(self, id):
        return self.__storage.get_tournament_by_id(id)

    def create_tournament(self, name, season, format):
        normalized_format = 'Round robin' if format is None else 'Round robin' if str(format).lower() != 'round robin' else 'Round robin'
        tournament = Tournament(None, name, season, normalized_format)
        created_id = self.__storage.add_tournament(tournament)
        return Tournament(created_id, name, season, normalized_format)

    def update_tournament(self, id, name, season, format):
        normalized_format = 'Round robin' if format is None else 'Round robin' if str(format).lower() != 'round robin' else 'Round robin'
        tournament = Tournament(id, name, season, normalized_format)
        self.__storage.update_tournament(tournament)
        return tournament

    def delete_tournament(self, id):
        self.__storage.delete_tournament(id)

    def get_tournament_teams(self, tournament_id):
        return self.__storage.get_tournament_teams(tournament_id)

    def add_team_to_tournament(self, tournament_id, team_id):
        teams = self.get_tournament_teams(tournament_id)
        for team in teams:
            if team.team_id == team_id:
                return None
        return self.__storage.add_team_to_tournament(tournament_id, team_id)

    def remove_team_from_tournament(self, tournament_id, team_id):
        self.__storage.remove_team_from_tournament(tournament_id, team_id)

    def get_tournament_matches(self, tournament_id):
        return self.__storage.get_tournament_matches(tournament_id)

    def update_match_score(self, match_id, home_score, away_score):
        self.__storage.update_match_score(match_id, home_score, away_score)

    def generate_schedule(self, tournament_id):
        tournament = self.get_tournament_by_id(tournament_id)
        if tournament is None:
            return []

        self.__storage.clear_matches(tournament_id)
        teams = self.get_tournament_teams(tournament_id)
        team_ids = [team.team_id for team in teams]

        if len(team_ids) < 2:
            return []

        if tournament.format.lower() == 'round robin':
            return self.__generate_round_robin_schedule(tournament_id, team_ids)

        return []

    def __generate_round_robin_schedule(self, tournament_id, team_ids):
        teams = list(team_ids)
        if len(teams) % 2 != 0:
            teams.append(None)

        rounds = len(teams) - 1
        created_matches = []

        for round_number in range(1, rounds + 1):
            for index in range(len(teams) // 2):
                home_team = teams[index]
                away_team = teams[-(index + 1)]

                if home_team is None or away_team is None:
                    continue

                if round_number % 2 == 0:
                    home_team, away_team = away_team, home_team

                match_id = self.__storage.add_match(tournament_id, round_number, home_team, away_team)
                created_matches.append(match_id)

            rotated = [teams[0]] + [teams[-1]] + teams[1:-1]
            teams = rotated

        return created_matches
