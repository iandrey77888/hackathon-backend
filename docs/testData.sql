set search_path = "$user", hack, public, public, topology, tiger;


insert into users(name, surname, role, username, pwdhash) values ('Петр', 'ССК', 1, 'admin', '$argon2i$v=19$m=512,t=2,p=2$aI2R0hpDyLm3ltLa+1/rvQ$LqPKjd6n8yniKtAithoR7A'); --password

insert into users(name, surname, role, username, pwdhash) values ('Иван', 'Прораб', 2, 'prorab', '$argon2i$v=19$m=16,t=2,p=1$WnFDck9BR0dYczlTejRvUw$SBXWdFYHiZSi2k1tVXokcg'); --prorab

insert into users(name, surname, role, username, pwdhash) values ('Василий', 'Госконтроль', 3, 'goscont', '$argon2i$v=19$m=16,t=2,p=1$WnFDck9BR0dYczlTejRvUw$wiI0YiTgvr25wp/L8T1zHw'); --goscont


insert into buildsite(sitename, coordinates, state, start_date, state_changed, manager, acceptor) select 'Флотская улица д. 54, д. 58к1', 
ST_GeomFromText('POLYGON ((37.5051017825647 55.8553877117224,37.5051681643041 55.8554111603478,37.5051839094663 55.8554171325542,37.5052104335301 55.8554272089655,37.5052348657006 55.8554364771022,37.505320665691 55.8554678736638,37.5053349417489 55.8554730914498,37.5055836076713 55.8555640746525,37.5055906010443 55.8555588560566,37.505591798714 55.8555593589798,37.5055985685554 55.8555543290062,37.5056303420759 55.8555306881272,37.5056370959415 55.8555256761153,37.5056600878064 55.8555085741961,37.5058007368723 55.8554036901291,37.5058058141532 55.8553994595778,37.5058264745316 55.8553823038336,37.5058565869194 55.8553572887768,37.5058941076043 55.8553261299751,37.5058990252053 55.8553220521141,37.506030315168 55.8552130096855,37.5061498259443 55.8551460554965,37.5061511670796 55.8551448339374,37.506213593672 55.855088202068,37.5063288189548 55.854983677786,37.5063448758986 55.8549371163449,37.5063579817703 55.8549113834093,37.506359386544 55.8549086529331,37.5063875457515 55.854853387743,37.5064135018962 55.8548020296519,37.5064183859271 55.8547875959652,37.5064683524653 55.8547021694697,37.5065189053775 55.8546957632065,37.506580507928 55.8546892396364,37.5066376875542 55.8546837581157,37.5066423660015 55.8546831112143,37.5066383562679 55.8546710401115,37.5064796084454 55.8546935286268,37.5064325378433 55.8547091229083,37.5064179459915 55.8547273562699,37.5064100429371 55.8547340838674,37.5063297798037 55.8547810703949,37.5063243988607 55.8547824358458,37.5062826123076 55.8547902068395,37.5062372486311 55.8547956876666,37.5060473782174 55.8548135424986,37.5060432735312 55.8548064741422,37.5059342937921 55.8548093080122,37.5059339105652 55.8548093080284,37.5059109169851 55.8548095245581,37.5058878899331 55.8547981547971,37.505860247908 55.8547845128748,37.5058420594336 55.8547755320137,37.5057650795589 55.8547812924072,37.5057538507148 55.8547541863417,37.5058338162198 55.8547462253348,37.5058292635512 55.8547320525295,37.5057479887717 55.8547404267413,37.5057112177327 55.8546368162834,37.5057012819385 55.8546064767773,37.5056961065692 55.8545921063964,37.5056253289212 55.8543950704779,37.5055467255931 55.8541794159221,37.505489030816 55.8540153060165,37.5051482574417 55.8540516224398,37.5049518915995 55.8540713889022,37.50493031976 55.8540735003217,37.5048811563929 55.8540782891946,37.504806109984 55.8540856117255,37.5047633974045 55.8540899422747,37.5044715464808 55.8541194830682,37.5041845491402 55.8541479182939,37.5039963738342 55.854169739792,37.5042904885571 55.8542673887718,37.5042507956255 55.8542942000486,37.5042623250932 55.854303890885,37.5042603451821 55.8543046453979,37.5042583493026 55.8543053909296,37.5043077727617 55.8543467768023,37.5043795497049 55.8543745548403,37.5045682772128 55.8544391628604,37.5044653106823 55.8545300689974,37.5041535800796 55.8544192179514,37.504152446466 55.8544202149427,37.5041510733578 55.8544214364811,37.5038739306543 55.8543150116956,37.5038236198945 55.8543538405119,37.5036672768572 55.8542970176433,37.5035196528681 55.8542445055551,37.5034712540028 55.8542272888801,37.5033165609946 55.8542358786618,37.5032786703044 55.8542405049875,37.5030198056521 55.8542622545852,37.502940878725 55.8542749201142,37.5029137636715 55.8542370451108,37.5029119751658 55.8542345482524,37.5028374215273 55.8542132451531,37.502808743388 55.8542050544049,37.5027640655535 55.8541922922719,37.502751150608 55.8542458768261,37.5027440306133 55.8542754713786,37.5027366392151 55.8543061527109,37.5027365434356 55.8543066556831,37.5027364636177 55.854307041894,37.502734196765 55.8543175773704,37.5027276194836 55.8543440822357,37.50271976478 55.8543704883235,37.5027106645848 55.8543967597065,37.5027090201318 55.854400909241,37.5027003029272 55.8544228784214,37.5026887117396 55.8544488354858,37.5026848639274 55.8544565507578,37.5026775834177 55.8544711909124,37.5026760985747 55.8544741458886,37.5026757792442 55.8544745949746,37.5026709413739 55.8544811336697,37.5026634528422 55.8544870796196,37.5026556129441 55.8544914986993,37.5026501042186 55.8544938250249,37.5026842118273 55.8545077100697,37.5027103354612 55.8545183349064,37.5027379441341 55.8545295704634,37.5028183429631 55.8545596036561,37.5030274922754 55.8546377310241,37.5032039556747 55.8547036526784,37.5032325065681 55.8547125528843,37.5032922593521 55.8547350775522,37.5033664633997 55.8547630447426,37.5036496114848 55.8548652581415,37.5037187697584 55.8548873961684,37.5037442366558 55.8548645732541,37.5038282297133 55.8548946236606,37.5038027628454 55.8549174465921,37.5041521987275 55.855052610714,37.5041678623299 55.8550425239198,37.5041952481398 55.8550525825631,37.5041965256129 55.8550530585529,37.5043572479836 55.8551133026096,37.504409592615 55.8551326115327,37.5044472942292 55.8551468732079,37.5046593084372 55.8552270724625,37.5047118289886 55.8552460848578,37.5047633276029 55.8552647290177,37.5049000985814 55.8553142490953,37.5051017825647 55.8553877117224))',
4326),
-1,
now(),
now(),
foo1.id,
foo2.id from (select id from users where username = 'admin') foo1, (select id from users where username = 'goscont') foo2;

insert into user2site(userid, siteid) select foo1.id, foo2.id from (select id from users where username = 'prorab') foo1, (select id from buildsite where sitename = 'Флотская улица д. 54, д. 58к1') foo2;

insert into buildsite(sitename, coordinates, state, start_date, state_changed, manager, acceptor) select 'Гостинный двор', 
ST_GeomFromText('MULTIPOLYGON(
((58.979856 53.379178, 58.979856 53.37826, 58.98006 53.378145, 58.982661 53.378186, 58.982924 53.378301, 58.983096 53.378605, 58.983091 53.378877, 58.98294 53.379172, 58.982704 53.379297, 58.980086 53.379281, 58.979856 53.379178)), 
 ((58.978751 53.379469, 58.978708 53.377895, 58.97933 53.377901, 58.979244 53.379482, 58.978751 53.379469)), 
 ((58.983933 53.377997, 58.984523 53.377997, 58.984523 53.379553, 58.983933 53.379553, 58.983933 53.377997), (58.984373 53.37938, 58.98404 53.379393, 58.984072 53.378151, 58.984362 53.378132, 58.984373 53.37938)))',
4326),
0,
now() + interval '1 day',
null,
foo1.id,
foo2.id from (select id from users where username = 'admin') foo1, (select id from users where username = 'goscont') foo2;

insert into user2site(userid, siteid) select foo1.id, foo2.id from (select id from users where username = 'prorab') foo1, (select id from buildsite where sitename = 'Гостинный двор') foo2;

insert into sitestage (site, seq, name, done) select foo1.id, 1, 'Замена бортового камня', false from (select id from buildsite where sitename = 'Флотская улица д. 54, д. 58к1') foo1;
insert into sitestage (site, seq, name, done) select foo1.id, 2, 'Ремонт АБП', false from (select id from buildsite where sitename = 'Флотская улица д. 54, д. 58к1') foo1;
insert into sitestage (site, seq, name, done) select foo1.id, 3, 'Ремонт газона', false from (select id from buildsite where sitename = 'Флотская улица д. 54, д. 58к1') foo1;

insert into sitestage (site, seq, name, done) select foo1.id, 4, 'После работы чисто читмил', false from (select id from buildsite where sitename = 'Гостинный двор') foo1;
insert into sitestage (site, seq, name, done) select foo1.id, 5, 'И жижкой заправиться', false from (select id from buildsite where sitename = 'Гостинный двор') foo1;





select * from buildsite;
update buildsite set coordinates = ST_GeomFromText('MULTIPOLYGON(
((58.979856 53.379178, 58.979856 53.37826, 58.98006 53.378145, 58.982661 53.378186, 58.982924 53.378301, 58.983096 53.378605, 58.983091 53.378877, 58.98294 53.379172, 58.982704 53.379297, 58.980086 53.379281, 58.979856 53.379178)), 
 ((58.978751 53.379469, 58.978708 53.377895, 58.97933 53.377901, 58.979244 53.379482, 58.978751 53.379469)), 
 ((58.983933 53.377997, 58.984523 53.377997, 58.984523 53.379553, 58.983933 53.379553, 58.983933 53.377997), (58.984373 53.37938, 58.98404 53.379393, 58.984072 53.378151, 58.984362 53.378132, 58.984373 53.37938)))',
4326) where id = 3;

with source_one as (
	insert into jobschedule(version, prev, planned_start, planned_end) select 1, null, to_timestamp('26.09.2025', 'DD-MM-YYYY'), to_timestamp('29.09.2025', 'DD-MM-YYYY') returning id
),
source_side as (
	insert into jobshift(affected_jobsch, creator, state, description, created_at, state_change, checker, newstart, newend, checker_comment)
	select source_one.id, foo1.id, 1, 'test shift', to_timestamp('25.09.2025', 'DD-MM-YYYY'), to_timestamp('26.09.2025', 'DD-MM-YYYY'), foo2.id, to_timestamp('01.10.2025', 'DD-MM-YYYY'), to_timestamp('15.10.2025', 'DD-MM-YYYY'), 'yep check' from source_one, (select id from users where username = 'prorab') foo1, (select id from users where username = 'admin') foo2
),
source_two as (
insert into jobschedule(version, prev, planned_start, planned_end) 
select 2, id, to_timestamp('01.10.2025', 'DD-MM-YYYY'), to_timestamp('15.10.2025', 'DD-MM-YYYY') from source_one returning id),
source_thr as (
insert into sitejob(name, description, scheduled, volume, measurement, status) 
select 'Ремонт газона в рамках благоустройства территории', 'описание газона', source_two.id,  356 v, 'Квадратный метр' m, 0 s from source_two
returning id)
insert into job2stage(stageid, jobid, seq) select nid1.id, source_thr.id, 1 from (select id from sitestage where name = 'Ремонт газона') nid1, source_thr;

select * from files;
select * from comments;
select * from comment2file cf ;


 with 
source_dates as (
insert into jobschedule(version, prev, planned_start, planned_end) 
select 1, null::bigint, to_timestamp('26.09.2025', 'DD-MM-YYYY'), to_timestamp('26.10.2025', 'DD-MM-YYYY')
union all
select 1, null::bigint, to_timestamp('26.10.2025', 'DD-MM-YYYY'), to_timestamp('30.10.2025', 'DD-MM-YYYY')
returning id
), source_thr as (
insert into sitejob(name, description, scheduled, volume, measurement, status) 
select n, d, f2.id, v, m, s from (
select 'Замена дорожного бортового камня в рамках благоустройства территории' n, 'описание замены' d, 250 v, 'погонный метр' m, 1 s, 1 conn
union all
select 'Замена садового бортового камня в рамках благоустройства территории' n, 'описание замены' d, 410 v, 'погонный метр' m, 0 s, 2 conn) foo left join (select id, row_number() OVER (order by id) as rn from source_dates) f2 on foo.conn = f2.rn
returning id)
insert into job2stage(stageid, jobid, seq) select nid1.id, source_thr.id, row_number() OVER (order by source_thr) from (select id from sitestage where name = 'Замена бортового камня') nid1, source_thr;

select * from job2stage;


 with 
source_two as (
insert into jobschedule(version, prev, planned_start, planned_end) 
select 1, null::bigint, to_timestamp('26.09.2025', 'DD-MM-YYYY'), to_timestamp('06.10.2025', 'DD-MM-YYYY')
union all
select 1, null::bigint, to_timestamp('06.10.2025', 'DD-MM-YYYY'), to_timestamp('26.10.2025', 'DD-MM-YYYY')
union all
select 1, null::bigint, to_timestamp('26.10.2025', 'DD-MM-YYYY'), to_timestamp('22.11.2025', 'DD-MM-YYYY')
returning id
),
pending_sh as (
	insert into jobshift(affected_jobsch, creator, state, description, created_at, state_change, checker, newstart, newend, checker_comment)
	select s.id, foo1.id, 0, 'test pending shift', to_timestamp('26.09.2025', 'DD-MM-YYYY'), null, null, to_timestamp('30.09.2025', 'DD-MM-YYYY'), to_timestamp('06.10.2025', 'DD-MM-YYYY'), null from (select id from source_two limit 1) s, (select id from users where username = 'prorab') foo1

), source_thr as (
insert into sitejob(name, description, scheduled, volume, measurement, status) 
select n, d, f2.id, v, m, s from (
select 'Ремонт покрытия асфальтобетонного проезда в рамках благоустройства территории' n, 'описание проезда' d, 150 v, 'Квадратный метр' m, 0 s, 1 conn
union all
select 'Ремонт покрытия асфальтобетонного тротуара в рамках благоустройства территории' n, 'описание тротуара' d, 260 v, 'Квадратный метр' m, 0 s, 2 conn
union all
select 'Ремонт покрытия асфальтобетонного пешеходной дорожки в рамках благоустройства территории' n, 'описание дорожки' d, 320 v, 'Квадратный метр' m, 0 s, 3 conn) foo left join (select id, row_number() OVER (order by id) as rn from source_two) f2 on foo.conn = f2.rn
returning id)
insert into job2stage(stageid, jobid, seq) select nid1.id, source_thr.id, row_number() OVER (order by source_thr) from (select id from sitestage where name = 'Ремонт АБП') nid1, source_thr;



with 
source_dates as (
insert into jobschedule(version, prev, planned_start, planned_end) 
select 1, null::bigint, to_timestamp('27.09.2025', 'DD-MM-YYYY'), to_timestamp('03.10.2025', 'DD-MM-YYYY')
union all
select 1, null::bigint, to_timestamp('03.10.2025', 'DD-MM-YYYY'), to_timestamp('30.10.2025', 'DD-MM-YYYY')
returning id
), source_thr as (
insert into sitejob(name, description, scheduled, volume, measurement, status) 
select n, d, f2.id, v, m, s from (
select 'Схавать воперов' n, 'чисто по кайфу закинуть вопер или два с соусом' d, 250 v, 'воперов' m, 0 s, 1 conn
union all
select 'Шлифануть коктейлем' n, 'пингвины пингвва пингу' d, 410 v, 'литров' m, 0 s, 2 conn) foo left join (select id, row_number() OVER (order by id) as rn from source_dates) f2 on foo.conn = f2.rn
returning id)
insert into job2stage(stageid, jobid, seq) select nid1.id, source_thr.id, row_number() OVER (order by source_thr) from (select id from sitestage where name = 'После работы чисто читмил') nid1, source_thr;

 with 
source_dates as (
insert into jobschedule(version, prev, planned_start, planned_end) 
select 1, null::bigint, to_timestamp('27.09.2025', 'DD-MM-YYYY'), to_timestamp('03.10.2025', 'DD-MM-YYYY')
union all
select 1, null::bigint, to_timestamp('03.10.2025', 'DD-MM-YYYY'), to_timestamp('30.10.2025', 'DD-MM-YYYY')
returning id
), source_thr as (
insert into sitejob(name, description, scheduled, volume, measurement, status) 
select n, d, f2.id, v, m, s from (
select 'Жижи мне' n, 'Жижа с гранатом всем' d, 6 v, 'флаконов' m, 0 s, 1 conn
union all
select 'Починка испарика' n, 'сгорел опять' d, 2 v, 'испарика' m, 0 s, 2 conn) foo left join (select id, row_number() OVER (order by id) as rn from source_dates) f2 on foo.conn = f2.rn
returning id)
insert into job2stage(stageid, jobid, seq) select nid1.id, source_thr.id, row_number() OVER (order by source_thr) from (select id from sitestage where name = 'И жижкой заправиться') nid1, source_thr;

select count(1) >= 1 from buildsite b left join sitestage s on s.site = b.id left join job2stage js on js.stageid = s.id left join sitejob sj on sj.id = js.jodbid left join jobschedule jsh on sj.scheduled = jsh.id
left join jobshift jf on jsh.id = jf.affected_jobsch  where jf.state = 0 and b.id = 1;

select js2.stageid, js2.jobid, js2.seq from job2stage js2 left join sitestage s2 on js2.stageid = s2.id left join sitejob s3 on js2.jobid = s3.id where (js2.stageid, js2.seq) in (select js.stageid, min(js.seq) from buildsite b left join sitestage s on s.site = b.id left join job2stage js on js.stageid = s.id left join sitejob sj on sj.id = js.jobid left join jobschedule jsh on sj.scheduled = jsh.id where b.id = 3 and sj.status = 0 and now() between jsh.planned_start and jsh.planned_end group by (js.stageid));


select * from jobshift j ;

select jf.* from buildsite b left join sitestage s on s.site = b.id left join job2stage js on js.stageid = s.id left join sitejob sj on sj.id = js.jobid left join jobschedule jsh on sj.scheduled = jsh.id
left join jobshift jf on jsh.id = jf.affected_jobsch  where jf.state = 0 and b.id = 1;

alter user mh_admin set search_path = hack, public, public, topology, tiger;

insert into material(name, properties, measurement)
select 'Бортовой камень 1000x300x150', '', 'штук'
union all
select 'Бетон', '', 'мешков'
union all
select 'Битуум', '', 'литров'
union all
select 'Вопер', '', 'штук'
union all
select 'Коктейльчик', '', 'стаканов';


insert into required_mats(jobid, materialid, volume)
select j.id, m.id, 100 from (select id from material where name = 'Бортовой камень 1000x300x150') m, (select id from sitejob where name = 'Замена дорожного бортового камня в рамках благоустройства территории') j
union all 
select j.id, m.id, 50 from (select id from material where name = 'Бортовой камень 1000x300x150') m, (select id from sitejob where name = 'Битуум') j
union all 
select j.id, m.id, 50 from (select id from material where name = 'Вопер') m, (select id from sitejob where name = 'Схавать воперов') j;

insert into supplier(name) 
select 'ООО Бекам'
union all
select 'Бургер Кинг'
union all
select '33 пингвина';


insert into shipment(scheduled_at, arrived_at, supplier, state, comment, acceptor, geo)
select now()+ interval '2 day', null, s.id, 0, null, null, null from (select id from supplier where name = 'Бургер Кинг') s, (select id from users where username = 'prorab') a;

with shipment as (
insert into shipment(scheduled_at, arrived_at, supplier, state, comment, acceptor, geo)
select now()+ interval '1 day', now()+ interval '1 day', s.id, 1, 'камни камни', a.id, St_MakePoint(37.505189, 55.854209) from (select id from supplier where name = 'ООО Бекам') s, (select id from users where username = 'prorab') a
returning id
)
insert into shipped_mats(shipmentid, materialid, volume, serial, accepted) 
select s.id, m.id, 120, '234f234f', true from shipment s, (select id from material where name = 'Бортовой камень 1000x300x150') m;

insert into mat_usage(regtime, sitejob, materialid, shipmentid, spent)
select to_timestamp('26.09.2025', 'DD-MM-YYYY'), s.id, m.mat, m.ship, 15 from (select id from sitejob where name = 'Замена дорожного бортового камня в рамках благоустройства территории') s, (select shipmentid ship, materialid mat from shipped_mats where volume = 120) m;

insert into jobprogres (linkedjob, comment, regtime, geo, volume) 
select s.id, 'положили немного', to_timestamp('27.09.2025', 'DD-MM-YYYY'), St_MakePoint(37.505189, 55.854209), 10 from (select id from sitejob where name = 'Замена дорожного бортового камня в рамках благоустройства территории') s;

insert into "comments"(site, author, created_at, state, comment, fix_time, docs, geo, type, rec_type, linked_job)
select s.id, a.id, to_timestamp('26.09.2025', 'DD-MM-YYYY'), 0, 'Свалка материала', 3, 'доки доки доки', ST_MakePoint(37.505372, 55.854146), 0, 0, null from (select id from buildsite where sitename = 'Флотская улица д. 54, д. 58к1') s, (select id from users where username = 'admin') a
union all
select s.id, a.id, to_timestamp('26.09.2025', 'DD-MM-YYYY'), 0, 'Нарушение укладки на неподготовленную поверхность', 3, 'доки доки доки', ST_MakePoint(37.505372, 55.854146), 1, 1, j.id from (select id from buildsite where sitename = 'Флотская улица д. 54, д. 58к1') s, (select id from users where username = 'goscont') a, (select id from sitejob where name = 'Замена дорожного бортового камня в рамках благоустройства территории') j;

select * from "comments" c ;

select * from material;

insert into shipment(scheduled_at, arrived_at, supplier, state, comment, acceptor, geo, doc_serial, package_state)
values


--37.505425, 55.854887
-----------------------------------------
select foo1.a, foo2.b from (select generate_series(0, 1) a ) foo1 join (select generate_series(0, 1) b) foo2 on true;

select * from sitejob left join jobschedule j on scheduled = j.id;

alter table sitejob alter column measurement type text;



select * from users;
select to_timestamp('15.04.2024', 'DD-MM-YYYY');
select 1, foo.id, 2 from (select id from users where name = 'Петр') foo;

select now()- interval '1 day';

alter table jobprogres add column volume numeric;

show search_path;
set search_path = hack, public, public, topology, tiger, "$user";

SELECT b.id, b.sitename, b.coordinates, c.id FROM buildsite b LEFT JOIN comments c ON c.site = b.id where c.state = 0;