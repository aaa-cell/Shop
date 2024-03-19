import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
from wordcloud import WordCloud
plt.style.use('ggplot')
plt.rcParams['font.sans-serif'] = 'SimHei'

st.set_page_config(
    page_title="广州汇悦广场，让生活更美好！",
    layout='wide',
)

st.write('# 客户管理')
radar_data = pd.read_csv('./temp/radar_data.csv').T
data = pd.read_csv('./temp/customer.csv')
names = ["一般价值客户", "低价值客户", "流失客户", "重要发展客户", "重要保持客户"]

# 数据处理
data['年龄'] = data['年龄'].astype(str)+'岁'
data['入会时长'] = '入会' + data['入会时长'].astype(str) + '天'
data['消费次数'] = '消费' + data['消费次数'].astype(str) + '次'
data['消费金额'] = '消费' + data['消费金额'].astype(int).astype(str) + '元'
data['最后一次消费距今时长'] = '最后一次距今' + data['最后一次消费距今时长'].astype(str) + '天'
data['客户类别'] = data['客户类别'].map({i:j for i, j in enumerate(names)})
data['此次消费的会员积分'] = data['此次消费的会员积分'].astype(int)
data['平均每单金额'] = data['平均每单金额'].astype(int)
total_card_ids = data['会员卡号'].unique()
categories = radar_data.index
fig = go.Figure()
for i in radar_data.columns:
    fig.add_trace(go.Scatterpolar(
          r=radar_data[i].values,
          theta=categories,
          fill='toself',
          name=names[i]
    ))
fig.update_layout(
  polar=dict(
    radialaxis=dict(
      visible=True,
      range=[radar_data.values.min(), radar_data.values.max()]
    )),
  # showlegend=False
)
col1, col2 = st.columns(2)
with col1:
    st.plotly_chart(fig)

with col2:
    card_id = st.text_input('会员卡号')
    if card_id not in total_card_ids and card_id!="":
        st.write('输入错误，请确认后重新尝试！')
    elif card_id in total_card_ids:
        # 数据筛选，取某个会员为例
        samples = data.loc[data['会员卡号'] == card_id, :]
        del samples['此次消费的会员积分'], samples['平均每单金额']
        # 转化，把特征标签全部合并为一句话，用空格分割
        texts = ' '.join(list(samples.values[0]))
        fig, ax = plt.subplots()
        # 绘制词云图
        wc = WordCloud(background_color='white', font_path='./data/msyh.ttc')
        # 把字符串处理为绘图的形式，词+词频
        words = wc.generate(texts)
        ax.imshow(words)
        ax.axis('off')
        st.pyplot(fig)

options = st.multiselect(
    '客户群体',  names)
ind = data['客户类别'].apply(lambda x: x in options)
# edited_df = st.data_editor(data.loc[ind, :])
st.dataframe(data.loc[ind, :])



