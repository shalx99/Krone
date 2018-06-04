CREATE TABLE IF NOT EXISTS games (
    id INTEGER PRIMARY KEY,
    div VARCHAR(10) NOT NULL,
    date DATE NOT NULL,
    home_team VARCHAR(30) NOT NULL,
    away_team VARCHAR(30) NOT NULL,
    home_team_goals INTEGER NOT NULL,
    away_team_goals INTEGER NOT NULL,
    full_time_result VARCHAR(1) NOT NULL,
    ht_shots INTEGER,
    at_shots INTEGER,
    ht_shots_target INTEGER,
    at_shots_target INTEGER
);

CREATE TABLE IF NOT EXISTS teams (
    id INTEGER PRIMARY KEY,
    name VARCHAR(30) NOT NULL,
    full_name VARCHAR(70),
    short_name VARCHAR(3)
);
