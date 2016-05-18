import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
colnames=['stat_month','msisdn','hm_prov','vstd_prov_count','rm_days','voice_mo_count','voice_mt_count','video_mo_count','video_mt_count','voice_mo_dur','voice_mt_dur','video_mo_dur','video_mt_dur','workday_days','holiday_days','specialday_days','workday_count','holiday_count','specialday_count','workday_dur','holiday_dur','specialday_dur','between_volte','volte223g']
newcolnames=['msisdn','stat_month','hm_prov','vstd_prov_cont','rm_days','workday_days','holiday_days','specialday_days','workday_cont','holiday_cont','specialday_cont','workday_dr','holiday_dr','specialday_dr','call_cont','call_dr','avg_day_cont_totle','avg_day_dr_totle','avg_day_cont_workday','avg_day_dr_workday','avg_day_cont_holiday','avg_day_dr_holiday']
local_201601 = pd.read_csv('E:/Clean Data/201601_local.csv',sep=',',header=None,names=colnames)
local_201602 =pd.read_csv('E:/Clean Data/201602_local.csv',sep=',',header=None,names=colnames)
rm_201601 = pd.read_csv('E:/Clean Data/201601_rm.csv',sep=',',header=None,names=colnames)
rm_201602 = pd.read_csv('E:/Clean Data/201602_rm.csv',sep=',',header=None,names=colnames)

data_201601=local_201601.append(rm_201601)
data_201602=local_201602.append(rm_201602)
data_201601=data_201601.groupby(['msisdn','stat_month','hm_prov']).sum()
data_201602=data_201602.groupby(['msisdn','stat_month','hm_prov']).sum()

def dataclean(a):
    a=a.drop(['between_volte','volte223g'],1)
    a['call_count'] = a['voice_mt_count']+a['video_mt_count']+a['voice_mo_count']+a['video_mo_count']
    a['call_dur'] = a['voice_mt_dur']+a['video_mt_dur']+a['voice_mo_dur']+a['video_mo_dur']
    a = a.drop(['voice_mt_count','video_mt_count','voice_mo_count','video_mo_count'],1)
    a = a.drop(['voice_mt_dur','video_mt_dur','voice_mo_dur','video_mo_dur'],1)
    a['avg_day_count_totle']=a['call_count']/a['rm_days']
    a['avg_day_dur_totle']=a['call_dur']/a['rm_days']
    a['avg_day_count_workday']=a['workday_count']/a['workday_days']
    a['avg_day_dur_workday']=a['workday_dur']/a['workday_days']
    a['avg_day_count_holiday']=a['holiday_count']/a['holiday_days']
    a['avg_day_dur_holiday']=a['holiday_dur']/a['holiday_days']
    a = a.fillna(0)
    return a
 
data_201601=dataclean(data_201601)
data_201602=dataclean(data_201602)
data_201601.to_csv('E:/Clean Data/data_201601.csv',header=False,index=True,index_lable=False)
data_201602.to_csv('E:/Clean Data/data_201602.csv',header=False,index=True,index_lable=False)
data_201601=pd.read_csv('E:/Clean Data/data_201601.csv',sep=',',header=None,names=newcolnames)
data_201602=pd.read_csv('E:/Clean Data/data_201602.csv',sep=',',header=None,names=newcolnames)
msisdn_201602=data_201602['msisdn']
flag=pd.DataFrame(np.zeros(len(msisdn_201602)))
maintain_flag=pd.concat([msisdn_201602,flag],axis=1)
maintain_flag.columns = ['msisdn','flag']
data_201601_mark=pd.merge(data_201601,maintain_flag,how='left',on=['msisdn','msisdn'])
data_201601_mark=data_201601_mark.fillna(1)
tmp=data_201601_mark.pop('flag')
data_201601_mark.insert(3,'flag',tmp)

data_maintain_sample=data_201601_mark[data_201601_mark['flag']==0]
data_lost_sample=data_201601_mark[data_201601_mark['flag']==1].sample(n=167464,replace=True)
data_final_201601_balanced=pd.concat([data_maintain_sample,data_lost_sample])
data_final_201601_balanced.to_csv('E:/Clean Data/data_final_201601_balanced.csv',header=True,index=False,index_lable=False)
data_201601_mark.to_csv('E:/Clean Data/data_final_201601_origin.csv',header=True,index=False,index_lable=False)