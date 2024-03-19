
from Radar import findk, radarplot
import pandas as pd
from  sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler, MinMaxScaler  # 数据标准化

# 读取数据
data = pd.read_csv('./temp/task3.csv', encoding='gbk')

# 筛选数据LRFM
vip_feature = data[['消费次数','最后一次消费距今时长','消费金额','入会时长']]

# 数据标准化
sc = StandardScaler() # 实例化
feature = sc.fit_transform(vip_feature)

# K值寻优,取5类
findk(feature)

# 聚类
model = KMeans(n_clusters=5, random_state=0)
model.fit(feature) # 训练

# 模型结果
# model.cluster_centers_ # 类中心
# model.labels_ # 聚类类别
pd.Series(model.labels_).value_counts() # 数量统计

# 给原始数据添加聚类标签
data['客户类别'] = model.labels_

data.to_csv('./temp/customer.csv', index=None, encoding='utf-8-sig')
radar_data = pd.DataFrame(
    model.cluster_centers_, columns=vip_feature.columns,
).to_csv('./temp/radar_data.csv', index=None, encoding='utf-8-sig')
# 聚类的雷达图
radarplot(model.cluster_centers_, vip_feature.columns)
