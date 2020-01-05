
import re
import requests
from bs4 import BeautifulSoup
import csv

# 字母列表
def getallcarbranch():
    cartypes = [chr(i) for i in range(65,91)]
    requests.adapters.DEFAULT_RETRIES = 5 # 增加重连次数
    sss = requests.session()
    sss.keep_alive = False
    with open('allbrahch.py', 'w') as file_obj:
        file_obj.write('branchs = {')
        for cartype in cartypes:
            baseCarBranchUrl = "http://www.autohome.com.cn/grade/carhtml/{}.html".format(cartype)
            html=sss.get(baseCarBranchUrl)
            html= html.text
            soup = BeautifulSoup(html, "html.parser")
            contents = soup.find_all('h4')
            for x in contents:
                l = x.a.string.replace(" ", "")
                if cartype == cartypes[-1] and x == contents[-1]:
                   file_obj.write('"' + l + '": ' +'"'+"https:"+ x.a.attrs['href'] +'"'+ "}")                  
                else:
                   file_obj.write('"' + l + '": ' +'"'+"https:"+ x.a.attrs['href'] +'"'+ ", ")

def getall(a):
    o = 0
    data = []
    das = []
    requests.adapters.DEFAULT_RETRIES = 5 # 增加重连次数
    sss = requests.session()
    sss.keep_alive = False
    from allbrahch import branchs
    
    if a != "":
        if a not in branchs:
           print("输入有误")
           return
        tempbranchs = {}
        tempbranchs[a] = branchs[a]
        f = open("%s.csv"%a,'w',encoding='utf-8')
    else:
        tempbranchs = branchs
        f = open('all.csv','w',encoding='utf-8')
    csv_writer = csv.writer(f)
    csv_writer.writerow(["品牌","车型","USB/Type-C接口数量"])
    with open("all2.csv",newline='',encoding='UTF-8') as csvfile:
        rows=csv.reader(csvfile)
        for row in rows:
            data.append(row[0])
            das.append([row[0],row[1],row[2]])
            csv_writer.writerow([row[0],row[1],row[2]])
            o+=1
            print(o)
    p = 1
    for xs, y  in tempbranchs.items():
        # if ("长安"  not in xs):
        #     continue
        p+=1
        print("进度：{}//{}".format(p,len(tempbranchs)))
        if xs in data:
            print("exists: {}".format(xs))
            continue
        paramurl = branchs[xs]
        html=sss.get(paramurl)
        html= html.text
        soup = BeautifulSoup(html, "html.parser")
        contents = soup.find_all('a', href= re.compile('//car.autohome.com.cn/config'))
        if len(contents) > 0 :
            href = "https:" + contents[0].attrs['href']
            #href = "https://car.autohome.com.cn/config/series/5393.html#pvareaid=3454437"
            html=sss.get(href)
            html= html.text
            soup = BeautifulSoup(html, "html.parser")
            pattern = re.compile(r"USB/Type-C(.*?)", re.MULTILINE | re.DOTALL)
            script = soup.find("script", text=pattern)
            br = []
            vr = []
            if script == None:
                continue
            for x in script:
                if '"name":"车型' in str(x):
                    a = str(x).rfind('"name":"车型')
                    b = str(x).rfind('{"id":0,"name":"厂')
                
                    if a==-1 or b == -1:
                        continue
                    h = eval(str(x)[a-8:b-1])
                    for hh in h["valueitems"]:
                        s = ""
                        for j in hh["value"].split("<span"):
                            k = j.rfind("span")
                            #print(j,"ps")
                            if k != -1:
                                s+=j[k:]
                                #print(j[k:],"ss")
                            if k == -1 and j !="":
                                s+=j
                        s = s.replace(" ","")
                        s = s.replace("span>","")
                        br.append(s)
                    a = str(x).rfind('"configid":214')
                    b = str(x).rfind('"configid":177')
                    
                    if a==-1 or b == -1:
                        continue
                 
                    dics = eval(str(x)[a-1:b-2])
                    for x in dics["valueitems"]:
                        if len(x["sublist"]) < 1:
                            continue
                        
                        j = x["sublist"][0]["subname"]
                        i = 0
               
                        for f in j.split("个"):
                            i+=1
                            if len(f)>1:
                                if i == 1:
                                    ｓ = ("前排:"+f[-1]+"个")
                                if i == 2:
                                    s+= ("/后排:"+f[-1]+"个")
                        vr.append(s)
                i = 0
 
                if (len(vr) != len(br)):
                    continue
                
                for xx in br: 
                    o += 1
                    das.append([xs,xx,vr[i]])
                    csv_writer.writerow([xs,xx,vr[i]])
                    i+=1
                    print(o)
    # print(len(das))
    # for x in das:
    #     csv_writer.writerow([x[0],x[1],x[2]])
                
def main():
    #getallcarbranch()
    a = input("请输入需要查询的汽车品牌,如果输入为空则默认为全部查询:")
    getall(a)


if __name__ == '__main__':
    main()


