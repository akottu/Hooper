DROP TABLE IF EXISTS Game, Player, Team, Plays, Performance, Roster CASCADE;
DROP FUNCTION IF EXISTS TF_Team_update, TF_Player_update, TF_Player_col_update, TF_Team_col_update, TF_Performance_col_update, TF_Plays_col_update, TF_Game_col_update CASCADE;

CREATE TABLE IF NOT EXISTS Player (
    player_id INT PRIMARY KEY NOT NULL,
    name VARCHAR(40) NOT NULL,
    position CHAR(1) NOT NULL CHECK(position='G' OR position='C' OR position='F'),
    tot_points INT NOT NULL,
    tot_rebounds INT NOT NULL,
    tot_assists INT NOT NULL,
    tot_steals INT NOT NULL,
    tot_blocks INT NOT NULL,
    tot_turnovers INT NOT NULL,
    tot_fgm INT NOT NULL,
    tot_fga INT NOT NULL,
    tot_ftm INT NOT NULL,
    tot_fta INT NOT NULL,
    gp INT NOT NULL,
    avg_points DECIMAL(6,3) NOT NULL,
    avg_rebounds DECIMAL(6,3) NOT NULL,
    avg_assists DECIMAL(6,3) NOT NULL,
    avg_steals DECIMAL(6,3) NOT NULL,
    avg_blocks DECIMAL(6,3) NOT NULL,
    avg_turnovers DECIMAL(6,3) NOT NULL,
    avg_fgm DECIMAL(6,3) NOT NULL,
    avg_fga DECIMAL(6,3) NOT NULL,
    avg_ftm DECIMAL(6,3) NOT NULL,
    avg_fta DECIMAL(6,3) NOT NULL,
    eff DECIMAL(6,3) NOT NULL
);

CREATE TABLE IF NOT EXISTS Team (
    team_id INT NOT NULL PRIMARY KEY,
    city VARCHAR(40) NOT NULL,
    nickname VARCHAR(40) NOT NULL,
    abbreviation CHAR(3) NOT NULL,
    owner VARCHAR(40) NOT NULL,
    general_manager VARCHAR(40) NOT NULL,
    head_coach VARCHAR(40) NOT NULL,
    conference CHAR(4) NOT NULL CHECK(conference='West' OR conference='East'),
    w INT NOT NULL,
    l INT NOT NULL,
    w_pct DECIMAL(4,3)
);

CREATE TABLE IF NOT EXISTS Game (
    game_id INT PRIMARY KEY NOT NULL,
    game_date_est DATE NOT NULL,
    game_time TIME WITH TIME ZONE NOT NULL,
    game_status_text VARCHAR(10) NOT NULL CHECK(game_status_text='Final' OR game_status_text='Upcoming')
);

CREATE TABLE IF NOT EXISTS Performance (
    player_id INT NOT NULL,
    game_id INT NOT NULL,
    points INT NOT NULL,
    assists INT NOT NULL,
    steals INT NOT NULL,
    blocks INT NOT NULL,
    turnovers INT NOT NULL,
    minutes INT NOT NULL,
    fgm INT NOT NULL,
    fga INT NOT NULL,
    fg3m INT NOT NULL,
    fg3a INT NOT NULL,
    ftm INT NOT NULL,
    fta INT NOT NULL,
    offensive_rebounds INT NOT NULL,
    defensive_rebounds INT NOT NULL,
    personal_fouls INT NOT NULL,
    plus_minus INT NOT NULL,
    fg_pct DECIMAL(4,3),
    fg3_pct DECIMAL(4,3),
    ft_pct DECIMAL(4,3),
    rebounds INT NOT NULL,
    PRIMARY KEY(game_id, player_id),
    FOREIGN KEY(game_id) REFERENCES Game(game_id),
    FOREIGN KEY(player_id) REFERENCES Player(player_id)
);

CREATE TABLE IF NOT EXISTS Plays (
    game_id INT NOT NULL PRIMARY KEY,
    home_team_id INT NOT NULL,
    visitor_team_id INT NOT NULL,
    pts_home INT NOT NULL,
    pts_away INT NOT NULL,
    fg_pct_home DECIMAL(4,3) NOT NULL,
    ft_pct_home DECIMAL(4,3) NOT NULL,
    fg3_pct_home DECIMAL(4,3) NOT NULL,
    ast_home INT NOT NULL,
    reb_home INT NOT NULL,
    fg_pct_away DECIMAL(4,3) NOT NULL,
    ft_pct_away DECIMAL(4,3) NOT NULL,
    fg3_pct_away DECIMAL(4,3) NOT NULL,
    ast_away INT NOT NULL,
    reb_away INT NOT NULL,
    home_team_wins INT NOT NULL,
    FOREIGN KEY(game_id) REFERENCES Game(game_id),
    FOREIGN KEY(home_team_id) REFERENCES Team(team_id),
    FOREIGN KEY(visitor_team_id) REFERENCES Team(team_id)
);

CREATE TABLE IF NOT EXISTS Roster (
    team_id INT,
    player_id INT,
    PRIMARY KEY(player_id),
    FOREIGN KEY(player_id) REFERENCES Player(player_id),
    FOREIGN KEY(team_id) REFERENCES Team(team_id)
);

CREATE FUNCTION TF_Team_update() RETURNS TRIGGER AS $$
BEGIN
  -- YOUR IMPLEMENTATION GOES HERE
  IF (TG_OP = 'DELETE') THEN
    IF (OLD.pts_home > OLD.pts_away) THEN
        UPDATE Team SET w = w - 1 WHERE team_id = OLD.home_team_id;
        UPDATE Team SET l = l - 1 WHERE team_id = OLD.visitor_team_id;
    ELSE
        UPDATE Team SET w = w - 1 WHERE team_id = OLD.visitor_team_id;
        UPDATE Team SET l = l - 1 WHERE team_id = OLD.home_team_id;
    END IF;
  ELSIF (TG_OP = 'INSERT') THEN
    IF (NEW.pts_home > NEW.pts_away) THEN
        UPDATE Team SET w = w + 1 WHERE team_id = NEW.home_team_id;
        UPDATE Team SET l = l + 1 WHERE team_id = NEW.visitor_team_id;
    ELSE
        UPDATE Team SET w = w + 1 WHERE team_id = NEW.visitor_team_id;
        UPDATE Team SET l = l + 1 WHERE team_id = NEW.home_team_id;
    END IF;
  ELSIF (TG_OP = 'UPDATE') THEN
    IF (NEW.home_team_wins <> OLD.home_team_wins) THEN
        UPDATE Team SET w = CASE WHEN NEW.home_team_wins = 1 THEN w + 1 ELSE w - 1 END WHERE team_id = NEW.home_team_id;
        UPDATE Team SET l = CASE WHEN NEW.home_team_wins = 1 THEN l - 1 ELSE l + 1 END WHERE team_id = NEW.home_team_id;
        UPDATE Team SET w = CASE WHEN NEW.home_team_wins = 1 THEN w - 1 ELSE w + 1 END WHERE team_id = NEW.visitor_team_id;
        UPDATE Team SET l = CASE WHEN NEW.home_team_wins = 1 THEN l + 1 ELSE l - 1 END WHERE team_id = NEW.visitor_team_id;
    END IF;
  END IF;

  RETURN NULL;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER TG_Team_update
  AFTER INSERT OR DELETE OR UPDATE ON Plays
  FOR EACH ROW
  EXECUTE PROCEDURE TF_Team_update();

CREATE FUNCTION TF_Player_update() RETURNS TRIGGER AS $$
BEGIN
    IF (TG_OP = 'DELETE') THEN
        UPDATE Player SET tot_points = tot_points - OLD.points, tot_rebounds = tot_rebounds - OLD.rebounds, tot_assists = tot_assists - OLD.assists,
        tot_steals = tot_steals - OLD.steals, tot_blocks = tot_blocks - OLD.blocks, tot_turnovers = tot_turnovers - OLD.turnovers, tot_fgm = tot_fgm - OLD.fgm,
        tot_fga = tot_fga - OLD.fga, tot_ftm = tot_ftm - OLD.ftm, tot_fta = tot_fta - OLD.fta, gp = gp - 1 WHERE player_id = OLD.player_id;
    ELSIF (TG_OP = 'INSERT') THEN
        UPDATE Player SET tot_points = tot_points + NEW.points, tot_rebounds = tot_rebounds + NEW.rebounds, tot_assists = tot_assists + NEW.assists,
        tot_steals = tot_steals + NEW.steals, tot_blocks = tot_blocks + NEW.blocks, tot_turnovers = tot_turnovers + NEW.turnovers, tot_fgm = tot_fgm + NEW.fgm,
        tot_fga = tot_fga + NEW.fga, tot_ftm = tot_ftm + NEW.ftm, tot_fta = tot_fta + NEW.fta, gp = gp + 1 WHERE player_id = NEW.player_id;
    ELSIF (TG_OP = 'UPDATE') THEN
        IF (OLD.points <> NEW.points) THEN
            UPDATE Player SET tot_points = tot_points + (NEW.points - OLD.points) WHERE player_id = NEW.player_id;
        END IF;
        IF (OLD.rebounds <> NEW.rebounds) THEN
            UPDATE Player SET tot_rebounds = tot_rebounds + (NEW.rebounds - OLD.rebounds) WHERE player_id = NEW.player_id;
        END IF;
        IF (OLD.assists <> NEW.assists) THEN
            UPDATE Player SET tot_assists = tot_assists + (NEW.assists - OLD.assists) WHERE player_id = NEW.player_id;
        END IF;
        IF (OLD.steals <> NEW.steals) THEN
            UPDATE Player SET tot_steals = tot_steals + (NEW.steals - OLD.steals) WHERE player_id = NEW.player_id;
        END IF;
        IF (OLD.blocks <> NEW.blocks) THEN
            UPDATE Player SET tot_blocks = tot_blocks + (NEW.blocks - OLD.blocks) WHERE player_id = NEW.player_id;
        END IF;
        IF (OLD.turnovers <> NEW.turnovers) THEN
            UPDATE Player SET tot_turnovers = tot_turnovers + (NEW.turnovers - OLD.turnovers) WHERE player_id = NEW.player_id;
        END IF;
        IF (OLD.fgm <> NEW.fgm) THEN
            UPDATE Player SET tot_fgm = tot_fgm + (NEW.fgm - OLD.fgm) WHERE player_id = NEW.player_id;
        END IF;
        IF (OLD.fga <> NEW.fga) THEN
            UPDATE Player SET tot_fga = tot_fga + (NEW.fga - OLD.fga) WHERE player_id = NEW.player_id;
        END IF;
        IF (OLD.ftm <> NEW.ftm) THEN
            UPDATE Player SET tot_ftm = tot_ftm + (NEW.ftm - OLD.ftm) WHERE player_id = NEW.player_id;
        END IF;
        IF (OLD.fta <> NEW.fta) THEN
            UPDATE Player SET tot_fta = tot_fta + (NEW.fta - OLD.fta) WHERE player_id = NEW.player_id;
        END IF;
    END IF;
    RETURN NULL;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER TG_Player_update
    AFTER INSERT OR DELETE ON Performance
    FOR EACH ROW
    EXECUTE PROCEDURE TF_Player_update();

CREATE FUNCTION TF_Player_col_update() RETURNS TRIGGER AS $$
BEGIN
    NEW.avg_points := CASE WHEN NEW.gp=0 THEN 0 ELSE NEW.tot_points::DECIMAL / NEW.gp END;
    NEW.avg_rebounds := CASE WHEN NEW.gp=0 THEN 0 ELSE NEW.tot_rebounds::DECIMAL / NEW.gp END;
    NEW.avg_assists := CASE WHEN NEW.gp=0 THEN 0 ELSE NEW.tot_assists::DECIMAL / NEW.gp END;
    NEW.avg_steals := CASE WHEN NEW.gp=0 THEN 0 ELSE NEW.tot_steals::DECIMAL / NEW.gp END;
    NEW.avg_blocks := CASE WHEN NEW.gp=0 THEN 0 ELSE NEW.tot_blocks::DECIMAL / NEW.gp END;
    NEW.avg_turnovers := CASE WHEN NEW.gp=0 THEN 0 ELSE NEW.tot_turnovers::DECIMAL / NEW.gp END;
    NEW.avg_fgm := CASE WHEN NEW.gp=0 THEN 0 ELSE NEW.tot_fgm::DECIMAL / NEW.gp END;
    NEW.avg_fga := CASE WHEN NEW.gp=0 THEN 0 ELSE NEW.tot_fga::DECIMAL / NEW.gp END;
    NEW.avg_ftm := CASE WHEN NEW.gp=0 THEN 0 ELSE NEW.tot_ftm::DECIMAL / NEW.gp END;
    NEW.avg_fta := CASE WHEN NEW.gp=0 THEN 0 ELSE NEW.tot_fta::DECIMAL / NEW.gp END;
    NEW.eff := NEW.avg_points + NEW.avg_rebounds + NEW.avg_assists + NEW.avg_steals + NEW.avg_blocks - NEW.avg_turnovers - (NEW.avg_fga - NEW.avg_fgm) - (NEW.avg_fta - NEW.avg_ftm);
    RETURN NEW; 
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER TG_Player_col_update
    BEFORE INSERT OR UPDATE ON Player
    FOR EACH ROW
    EXECUTE PROCEDURE TF_Player_col_update();

CREATE FUNCTION TF_Team_col_update() RETURNS TRIGGER AS $$
BEGIN
    NEW.w_pct := CASE WHEN (NEW.w + NEW.l) = 0 THEN NULL ELSE NEW.w::DECIMAL / (NEW.w + NEW.l) END;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER TG_Team_col_update
    BEFORE INSERT OR UPDATE ON Team
    FOR EACH ROW
    EXECUTE PROCEDURE TF_Team_col_update();

CREATE FUNCTION TF_Performance_col_update() RETURNS TRIGGER AS $$
BEGIN
    NEW.fg_pct := CASE WHEN NEW.fga = 0 THEN NULL ELSE NEW.fgm::DECIMAL / NEW.fga END;
    NEW.fg3_pct := CASE WHEN NEW.fg3a = 0 THEN NULL ELSE NEW.fg3m::DECIMAL / NEW.fg3a END;
    NEW.ft_pct := CASE WHEN NEW.fta = 0 THEN NULL ELSE NEW.ftm::DECIMAL / NEW.fta END;
    NEW.rebounds := NEW.offensive_rebounds + NEW.defensive_rebounds;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER TG_Performance_col_update
    BEFORE INSERT OR UPDATE ON Performance
    FOR EACH ROW
    EXECUTE PROCEDURE TF_Performance_col_update();

CREATE FUNCTION TF_Plays_col_update() RETURNS TRIGGER AS $$
BEGIN
    IF NEW.pts_home > NEW.pts_away THEN
        NEW.home_team_wins := 1;
    ELSE
        NEW.home_team_wins := 0;
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER TG_Plays_col_update
    BEFORE INSERT OR UPDATE ON Plays
    FOR EACH ROW
    EXECUTE PROCEDURE TF_Plays_col_update();

CREATE VIEW PlayerRoster AS
    SELECT *
    FROM Player NATURAL JOIN Roster;

CREATE VIEW GameView AS
    SELECT G.game_id, G.game_date_est game_date_est, G.game_time game_time, G.game_status_text game_status_text, T1.city home_team_city, T1.nickname home_team_nickname, T2.city visitor_team_city, T2.nickname visitor_team_nickname
    FROM Game G, Plays P, Team T1, Team T2
    WHERE G.game_id = P.game_id AND P.home_team_id = T1.team_id AND P.visitor_team_id = T2.team_id