
# 此处为预处理部分，但部分数据变换无法快速实现，仍在研究中
# colnames<-c('stat_month','msisdn','hm_prov','vstd_prov_count','rm_days','voice_mo_count','voice_mt_count','video_mo_count','video_mt_count','voice_mo_dur','voice_mt_dur','video_mo_dur','video_mt_dur','workday_days','holiday_days','specialday_days','workday_count','holiday_count','specialday_count','workday_dur','holiday_dur','specialday_dur','between_volte','volte223g')
# local_201601<-read.table('E:/Clean Data/201601_local.csv',sep=',',header=FALSE,col.names=colnames)
# local_201602<-read.table('E:/Clean Data/201602_local.csv',sep=',',header=FALSE,col.names=colnames)
# rm_201601<-read.table('E:/Clean Data/201601_rm.csv',sep=',',header=FALSE,col.names=colnames)
# rm_201602<-read.table('E:/Clean Data/201602_rm.csv',sep=',',header=FALSE,col.names=colnames)
# data_201601<-rbind(local_201601,rm_201601)
# data_201602<-rbind(local_201602,rm_201602)
# data_201601$stat_month<-as.factor(data_201601$stat_month)
# data_201601$msisdn<-as.factor(data_201601$msisdn)
# data_201601$hm_prov<-as.factor(data_201601$hm_prov)
# data_201602$stat_month<-as.factor(data_201602$stat_month)
# data_201602$msisdn<-as.factor(data_201602$msisdn)
# data_201602$hm_prov<-as.factor(data_201602$hm_prov)
# can not quickly group
# data_201601_agg<-aggregate(data_201601[,4:24],by=data_201601[,1:3],FUN=sum)
# data_201602_agg<-aggregate(data_201602[,4:24],by=data_201602[,1:3],FUN=sum)

final_col<-c('msisdn', 'stat_month', 'hm_prov', 'flag', 'vstd_prov_cont', 'rm_days', 'workday_days', 'holiday_days', 'specialday_days', 'workday_cont', 'holiday_cont', 'specialday_cont', 'workday_dr', 'holiday_dr', 'specialday_dr', 'call_cont', 'call_dr', 'avg_day_cont_totle', 'avg_day_dr_totle', 'avg_day_cont_workday', 'avg_day_dr_workday', 'avg_day_cont_holiday', 'avg_day_dr_holiday')
data_201601<-read.table('E:/Clean Data/data_final_201601.csv',sep=',',header=TRUE)
data_201601<-cbind(data_201601[,1:3],data_201601[,15:23],data_201601[,4:14])
data_201601$flag<-as.factor(data_201601$flag)
data_201601$stat_month<-as.factor(data_201601$stat_month)
data_201601$msisdn<-as.factor(data_201601$msisdn)
data_201601$hm_prov<-as.factor(data_201601$hm_prov)
datatmp<-data_201601[,-1:-3]
library(randomForest)
library(foreign)
ind<-sample(2,nrow(data_201601),replace=TRUE,prob=c(0.7,0.3))
traindata<- data_201601 [ind==1,]
testdata<- data_201601 [ind==2,]
rf <- randomForest(flag~.,data=datatmp,ntree=100)
table(predict(rf), data_201601$flag)
print(rf)
plot(rf)
importance(rf)