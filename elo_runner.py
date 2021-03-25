from blaseball_mike.models import Team
from blaseball_mike.models import Game

teams = Team.load_all()
games = []

NUM_SEASONS = 14
for i in range(1, NUM_SEASONS + 1):
    games.append(Game.load_by_season(i))

print(len(games))
