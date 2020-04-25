from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, IntegerField, SelectField, SubmitField, DecimalField
from wtforms.validators import DataRequired
# from wtforms_components import TimeField

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



'''


class DrinkerEditFormFactory:
    @staticmethod
    def form(drinker, beers, bars):
        class F(FlaskForm):
            name = StringField(default=drinker.name)
            address = StringField(default=drinker.address)
            @staticmethod
            def beer_field_name(index):
                return 'beer_{}'.format(index)
            def beer_fields(self):
                for i, beer in enumerate(beers):
                    yield beer.name, getattr(self, F.beer_field_name(i))
            def get_beers_liked(self):
                for beer, field in self.beer_fields():
                    if field.data:
                        yield beer
            @staticmethod
            def bar_field_name(index):
                return 'bar_{}'.format(index)
            def bar_fields(self):
                for i, bar in enumerate(bars):
                    yield bar.name, getattr(self, F.bar_field_name(i))
            def get_bars_frequented(self):
                for bar, field in self.bar_fields():
                    if field.data != 0:
                        yield bar, field.data
        beers_liked = [like.beer for like in drinker.likes]
        for i, beer in enumerate(beers):
            field_name = F.beer_field_name(i)
            default = 'checked' if beer.name in beers_liked else None
            setattr(F, field_name, BooleanField(default=default))
        bars_frequented = {frequent.bar: frequent.times_a_week\
                           for frequent in drinker.frequents}
        for i, bar in enumerate(bars):
            field_name = F.bar_field_name(i)
            default = bars_frequented[bar.name] if bar.name in bars_frequented else 0
            setattr(F, field_name, IntegerField(default=default))
        return F()

class ServingsFormFactory:
    @staticmethod
    def form(beer_names):
        class F(FlaskForm):
            beer_sel = SelectField('Beer Name', choices= beer_names )
            submit = SubmitField('Submit')
        return F()
'''
