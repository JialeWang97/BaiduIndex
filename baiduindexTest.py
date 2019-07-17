# -*- coding: utf-8 -*-
"""
Created on Mon Feb 25 15:36:24 2019

@author: lenovo
"""
import time
from selenium import webdriver
import csv

# 打开浏览器
def openbrowser():
    global browser
    
    # https://passport.baidu.com/v2/?login
    url = "https://passport.baidu.com/v2/?login&tpl=mn&u=http%3A%2F%2Fwww.baidu.com%2F"
    # 声明浏览器对象，打开Chrome浏览器
    browser = webdriver.Chrome()
    # 输入网址
    browser.get(url)
    
    print("等待3秒打开浏览器...")
    time.sleep(3)
    #print(browser.page_source)
    
    #选择账号密码的方式登录 
    browser.find_element_by_id("TANGRAM__PSP_3__footerULoginBtn").click()
    
    # 清空账号、密码输入框
    browser.find_element_by_id("TANGRAM__PSP_3__userName").clear()
    browser.find_element_by_id("TANGRAM__PSP_3__password").clear()
    
    # 输入账号密码
    account = ["百度账号","百度密码"]
               
    browser.find_element_by_id("TANGRAM__PSP_3__userName").send_keys(account[0])
    browser.find_element_by_id("TANGRAM__PSP_3__password").send_keys(account[1])
    
    # 点击登陆登陆
    browser.find_element_by_id("TANGRAM__PSP_3__submit").click()

    # 等待登陆3秒
    print('等待登陆10秒...')
    time.sleep(3)
    print("等待网址加载完毕...")

    select = input("请观察浏览器网站是否已经登陆(y/n)：")
    
    while 1:
        if select == "y" or select == "Y":
            print("登陆成功，准备打开新的窗口...")
            break

        elif select == "n" or select == "N":
            selectno = input("账号密码错误请按0，验证码出现请按1...")
            # 账号密码错误则重新输入
            if selectno == "0":
                print("error")
                exit()
            elif selectno == "1":
                input("请在浏览器中输入验证码并登陆...")
                select = input("请观察浏览器网站是否已经登陆(y/n)：")
        else:
            print("请输入“y”或者“n”！")
            select = input("请观察浏览器网站是否已经登陆(y/n)：")

def writeIntoCsvFile(result,filename):
    arr=[]
    with open('baiduindex'+ filename +'.csv','w',newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["城市","抑郁","焦虑","自杀","心理疾病"])
        for key in result.keys():
            arr.clear()
            arr.append(key)
            for value in result[key]:
                arr.append(value)
            writer.writerow(arr)
    csvfile.close()
    
    

def getindex(keywords, cities):
    openbrowser()
    time.sleep(2)
    
    #result存储数据按照 "抑郁","焦虑","自杀","心理疾病" 的顺序
    result={}
    
    provList1=["安徽","澳门","北京","重庆","福建","广东","广西","甘肃","贵州"]
    provList2=["河北","黑龙江","河南","湖南","湖北","海南","吉林","江苏","江西"]
    provList3=["辽宁","内蒙古","宁夏","青海","上海","四川","山东","山西","陕西"]
    #provList4=["天津","台湾","西藏","香港","新疆","云南","浙江"]
    
    #通过执行js脚本来新开一个窗口
    js = 'window.open("http://index.baidu.com/v2/main/index.html#/trend/%E4%B8%AD%E5%9B%BD?words=%E4%B8%AD%E5%9B%BD");'
    browser.execute_script(js)
    
    # 新窗口句柄切换，进入百度指数
    # 获得当前打开所有窗口的句柄handles
    # handles为一个数组
    handles = browser.window_handles

    # 切换到当前最新打开的窗口
    browser.switch_to_window(handles[-1])
    
    # 最大化窗口
    browser.maximize_window()

    time.sleep(5)
     
    #勾选平均值
    browser.find_element_by_xpath("//span[contains(text(),'平均值')]/preceding-sibling::span[1]").click()
              
    #时间选择 2011年至2018年的数据 0-7分别代表2018-2011年
    for date in range(8):
        result.clear()
        if date == 0:
            #选择日期
            browser.find_element_by_xpath("/html/body/div[1]/div[2]/div[2]/div[2]/div[2]/div[1]/div[1]/div[1]/div[1]/div[1]/button").click()  
            #起始时间
            browser.find_element_by_xpath("/html/body/div[11]/div[1]/div[1]/div[2]/div[1]/img").click()
            #年份设置为2018
            browser.find_element_by_xpath("html/body/div[11]/div[1]/div[2]/div[1]/div[1]/div[1]/span[1]/button[1]").click()
            #月份默认为1月，设置日为1号
            browser.find_element_by_xpath("//button[contains(@aria-label,'2018年1月1日')]").click()
            #终止时间
            browser.find_element_by_xpath("/html/body/div[11]/div[1]/div[1]/div[3]/div[1]/img").click()
            #年份设置为2018
            browser.find_element_by_xpath("/html/body/div[11]/div[1]/div[3]/div[1]/div[1]/div[1]/span[1]/button[1]").click()
            #月份设置为12月，现在是2月，右按钮需要点击十下      
            for i in range(10):
                browser.find_element_by_xpath("/html/body/div[11]/div[1]/div[3]/div[1]/div[1]/div[1]/span[2]/button[3]").click()
                time.sleep(0.1)
            #日设置31号  
            browser.find_element_by_xpath("//button[contains(@aria-label,'2018年12月31日')]").click()
            #点击确定
            browser.find_element_by_xpath("//div[@class='button-group']/span[1]").click()
        else:
            #选择日期
            browser.find_element_by_xpath("/html/body/div[1]/div[2]/div[2]/div[2]/div[2]/div[1]/div[1]/div[1]/div[1]/div[1]/button").click() 
            #起始时间
            browser.find_element_by_xpath("/html/body/div[11]/div[1]/div[1]/div[2]/div[1]/img").click()
            #年份递减
            browser.find_element_by_xpath("html/body/div[11]/div[1]/div[2]/div[1]/div[1]/div[1]/span[1]/button[1]").click()
            #设置日为1号
            browser.find_element_by_xpath("//button[contains(@aria-label,'"+ str(2018-date) + "年1月1日')]").click()
            #终止时间
            browser.find_element_by_xpath("/html/body/div[11]/div[1]/div[1]/div[3]/div[1]/img").click()
            #年份递减
            browser.find_element_by_xpath("/html/body/div[11]/div[1]/div[3]/div[1]/div[1]/div[1]/span[1]/button[1]").click()
            #日设置31号  
            browser.find_element_by_xpath("//button[contains(@aria-label,'"+ str(2018-date) + "年12月31日')]").click()
            #点击确定
            browser.find_element_by_xpath("//div[@class='button-group']/span[1]").click()
            
        time.sleep(0.5)
                   
        #遍历关键词
        for word in keywords:
            #设置关键词
            browser.find_element_by_xpath("//input[@type='search' and @class='search-input']").click()
            browser.find_element_by_xpath("//input[@type='search' and @class='search-input']").clear()
            browser.find_element_by_xpath("//input[@type='search' and @class='search-input']").send_keys(word)
                
            for province in cities.keys():
                #直辖市不用选择city
                if len(cities[province])==1:
                    #设置城市
                    browser.find_element_by_xpath("/html/body/div[1]/div[2]/div[2]/div[2]/div[2]/div[1]/div[1]/div[1]/div[1]/div[4]/button").click()
                    #设置省份
                    if province in provList1:
                        browser.find_element_by_xpath("/html/body/div[5]/div[1]/div[1]/div[2]/div[2]/span[contains(text(),'"+ province +"')]").click()
                    elif province in provList2:
                        browser.find_element_by_xpath("/html/body/div[5]/div[1]/div[1]/div[3]/div[2]/span[contains(text(),'"+ province +"')]").click()
                    elif province in provList3:
                        browser.find_element_by_xpath("/html/body/div[5]/div[1]/div[1]/div[4]/div[2]/span[contains(text(),'"+ province +"')]").click()
                    else:
                        browser.find_element_by_xpath("/html/body/div[5]/div[1]/div[1]/div[5]/div[2]/span[contains(text(),'"+ province +"')]").click()
                    #点击确定，进行搜索
                    browser.find_element_by_xpath("//span[contains(text(),'探索')]").click()
                    time.sleep(1)
                    value = browser.find_element_by_xpath("/html/body/div[1]/div[2]/div[2]/div[2]/div[2]/div[2]/table/tbody/tr/td[2]/div").text
                    print(province+": "+value)
                    #将数据写入result字典里
                    if province not in result.keys():
                        arr=[]
                        arr.append(value)
                        result[province]=arr
                    else:
                        result[province].append(value)
                else:
                    for city in cities[province]:
                        #设置城市
                        browser.find_element_by_xpath("/html/body/div[1]/div[2]/div[2]/div[2]/div[2]/div[1]/div[1]/div[1]/div[1]/div[4]/button").click()
                        #设置省份
                        #安徽-贵州 /html/body/div[5]/div[1]/div[1]/div[2]/div[2]/
                        #河北-江西 /html/body/div[5]/div[1]/div[1]/div[3]/div[2]/
                        #辽宁-陕西 /html/body/div[5]/div[1]/div[1]/div[4]/div[2]/
                        #天津-浙江 /html/body/div[5]/div[1]/div[1]/div[5]/div[2]/
                        if province in provList1:
                            browser.find_element_by_xpath("/html/body/div[5]/div[1]/div[1]/div[2]/div[2]/span[contains(text(),'"+ province +"')]").click()
                        elif province in provList2:
                            browser.find_element_by_xpath("/html/body/div[5]/div[1]/div[1]/div[3]/div[2]/span[contains(text(),'"+ province +"')]").click()
                        elif province in provList3:
                            browser.find_element_by_xpath("/html/body/div[5]/div[1]/div[1]/div[4]/div[2]/span[contains(text(),'"+ province +"')]").click()
                        else:
                            browser.find_element_by_xpath("/html/body/div[5]/div[1]/div[1]/div[5]/div[2]/span[contains(text(),'"+ province +"')]").click()
                        
                        #设置省份对应的城市
                        browser.find_element_by_xpath("//span[contains(text(),'"+ city +"')]").click()
                        #点击确定，进行搜索
                        browser.find_element_by_xpath("//span[contains(text(),'探索')]").click()
                        time.sleep(1)
                        #抓取搜索指数均值
                        value = browser.find_element_by_xpath("/html/body/div[1]/div[2]/div[2]/div[2]/div[2]/div[2]/table/tbody/tr/td[2]/div").text
                        print(city+": "+value)
                        #将数据写入result字典里
                        if city not in result.keys():
                            arr=[]
                            arr.append(value)
                            result[city]=arr
                        else:
                            result[city].append(value)
                #每一个省休息5秒            
                time.sleep(5)
            #每一个关键字休息10秒 
            time.sleep(10) 
        #每一个时间段休息30秒
        time.sleep(30)                   
        writeIntoCsvFile(result,str(2018 - date))          
   
    
if __name__ == "__main__":
    
    keywords=["抑郁","焦虑","自杀","心理疾病"]
    cities={"安徽":["合肥","铜陵","黄山","池州","宣城","巢湖","淮南","宿州","六安","滁州","淮北","阜阳","马鞍山","安庆","蚌埠","芜湖","亳州"],
            "澳门":["澳门"],
            "北京":["北京"],
            "重庆":["重庆"],
            "福建":["福州","莆田","三明","龙岩","厦门","泉州","漳州","宁德","南平"],
            "广东":["广州","深圳","东莞","云浮","佛山","湛江","江门","惠州","珠海","韶关","阳江","茂名","潮州","揭阳","中山","清远","肇庆","河源","梅州","汕头","汕尾"],
            "广西":["南宁","柳州","桂林","贺州","贵港","玉林","河池","北海","钦州","防城港","百色","梧州","来宾","崇左"],
            "甘肃":["兰州","庆阳","定西","武威","酒泉","张掖","嘉峪关","平凉","天水","白银","金昌","陇南","临夏","甘南"],
            "贵州":["贵阳","黔南","六盘水","遵义","黔东南","铜仁","安顺","毕节","黔西南"],
            "河北":["石家庄","衡水","张家口","承德","秦皇岛","廊坊","沧州","保定","唐山","邯郸","邢台"],
            "黑龙江":["哈尔滨","大庆","伊春","大兴安岭","黑河","鹤岗","七台河","齐齐哈尔","佳木斯","牡丹江","鸡西","绥化","双鸭山"],
            "河南":["郑州","南阳","新乡","开封","焦作","平顶山","许昌","安阳","驻马店","信阳","鹤壁","周口","商丘","洛阳","漯河","濮阳","三门峡","济源"],
            "湖南":["长沙","岳阳","衡阳","株洲","湘潭","益阳","郴州","湘西","娄底","怀化","常德","张家界","永州","邵阳"],
            "湖北":["武汉","黄石","荆州","襄阳","黄冈","荆门","宜昌","十堰","随州","恩施","鄂州","咸宁","孝感","仙桃","天门","潜江","神农架"],
            "海南":["海口","万宁","琼海","三亚","儋州","东方","五指山","文昌","陵水","澄迈","乐东","临高","定安","昌江","屯昌","保亭","白沙","琼中"],
            "吉林":["长春","四平","辽源","松原","吉林","通化","白山","白城","延边"],
            "江苏":["南京","苏州","无锡","连云港","淮安","扬州","泰州","盐城","徐州","常州","南通","镇江","宿迁"],
            "江西":["南昌","九江","鹰潭","抚州","上饶","赣州","吉安","萍乡","景德镇","新余","宜春"],
            "辽宁":["沈阳","大连","盘锦","鞍山","朝阳","锦州","铁岭","丹东","本溪","营口","抚顺","阜新","辽阳","葫芦岛"],
            "内蒙古":["呼和浩特","包头","鄂尔多斯","巴彦淖尔","乌海","阿拉善盟","锡林郭勒盟","赤峰","通辽","呼伦贝尔","乌兰察布","兴安盟"],
            "宁夏":["银川","吴忠","固原","石嘴山","中卫"],
            "青海":["西宁","海西","海东","玉树","海南","海北","黄南","果洛"],
            "上海":["上海"],
            "四川":["成都","宜宾","绵阳","广元","遂宁","巴中","内江","泸州","南充","德阳","乐山","广安","资阳","自贡","攀枝花","达州","雅安","眉山","甘孜","阿坝","凉山"],
            "山东":["济南","滨州","青岛","烟台","临沂","潍坊","淄博","东营","聊城","菏泽","枣庄","德州","威海","济宁","泰安","莱芜","日照"],
            "山西":["太原","大同","长治","忻州","晋中","临汾","运城","晋城","朔州","阳泉","吕梁"],
            "陕西":["西安","铜川","安康","宝鸡","商洛","渭南","汉中","咸阳","榆林","延安"],
            "天津":["天津"],
            "台湾":["台湾"],
            "西藏":["拉萨","日喀则","那曲","林芝","山南","昌都","阿里"],
            "香港":["香港"],
            "新疆":["乌鲁木齐","石河子","吐鲁番","昌吉","哈密","阿克苏","克拉玛依","博尔塔拉","阿勒泰","喀什","和田","巴音郭楞","伊犁","塔城","克孜勒苏柯尔克孜","五家渠","阿拉尔","图木舒克"],
            "云南":["昆明","玉溪","楚雄","大理","昭通","红河","曲靖","丽江","临沧","文山","保山","普洱","西双版纳","德宏","怒江","迪庆"],
            "浙江":["杭州","丽水","金华","温州","台州","衢州","宁波","绍兴","嘉兴","湖州","舟山"],         
            }
    
    getindex(keywords,cities)
    
    
    
    
    
    
    
    
    
    
    
    