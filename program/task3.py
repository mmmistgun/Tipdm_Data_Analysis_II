import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator

def task3_1():
    data_csv = pd.read_csv(r"..\result\task1_1.csv", encoding='gbk')
    xiaoshou_top=pd.pivot_table(data=data_csv,index=["顾客编号"],values=["销售金额"],fill_value=0,aggfunc=[np.sum,len])

    #顾客消费金额降序排列
    a2=pd.DataFrame({"消费总额":xiaoshou_top.iloc[:,0]})
    xiaoshou_sort=a2.sort_values(by="消费总额",ascending=False)
    guke_top10=xiaoshou_sort.head(10)


    #获取前10编号
    head10_bianhao = list(guke_top10.index)
    print(head10_bianhao)
    top1=[]

    #获取这些顾客的消费信息
    for i in range(0,len(head10_bianhao)):
        top1.append(data_csv[data_csv["顾客编号"]==head10_bianhao[i]])

    top1_shangpin=[]
    a3=[]

    for i in range(0,len(head10_bianhao)):
        top1_shangpin.append(pd.pivot_table(data=top1[i],index=["小类名称"],values=["销售金额"],fill_value=0,aggfunc=[np.sum,len]))
        a3.append(pd.DataFrame({"消费总额":top1_shangpin[i].iloc[:,0],"消费数量":top1_shangpin[i].iloc[:,1]}))
        print(a3[i])
        #a4=list(a3.index)


    plt.figure( dpi=120)
    plt.rcParams['font.sans-serif']=['SimHei'] #用来正常显示中文标签
    font = r'C:\Windows\Fonts\simfang.TTF'
    wc = WordCloud(font_path=font, #如果是中文必须要添加这个，否则会显示成框框
                   background_color='white',
                   max_words=200, # 最多显示词数
                   max_font_size=500, # 字体最大值
                   width=1000,
                   height=800,
                   )
    for i in range(0,len(head10_bianhao)):#保存图像
        wc.generate_from_frequencies(a3[i]["消费总额"])
        plt.title("顾客"+str(head10_bianhao[i])+"画像")
        plt.imshow(wc)  #用plt显示图片
        plt.axis('off') #不显示坐标轴
        plt.show()
        # plt.savefig('D:\\工作\\科学比赛\\泰迪杯\\消费前十顾客画像\\'+ str(i) + ".png")
    print("task3_1 complete")

def task3_2():
    # ===================任务3-2===分析各大类的销售情况并分析============
    data_csv = pd.read_csv(r"..\result\task1_1.csv", encoding='gbk')
    # data_csv = pd.DataFrame(data_csv)
    print(data_csv.columns)
    data_csv_bigclass = data_csv['大类名称']
    print(data_csv_bigclass)
    # 通过集合去重获取大类的名称
    big_class_set = list(set(data_csv_bigclass))

    # 循环分类 总表分割获取各个大类独自对应的内容
    save_class = []
    for i in range(0, len(big_class_set)):
        save_class.append(data_csv[data_csv['大类名称'] == big_class_set[i]])
    data_all_list = []
    merge_data = []

    # 计算各个大类的每日总销售额
    for i in range(0, len(big_class_set)):  # values=['销售金额']可以获得当日销售总额
        data_all_list.append(
            pd.pivot_table(data=save_class[i], index=['销售日期'], values=['销售数量'], fill_value=0, aggfunc=[np.sum, len]))
    print(data_all_list)

    # -----------------------画图-------------------------------
    plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
    plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号
    # 循环画图 根据类的个数
    for i in range(0, len(big_class_set)):
        # 日期用sort_value()排序
        plt.plot(data_all_list[i].index.sort_values(), data_all_list[i].iloc[:, 0], label=big_class_set[i], linewidth=1,
                 marker='o', markerfacecolor='red', markersize=1)

    plt.xticks(color='black', rotation=70)  # 此处locs参数与X值数组相同
    plt.xlabel('日期')
    plt.ylabel('各大类每日销售总数量')
    # plt.asix()
    plt.title('各大类商品的销售总数量折线图')
    plt.legend()
    plt.show()
    print("task3_2 complete")

def task3_3():
    data_csv = pd.read_csv(r"..\result\task1_1.csv", encoding='gbk')

    chuxiao_dalei = data_csv[data_csv["是否促销"] == "是"]
    chuxiao = pd.pivot_table(data=chuxiao_dalei, index=["大类名称"], values=["销售金额"], fill_value=0, aggfunc=[np.sum, len])
    chuxiao_name = list(chuxiao.index)
    print(chuxiao_name)

    dalei_yes = []
    dalei_no = []
    xiaoshou_money = []
    xiaoshou_money2 = []
    for i in range(0, len(chuxiao_name)):
        dalei_yes.append(data_csv[(data_csv["大类名称"] == chuxiao_name[i]) & (data_csv["是否促销"] == "是")])
        riqi1 = len(dalei_yes[i]["销售日期"].to_list())
        xiaoshou_money.append(dalei_yes[i]["销售金额"].sum() / riqi1)

        dalei_no.append(data_csv[(data_csv["大类名称"] == chuxiao_name[i]) & (data_csv["是否促销"] == "否")])
        riqi2 = len(dalei_no[i]["销售日期"].to_list())
        xiaoshou_money2.append(dalei_no[i]["销售金额"].sum() / riqi2)

    print(xiaoshou_money)
    print('\n')
    print(xiaoshou_money2)

    plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
    plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号

    bar_width = 0.4
    # 将X轴数据改为使用range(len(x_data), 就是0、1、2...
    plt.bar(chuxiao.index, height=xiaoshou_money2, label='促销日均销售金额', color='indianred', alpha=0.8, width=bar_width)
    # 将X轴数据改为使用np.arange(len(x_data))+bar_width,
    # 就是bar_width、1+bar_width、2+bar_width...这样就和第一个柱状图并列了
    plt.bar(x=np.arange(0, 10) + bar_width, height=xiaoshou_money, label='非促销日均销售金额', color='steelblue', alpha=0.8,
            width=bar_width)

    # 设置标题
    plt.title("促销日均销售金额和非促销日均销售金额对比")
    # 为两条坐标轴设置名称
    plt.xlabel("大类名称")
    plt.ylabel("日均销售金额")
    plt.xlim((-1, 11))

    # 显示图例
    plt.legend()
    plt.show()
    print("task3_3 complete")

if __name__ == '__main__':
    task3_1()
    task3_2()
    task3_3()


