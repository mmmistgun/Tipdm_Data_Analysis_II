import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def task1_1():
    data_csv = pd.read_csv(r"../result/附件.csv", encoding='gbk')
    print(data_csv.columns)
    print("原始数据数量" + str(len(data_csv)))
    print("\n")

    print("数据去重后")
    data_csv.drop_duplicates(inplace=True)
    print(len(data_csv))
    print("\n")

    print("去空值")
    print(data_csv.isnull().sum())
    data_csv = data_csv.dropna(how='any')
    print(len(data_csv))
    print("\n")

    # 数据标准化
    data_csv["销售金额"] = data_csv["销售金额"].round(decimals=5)


    print("数据合法性")
    # 日期合法性
    data_csv["销售日期"] = pd.to_datetime(data_csv["销售日期"],format='%Y%m%d',errors='coerce')
    print(data_csv.isnull().sum())
    data_csv = data_csv.dropna(how='any')
    print(len(data_csv))
    print("\n")

    # 验证销售金额于单价和数量
    data_csv_check = data_csv[data_csv["是否促销"]=='否'].eval('应付减实付 =(商品单价*销售数量 - 销售金额)')
    print(data_csv_check[data_csv_check["应付减实付"] > 1]["大类名称"].value_counts())

    # 删除商品总额为零的数据
    print("商品总额为零的数据")
    data_csv = data_csv.drop(data_csv[data_csv["销售金额"] == 0].index)
    print(len(data_csv))
    print("\n")

    # 由此可知销售金额为负，销售数量为负，设为退款
    xiaoshoujine_fushu = data_csv[data_csv["销售金额"] < 0]
    xiaoshoushuliang_fushu = data_csv[data_csv["销售数量"] < 0]
    print((xiaoshoujine_fushu == xiaoshoushuliang_fushu).sum())
    print("\n")


    # 匹配出退款订单,并删除
    for i in range (len(xiaoshoushuliang_fushu)):
        data_csv.drop(data_csv[
                          (data_csv["顾客编号"] == list(xiaoshoushuliang_fushu["顾客编号"])[i]) &
                          (data_csv["小类名称"] == list(xiaoshoushuliang_fushu["小类名称"])[i]) &
                          (abs(data_csv["销售金额"]) == abs(list(xiaoshoushuliang_fushu["销售金额"])[i]))
                      ].index, inplace=True)
    print(len(data_csv))


    print("去冗余，交叉验证")
    print(pd.crosstab(data_csv['小类编码'],data_csv["商品编码"],margins_name=True))
    print("\n")
    print(pd.crosstab(data_csv['小类编码'],data_csv["小类名称"],margins_name=True))
    print(pd.crosstab(data_csv['中类编码'],data_csv["中类名称"],margins_name=True))
    print(pd.crosstab(data_csv['大类编码'],data_csv["大类名称"],margins_name=True))

    data_csv.to_csv(r"../result/task1_1.csv", index=False,index_label=False,encoding='gbk')
    print("task1_1 completed")


def task1_2():
    data_csv = pd.read_csv(r"../result/task1_1.csv", encoding='gbk')
    xiaoshou_money = pd.pivot_table(data=data_csv, index=["大类名称"], values=["销售金额"], fill_value=0, aggfunc=[np.sum, len])
    data_csv_all_sum = pd.DataFrame({"大类名称": xiaoshou_money.index, "总销售总额": xiaoshou_money.iloc[:, 0]})
    data_csv_all_sum.to_csv(r"../result/task1_2.csv", index=False, encoding='gbk')
    print("task1_2 completed")



def task1_3():
    data_csv = pd.read_csv(r"../result/task1_1.csv", encoding='gbk')

    # 按是否促销
    data_csv_yes = data_csv[data_csv["是否促销"] == '是']
    data_csv_no = data_csv[data_csv["是否促销"] == '否']

    # 按中类名称
    yes_mid_meoney = pd.pivot_table(data=data_csv_yes, index=["中类名称"], values=["销售金额"], fill_value=0,
                                    aggfunc=[np.sum, len])
    no_mid_meoney = pd.pivot_table(data=data_csv_no, index=["中类名称"], values=["销售金额"], fill_value=0,
                                   aggfunc=[np.sum, len])
    # 合并促销和非促销
    data_csv_all_sum = pd.DataFrame({"促销销售金额": yes_mid_meoney.iloc[:, 0], "非促销销售金额": no_mid_meoney.iloc[:, 0]})

    data_csv_all_sum.fillna(0, inplace=True)
    data_csv_all_sum.to_csv(r"../result/task1_3.csv", encoding='gbk')
    print("task1_3 completed")


def task1_4():
    data_csv = pd.read_csv(r"../result/task1_1.csv", encoding='gbk')

    data_csv["销售日期"] = pd.to_datetime(data_csv["销售日期"], format='%Y-%m-%d', errors='coerce')

    data_csv_shengxian = data_csv[data_csv["商品类型"] == "生鲜"]
    data_csv_yiban = data_csv[data_csv["商品类型"] == "一般商品"]

    data_csv_shengxian["周"] = data_csv['销售日期'].apply(lambda x: x.weekofyear)
    data_csv_yiban["周"] = data_csv['销售日期'].apply(lambda x: x.weekofyear)

    shengxaian_meoney = pd.pivot_table(data=data_csv_shengxian, index=["周"], values=["销售金额"], fill_value=0,aggfunc=[np.sum])
    yibanmeoney = pd.pivot_table(data=data_csv_yiban, index=["周"], values=["销售金额"], fill_value=0, aggfunc=[np.sum])

    data_csv_all_sum = pd.DataFrame({"生鲜销售金额": shengxaian_meoney.iloc[:, 0], "一般商品销售金额": yibanmeoney.iloc[:, 0]})

    data_csv_all_sum.fillna(0, inplace=True)
    data_csv_all_sum.to_csv(r"../result/task1_4.csv", encoding='gbk')
    print("task1_4 completed")

def task1_5():
    data_csv = pd.read_csv(r"../result/task1_1.csv", encoding='gbk')

    print("按月分")
    month1 = data_csv[data_csv["销售月份"] == 201501]
    month2 = data_csv[data_csv["销售月份"] == 201502]
    month3 = data_csv[data_csv["销售月份"] == 201503]
    month4 = data_csv[data_csv["销售月份"] == 201504]

    def get_times(all_day):
        return len(np.unique(all_day))


    guke_month1 = pd.pivot_table(data=month1, index=["顾客编号"], values=["销售金额"], fill_value=0, aggfunc=[np.sum])
    guke_month1_time = pd.pivot_table(data=month1, index=["顾客编号"], values=["销售日期"], fill_value=0, aggfunc=[get_times])
    print(guke_month1_time)

    # guke_month_1=pd.DataFrame({"月销售总额":guke_month1.iloc[:,0],"消费天数":guke_month1.iloc[:,1]})

    guke_month2 = pd.pivot_table(data=month2, index=["顾客编号"], values=["销售金额"], fill_value=0, aggfunc=[np.sum])
    guke_month2_time = pd.pivot_table(data=month2, index=["顾客编号"], values=["销售日期"], fill_value=0, aggfunc=[get_times])
    print(guke_month2_time)
    # guke_month_2=pd.DataFrame({"月销售总额":guke_month2.iloc[:,0],"消费天数":guke_month2.iloc[:,1]})

    guke_month3 = pd.pivot_table(data=month3, index=["顾客编号"], values=["销售金额"], fill_value=0, aggfunc=[np.sum])
    guke_month3_time = pd.pivot_table(data=month3, index=["顾客编号"], values=["销售日期"], fill_value=0, aggfunc=[get_times])
    print(guke_month3_time)
    # guke_month_3=pd.DataFrame({"月销售总额":guke_month3.iloc[:,0],"消费天数":guke_month3.iloc[:,1]})

    guke_month4 = pd.pivot_table(data=month4, index=["顾客编号"], values=["销售金额"], fill_value=0, aggfunc=[np.sum])
    guke_month4_time = pd.pivot_table(data=month4, index=["顾客编号"], values=["销售日期"], fill_value=0, aggfunc=[get_times])
    print(guke_month4_time)
    # guke_month_4=pd.DataFrame({"月销售总额":guke_month4.iloc[:,0],"消费天数":guke_month4.iloc[:,1]})

    guke = pd.DataFrame({"1月销售总额": guke_month1.iloc[:, 0], "1月消费天数": guke_month1_time.iloc[:, 0],
                         "2月销售总额": guke_month2.iloc[:, 0], "2月消费天数": guke_month2_time.iloc[:, 0],
                         "3月销售总额": guke_month3.iloc[:, 0], "3月消费天数": guke_month3_time.iloc[:, 0],
                         "4月销售总额": guke_month4.iloc[:, 0], "4月消费天数": guke_month4_time.iloc[:, 0]})
    guke.fillna(0,inplace=True)
    print(guke.head(11))
    guke = guke.fillna(0)
    guke.to_csv(r"../result/task1_5.csv", encoding='gbk')
    print("task1_5 completed")


if __name__ == '__main__':
    task1_1()
    task1_2()
    task1_3()
    task1_4()
    task1_5()