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

class PlaysEditFormFactory:
    @staticmethod
    def form(play):
        class F(FlaskForm):
            game_id = IntegerField(default=play.game_id)
            home_team_id = IntegerField(default=play.game_id)
            visitor_team_id = IntegerField(default=play.game_id)
            pts_home = DecimalField(default=play.pts_home)
            fg_pct_home = DecimalField(default=play.fg_pct_home)
            ft_pct_home = DecimalField(default=play.ft_pct_home)
            fg3_pct_home = DecimalField(default=play.fg3_pct_home)
            ast_home = DecimalField(default=play.ast_home)
            reb_home = DecimalField(default=play.reb_home)
            pts_away = DecimalField(default=play.pts_away)
            fg_pct_away = DecimalField(default=play.fg_pct_away)
            ft_pct_away = DecimalField(default=play.ft_pct_away)
            fg3_pct_away = DecimalField(default=play.fg3_pct_away)
            ast_away = DecimalField(default=play.ast_away)
            reb_away = DecimalField(default=play.reb_away)
            home_team_wins = BooleanField(default=play.home_team_wins)
        return F()
