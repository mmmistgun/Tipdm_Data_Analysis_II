import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def task2_1():
    # ----------------任务2-1生鲜类商品和一般商品每天销售金额的折线图-----------------
    data_csv = pd.read_csv(r"h:\spider\TASK_A\task1_1.csv", encoding='gbk')
    print(data_csv.columns)

    # 分割数据
    data_csv_sx = data_csv[data_csv['商品类型'] == "生鲜"]
    data_csv_normal = data_csv[data_csv['商品类型'] == "一般商品"]

    data_x_sx = data_csv_sx['销售金额']
    data_x_normal = data_csv_normal['销售金额']
    print(data_x_normal)

    # 根据销售日期分别计算生鲜和一般商品的当日销售额sum
    sx_money_daysum = pd.pivot_table(data=data_csv_sx, index=['销售日期'], values=['销售金额'], fill_value=0,
                                     aggfunc=[np.sum, len])
    normal_meoney_daysum = pd.pivot_table(data=data_csv_normal, index=['销售日期'], values=['销售金额'], fill_value=0,
                                          aggfunc=[np.sum, len])
    a2 = pd.DataFrame({"生鲜类每日销售金额": sx_money_daysum.iloc[:, 0], "一般商品类每日金额": normal_meoney_daysum.iloc[:, 0]})

    plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
    plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号
    sx_money_y = list(a2['生鲜类每日销售金额'])
    normal_money_y = list(a2['一般商品类每日金额'])

    # time_x=list(a2.index)
    plt.plot(a2.index, sx_money_y, label='生鲜类每日销售金额', linewidth=1, color='r', marker='o', markerfacecolor='blue',
             markersize=1)
    plt.plot(a2.index, normal_money_y, label='一般商品类每日金额', linewidth=1, color='g', marker='o', markerfacecolor='red',
             markersize=1)
    plt.xticks(color='blue', rotation=70)  # 此处locs参数与X值数组相同
    plt.xlabel('日期')
    plt.ylabel('每日销售额')
    # plt.xticks(pd.date_range(a2.index[0],a2.index[-1],freq='M'),rotation=75)
    # plt.asix()
    plt.title('生鲜类商品和一般商品每天销售金额的折线图')
    plt.legend()

    plt.show()

    print("task2_1 completed")

def task2_2():
    data_csv = pd.read_csv(r"h:\spider\TASK_A\task1_1.csv", encoding='gbk')

    print("按月分块")
    month = []
    for i in range(0, 4):
        month.append(data_csv[data_csv["销售月份"] == (201501 + i)])

    xiaoshou_money = []
    a2 = []
    for i in range(0, 4):
        xiaoshou_money.append(
            pd.pivot_table(data=month[i], index=["大类名称"], values=["销售金额"], fill_value=0, aggfunc=[np.sum, len]))
        a2.append(pd.DataFrame({"大类名称": xiaoshou_money[i].index, "月销售总额": xiaoshou_money[i].iloc[:, 0]}))
        print(a2[i])

    plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签

    labels = []
    sizes = []
    for i in range(0, 4):
        labels.append(list(a2[i]["大类名称"]))
        sizes.append(list(a2[i]["月销售总额"]))
        plt.pie(sizes[i], labels=labels[i], labeldistance=1.1, autopct='%1.1f%%', shadow=False, startangle=90,
                pctdistance=1.0)
        plt.axis('equal')
        plt.title(str(i + 1) + "月销售金额占比")
        plt.legend()
        # plt.savefig('D:\\工作\\科学比赛\\泰迪杯\\月销售金额占比饼状图\\'+ str(i) + ".png")
        plt.show()

    print("task2_2 completed")


def task2_3():
    ##----------------任务2-3----促销销售金额和非促销销售金额周环比增长率对比柱状图-------------

    #获取数据
    data_csv = pd.read_csv(r"h:\spider\TASK_A\task1_1.csv", encoding='gbk')
    data_csv["销售日期"] = pd.to_datetime(data_csv["销售日期"],format='%Y-%m-%d',errors='coerce')
    data_csv_yes = data_csv[data_csv["是否促销"]=="是"]
    data_csv_no = data_csv[data_csv["是否促销"]=="否"]

    #分割为周
    data_csv_yes["周"] = data_csv['销售日期'].apply(lambda x: x.weekofyear)
    data_csv_no["周"] = data_csv['销售日期'].apply(lambda x: x.weekofyear)

    #生鲜和一般商品分割
    shengxaian_meoney=pd.pivot_table(data=data_csv_yes,index=["周"],values=["销售金额"],fill_value=0,aggfunc=[np.sum])
    yibanmeoney=pd.pivot_table(data=data_csv_no,index=["周"],values=["销售金额"],fill_value=0,aggfunc=[np.sum])
    data_csv_all_sum=pd.DataFrame({"促销销售金额":shengxaian_meoney.iloc[:,0],"非促销销售金额":yibanmeoney.iloc[:,0]})
    print(data_csv_all_sum)

    #print(data_csv_all_sum['促销销售金额'])
    length=len(list(data_csv_all_sum.index))
    print(length)

    discount=list(data_csv_all_sum['促销销售金额'])
    undiscount=list(data_csv_all_sum['非促销销售金额'])
    discount_rate=[]
    undiscount_rate=[]

    #计算促销和非促销的周环比增长率保存到list
    for i in range(1,18):
            discount_rate.append((discount[i]-discount[i-1])/discount[i-1])
            undiscount_rate.append((undiscount[i]-undiscount[i-1])/undiscount[i-1])

    # print(discount_rate)
    # print(undiscount_rate)

    plt.rcParams['font.sans-serif']=['SimHei'] #用来正常显示中文标签
    plt.rcParams['axes.unicode_minus'] =False  # 用来正常显示负号

    bar_width=0.3
    # 将X轴数据改为使用range(len(x_data), 就是0、1、2...
    plt.bar(x=range(1,18), height=discount_rate, label='促销销售金额周环比增长率',color='steelblue', alpha=0.8, width=bar_width)
    # 将X轴数据改为使用np.arange(len(x_data))+bar_width,
    # 就是bar_width、1+bar_width、2+bar_width...这样就和第一个柱状图并列了
    plt.bar(x=np.arange(1,18)+bar_width, height=undiscount_rate,label='非促销销售金额周环比增长率', color='indianred', alpha=0.8, width=bar_width)
    # 在柱状图上显示具体数值, ha参数控制水平对齐方式, va控制垂直对齐方式
    for x, y in enumerate(discount_rate):
        plt.text(x, y + 100, '%s' % y, ha='center', va='bottom')
    for x, y in enumerate(undiscount_rate):
        plt.text(x+bar_width, y + 100, '%s' % y, ha='center', va='top')
    # 设置标题
    plt.title("促销销售金额和非促销销售金额周环比增长率对比")
    # 为两条坐标轴设置名称
    plt.xlabel("第/周")
    plt.ylabel("周环比增长率")
    plt.xlim((0, 18))
    # 显示图例
    plt.legend()
    plt.show()
    print("task2_3 completed")


if __name__ == '__main__':
    task2_1()
    task2_2()
    task2_3()
