from flask import Flask, render_template, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
from sqlalchemy import create_engine
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey
from sqlalchemy import inspect
import models
import forms
import urllib.parse
from flask_admin import Admin
from flask_login import LoginManager, login_user, logout_user


app = Flask(__name__)
app.secret_key = 's3cr3t'
app.config.from_object('config')
db = SQLAlchemy(app, session_options={'autocommit': False})

login = LoginManager(app)


@login.user_loader
def load_user(user_id):
    return models.HooperUser.query.get(user_id)


admin = Admin(app)
admin.add_view(models.HooperModelView(models.HooperUser, db.session))
admin.add_view(models.HooperModelView(models.Players, db.session))
admin.add_view(models.HooperModelView(models.Teams, db.session))
admin.add_view(models.HooperModelView(models.Rosters, db.session))
admin.add_view(models.HooperModelView(models.Games, db.session))
admin.add_view(models.HooperModelView(models.Plays, db.session))
admin.add_view(models.HooperModelView(models.Performance, db.session))

@app.route('/')
def index():
    players = db.session.query(models.Players)\
        .order_by(models.Players.eff.desc())\
        .all()[0:10]
    west_standings = db.session.query(models.Teams)\
        .filter(models.Teams.conference == "West")\
        .order_by(models.Teams.w_pct.desc())\
        .all()[0:8]
    east_standings = db.session.query(models.Teams)\
        .filter(models.Teams.conference == "East")\
        .order_by(models.Teams.w_pct.desc())\
        .all()[0:8]
    return render_template('index.html', players=players, west_standings=west_standings, east_standings=east_standings)

@app.route('/view-players')
def view_players():
    players = db.session.query(models.Players).all()
    return render_template('view-all-players.html', players=players)

@app.route('/view-standings')
def view_standings():
    west_standings = db.session.query(models.Teams)\
        .filter(models.Teams.conference == "West") \
        .order_by(models.Teams.w_pct.desc())\
        .all()
    east_standings = db.session.query(models.Teams) \
        .filter(models.Teams.conference == "East") \
        .order_by(models.Teams.w_pct.desc()) \
        .all()
    return render_template('view-standings.html', west_standings=west_standings, east_standings=east_standings)

@app.route('/view-team/<team_id>')
def view_teams(team_id):
    all_teams = db.session.query(models.Teams)\
        .order_by(models.Teams.nickname)\
        .all()
    team = db.session.query(models.Teams) \
        .filter(models.Teams.team_id == team_id).first()
    players_on_roster = db.session.query(models.PlayersRosters)\
        .filter(models.PlayersRosters.team_id == team_id)\
        .all()
    return render_template('view-team.html', team=team, all_teams=all_teams, players_on_roster=players_on_roster)

@app.route('/view-player/<player_id>')
def view_player(player_id):
    player = db.session.query(models.Players)\
        .filter(models.Players.player_id == player_id)\
        .first()
    player_team = db.session.query(models.Teams)\
        .filter(models.Teams.team_id == db.session.query(models.Rosters).filter(models.Rosters.player_id == player_id).first().team_id)\
        .first()
    all_players = db.session.query(models.Players)\
        .all()
    player_performances = db.session.query(models.Performance)\
        .filter(models.Performance.player_id == player_id)\
        .all()
    return render_template('view-player.html', player=player, player_team=player_team, all_players=all_players, player_performances=player_performances)

@app.route('/view-game/<game_id>')
def view_game(game_id):
    game = db.session.query(models.Plays) \
        .filter(models.Plays.game_id == game_id).first()
    home_team = db.session.query(models.Teams) \
        .filter(models.Teams.team_id == game.home_team_id).first()
    away_team = db.session.query(models.Teams) \
        .filter(models.Teams.team_id == game.visitor_team_id).first()
    return render_template('view-game.html', game=game, home_team=home_team, away_team=away_team)

@app.route('/view-games')
def view_games():
    games = db.session.query(models.GameView).all()
    return render_template('view-all-games.html', games=games)

@app.route('/view-performance')
def view_performance():
    performances = db.session.query(models.Teams).all()
    return render_template('view-all-performances.html', entries=performances)

@app.route('/edit-player/<name>', methods=['GET', 'POST'])
def edit_player(name):
    player = db.session.query(models.Players)\
        .filter(models.Players.name == name).first()
    form = forms.PlayerEditFormFactory.form(player)
    engine = create_engine('postgresql://user:Hooperdb2020@vcm-13382.vm.duke.edu:5432/hooper')
    if form.validate_on_submit():
        print('submitted')
        try:
            form.errors.pop('database', None)
            player.player_id = form.player_id.data
            conn = engine.connect()
            conn.execute(text('UPDATE player SET name = :form_name  WHERE player_id = :form_player_id'), form_name=form.name.data, form_player_id=form.player_id.data)
            conn.execute(text('UPDATE player SET position = :form_position WHERE player_id = :form_player_id'), form_position=form.position.data, form_player_id=form.player_id.data)
            conn.close()
            return redirect(url_for('view_players'))
        except BaseException as e:
            form.errors['database'] = str(e)
            return render_template('edit-player.html', player=player, form=form)
    else:
        return render_template('edit-player.html', player=player, form=form)


@app.route('/edit-team/<team_id>', methods=['GET', 'POST'])
def edit_team(team_id):
    team = db.session.query(models.Teams)\
        .filter(models.Teams.team_id == team_id).first()
    form = forms.TeamEditFormFactory.form(team)
    engine = create_engine('postgresql://user:Hooperdb2020@vcm-13382.vm.duke.edu:5432/hooper')
    if form.validate_on_submit():
        try:
            form.errors.pop('database', None)
            player.team_id = form.team_id.data
            conn.execute(text('UPDATE team SET nickname = :form_nickname  WHERE team_id = :form_team_id'), form_nickname=form.nickname.data, form_team_id=form.team_id.data)
            conn.execute(text('UPDATE team SET city = :form_city WHERE team_id = :form_team_id'), form_city=form.city.data, form_team_id=form.team_id.data)
            conn.execute(text('UPDATE team SET abbreviation = :form_abbreviation WHERE team_id = :form_team_id'), form_abbreviation=form.abbreviation.data, form_team_id=form.team_id.data)
            conn.execute(text('UPDATE team SET owner = :form_owner WHERE team_id = :form_team_id'), form_owner=form.owner.data, form_team_id=form.team_id.data)
            conn.execute(text('UPDATE team SET head_coach = :form_head_coach WHERE team_id = :form_team_id'), form_head_coach=form.head_coach.data, form_team_id=form.team_id.data)
            conn.execute(text('UPDATE team SET general_manager = :form_general_manager WHERE team_id = :form_team_id'), form_general_manager=form.general_manager.data, form_team_id=form.team_id.data)
            conn.execute(text('UPDATE team SET conference = :form_conference WHERE team_id = :form_team_id'), form_conference=form.conference.data, form_team_id=form.team_id.data)
            conn.execute(text('UPDATE team SET w = :form_w WHERE team_id = :form_team_id'), form_w=form.w.data, form_team_id=form.team_id.data)
            conn.execute(text('UPDATE team SET l = :form_l WHERE team_id = :form_team_id'), form_l=form.l.data, form_team_id=form.team_id.data)
            conn.execute(text('UPDATE team SET w_pct = :form_w_pct WHERE team_id = :form_team_id'), form_w_pct=form.w_pct.data, form_team_id=form.team_id.data)
            db.session.commit()
            return redirect(url_for('view_teams'))
        except BaseException as e:
            form.errors['database'] = str(e)
            return render_template('edit-team.html', team=team, form=form)
    else:
        return render_template('edit-team.html', team=team, form=form)


@app.route('/edit-game/<name>', methods=['GET', 'POST'])
def edit_game(gameID):
    game = db.session.query(models.Plays)\
        .filter(models.Plays.game_id == gameID).first()
    form = forms.GameEditFormFactory.form(play)
    engine = create_engine('postgresql://user:Hooperdb2020@vcm-13382.vm.duke.edu:5432/hooper')
    if form.validate_on_submit():
        try:
            form.errors.pop('database', None)
            team.game_id = form.game_id.data
            conn = engine.connect()
            conn.execute(text('UPDATE team SET home_team_id = :form_home_team_id  WHERE team_id = :form_team_id'), form_home_team_id=form.home_team_id.data, form_team_id=form.team_id.data)
            conn.execute(text('UPDATE team SET visitor_team_id = :form_visitor_team_id WHERE team_id = :form_team_id'), form_visitor_team_id=form.visitor_team_id.data, form_team_id=form.team_id.data)
            conn.execute(text('UPDATE team SET pts_home = :form_pts_home WHERE team_id = :form_team_id'), form_pts_home=form.pts_home.data, form_team_id=form.team_id.data)
            conn.execute(text('UPDATE team SET fg_pct_home = :form_fg_pct_home WHERE team_id = :form_team_id'), form_fg_pct_home=form.fg_pct_home.data, form_team_id=form.team_id.data)
            conn.execute(text('UPDATE team SET fg3_pct_home = :form_fg3_pct_home WHERE team_id = :form_team_id'), form_fg3_pct_home=form.fg3_pct_home.data, form_team_id=form.team_id.data)
            conn.execute(text('UPDATE team SET fg3_pct_home = :form_fg3_pct_home WHERE team_id = :form_team_id'), form_fg3_pct_home=form.fg3_pct_home.data, form_team_id=form.team_id.data)
            conn.execute(text('UPDATE team SET ast_home = :form_ast_home WHERE team_id = :form_team_id'), form_ast_home=form.ast_home.data, form_team_id=form.team_id.data)
            conn.execute(text('UPDATE team SET reb_home = :form_reb_home WHERE team_id = :form_team_id'), form_reb_home=form.reb_home.data, form_team_id=form.team_id.data)
            conn.execute(text('UPDATE team SET pts_away = :form_pts_away WHERE team_id = :form_team_id'), form_pts_away=form.pts_away.data, form_team_id=form.team_id.data)
            conn.execute(text('UPDATE team SET fg_pct_away = :form_fg_pct_away WHERE team_id = :form_team_id'), form_fg_pct_away=form.fg_pct_away.data, form_team_id=form.team_id.data)
            conn.execute(text('UPDATE team SET ft_pct_away = :form_ft_pct_away  WHERE team_id = :form_team_id'), form_ft_pct_away=form.ft_pct_away.data, form_team_id=form.team_id.data)
            conn.execute(text('UPDATE team SET fg3_pct_away = :form_fg3_pct_away WHERE team_id = :form_team_id'), form_fg3_pct_away=form.fg3_pct_away.data, form_team_id=form.team_id.data)
            conn.execute(text('UPDATE team SET ast_away = :form_ast_away WHERE team_id = :form_team_id'), form_ast_away=form.ast_away.data, form_team_id=form.team_id.data)
            conn.execute(text('UPDATE team SET reb_away = :form_reb_away WHERE team_id = :form_team_id'), form_reb_away=form.reb_away.data, form_team_id=form.team_id.data)
            conn.execute(text('UPDATE team SET home_team_wins = :form_home_team_wins WHERE team_id = :form_team_id'), form_home_team_wins=form.home_team_wins.data, form_team_id=form.team_id.data)
            db.session.commit()
            return redirect(url_for('view_games'))
        except BaseException as e:
            form.errors['database'] = str(e)
            return render_template('edit-game.html', game=game, form=form)
    else:
        return render_template('edit-game.html', game=game, form=form)


@app.route('/drinker/<name>')
def drinker(name):
    drinker = db.session.query(models.Drinker)\
        .filter(models.Drinker.name == name).one()
    return render_template('drinker.html', drinker=drinker)

@app.route('/serves', methods=['GET', 'POST'])
def serves():
    beers = db.session.query(models.Beer).all()
    beer_names = [beer.name for beer in beers]
    form = forms.ServingsFormFactory.form(beer_names)
    if form.validate_on_submit():
        return render_template('/servings/' + form.beer_sel.data)
    return render_template('serves.html', form=form)

@app.route('/servings/<beer_name>', methods=['GET', 'POST'])
def servings_for(beer_name):
    selected_beer = request.args.get('list_status')
    results = db.session.query(models.Serves, models.Bar) \
                .filter(models.Serves.beer == beer_name) \
                .filter(models.Serves.bar == models.Bar.name) \
                .all()
    return render_template('servings_for.html', beer_name=beer_name, data=results)

@app.route('/edit-drinker/<name>', methods=['GET', 'POST'])
def edit_drinker(name):
    drinker = db.session.query(models.Drinker)\
        .filter(models.Drinker.name == name).one()
    beers = db.session.query(models.Beer).all()
    bars = db.session.query(models.Bar).all()
    form = forms.DrinkerEditFormFactory.form(drinker, beers, bars)
    if form.validate_on_submit():
        try:
            form.errors.pop('database', None)
            models.Drinker.edit(name, form.name.data, form.address.data,
                                form.get_beers_liked(), form.get_bars_frequented())
            return redirect(url_for('drinker', name=form.name.data))
        except BaseException as e:
            form.errors['database'] = str(e)
            return render_template('edit-drinker.html', drinker=drinker, form=form)
    else:
        return render_template('edit-drinker.html', drinker=drinker, form=form)

@app.template_filter('pluralize')
def pluralize(number, singular='', plural='s'):
    return singular if number in (0, 1) else plural

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002)