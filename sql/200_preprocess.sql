create table dom_200_201603(
stat_month int(8),
vstd_prov varchar(3),
msisdn varchar(15),
hm_prov varchar(3),
rm_days int(3),
calling_count int(10),
called_count int(10),
calling_rm_dur int(20),
called_rm_dur int(20),
calling_chg int(20),
called_chg int(20),
workday_rm int(3),
holiday_rm int(3),
nationalday_rm int(3),
workday_count int(10),
holiday_count int(10),
nationalday_count int(10)
);

load data local infile '/mnt/shared/200_return/201603_all_result' into table dom_200_201603
fields terminated by ','
lines terminated by '\n';

-- create table prefix(
-- prefix int(4),
-- operator varchar(7));

-- load data local infile '/mnt/shared/prefix' into table prefix
-- fields terminated by ','
-- lines terminated by '\r\n';

delete from dom_200_201602 where calling_count=0 and called_count=0;

select substr(msisdn,1,3),count(1) from dom_200_201602 group by substr(msisdn,1,3);

select sum(calling_count+called_count) from dom_200_201603;
 
alter table dom_200_201603 add flag int(2) default '1';

create index idx_msisdn on dom_200_201603(msisdn)

insert into dom_200_201602 (select stat_month,vstd_prov,msisdn,hm_prov,
0 as rm_days,
0 as calling_count,
0 as called_count,
0 as calling_rm_dur,
0 as called_rm_dur,
0 as calling_chg,
0 as called_chg,
0 as workday_rm,
0 as holiday_rm,
0 as nationalday_rm,
0 as workday_count,
0 as holiday_count,
0 as nationalday_count,
10 as flag
from dom_200_201603);


create table tmp as (select msisdn,
sum(rm_days) rm_days,
sum(calling_count) calling_count,
sum(called_count) called_count,
sum(calling_rm_dur) calling_rm_dur,
sum(called_rm_dur) called_rm_dur,
sum(calling_chg) calling_chg,
sum(called_chg) called_chg,
sum(workday_rm) workday_rm,
sum(holiday_rm) holiday_rm,
sum(nationalday_rm) nationalday_rm,
sum(workday_count) workday_count,
sum(holiday_count) holiday_count,
sum(nationalday_count) nationalday_count,
sum(flag) flag
from  dom_200_201603 where msisdn = '13410000874' group by msisdn limit 1) ;

-- procedure to select cmcc_prefix number
drop procedure findsub;
delimiter //
create procedure findsub()
begin
declare no_more_prefix int(1);
declare prefixnum int(4);
declare cur_prefix CURSOR FOR select substr(prefix,1,3) from gsm.prefix where operator = 'cmcc';
declare continue HANDLER for not found set no_more_prefix=1;
open cur_prefix;
fetch cur_prefix into prefixnum;
repeat
insert into tmp  (select msisdn,
sum(rm_days) rm_days,
sum(calling_count) calling_count,
sum(called_count) called_count,
sum(calling_rm_dur) calling_rm_dur,
sum(called_rm_dur) called_rm_dur,
sum(calling_chg) calling_chg,
sum(called_chg) called_chg,
sum(workday_rm) workday_rm,
sum(holiday_rm) holiday_rm,
sum(nationalday_rm) nationalday_rm,
sum(workday_count) workday_count,
sum(holiday_count) holiday_count,
sum(nationalday_count) nationalday_count,
sum(flag) flag
from  dom_200_201602 where substr(msisdn,1,3)=prefixnum group by msisdn);
select "finish",prefixnum;
fetch cur_prefix into prefixnum;
until no_more_prefix=1
end repeat;
select "complete";
close cur_prefix;
end //
delimiter ;

--verified the insert
select substr(msisdn,1,3),sum(calling_count+called_count) from tmp group by substr(msisdn,1,3);

CREATE TABLE sub_ana_03 (
msisdn varchar(15) DEFAULT NULL,
rm_days int(2) DEFAULT NULL,
calling_count int(10) DEFAULT NULL,
called_count int(10) DEFAULT NULL,
calling_rm_dur int(20) DEFAULT NULL,
called_rm_dur int(20) DEFAULT NULL,
calling_chg int(20) DEFAULT NULL,
called_chg int(20) DEFAULT NULL,
workday_rm int(3) DEFAULT NULL,
holiday_rm int(3) DEFAULT NULL,
nationalday_rm int(3) DEFAULT NULL,
workday_count int(10) DEFAULT NULL,
holiday_count int(10) DEFAULT NULL,
nationalday_count int(10) DEFAULT NULL,
flag int(1) DEFAULT NULL
);

mysql -uroot -p123456 -h127.0.0.1 -P3306 --default-character-set=utf8 -B -e 'select * from gsm.dom_200_201603'>/mnt/shared/clusterdata.csv


-- create table imsi_03 (
-- stat_month varchar(15),
-- imsi varchar(15),
-- vstd_prov varchar(3),
-- hm_prov varchar(3)
-- );


-- load data local infile '/mnt/shared/200_return/sub_201603_200.csv' into table imsi_03
-- fields terminated by ','
-- lines terminated by '\n';

-- caculating main feature of data
select flag,
count(msisdn) sub_count,
avg(rm_days) rm_days,
avg(called_count+calling_count) call_count,
avg(called_rm_dur+calling_rm_dur) call_dur,
avg(workday_rm) workday_rm,
avg(workday_count) workday_count,
avg(holiday_rm) holiday_rm,
avg(holiday_count) holiday_count,
avg(nationalday_rm) nationalday_rm,
avg(nationalday_count) nationalday_count,
avg((called_count+calling_count)/rm_days) avg_daycount,
avg((called_rm_dur+calling_rm_dur)/rm_days) avg_daydur,
avg(workday_count/workday_rm) avg_worddaycount,
avg(holiday_count/holiday_rm) avg_holidaydaycount,
avg(nationalday_count/nationalday_rm) avg_spcdaycount
from sub_ana where flag!=10
group by flag;


-- dualing with March data
insert into dom_200_201603 (select 20160300 as stat_month,100 as vstd_prov,msisdn,200 as hm_prov,
0 as rm_days,
0 as calling_count,
0 as called_count,
0 as calling_rm_dur,
0 as called_rm_dur,
0 as calling_chg,
0 as called_chg,
0 as workday_rm,
0 as holiday_rm,
0 as nationalday_rm,
0 as workday_count,
0 as holiday_count,
0 as nationalday_count,
10 as flag
from sub_ana where flag=11);


insert into sub_ana_03 (select msisdn,
sum(rm_days) rm_days,
sum(calling_count) calling_count,
sum(called_count) called_count,
sum(calling_rm_dur) calling_rm_dur,
sum(called_rm_dur) called_rm_dur,
sum(calling_chg) calling_chg,
sum(called_chg) called_chg,
sum(workday_rm) workday_rm,
sum(holiday_rm) holiday_rm,
sum(nationalday_rm) nationalday_rm,
sum(workday_count) workday_count,
sum(holiday_count) holiday_count,
sum(nationalday_count) nationalday_count,
sum(flag) flag
from dom_200_201603
group by msisdn
);


create table imsi_msisdn(
imsi varchar(7),
area_cd varchar(5),
msisdn varchar(8),
flag int(1),
effect_tm datetime,
expire_tm datetime,
area_name varchar(12)
);

load data local infile '/mnt/shared/ld_area_cd.csv.bak' into table ld_area_cd
fields terminated by ','
lines terminated by '\n';


create table ld_area_cd (
LD_AREA_CD varchar(5),
prov_cd varchar(3),
ld_area_nm varchar(12),
effect_tm datetime,
expire_tm datetime
);


create table tmp as (select 
msisdn,
flag,
rm_days,
calling_count,
called_count,
calling_rm_dur,
called_rm_dur,
(called_count+calling_count)/rm_days day_callcount,
(called_rm_dur+calling_rm_dur)/rm_days day_dur,
workday_count/workday_rm workdaycount,
holiday_count/holiday_rm holidaydaycount,
substr(msisdn,1,7) haoduan,
substr(msisdn,1,5) prefix
from sub_ana_03
);

create table prefixtmp as (select substr(msisdn,1,5) prefixtmp,count(*) count from transform_03 group by substr(msisdn,1,5));


create table transform_03(
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
holidaydaycount float(8,6)
);


delimiter //
drop procedure if exists transformdata;
create procedure transformdata()
begin
declare no_more_prefix int(1);
declare prefixnum int(4);
declare cur_prefix CURSOR FOR select prefixtmp from gsm.prefixtmp;
declare continue HANDLER for not found set no_more_prefix=1;
open cur_prefix;
fetch cur_prefix into prefixnum;
repeat
select "start",prefixnum;
create table imsi_tmp as (select * from imsi_msisdn_200 where substr(msisdn,1,5)=prefixnum);
insert into transform_03 (
select a.msisdn,a.flag,a.rm_days,b.area_cd,b.area_name,
a.calling_count,
a.called_count,
a.calling_rm_dur,
a.called_rm_dur,
a.day_callcount,
a.day_dur,
ifnull(workdaycount,0),
ifnull(holidaydaycount,0)
from tmp a left join imsi_tmp b on a.haoduan=b.msisdn where a.prefix=prefixnum);
drop table imsi_tmp;
select "finish",prefixnum;
fetch cur_prefix into prefixnum;
until no_more_prefix=1
end repeat;
select "complete";
close cur_prefix;
end//
delimiter ;
