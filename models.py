from app import db
from sqlalchemy import orm


class Players(db.Model):
    __tablename__ = 'player'
    name = db.Column('name', db.String(100))
    player_id = db.Column('player_id', db.Integer, primary_key=True)
    position = db.Column('position', db.String(1))
    avg_points = db.Column('avg_points', db.Numeric(6, 3))
    avg_rebounds = db.Column('avg_rebounds', db.Numeric(6, 3))
    avg_assists = db.Column('avg_assists', db.Numeric(6, 3))
    avg_steals = db.Column('avg_steals', db.Numeric(6, 3))
    avg_blocks = db.Column('avg_blocks', db.Numeric(6, 3))
    avg_turnovers = db.Column('avg_turnovers', db.Numeric(6, 3))
    avg_fgm = db.Column('avg_fgm', db.Numeric(6, 3))
    avg_fga = db.Column('avg_fga', db.Numeric(6, 3))
    avg_ftm = db.Column('avg_ftm', db.Numeric(6, 3))
    avg_fta = db.Column('avg_fta', db.Numeric(6, 3))
    eff = db.Column('eff', db.Numeric(6,3))

class Rosters(db.Model):
    __tablename__ = 'roster'
    player_id = db.Column('player_id', db.Integer, primary_key=True)
    team_id = db.Column('team_id', db.Integer)

class PlayersRosters(db.Model):
    __tablename__ = 'playerroster'
    player_id = db.Column('player_id', db.Integer, primary_key=True)
    team_id = db.Column('team_id', db.Integer)
    name = db.Column('name', db.String(100))
    position = db.Column('position', db.String(1))

class GameView(db.Model):
    __tablename__ = 'gameview'
    game_id = db.Column('game_id', db.Integer, primary_key=True)
    game_date_est = db.Column('game_date_est', db.Date)
    game_time = db.Column('game_time', db.Time)
    game_status_text = db.Column('game_status_text', db.String(10))
    home_team_city = db.Column('home_team_city', db.String(50))
    home_team_nickname = db.Column('home_team_nickname', db.String(50))
    visitor_team_city = db.Column('visitor_team_city', db.String(50))
    visitor_team_nickname = db.Column('visitor_team_nickname', db.String(50))

# class Standings(db.Model):
#     __tablename__ = 'Standings'
#     team_id = db.Column('team_id', db.Integer, primary_key=True)
#     league_id = db.Column('league_id', db.Integer, primary_key=True)
#     season_id = db.Column('season_id', db.Integer, primary_key=True)
#     standings_date = db.Column('standingsdate', db.Date, primary_key=True)
#     conference = db.Column('conference', db.String(4))
#     team = db.Column('team', db.String(30))
#     gp = db.Column('gp', db.Integer)
#     w = db.Column('w', db.Integer)
#     l = db.Column('l', db.Integer)
#     w_pct = db.Column('w_pct', db.Numeric(4, 3))
#     home_record = db.Column('home_record', db.String(15))
#     away_record = db.Column('road_record', db.String(15))

class Teams(db.Model):
    __tablename__ = 'team'
    team_id = db.Column('team_id', db.Integer, primary_key=True)
    # min_year = db.Column('min_year', db.Integer)
    # max_year = db.Column('max_year', db.Integer)
    abbreviation = db.Column('abbreviation', db.String(3))
    nickname = db.Column('nickname', db.String(50))
    # year_founded = db.Column('year_founded', db.Integer)
    city = db.Column('city', db.String(50))
    # arena = db.Column('arena', db.String(100))
    # arena_capacity = db.Column('arena_capacity', db.Integer)
    owner = db.Column('owner', db.String(100))
    general_manager = db.Column('general_manager', db.String(100))
    head_coach = db.Column('head_coach', db.String(100))
    # g_league_affiliation = db.Column('g_league_affiliation', db.String(100))
    conference = db.Column('conference', db.String(4))
    w = db.Column('w', db.Integer)
    l = db.Column('l', db.Integer)
    gp = w + l
    w_pct = db.Column('w_pct', db.Numeric(4, 3))
    # home_record = db.Column('home_record', db.String(15))
    # away_record = db.Column('away_record', db.String(15))

class Games(db.Model):
    __tablename__ = 'game'
    game_date_est = db.Column('game_date_est', db.Date)
    game_time = db.Column('game_time', db.Time)
    game_id = db.Column('game_id', db.Integer, primary_key=True)
    game_status_text = db.Column('game_status_text', db.String(10))

class Plays(db.Model):
    __tablename__ = 'plays'
    game_id = db.Column('game_id', db.Integer, primary_key=True)
    home_team_id = db.Column('home_team_id', db.Integer)
    visitor_team_id = db.Column('visitor_team_id', db.Integer)
    pts_home = db.Column('pts_home', db.Numeric(4, 1))
    fg_pct_home = db.Column('fg_pct_home', db.Numeric(4, 3))
    ft_pct_home = db.Column('ft_pct_home', db.Numeric(4, 3))
    fg3_pct_home = db.Column('fg3_pct_home', db.Numeric(4, 3))
    ast_home = db.Column('ast_home', db.Numeric(4, 1))
    reb_home = db.Column('reb_home', db.Numeric(4, 1))
    pts_away = db.Column('pts_away', db.Numeric(4, 1))
    fg_pct_away = db.Column('fg_pct_away', db.Numeric(4, 3))
    ft_pct_away = db.Column('ft_pct_away', db.Numeric(4, 3))
    fg3_pct_away = db.Column('fg3_pct_away', db.Numeric(4, 3))
    ast_away = db.Column('ast_away', db.Numeric(4, 1))
    reb_away = db.Column('reb_away', db.Numeric(4, 1))
    home_team_wins = db.Column('home_team_wins', db.Boolean)

class Performance(db.Model):
    __tablename__ = 'performance'
    game_id = db.Column('game_id', db.Integer, primary_key=True)
    player_id = db.Column('player_id', db.Integer, primary_key=True)
    minutes = db.Column('minutes', db.String(5))
    fgm = db.Column('fgm', db.Integer)
    fga = db.Column('fga', db.Integer)
    fg_pct = db.Column('fg_pct', db.Numeric(3, 1))
    fg3m = db.Column('fg3m', db.Integer)
    fg3a = db.Column('fg3a', db.Integer)
    fg3_pct = db.Column('fg3_pct', db.Numeric(3, 1))
    ftm = db.Column('ftm', db.Integer)
    fta = db.Column('fta', db.Integer)
    ft_pct = db.Column('ft_pct', db.Numeric(3, 1))
    offensive_rebounds = db.Column('offensive_rebounds', db.Integer)
    defensive_rebounds = db.Column('defensive_rebounds', db.Integer)
    rebounds = db.Column('rebounds', db.Integer)
    assists = db.Column('assists', db.Integer)
    steals = db.Column('steals', db.Integer)
    blocks = db.Column('blocks', db.Integer)
    turnovers = db.Column('turnovers', db.Integer)
    personal_fouls = db.Column('personal_fouls', db.Integer)
    points = db.Column('points', db.Integer)
    plus_minus = db.Column('plus_minus', db.Integer)
