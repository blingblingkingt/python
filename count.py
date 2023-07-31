import pandas as pd
import numpy as np

print("请在此程序文件夹下，将需要编辑的表格命名为：ip统计.xlsx,将需要筛选的互联网出口.xlsx放在同级")
input("按回车建继续")

# 读取原始数据表格
df = pd.read_excel('ip统计.xlsx')

# 删除一级告警类型列
# 删除一级警告类型，按列操作，在原始数据进行修改，如果按行操作，为axis=0
df.drop('一级告警类型', axis=1, inplace=True)

# 过滤互联网出口ip的b段(弱智行为)
df['攻击IP'] = df['攻击IP'].str.replace('^210\.72.*', '', regex=True)
df['攻击IP'] = df['攻击IP'].str.replace('^211\.99.*', '', regex=True)
df['攻击IP'] = df['攻击IP'].str.replace('^211\.160.*', '', regex=True)
df['攻击IP'] = df['攻击IP'].str.replace('112.30.39.71', '', regex=True)
df['攻击IP'] = df['攻击IP'].str.replace('36.17.137.159', '', regex=True)
df['攻击IP'] = df['攻击IP'].str.replace('^220\.178.*', '', regex=True)
df['攻击IP'] = df['攻击IP'].str.replace('^36\.33\.26.*', '', regex=True)
df['攻击IP'] = df['攻击IP'].str.replace('^220\.178.*', '', regex=True)
df['攻击IP'] = df['攻击IP'].str.replace('^220\.248.*', '', regex=True)
df['攻击IP'] = df['攻击IP'].str.replace('^36\.7\.130.*', '', regex=True)
df['攻击IP'] = df['攻击IP'].str.replace('182.150.56.83', '', regex=True)
df['攻击IP'] = df['攻击IP'].str.replace('^221\.237\.156.*', '', regex=True)
df['攻击IP'] = df['攻击IP'].str.replace('^125\.70.*', '', regex=True)
df['攻击IP'] = df['攻击IP'].str.replace('^180\.213.*', '', regex=True)
df['攻击IP'] = df['攻击IP'].str.replace('^106\.38\.78.*', '', regex=True)
df['攻击IP'] = df['攻击IP'].str.replace('^106\.39\.98.*', '', regex=True)
df['攻击IP'] = df['攻击IP'].str.replace('^106\.39\.125.*', '', regex=True)
df['攻击IP'] = df['攻击IP'].str.replace('123.151.198.229', '', regex=True)
df['攻击IP'] = df['攻击IP'].str.replace('60.26.123.151', '', regex=True)
df['攻击IP'] = df['攻击IP'].str.replace('220.250.1.50', '', regex=True)
df['攻击IP'] = df['攻击IP'].str.replace('^112\.48\.25.*', '', regex=True)
df['攻击IP'] = df['攻击IP'].str.replace('^117\.157\.78.*', '', regex=True)
df['攻击IP'] = df['攻击IP'].str.replace('118.212.69.39', '', regex=True)
df['攻击IP'] = df['攻击IP'].str.replace('^10\.137.*', '', regex=True)
df['攻击IP'] = df['攻击IP'].str.replace('^10\.138.*', '', regex=True)
df['攻击IP'] = df['攻击IP'].str.replace('^192\.168.*', '', regex=True)
df['攻击IP'] = df['攻击IP'].str.replace('^172\.16.*', '', regex=True)
df['攻击IP'] = df['攻击IP'].str.replace('^172\.17.*', '', regex=True)
# 筛选攻击IP列的数据并去重，去掉空白和重复数据

# 使用str.strip()方法去除每个元素的首尾空白字符，并将修改后的结果赋值给"攻击IP"列。
df['攻击IP'] = df['攻击IP'].str.strip()
# 使用replace()方法将空字符串（''）替换为NaN（缺失值）
df['攻击IP'].replace('', np.nan, inplace=True)
# 使用dropna()方法删除包含缺失值（NaN）的行。通过设置subset参数为['攻击IP']，只针对"攻击IP"列进行缺失值检查和删除。
df.dropna(subset=['攻击IP'], inplace=True)
# 对DataFrame中的"攻击IP"列进行操作，使用drop_duplicates()方法删除重复的行。通过设置subset参数为['攻击IP']，只针对"攻击IP"列进行重复值检查和删除。
df.drop_duplicates(subset=['攻击IP'], inplace=True)

# 去掉攻击IP列中192.168和172.16开头的数据
# df = df[~df['攻击IP'].str.startswith('192.168')]
# df = df[~df['攻击IP'].str.startswith('172.16')]
# df = df[~df['攻击IP'].str.startswith('172.17')]

# 读取互联网出口的表格中出口ip列的数据
# outbound_df = pd.read_excel('互联网出口.xlsx')
# outbound_ips = outbound_df['出口ip'].tolist()

# 在ip统计表格中攻击IP列中进行对比，把找到的一整行数据进行删除
# df = df[~df['攻击IP'].isin(outbound_ips)]

# 受害IP：替换192.168开头的ip和172.16开头的ip替换为210.72.240.12
df['受害IP'] = df['受害IP'].str.replace('^192\.168.*', '210.72.240.12', regex=True)
df['受害IP'] = df['受害IP'].str.replace('^172\.16.*', '210.72.240.12', regex=True)
df['受害IP'] = df['受害IP'].str.replace('^172\.17.*', '210.72.240.12', regex=True)
# 按时间排序
df.sort_values(by='最近发生时间', inplace=True)

# 修改列名称
df = df.rename(columns={'受害IP': '被攻击系统ip'})
df = df.rename(columns={'攻击IP': '攻击源ip'})
df = df.rename(columns={'最近发生时间': '攻击时间'})
df = df.rename(columns={'二级告警类型': '攻击类型'})
# 在第一列之前插入一列网络区域，默认值欸互联网大区
df.insert(1, '网络区域', '互联网大区')
# 在网络区域列后插入一列"被攻击系统"，默认值为空
df.insert(df.columns.get_loc('网络区域')+1, '被攻击系统', '')

# 重命名原来的攻击时间列为 "原攻击时间"
df.rename(columns={"攻击时间": "原攻击时间"}, inplace=True)

# 将原攻击时间列移动到攻击源 IP 列后边
df.insert(df.columns.get_loc("攻击源ip")+1, "攻击时间", df["原攻击时间"])

# 删除原来的攻击时间列
df.drop("原攻击时间", axis=1, inplace=True)


# 输出处理后的数据表格
df.to_excel('处理后的数据表格.xlsx', index=False)

print("生成：处理后的数据表格.xlsx")
