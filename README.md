# fuckyouSE
目前使用django4.1（前后端框架）+bootstrap5.3.0-alpha（界面设计）+echarts5.5.0（界面设计）+jquery3.7.1（提供数据传输）
亲测5.3.0-alpha有一丢丢bug，不过目前通过引入稍低版本（5.0.2）的js可以解决
<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha1/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-GLhlTQ8iRABdZLl6O3oVMWSktQOp6b7In1Zl3/Jr59b6EGGoI1aFkw7cmDA6j6gD" crossorigin="anonymous">
<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/js/bootstrap.bundle.min.js" integrity="sha384-MrcW6ZMFYlzcLA8Nl+NtUVF0sA7MsXsP1UyJoMp4YLEuNSfAP+JcXn/tWtIaxVXM" crossorigin="anonymous"></script>
<script src="https://cdn.bootcdn.net/ajax/libs/echarts/5.5.0/echarts.js"></script>
<script src="/js/echarts.js"></script>
<script src="https://code.jquery.com/jquery-3.7.1.min.js" integrity="sha256-/JqT3SQfawRcv/BIHPThkBvs0OEvtFFmqPF/lYI/Cxo=" crossorigin="anonymous"></script>（这玩意本地有点大，需要的话再把本地文件加进去）

20240522战略会议达成以下共识
# 爬取的参数（京东）
啪啪啪：名称，价格，屏幕尺寸，运行内存，机身内存，摄像头（前摄、后摄），电池容量，充电功率，无线充电（有就写功率，无就无），CPU
待定：颜色，OS，上市时间，机身重量

# 爬取的参数（淘宝）
对比界面有：CPU，前摄后摄像素，充电功率，屏幕尺寸，电池容量，上市时间，运存+内存
在第一界面有的：颜色
要通过别的方式得到的：名称，价格

# 评价可视化
词云+天梯图（？）+饼图（？？）

# 运行：
python manage.py 0.0.0.0:8000 （目录：与manage.py同级）
然后访问 http://127.0.0.1:8000/test-mainwindow/
