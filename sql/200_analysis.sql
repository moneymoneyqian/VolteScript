select bb.class,count(*) from
(
select
	if(aa.class_1<aa.class_2,if(aa.class_1<aa.class_3,'class_1','class_3'),if(aa.class_2<aa.class_3,'class_2','class_3')) as class
from
(SELECT 
    SQRT(POWER(day_callcount - 23.800738192821, 2) + POWER(day_dur - 64.845967021633, 2) + POWER(a.workdaycount - 19.330929773966, 2) + POWER(holidaydaycount - 17.828248896998, 2)) as class_1,
	SQRT(POWER(day_callcount - 10.110373965713, 2) + POWER(day_dur - 25.512785744855, 2) + POWER(a.workdaycount - 7.3086403108631, 2) + POWER(holidaydaycount - 7.1180317197771, 2)) as class_2,
	SQRT(POWER(day_callcount - 3.2812976142555, 2) + POWER(day_dur - 6.7875865885172, 2) + POWER(a.workdaycount - 1.9724197899419, 2) + POWER(holidaydaycount - 2.0176281428516, 2)) as class_3
    FROM
    transform_03 a
) aa )
bb group by bb.class


select aa.*,
if(class_1<class_2,if(class_1<class_3,'class_1','class_3'),if(class_2<class_3,'class_2','class_3')) as class
from (
select a.msisdn,
a.flag,
a.rm_days,
a.area_cd,
a.area_name,
a.calling_count,
a.called_count,
a.calling_rm_dur,
a.called_rm_dur,
a.day_callcount,
a.day_dur,
a.workdaycount,
a.holidaydaycount,
SQRT(POWER(day_callcount - 23.800738192821, 2) + POWER(day_dur - 64.845967021633, 2) + POWER(a.workdaycount - 19.330929773966, 2) + POWER(holidaydaycount - 17.828248896998, 2)) as class_1,
SQRT(POWER(day_callcount - 10.110373965713, 2) + POWER(day_dur - 25.512785744855, 2) + POWER(a.workdaycount - 7.3086403108631, 2) + POWER(holidaydaycount - 7.1180317197771, 2)) as class_2,
SQRT(POWER(day_callcount - 3.2812976142555, 2) + POWER(day_dur - 6.7875865885172, 2) + POWER(a.workdaycount - 1.9724197899419, 2) + POWER(holidaydaycount - 2.0176281428516, 2)) as class_3
-- if(class_1<class_2,if(class_1<class_3,'class_1','class_3'),if(class_2<class_3,'class_2','class_3')) as class
from tmp a) aa;

create table clustering_03(
msisdn varchar(15),
flag varchar(1),
area_cd varchar(4),
rm_days int(3),
area_name varchar(12),
calling_count int(10) DEFAULT NULL,
called_count int(10) DEFAULT NULL,
calling_rm_dur int(20) DEFAULT NULL,
called_rm_dur int(20) DEFAULT NULL,
day_callcount float(8,6),
day_dur float(8,6),
workdaycount float(8,6),
holidaydaycount float(8,6),
class_1 float(8,6),
class_2 float(8,6),
class_3 float(8,6),
class varchar(8)
);


delimiter //
drop procedure if exists createtmptable;
create procedure createtmptable()
	begin
drop table if exists clustering_tmp;
create table clustering_tmp (
msisdn varchar(15),
flag varchar(1),
area_cd varchar(4),
rm_days int(3),
area_name varchar(12),
calling_count int(10) DEFAULT NULL,
called_count int(10) DEFAULT NULL,
calling_rm_dur int(20) DEFAULT NULL,
called_rm_dur int(20) DEFAULT NULL,
day_callcount float(8,6),
day_dur float(8,6),
workdaycount float(8,6),
holidaydaycount float(8,6),
class_1 float(8,6),
class_2 float(8,6),
class_3 float(8,6)
);
end//
delimiter ;




delimiter //
drop procedure if exists clustering;
create procedure clustering()
begin
declare no_more_prefix int(1);
declare prefixnum int(4);
declare cur_prefix CURSOR FOR select prefixtmp from gsm.prefixtmp;
declare continue HANDLER for not found set no_more_prefix=1;
open cur_prefix;
fetch cur_prefix into prefixnum;
repeat
select "start",prefixnum;
drop table if exists imsi_tmp;
create table imsi_tmp as (select * from imsi_msisdn_200 where substr(msisdn,1,5)=prefixnum);
call createtmptable();
insert into clustering_tmp (
select a.msisdn,
a.flag,
a.rm_days,
a.area_cd,
a.area_name,
a.calling_count,
a.called_count,
a.calling_rm_dur,
a.called_rm_dur,
a.day_callcount,
a.day_dur,
a.workdaycount,
a.holidaydaycount,
SQRT(POWER(day_callcount - 23.800738192821, 2) + POWER(day_dur - 64.845967021633, 2) + POWER(a.workdaycount - 19.330929773966, 2) + POWER(holidaydaycount - 17.828248896998, 2)) as class_1,
SQRT(POWER(day_callcount - 10.110373965713, 2) + POWER(day_dur - 25.512785744855, 2) + POWER(a.workdaycount - 7.3086403108631, 2) + POWER(holidaydaycount - 7.1180317197771, 2)) as class_2,
SQRT(POWER(day_callcount - 3.2812976142555, 2) + POWER(day_dur - 6.7875865885172, 2) + POWER(a.workdaycount - 1.9724197899419, 2) + POWER(holidaydaycount - 2.0176281428516, 2)) as class_3
from transform_03 a
where substr(msisdn,1,5)=prefixnum
);
insert into clustering_03 (
	select a.*,
	if(class_1<class_2,if(class_1<class_3,'class_1','class_3'),if(class_2<class_3,'class_2','class_3')) as class
	from clustering_tmp a
);
select "finish",prefixnum;
fetch cur_prefix into prefixnum;
until no_more_prefix=1
end repeat;
select "complete";
close cur_prefix;
end//
delimiter ;
