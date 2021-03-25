from operator import itemgetter

import requests

from Game import Game
from Team import Team

teams = requests.get('https://www.blaseball.com/database/allTeams').json()

team_lookup = {}

for team in teams:
    new_team = Team(team["id"], team["lineup"], team["rotation"],
                    team["fullName"], team["location"], team["nickname"], team["shorthand"])
    team_lookup[team["id"]] = new_team
    print(f'{new_team.fullName.ljust(30)} {new_team.id}')


season = 0
games_endpoint = 'https://www.blaseball.com/database/games?'
startOfSeasonTeams = []
endOfSeasonTeams = []


players = requests.get('https://reblase.sibr.dev/newapi/teams')

while True:
    day = 0

    startOfSeasonTeams = []

    while True:
        games = requests.get(f'{games_endpoint}day={day}&season={season}').json()

        for game in games:
            awayTeam = team_lookup[game["awayTeam"]]
            homeTeam = team_lookup[game["homeTeam"]]
            awayElo = awayTeam.elo
            homeElo = homeTeam.elo

            if day == 0:
                startOfSeasonTeams.append((awayTeam, awayElo))
                startOfSeasonTeams.append((homeTeam, homeElo))

            g = Game(game["id"], season, day, game["gameStart"], game["gameComplete"],
                     game["awayPitcher"], awayTeam, game["awayOdds"], game["awayScore"], awayElo,
                     game["homePitcher"], homeTeam, game["homeOdds"], game["homeScore"], homeElo)

            awayTeam.elo += g.awayAdjustment
            homeTeam.elo += g.homeAdjustment

        if len(games) == 0:
            break

        day += 1

    endOfSeasonTeams = []

    for teamElo in startOfSeasonTeams:
        team = teamElo[0]
        elo = teamElo[1]

        eloMod = '' if elo > team.elo else '+'

        endOfSeasonTeams.append((team, team.elo, eloMod + str(team.elo - elo)))

    endOfSeasonTeams.sort(key=itemgetter(1), reverse=True)

    print(f'=========END OF SEASON {season + 1} REPORT=========')
    for team in endOfSeasonTeams:
        print(f'{team[0].fullName.ljust(40)} {team[1]} ({team[2]})')

    if day == 0:
        break

    season += 1
