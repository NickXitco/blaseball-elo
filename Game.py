class Game:
    def __str__(self) -> str:
        awayEloMod = '' if self.awayAdjustment < 0 else '+'
        homeEloMod = '' if self.homeAdjustment < 0 else '+'

        time_string = f'S{self.season + 1}D{self.day + 1}'
        away_string = f'({self.awayElo}{awayEloMod}{self.awayAdjustment}) {self.awayTeam.nickname} {self.awayScore}'
        home_string = f'({self.homeElo}{homeEloMod}{self.homeAdjustment}) {self.homeTeam.nickname} {self.homeScore}'

        return f'{time_string.ljust(8)}{away_string.ljust(30)}{home_string.ljust(30)}'

    def __init__(self, game_id, season, day, gameStart, gameComplete,
                 awayPitcher, awayTeam, awayOdds, awayScore, awayElo,
                 homePitcher, homeTeam, homeOdds, homeScore, homeElo):
        self.game_id = game_id
        self.season = season
        self.day = day
        self.gameStart = gameStart
        self.gameComplete = gameComplete

        self.awayScore = awayScore
        self.awayOdds = awayOdds
        self.awayTeam = awayTeam
        self.awayPitcher = awayPitcher
        self.awayElo = awayElo

        self.homeScore = homeScore
        self.homeOdds = homeOdds
        self.homeTeam = homeTeam
        self.homePitcher = homePitcher
        self.homeElo = homeElo

        self.awayAdjustment, self.homeAdjustment = self.evaluate()

    def evaluate(self):
        rA = self.awayElo
        rB = self.homeElo

        eA = 1 / (1 + 10 ** ((rA - rB) / 400))
        eB = 1.0 - eA

        #  TODO account for sun2 and black hole?

        scoreA = 1 if self.awayScore > self.homeScore else 0
        scoreB = abs(1.0 - scoreA)

        K = 16

        newEloA = int(rA + K * (scoreA - eA))
        newEloB = int(rB + K * (scoreB - eB))

        return newEloA - rA, newEloB - rB
