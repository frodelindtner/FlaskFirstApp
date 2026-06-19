class Team:
    def __init__(self, id, season, city, name, league, division):
        self.id = id
        self.season = season
        self.city = city
        self.name = name
        self.league = league
        self.division = division

# "Season":2026,"SeasonType":1,"TeamID":16,"Key":"CHW","City":"Chicago",
#   "Name":"White Sox","League":"AL","Division":"Central","Wins":38,"Losses":33,
#   "Percentage":0.5352112676056338028169014085,"DivisionWins":12,"DivisionLosses":5,
#   "GamesBehind":0.00,"LastTenGamesWins":6,"LastTenGamesLosses":4,"Streak":"L1",
#   "LeagueRank":4,"DivisionRank":2,"WildCardRank":2,"WildCardGamesBehind":-2.50,"HomeWins":24,
#   "HomeLosses":12,"AwayWins":14,"AwayLosses":21,"DayWins":16,"DayLosses":17,"NightWins":22,
#   "NightLosses":16,"RunsScored":335,"RunsAgainst":333,"GlobalTeamID":10000016,
#   "ClinchedBestLeagueRecord":false,"ClinchedWildCard":false,"ClinchedDivision":false,
#   "EliminatedFromPlayoffContention":false        