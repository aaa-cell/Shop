import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
plt.style.use('ggplot')
plt.rcParams['font.sans-serif'] = 'SimHei'

st.set_page_config(
    page_title="广州汇悦广场，让生活更美好！", layout='wide',
)
st.write('# 客户中心')

@st.cache_data
def get_data(path):
    vip_data = pd.read_csv(path, encoding='gbk')
    vip_data['消费产生的时间'] = pd.to_datetime(vip_data['消费产生的时间'].str.split('.').str[0])
    return vip_data

vip_data = get_data('./temp/task2.csv')
total_card_ids = vip_data['会员卡号'].unique()
card_id = st.text_input('会员卡号')
# card_id = 'fffa7c0b'
card_pw = st.text_input('密码')
# if st.button('登录'):
if card_id not in total_card_ids or card_pw != 'pw123456':
    st.write('账号或密码错误，请确认后重新尝试！')
else:
    st.write(f'欢迎{card_id}！')
    card_id_data = vip_data.loc[vip_data['会员卡号']==card_id, :]

    col1, col2 = st.columns(2)
    with col1:
        st.write('消费记录')
        year = st.selectbox('年份', [2018, 2017, 2016, 2015])
        month = st.selectbox('月份', list(range(1, 13)))
        tmp = card_id_data.loc[
            (card_id_data['年份']==year) & (card_id_data['月份']==month), :
        ]
        if len(tmp) == 0:
            st.write('本月无消费记录！')
        else:
            tmp2 = tmp[['消费产生的时间', '商品编码', '销售数量', '商品售价', '消费金额', '商品名称',
                        '此次消费的会员积分', '单据号']]
            tmp2.index = range(len(tmp2))
            tmp2 = tmp2.rename(columns={'消费产生的时间':'消费时间', '此次消费的会员积分': '本次积分'})
            st.dataframe(tmp2)

    with col2:
        st.write('消费趋势折线图')
        tmp = pd.DataFrame(
            card_id_data.set_index("消费产生的时间")['消费金额'].resample('1M').sum())
        tmp['time'] = tmp.index.date
        # st.line_chart(tmp.set_index("time"))
        fig = px.bar(tmp, y='消费金额', x='time')
        st.plotly_chart(fig)
