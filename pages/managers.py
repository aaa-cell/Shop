import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
plt.style.use('ggplot')
plt.rcParams['font.sans-serif'] = 'SimHei'

st.set_page_config(
    page_title="广州汇悦广场，让生活更美好！",
    layout='wide',
)

st.write("# 广州汇悦广场销售情况")
@st.cache_data
def get_data(path):
    # 读取数据
    data = pd.read_csv(path,
                       encoding='gbk',
                       parse_dates=['消费产生的时间','出生日期','登记时间'])

    # 提取会员数据和非会员数据
    vip = data[data['会员卡号'].notnull()]
    nvip = data[data['会员卡号'].isnull()]
    # 删除不在会员信息表出现的会员
    vip_data = vip.dropna()
    # 计算年龄
    dates = vip_data['消费产生的时间'].max()
    vip_data['年龄'] = dates.year - vip_data['出生日期'].dt.year

    return vip_data, nvip

vip_data, nvip = get_data('./temp/task1.csv')
age = vip_data['年龄'].value_counts()
tmp = pd.DataFrame({'age': age.index, 'number': age.values})

# 不同年龄段的消费情况
vip_money = vip_data[['消费金额','年龄']].groupby(by='年龄').sum()

col = st.columns(2)
tab1, tab2 = st.tabs(["VIP年龄分布", "VIP不同年龄段的消费能力"])
with col[0]:
    with tab1:
        st.bar_chart(data=tmp, x='age', y='number')
    with tab2:
        st.line_chart(vip_money)

# 会员的性别占比
sex_count = vip_data['性别'].value_counts()
tmp = pd.DataFrame({
    'label': [{0: '女性', 1: '男性'}[i] for i in sex_count.index],
    'num': sex_count.values
})
fig = px.pie(tmp, values='num', names='label')
fig.update_traces(textposition='inside', textinfo='percent+label')
with col[0]:
    st.write('会员的性别占比')
    st.plotly_chart(fig)

# 会员和非会员订单占比
ordernum = pd.DataFrame({
    'num': [len(vip_data['单据号'].unique()), len(nvip['单据号'].unique())],
    'label': ['VIP', '非VIP'],
})
fig = px.pie(ordernum, values='num', names='label')
fig.update_traces(textposition='inside', textinfo='percent+label')

# 会员和非会员消费金额占比
ordermoney = pd.DataFrame({
    'num': [vip_data['消费金额'].sum(), nvip['消费金额'].sum()],
    'label': ['VIP', '非VIP']
})

fig2 = px.pie(ordermoney, values='num', names='label')
fig2.update_traces(textposition='inside', textinfo='percent+label')

tab1, tab2 = st.tabs(["VIP/非VIP订单占比", "VIP/非VIP的消费金额占比"])
with col[0]:
    with tab1:
        st.plotly_chart(fig, theme='streamlit', use_container_width=True)
    with tab2:
        st.plotly_chart(fig2, theme='streamlit', use_container_width=True)

# 会员年消费趋势
vip_data['年份'] = vip_data['消费产生的时间'].dt.year # 提取年份
vipyear = vip_data.groupby(by='年份').agg({'消费金额':sum, '单据号':np.count_nonzero})
vipyear['单据号'] = vipyear['单据号']/100
vipyear['年份'] = [f'{i}年' for i in vipyear.index]
# 绘制散点气泡图
fig = px.scatter(
    vipyear,
    x="年份",
    size="消费金额",
    y="单据号",
)

with col[1]:
    st.write('消费金额和订单数变化')
    st.plotly_chart(fig, theme='streamlit', use_container_width=True)

tab1, tab2, tab3 = st.tabs([
    "VIP不同年份月份的消费额情况",
    "VIP不同月份的消费人数",
    "VIP消费时间分析"
])
# 会员不同月份的消费人数
vip_data['月份'] = vip_data['消费产生的时间'].dt.month
# 按月统计人数
month_count = vip_data['月份'].value_counts().sort_index()
tmp = pd.DataFrame({'月份': month_count.index,
                    '订单数': month_count.values})
# 会员不同年份月份的消费额情况
# 按年按月统计总消费金额
yeargro = vip_data.groupby(by=['年份','月份'])['消费金额'].sum()
yeargro = yeargro.reset_index()
# 格式转换，按年分组，按月份为行去转格式
yearpivot = pd.pivot_table(yeargro, index='月份', columns='年份', values='消费金额')
# yearpivot.plot.line(title='每年每月的消费情况')
# plt.show()

# 会员消费时间分析
vip_data['时刻'] = vip_data['消费产生的时间'].dt.hour
hour_count = vip_data['时刻'].value_counts().sort_index()
tmp2 = pd.DataFrame({'小时': hour_count.index,
                     '订单数': hour_count.values})

with tab2:
    st.bar_chart(data=tmp, x='月份', y='订单数')
with tab1:
    st.line_chart(yearpivot)
with tab3:
    st.bar_chart(data=tmp2, x='小时', y='订单数')


