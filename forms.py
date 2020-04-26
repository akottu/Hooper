from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, IntegerField, SelectField, SubmitField, DecimalField
from wtforms.validators import DataRequired
from wtforms_components import TimeField

class PlayerEditFormFactory:
    @staticmethod
    def form(player):
        class F(FlaskForm):
            name = StringField(default=player.name)
            player_id = IntegerField(default=player.player_id)
            position = StringField(default=player.position)
            avg_points = DecimalField(default=player.avg_points)
            avg_rebounds = DecimalField(default=player.avg_rebounds)
            avg_assists = DecimalField(default=player.avg_assists)
            avg_steals = DecimalField(default=player.avg_steals)
            avg_blocks = DecimalField(default=player.avg_blocks)
            avg_turnovers = DecimalField(default=player.avg_turnovers)
            avg_fgm = DecimalField(default=player.avg_fgm)
            avg_fga = DecimalField(default=player.avg_fga)
            avg_ftm = DecimalField(default=player.avg_ftm)
            avg_fta = DecimalField(default=player.avg_fta)
            eff = DecimalField(default=player.eff)
        return F()

class TeamEditFormFactory:
    @staticmethod
    def form(team):
        class F(FlaskForm):
            team_id = IntegerField(default=team.team_id)
            abbreviation = StringField(default=team.abbreviation)
            nickname = StringField(default=team.nickname)
            city = StringField(default=team.city)
            owner = StringField(default=team.owner)
            general_manager = StringField(default=team.general_manager)
            head_coach = StringField(default=team.head_coach)
            conference =StringField(default=team.conference)
            w = IntegerField(default=team.w)
            l = IntegerField(default=team.l)
            gp = IntegerField(default=team.w + team.l)
            w_pct = DecimalField(default=team.w_pct)
        return F()

class GameEditFormFactory:
    @staticmethod
    def form(game):
        class F(FlaskForm):
            game_date_est = DateField(default=game.game_date_est)
            game_time = TimeField(default=game.game_time)
            game_id = IntegerField(default=game.game_id)
            game_status_text = StringField(default=game.game_status_text)
        return F()
