import streamlit as st
import matplotlib.pyplot as plt

st.set_page_config(
    page_title="广州汇悦广场，让生活更美好！",
    # page_icon="👋",
    layout='wide',
)

col = st.columns(4)
col_names = ['首页', '销售情况', '客户管理', '会员中心']
col[0].write(col_names[0])
py_names = ['managers.py', 'second.py', 'customer_load.py', ]
for i in range(1, 4):
    with col[i]:
        st.page_link(f"pages/{py_names[i-1]}", label=col_names[i])

st.write("# 欢迎光临广州汇悦广场！ 👋")
st.write(
    '''
    💥广州汇悦广场，你的购物新天堂！🛍️

📍位于繁华的广州市中心，汇悦广场地理位置优越，交通便捷，无论是自驾还是乘坐公共交通，都能轻松抵达。这里汇聚了城市的繁华与便捷，是你不可错过的购物胜地！

🏢规模宏大，占地广阔，汇悦广场拥有多层购物空间，各类品牌店铺琳琅满目，无论是高端奢侈品牌还是亲民实惠的时尚单品，这里都能满足你的需求。无论你是想要享受奢华的购物体验，还是寻找性价比高的好物，汇悦广场都能让你满载而归！

🎉特色鲜明，汇悦广场注重顾客体验，提供了宽敞舒适的购物环境，让你在购物的同时也能享受到轻松愉悦的氛围。商场内还有各种美食餐厅和休闲娱乐设施，让你在购物之余也能品尝到各种美食，享受休闲娱乐的乐趣。

💖总之，广州汇悦广场是一个集购物、餐饮、娱乐于一体的综合性大型商场，无论是和闺蜜一起逛街，还是和家人一起享受亲子时光，这里都是你的不二之选！快来汇悦广场，开启你的购物之旅吧！👣
    '''
)

#%% 多媒体组件
img = plt.imread('./pictures/Inside.jpg')
st.image(img)
