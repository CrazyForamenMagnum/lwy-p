<h1>淘宝某商品平均数据分析</h1>
<h4>1.1 数据爬取</h4>
<p>想要爬取天猫某品牌电视机的买家评论等相关信息，首先打开代码检查页面，在network下，不断加载新的评论页面，观察“Name”列文件的变化</p>
<img src="https://github.com/CrazyForamenMagnum/lwy-s/blob/master/Desktop/%E5%9B%BE%E7%89%87/1-tb/pic1.png"/>
<p>找到爬虫入口，通过Preview确定有我们想要的数据以后，切换回Headers页面找到入口的URL，并对URL的组成进行分析，去掉不重要的部分，发现淘宝评论的json数据全部在
    
```    
https://rate.taobao.com/feedRateList.htm?auctionNumId=546651887101&currentPageNum=1
```

其中auctionNumId即该商品ID，currentPageNum则是第几页评论的内容。通过循环改变currentPageNum即可爬取评论数据json文件。</p>
<p>接下来就可以正式写爬虫了，听说淘宝反爬技术很厉害，所以先爬几页试试：</p>

```
for i in range(1, 6):
    currentPage = i + 1
    url = 'https://rate.taobao.com/feedRateList.htm?auctionNumId=546651887101%s' % \
          ('&currentPageNum=' + str(currentPage))
 
    # 获取数据
    response = requests.get(url, headers=headers).text
    print(response)
```

发现只有两页能爬，第三页就变成了验证码页面。
用第三方库fake_useragent构造headers：

```
from fake_useragent import UserAgent
ua = UserAgent()
headers = {"User-Agent": ua.random}
```

<p>再找几个代理IP，注意如果目标页面是https就要找https的代理IP：</p>

```
ip = [/*略*/]
choice = random.choice(ip)
proxies = {"http": "http://"+choice, "https": "https://"+choice}
response = requests.get(url, headers=headers, proxies=proxies).text
```

<p>设置一个页面随机休眠，防止别人监察到爬虫：</p>

```
if currentPage % 5 == 0:
    time.sleep(random.randint(0, 10))
```

<p>折腾了许久终于拿到了些许数据，我的个人习惯是先将json数据爬取下来再用pandas库做数据提取，所以之前requests下来的数据都存在一个txt文件中（也可以是存在csv文件，怎么方便怎么来）</p>
<img src="https://github.com/CrazyForamenMagnum/lwy-s/blob/master/Desktop/%E5%9B%BE%E7%89%87/1-tb/pic2.png" />
<br>
<h4>1.2数据提取</h4>
<p>其实数据的存储也是很有规律的，每一页评论的json文件都只会占一行，所以读取文件的时候逐行读取就可以了。</p>

```
file = open('response1.txt', mode='r', encoding='utf-8')
tb_contents = pd.DataFrame(columns=['No', 'date', 'nick', 'rank', 'sku', 'content'])
for i in range(0, 97):
    response = file.readline()
    if response.startswith(u'\ufeff'):
        response = response.encode('utf8')[3:].decode('utf8')//不加就报错，同globals
    globals = {
        'true': 0,
        'false': 0,
        'null': 0
    }    #之前一直json.loads不成功，查了资料说要加上这个globals
    dict = json.loads(response)  #字符串->dict
```

<p>在提取数据之前还要先进行文件结构分析，看一下想要的信息存放在那个节点下。这次我主要是想要买家的购买日期、昵称、淘宝等级积分、购买套餐类型、评论内容，不难发现他们分别在“comments”下：</p>

```
cmntlist = dict["comments"]
for cmnt in cmntlist:
date = cmnt["date"]   #购买日期
nick = cmnt["user"]["nick"]    #买家昵称
rank = cmnt["user"]["rank"]	   #淘宝等级积分
sku = cmnt["auction"]["sku"]   #购买套餐类型
content = cmnt["content"]	#评论内容
tb_contents = tb_contents.append({'No': len(tb_contents)+1, 'date': date, 'nick': nick, 'rank': rank, 'sku': sku, 'content': content},
                                 ignore_index=True)
存到一个csv文件下，方便数据分析
tb_contents.to_csv('tb_comments.csv', encoding='utf_8_sig')
```

<br>
<h4>2.1商品销量走势分析</h4>
<p>通过pandas库简单的groupby以后，用pyecharts的Bar、Line做出每日评论数的走势图：</p>
<img src="https://github.com/CrazyForamenMagnum/lwy-s/blob/master/Desktop/%E5%9B%BE%E7%89%87/1-tb/pic3.png" />
<p>不难发现，在11月17日以前日均评论只有一条多一点，从17号就开始越来越多。</p>
<p>每个用户从购买商品、签收商品、正式安装使用，加上11月11日是大型购物节，由于订单数目骤然增加，电商们发货速度有所下降、物流速度下降，用户正式收到货物并使用、登录平台进行评价的平均时间间隔有所延长，所以有理由推测11月17日以后增多的买家评论购买时间都是在11月11日，统计从11月17日至下一个购物节12月12日之间的评论数已经高达1570条，相比17日之前的评论数目，增幅相当的大。有理由说明“双十一”大大促进了电商的订单成交数。</p>
<br>
<h4>2.2买家评论的情感打分及商品综合评分</h4>
<p>Python有一个第三方库（snownlp），专门对电商的买家评论进行情感打分。</p>

```
def setiment(content):
    s = SnowNLP(content)
    return s.sentiments
df['setiment'] = df['content'].apply(setiment)
```
<p>简单调用即可对每一条买家评论进行打分，越接近1表示正面情绪，越接近0表示负面情绪。</p>

```
0       0.000000e+00
1       1.000000e+00
2       9.997915e-01
3       1.454280e-01
4       5.692152e-04
5       9.798498e-01
```

<p>简单抽选几条评分结果对照评论原文：</p>

```

Index=7 
真心觉得这个电视差极了，那么多好评不知道怎么刷出来的！就电视来说，一个小指头点晃悠这么厉害，找客服说退货她说得自己出三百运费，这明明底座不行就是产品问题，非得让我花钱挂墙壁上，那有支架为什么不能用，你们就不能提高产品质量吗？小米真垃圾！收货第二天就要求退货，结果他们七拖八欠的，最后说什么过了七天退货期，我说产品质量不好换货吧，她又说无理由！还小米官方旗舰店，垃圾！我挣钱容易吗，非得让我花三百退货！！！
情绪评分：0.000000e+00
Index=14
第一次上网买这么大件的产品，第一次双十一熬夜剁手，这个小米电视还是承载了很多瞬间的。有意义。小米的售前售后总体都做的比较让人满意。电视质量也很好，小米盒子内置，桌面看起来干净清爽。画质也不错，音效也可以。这个价钱算是性价比超高
情绪评分： 1.000000e+00
Index=26
敲重点注意买的时候的需求 重点是性价比 不要想着画质好 电视硬件配置会高 音质强什么的都是虚无的东西 买的就是一个字 大 还相对便宜 对画质有要求的建议换一家可能不会让你太满意 对音质有要求的 嘿嘿嘿 小米电视音箱了解一下.可以安慰一下自己不要想太多系统不舒服 需求：大 便宜！
情绪评分：9.999889e-01
```

<p>总体来说评分准确率还是比较高的，为了让商品综合评分更科学，这里运用了淘宝会员等级积分为评论内容打分加权求平均的方法去求得该商品的综合评分：</p>

```
rank_list = df['rank'].values.tolist()
max_rank = max(rank_list)
Grade = []
rank = 0
self_grade = 0
good_grade = 0
len = df.shape[0]
for index, row in df.iterrows():
    rank = row['rank']/max_rank    #将等级积分归一
    self_grade = row['setiment']*rank*100    #为了结果更具可理解性，乘以100
    Grade.append(self_grade)
good_grade = sum(Grade)/len
```

<p>OUTPUT:该商品综合分数为： 6.0198448335820185/10</p>
<br>
<h4>2.3买家评论的高频词汇统计及词云图</h4>
<p>要进行高频词统计要先进行分词，这里采取jieba分词：</p>

```
all_content = df['content'].tolist()
segments = []
for line in all_content:
    try:
        segs = jieba.lcut(line)
        for seg in segs:
            if len(seg) > 1 and seg !='\r\n':
                segments.append(seg)
            print(seg)
    except:
        print(line)
        continue

words_df = pd.DataFrame({"segment": segments})
#加了一列计数列 .agg()
words_stat = words_df.groupby('segment')['segment'].agg({"计数": np.size})   words_stat = words_stat.reset_index().sort_values(by=["计数"], ascending=False)
```

<p>结果：</p>
<img src="https://github.com/CrazyForamenMagnum/lwy-s/blob/master/Desktop/%E5%9B%BE%E7%89%87/1-tb/pic4.png"/>
