import pandas as pd
import datetime
from matplotlib import pyplot as plt

df = pd.read_csv(r'.btctradeCNY.csv', names=['timestamp', 'price', 'volume'])

# 时间戳转化为日期格式
for i in range(len(df)):
    timestamp = df.loc[i]['timestamp']
    a = int(timestamp)
    date = datetime.datetime.utcfromtimestamp(a)
    NewDate = date.strftime("%Y-%m-%d %H:%M:%S")
    df.loc[i, 'timestamp'] = NewDate
    df.loc[i, 'YM'] = date.strftime("%Y-%m")

# 去重
df1 = df.drop_duplicates(['timestamp', 'price', 'volume'], keep='last')

# 删除部分数据
li = df1[(df1['price'] == 0)].index.tolist()
df2 = df1.drop(li)

df2.to_csv(r'result_sbi.csv', encoding='gbk')
dic = {}
dic1 = {}
grouped = df2.groupby('YM')
for month, group in grouped:
    dic[month] = group.volume.sum()
    dic1[month] = group.price
result = max(dic.items(), key=lambda x: x[1])
print(f"合计交易量（volume）最大的月份是{result[0]},数据为{round(result[1], 3)}")

# 绘制交易量最大月份得价格曲线图
# 设置中文字体
plt.rcParams['font.sans-serif'] = ['simhei']
plt.title(result[0] + '的价格曲线图')
plt.xlabel(result[0])
plt.ylabel("price")

y = []
for p in dic1[result[0]]:
    y.append(p)
x = list(range(1, len(y) + 1))

plt.plot(x, y)
plt.xticks([])
plt.show()
