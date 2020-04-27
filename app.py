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

@app.route('/create-game', methods=['GET', 'POST'])
def create_game():
    game = models.Games()
    game.game_id = db.session.query(models.Games).count() + 1
    game.game_status_text = ""
    form = forms.GameEditFormFactory.form(game)
    if form.validate_on_submit():
        try:
            form.errors.pop('database', None)
            game.game_date_est = form.game_date_est.data
            game.game_time = form.game_time.data
            game.game_status_text = form.game_status_text.data
            db.session.add(game)
            db.session.commit()
            return redirect(url_for('create_game'))
        except BaseException as e:
            form.errors['database'] = str(e)
            return render_template('create_game.html', team=game, form=form)
    else:
        return render_template('create_game.html', game=game, form=form)

@app.route('/create-player', methods=['GET', 'POST'])
def create_player():
    player = models.Players()
    player.player_id = db.session.query(models.Players).count() + 1
    player.name = ""
    player.position = ""
    player.eff = 0
    player.avg_assists = 0
    player.avg_blocks = 0
    player.avg_fga = 0
    player.avg_fgm = 0
    player.avg_fta = 0
    player.avg_ftm = 0
    player.avg_points = 0
    player.avg_rebounds = 0
    player.avg_steals = 0
    player.avg_turnovers = 0
    form = forms.PlayerEditFormFactory.form(player)
    if form.validate_on_submit():
        try:
            form.errors.pop('database', None)
            player.name = form.name.data
            player.position = form.position.data
            db.session.add(player)
            db.session.commit()
            return redirect(url_for('view_players'))
        except BaseException as e:
            form.errors['database'] = str(e)
            return render_template('create_player.html', player=player, form=form)
    else:
        return render_template('create_player.html', player=player, form=form)

@app.route('/create-team', methods=['GET', 'POST'])
def create_team():
    team = models.Teams()
    team.team_id = db.session.query(models.Teams).count() + 1
    team.city = ""
    team.nickname = ""
    team.abbreviation = ""
    team.owner = ""
    team.general_manager = ""
    team.head_coach = ""
    team.conference = ""
    team.l = 0
    team.w = 0
    team.gp = 0
    team.w_pct = 0
    form = forms.TeamEditFormFactory.form(team)
    if form.validate_on_submit():
        try:
            form.errors.pop('database', None)
            team.city = form.city.data
            team.nickname = form.nickname.data
            team.owner = form.owner.data
            team.conference = form.conference.data
            team.general_manager = form.general_manager.data
            team.head_coach = form.head_coach.data
            db.session.add(team)
            db.session.commit()
            return redirect(url_for('create_team'))
        except BaseException as e:
            form.errors['database'] = str(e)
            return render_template('create_team.html', team=team, form=form)
    else:
        return render_template('create_team.html', team=team, form=form)

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

@app.template_filter('pluralize')
def pluralize(number, singular='', plural='s'):
    return singular if number in (0, 1) else plural

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002)