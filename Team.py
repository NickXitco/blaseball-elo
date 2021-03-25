class Team:
    def __init__(self, team_id, lineup, rotation, fullName, location, nickname, shorthand):
        self.id = team_id

        self.lineup = lineup
        self.rotation = rotation

        self.fullName = fullName
        self.location = location
        self.nickname = nickname
        self.shorthand = shorthand

        self.elo = 1200

    def box(self):
        return f'{self.shorthand} {self.elo}'
