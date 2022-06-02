import requests,json,main,time
with open('result.json','r',encoding='utf8') as origin_file:
    origin=origin_file.read()
origin=json.loads(origin)
pushdata={}
#推送渠道
pushdata['channel']='wechat'

pushdata['content']=''
# 具体请查看pushplus api文档https://www.pushplus.plus/doc/guide/api.html
# token=''

time.sleep(60)#平台统计有延迟
errorcount=0
for member in origin:
    if member['status']== 'error':
        errorcount+=1
        continue
    XLtoken=main.ConverMidToXLToken(member['member'])
    profile=main.GetProfile(XLtoken)
    score_now=profile.score()
    score_add=score_now-member['score']
    if score_now < 100:
        score_need=100-score_now
    elif score_now < 200:
        score_need=200-score_now
    elif score_now < 500:
        score_need=500-score_now
    elif score_now < 1000:
        score_need=1000-score_now
    elif score_now < 5000:
        score_need=5000-score_now
    else:
        score_need=0
    member['result']+='\n此次执行增加了'+str(score_add)+'积分'+'\n当前为'+profile.medal()+'，距离下一徽章还需'+str(score_need)+'积分'

#检查token
if ('token' in locals().keys()) == True:
    pass
else:
    exit('+===============+\n| Token未定义！ |\n+===============+')

if errorcount!=len(main.memberlist):
    titledone=False
    for i in origin:
        if i['status']!='error':
            if titledone==False:
                pushdata['title']='['+str(len(main.memberlist)-errorcount)+'/'+str(len(main.memberlist))+']'+i['status']+'啦'
                titledone=True
        pushdata['content']+='mid或X-Litemall-Token：'+i['member']+'\n名称：'+i['name']+'\n'+i['result']+'\n\n'
else:
    pushdata['title']='任务执行失败'
    pushdata['content']='所有mid或X-Litemall-Token皆打卡失败'

#向pushplus发出推送请求
pushdata['token']=token
push=json.loads(requests.post('http://www.pushplus.plus/send/',data=pushdata).text)
if push['code'] == 200:
    print('推送成功')
else:
    exit('推送失败：'+push['msg'])