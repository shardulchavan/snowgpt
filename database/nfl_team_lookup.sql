USE ROLE TEAM2_ROLE;
USE WAREHOUSE TEAM2_DW;
USE DATABASE TEAM2_DB;
USE SCHEMA NFL_SPONSOR;



CREATE TABLE TEAM_STATE_LOOKUP (
    TEAM_NAME VARCHAR(255),
    STATE_CODE CHAR(2)
);

INSERT INTO TEAM_STATE_LOOKUP (TEAM_NAME, STATE_CODE) VALUES
('Arizona Cardinals', 'AZ'),
('Atlanta Falcons', 'GA'),
('Baltimore Ravens', 'MD'),
('Buffalo Bills', 'NY'),
('Carolina Panthers', 'NC'),
('Chicago Bears', 'IL'),
('Cincinnati Bengals', 'OH'),
('Cleveland Browns', 'OH'),
('Dallas Cowboys', 'TX'),
('Denver Broncos', 'CO'),
('Detroit Lions', 'MI'),
('Green Bay Packers', 'WI'),
('Houston Texans', 'TX'),
('Indianapolis Colts', 'IN'),
('Jacksonville Jaguars', 'FL'),
('Kansas City Chiefs', 'MO'),
('Las Vegas Raiders', 'NV'),
('Los Angeles Chargers', 'CA'),
('Los Angeles Rams', 'CA'),
('Miami Dolphins', 'FL'),
('Minnesota Vikings', 'MN'),
('New England Patriots', 'MA'),
('New Orleans Saints', 'LA'),
('New York Giants', 'NY'),
('New York Jets', 'NY'),
('Philadelphia Eagles', 'PA'),
('Pittsburgh Steelers', 'PA'),
('San Francisco 49ers', 'CA'),
('Seattle Seahawks', 'WA'),
('Tampa Bay Buccaneers', 'FL'),
('Tennessee Titans', 'TN'),
('Washington Commanders', 'DC');

