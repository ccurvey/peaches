/* unlogged table to bulk load data */
drop table if exists raw_data;

create unlogged table raw_data
( id serial
, rank integer
, team_name varchar(100)
, team_id integer
, abbrev varchar(10)
, game_date date
, opponent_name varchar(100)
, opponent_id integer
, "location" varchar(1)
, straight_up_result varchar(1)
, points_for integer
, points_against integer
, field_goal_pct float
, free_throw_pct float
, three_point_pct float
, effective_field_goal_pct float
, ppws float
, turnover_ratio float
, blocks integer
, fouls integer
, offensive_rebounds integer
, total_rebounds integer
, steals integer
, assists integer
, posessions integer
, offensive_points_per_posession float
, defensive_points_per_posession float

);

copy raw_data 
( rank 
, team_name 
, team_id 
, abbrev 
, game_date 
, opponent_name 
, opponent_id 
, "location"
, straight_up_result 
, points_for 
, points_against 
, field_goal_pct 
, free_throw_pct 
, three_point_pct 
, effective_field_goal_pct 
, ppws 
, turnover_ratio 
, blocks 
, fouls 
, offensive_rebounds 
, total_rebounds 
, steals 
, assists 
, posessions 
, offensive_points_per_posession 
, defensive_points_per_posession 
) from '/tmp/Team Performances - 1997.csv' with (format csv, header);

copy raw_data 
( rank 
, team_name 
, team_id 
, abbrev 
, game_date 
, opponent_name 
, opponent_id 
, "location"
, straight_up_result 
, points_for 
, points_against 
, field_goal_pct 
, free_throw_pct 
, three_point_pct 
, effective_field_goal_pct 
, ppws 
, turnover_ratio 
, blocks 
, fouls 
, offensive_rebounds 
, total_rebounds 
, steals 
, assists 
, posessions 
, offensive_points_per_posession 
, defensive_points_per_posession 
) from '/tmp/Team Performances - 1998.csv' with (format csv, header);

copy raw_data 
( rank 
, team_name 
, team_id 
, abbrev 
, game_date 
, opponent_name 
, opponent_id 
, "location"
, straight_up_result 
, points_for 
, points_against 
, field_goal_pct 
, free_throw_pct 
, three_point_pct 
, effective_field_goal_pct 
, ppws 
, turnover_ratio 
, blocks 
, fouls 
, offensive_rebounds 
, total_rebounds 
, steals 
, assists 
, posessions 
, offensive_points_per_posession 
, defensive_points_per_posession 
) from '/tmp/Team Performances - 1999.csv' with (format csv, header);

copy raw_data 
( rank 
, team_name 
, team_id 
, abbrev 
, game_date 
, opponent_name 
, opponent_id 
, "location"
, straight_up_result 
, points_for 
, points_against 
, field_goal_pct 
, free_throw_pct 
, three_point_pct 
, effective_field_goal_pct 
, ppws 
, turnover_ratio 
, blocks 
, fouls 
, offensive_rebounds 
, total_rebounds 
, steals 
, assists 
, posessions 
, offensive_points_per_posession 
, defensive_points_per_posession 
) from '/tmp/Team Performances - 2000.csv' with (format csv, header);

copy raw_data 
( rank 
, team_name 
, team_id 
, abbrev 
, game_date 
, opponent_name 
, opponent_id 
, "location"
, straight_up_result 
, points_for 
, points_against 
, field_goal_pct 
, free_throw_pct 
, three_point_pct 
, effective_field_goal_pct 
, ppws 
, turnover_ratio 
, blocks 
, fouls 
, offensive_rebounds 
, total_rebounds 
, steals 
, assists 
, posessions 
, offensive_points_per_posession 
, defensive_points_per_posession 
) from '/tmp/Team Performances - 2001.csv' with (format csv, header);

copy raw_data 
( rank 
, team_name 
, team_id 
, abbrev 
, game_date 
, opponent_name 
, opponent_id 
, "location"
, straight_up_result 
, points_for 
, points_against 
, field_goal_pct 
, free_throw_pct 
, three_point_pct 
, effective_field_goal_pct 
, ppws 
, turnover_ratio 
, blocks 
, fouls 
, offensive_rebounds 
, total_rebounds 
, steals 
, assists 
, posessions 
, offensive_points_per_posession 
, defensive_points_per_posession 
) from '/tmp/Team Performances - 2002.csv' with (format csv, header);

copy raw_data 
( rank 
, team_name 
, team_id 
, abbrev 
, game_date 
, opponent_name 
, opponent_id 
, "location"
, straight_up_result 
, points_for 
, points_against 
, field_goal_pct 
, free_throw_pct 
, three_point_pct 
, effective_field_goal_pct 
, ppws 
, turnover_ratio 
, blocks 
, fouls 
, offensive_rebounds 
, total_rebounds 
, steals 
, assists 
, posessions 
, offensive_points_per_posession 
, defensive_points_per_posession 
) from '/tmp/Team Performances - 2003.csv' with (format csv, header);

copy raw_data 
( rank 
, team_name 
, team_id 
, abbrev 
, game_date 
, opponent_name 
, opponent_id 
, "location"
, straight_up_result 
, points_for 
, points_against 
, field_goal_pct 
, free_throw_pct 
, three_point_pct 
, effective_field_goal_pct 
, ppws 
, turnover_ratio 
, blocks 
, fouls 
, offensive_rebounds 
, total_rebounds 
, steals 
, assists 
, posessions 
, offensive_points_per_posession 
, defensive_points_per_posession 
) from '/tmp/Team Performances - 2004.csv' with (format csv, header);

copy raw_data 
( rank 
, team_name 
, team_id 
, abbrev 
, game_date 
, opponent_name 
, opponent_id 
, "location"
, straight_up_result 
, points_for 
, points_against 
, field_goal_pct 
, free_throw_pct 
, three_point_pct 
, effective_field_goal_pct 
, ppws 
, turnover_ratio 
, blocks 
, fouls 
, offensive_rebounds 
, total_rebounds 
, steals 
, assists 
, posessions 
, offensive_points_per_posession 
, defensive_points_per_posession 
) from '/tmp/Team Performances - 2005.csv' with (format csv, header);

copy raw_data 
( rank 
, team_name 
, team_id 
, abbrev 
, game_date 
, opponent_name 
, opponent_id 
, "location"
, straight_up_result 
, points_for 
, points_against 
, field_goal_pct 
, free_throw_pct 
, three_point_pct 
, effective_field_goal_pct 
, ppws 
, turnover_ratio 
, blocks 
, fouls 
, offensive_rebounds 
, total_rebounds 
, steals 
, assists 
, posessions 
, offensive_points_per_posession 
, defensive_points_per_posession 
) from '/tmp/Team Performances - 2006.csv' with (format csv, header);

copy raw_data 
( rank 
, team_name 
, team_id 
, abbrev 
, game_date 
, opponent_name 
, opponent_id 
, "location"
, straight_up_result 
, points_for 
, points_against 
, field_goal_pct 
, free_throw_pct 
, three_point_pct 
, effective_field_goal_pct 
, ppws 
, turnover_ratio 
, blocks 
, fouls 
, offensive_rebounds 
, total_rebounds 
, steals 
, assists 
, posessions 
, offensive_points_per_posession 
, defensive_points_per_posession 
) from '/tmp/Team Performances - 2007.csv' with (format csv, header);

copy raw_data 
( rank 
, team_name 
, team_id 
, abbrev 
, game_date 
, opponent_name 
, opponent_id 
, "location"
, straight_up_result 
, points_for 
, points_against 
, field_goal_pct 
, free_throw_pct 
, three_point_pct 
, effective_field_goal_pct 
, ppws 
, turnover_ratio 
, blocks 
, fouls 
, offensive_rebounds 
, total_rebounds 
, steals 
, assists 
, posessions 
, offensive_points_per_posession 
, defensive_points_per_posession 
) from '/tmp/Team Performances - 2008.csv' with (format csv, header);

copy raw_data 
( rank 
, team_name 
, team_id 
, abbrev 
, game_date 
, opponent_name 
, opponent_id 
, "location"
, straight_up_result 
, points_for 
, points_against 
, field_goal_pct 
, free_throw_pct 
, three_point_pct 
, effective_field_goal_pct 
, ppws 
, turnover_ratio 
, blocks 
, fouls 
, offensive_rebounds 
, total_rebounds 
, steals 
, assists 
, posessions 
, offensive_points_per_posession 
, defensive_points_per_posession 
) from '/tmp/Team Performances - 2009.csv' with (format csv, header);

copy raw_data 
( rank 
, team_name 
, team_id 
, abbrev 
, game_date 
, opponent_name 
, opponent_id 
, "location"
, straight_up_result 
, points_for 
, points_against 
, field_goal_pct 
, free_throw_pct 
, three_point_pct 
, effective_field_goal_pct 
, ppws 
, turnover_ratio 
, blocks 
, fouls 
, offensive_rebounds 
, total_rebounds 
, steals 
, assists 
, posessions 
, offensive_points_per_posession 
, defensive_points_per_posession 
) from '/tmp/Team Performances - 2010.csv' with (format csv, header);

copy raw_data 
( rank 
, team_name 
, team_id 
, abbrev 
, game_date 
, opponent_name 
, opponent_id 
, "location"
, straight_up_result 
, points_for 
, points_against 
, field_goal_pct 
, free_throw_pct 
, three_point_pct 
, effective_field_goal_pct 
, ppws 
, turnover_ratio 
, blocks 
, fouls 
, offensive_rebounds 
, total_rebounds 
, steals 
, assists 
, posessions 
, offensive_points_per_posession 
, defensive_points_per_posession 
) from '/tmp/Team Performances - 2011.csv' with (format csv, header);



copy raw_data 
( rank 
, team_name 
, team_id 
, abbrev 
, game_date 
, opponent_name 
, opponent_id 
, "location"
, straight_up_result 
, points_for 
, points_against 
, field_goal_pct 
, free_throw_pct 
, three_point_pct 
, effective_field_goal_pct 
, ppws 
, turnover_ratio 
, blocks 
, fouls 
, offensive_rebounds 
, total_rebounds 
, steals 
, assists 
, posessions 
, offensive_points_per_posession 
, defensive_points_per_posession 
) from '/tmp/Team Performances - 2012.csv' with (format csv, header);


copy raw_data 
( rank 
, team_name 
, team_id 
, abbrev 
, game_date 
, opponent_name 
, opponent_id 
, "location"
, straight_up_result 
, points_for 
, points_against 
, field_goal_pct 
, free_throw_pct 
, three_point_pct 
, effective_field_goal_pct 
, ppws 
, turnover_ratio 
, blocks 
, fouls 
, offensive_rebounds 
, total_rebounds 
, steals 
, assists 
, posessions 
, offensive_points_per_posession 
, defensive_points_per_posession 
) from '/tmp/Team Performances - 2013.csv' with (format csv, header);

/*************************************************************
--2014 added new fields, so we will skip that for now.
copy raw_data 
( rank 
, team_name 
, team_id 
, abbrev 
, game_date 
, opponent_name 
, opponent_id 
, "location"
, straight_up_result 
, points_for 
, points_against 
, field_goal_pct 
, free_throw_pct 
, three_point_pct 
, effective_field_goal_pct 
, ppws 
, turnover_ratio 
, blocks 
, fouls 
, offensive_rebounds 
, total_rebounds 
, steals 
, assists 
, posessions 
, offensive_points_per_posession 
, defensive_points_per_posession 
) from '/tmp/Team Performances - 2014.csv' with (format csv, header);
*************************************************************/

/********************************************************
** make some fixups to the data
*********************************************************/
begin;
update raw_data
set team_name = 'Cleveland State'
where abbrev = 'CLST'
and team_name = 'Cleveland';

update raw_data
set opponent_name = 'Cleveland State'
where opponent_name = 'Cleveland';

update raw_data
set team_name = 'Florida International'
where abbrev = 'FAU'
and team_name = 'Florida Atlantic';

update raw_data
set opponent_name = 'Florida International'
where opponent_name = 'Florida Atlantic';

update raw_data
set team_name = 'La Salle'
where abbrev = 'LAS'
and team_name = 'LaSalle';

update raw_data
set opponent_name = 'La Salle'
where opponent_name = 'LaSalle';

update raw_data
set team_name = 'Middle Tennessee State'
where abbrev = 'MTSU'
and team_name = 'Middle Tennessee';

update raw_data
set opponent_name = 'Middle Tennessee State'
where opponent_name = 'Middle Tennessee';

update raw_data
set team_name = 'San Diego State'
where abbrev = 'SDSU'
and team_name = 'Saint Mary''s';

update raw_data
set team_name = 'Saint Joseph''s'
where abbrev = 'SJU'
and team_name = 'St. Joseph''s';

update raw_data
set opponent_name = 'Saint Joseph''s'
where opponent_name = 'St. Joseph''s';

update raw_data
set team_name = 'Saint Mary''s'
where abbrev = 'SMC'
and team_name = 'San Diego State';

update raw_data
set team_name = 'Saint John''s (NY)'
where abbrev = 'STJ'
and team_name = 'Saint John''s';

update raw_data
set opponent_name = 'Saint John''s (NY)'
where opponent_name = 'Saint John''s';

commit;

/*******************************************************
** create years, schools and teams.  (Assumes that the django
** tables have been created via migration.)
*******************************************************/
insert into games_school(abbrev, "name")
select distinct abbrev, team_name
from raw_data;

insert into games_schoolalias (school_id, "alias")
select distinct abbrev, team_name
from raw_data;


insert into games_season("year", start_date, end_date) values (1997, '11/1/1996','4/30/1997');
insert into games_season("year", start_date, end_date) values (1998, '11/1/1997','4/30/1998');
insert into games_season("year", start_date, end_date) values (1999, '11/1/1998','4/30/1999');
insert into games_season("year", start_date, end_date) values (2000, '11/1/1999','4/30/2000');
insert into games_season("year", start_date, end_date) values (2001, '11/1/2000','4/30/2001');
insert into games_season("year", start_date, end_date) values (2002, '11/1/2001','4/30/2002');
insert into games_season("year", start_date, end_date) values (2003, '11/1/2002','4/30/2003');
insert into games_season("year", start_date, end_date) values (2004, '11/1/2003','4/30/2004');
insert into games_season("year", start_date, end_date) values (2005, '11/1/2004','4/30/2005');
insert into games_season("year", start_date, end_date) values (2006, '11/1/2005','4/30/2006');
insert into games_season("year", start_date, end_date) values (2007, '11/1/2006','4/30/2007');
insert into games_season("year", start_date, end_date) values (2008, '11/1/2007','4/30/2008');
insert into games_season("year", start_date, end_date) values (2009, '11/1/2008','4/30/2009');
insert into games_season("year", start_date, end_date) values (2010, '11/1/2009','4/30/2010');
insert into games_season("year", start_date, end_date) values (2011, '11/1/2010','4/30/2011');
insert into games_season("year", start_date, end_date) values (2012, '11/1/2011','4/30/2012');
insert into games_season("year", start_date, end_date) values (2013, '11/1/2012','4/30/2013');
insert into games_season("year", start_date, end_date) values (2014, '11/1/2013','4/30/2014');
insert into games_season("year", start_date, end_date) values (2015, '11/1/2014','4/30/2015');

-- note lack of join clause.  We want all combinations.  (When adding a year in the future, we 
-- would copy all teams for a single year.
insert into games_team(school_id, season_id)
select games_school.abbrev, games_season."year"
from games_school
, games_season;

/****************************************************************************************
** create our game records.  This takes a few minutes (but only a few)
*****************************************************************************************/
delete from games_game;

insert into games_game
( assists
, blocks
, defensive_points_per_posession
, field_goal_pct
, fouls
, free_throw_pct
, game_date
, location
, offensive_points_per_posession
, offensive_rebounds
, opponent_id
, points_against
, points_for
, posessions
, ppws
, result
, steals
, team_id
, three_point_pct
, to_r
, total_rebounds
, turnover_ratio
, season_id)
select r.assists
, r.blocks
, r.defensive_points_per_posession
, r.field_goal_pct
, r.fouls
, r.free_throw_pct
, r.game_date
, r.location
, r.offensive_points_per_posession
, r.offensive_rebounds
, ot.id
, r.points_against
, r.points_for
, r.posessions
, r.ppws
, r.straight_up_result
, r.steals
, t.id
, r.three_point_pct
, r.turnover_ratio
, r.total_rebounds
, r.turnover_ratio
, s.year
from raw_data r
join games_season s on r.game_date between s.start_date and s.end_date
join games_school os on r.opponent_name = os.name
join games_team ot on os.abbrev = ot.school_id
                  and s.year = ot.season_id
join games_team t on r.abbrev = t.school_id
                 and s.year = t.season_id;


