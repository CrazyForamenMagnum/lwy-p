<h1>智联招聘JAVA岗位数据分析</h1>
<h5>1.2数据爬取</h5>
<p>其实写简单的爬虫的步骤都是那几个：打开目标页面，右键-检查-network，刷新页面、观察变化的项目，确认爬虫入口。然后用Python去请求就可以了。</h5>
<p>本次目标网站——智联招聘并没有过多的反爬手段，还是照例先分析一下入口的url：</h5>

```
https://fe-api.zhaopin.com/c/i/sou?&start=0&pageSize=90&cityId=489&workExperience=-1&education=-1&companyType=-1&employmentType=-1&jobWelfareTag=-1&kw=JAVA开发&%%E5%%BC%%80%%E5%%8F%%91&kt=3&=2001&at=65184d91b8214a5295518713d55903c1&rt=c335788de08e4a6c9c7359dea0c15f80&_v=0.77728626&userCode=1021480743&x-zp-page-request-id=77032d662a0e41299828275c286df298-1545722424963-430574
```

<p>需要修改的只有两个地方：<br>
start=0<br>
表示从第0条记录开始<br>
kw=JAVA开发<br>
Kw表示要搜索的岗位的关键词，本次主要分析JAVA开发岗位，所以这一项不用修改。
爬虫代码简单，就不多说了，接下来重点讲数据的整理与数据清洗。</p>
<br>
<h5>1.2数据提取</h5>
<p>我从这些json格式的数据里面提取了公司名、公司类型、公司位置、公司规模、工作名称、工作经验要求、待遇福利、工作薪酬、教育水平要求、职位类型、公司积分这十一个字段，有些字段的格式不是我们想要的，所以要进行整理。</p>
<br>
<h5>1.3数据整理</h5>
<p>首先要动手整理的是薪酬那一列的数据格式，原本的数据格式是6K-8K，除了这些具体到数据的以外，还有“薪酬面议”这种数据的存在，没有办法进行合理的分析。所以要新增三列，分别是最低工资low_salary、最高工资high_salary、以及 平均工资avg_salary，并且将“薪酬面议”全部改成NaN，防止它对后续的数据分析造成太大的误差。</p>

```
for s in df_job['job_salary']:
    if s == '薪资面议':
        low_s = np.nan
        high_s = np.nan
    else:
        low_s = s.split('-')[0].replace('K', '')
        high_s = s.split('-')[1].replace('K', '')
    low_s = float(low_s)*1000
    high_s = float(high_s)*1000
    avg_s = (low_s+high_s)/2
    low_salary.append(low_s)
    high_salary.append(high_s)
    avg_salary.append(avg_s)
df_job['low_salary'] = low_salary
df_job['high_salary'] = high_salary
df_job['avg_salary'] = avg_salary
```

<p>除了这一项数据有问题以外，可以注意到公司所在城市这一项也是很乱，有一些是只显示城市，有一些会带上区县，所以要把他们统一一下，只需要显示到地市即可。</p>

```
citys = []
for loc in df_job['company_loc']:
    if loc.find('-'):
        city = loc.split('-')[0]
    else:
        city = loc
    citys.append(city)
df_job['company_city'] = citys
```

<p>现在可以将dataframe存到一个新的csv中，初步的数据整理已经完毕了。</p>

<h4>2 单因素对工作薪酬的影响</h4>
<h5>2.1 公司城市分布情况</h5>
<p>大家找工作关注的一个重点就是工作的城市了，那么我们就先来看看JAVA开发岗位的城市分布情况吧，这次我选择了更加直观的地图去表现这个岗位在全国各个城市的分布情况，用的还是pyecharts库。<br>
使用pyecharts来画地图的时候不要忘记先把地图包装上，不然是空白一片的。<br>
城市数据十分整洁，不需要再做处理。但是导入的时候发现，还是有几个地图模块上没有记录经纬度的城市，fine，遍历一遍把那些数据删除就可以了。#[‘日本’,’澄迈’,’西平’,’黔西南’,]这几个城市是没有的。</p>

```
city_count = df_job.groupby('company_city')['company_city'].count()
city_data = []
nocoordinate = ['日本', '澄迈', '西平', '黔西南']
for item in zip(city_count.index, city_count.values):
    if item[0] in nocoordinate:
        continue    #跳出循环：遇到不存在经纬度的城市跳过，不用存储到city_data
    city_data.append(item)
#print(city_data)
geo = Geo("公司城市分布情况", "data from ZHILIAN", title_color="#fff", title_pos="center", width=800, height=600,
          background_color='#404a59')
attr, value = geo.cast(city_data)
geo.add("城市分布情况", attr, value, visual_range=[0, 360], visual_text_color="#fff", symbol_size=10, is_visualmap=True)
```

OUTPUT：
<img src="https://github.com/CrazyForamenMagnum/lwy-p/blob/%E6%99%BA%E8%81%94%E6%8B%9B%E8%81%98JAVA%E5%BC%80%E5%8F%91%E5%B2%97%E4%BD%8D%E6%95%B0%E6%8D%AE%E5%88%86%E6%9E%90/3-zl/pic1.png">

为了更直观的了解分布数据的情况，再加上个条形图吧，加条形图的时候发现有些城市只出现了一两次，但是让整个图变得不是太美观，数据都看不清楚，所以我将出现频数在十次以下的城市删除掉了。

```
#公司分布城市统计
#删除出现次数少于10次的城市
for index, value in city_count.items():
    if value < 10:
        city_count = city_count.drop(index)
    else:
        continue
bar_city = Bar("公司分布城市统计")
bar_city.add("城市", city_count.index, city_count.values, is_label_show=True, xaxis_interval=0, xaxis_rotate=-45)
```

OUTPUT：
<img src="https://github.com/CrazyForamenMagnum/lwy-p/blob/%E6%99%BA%E8%81%94%E6%8B%9B%E8%81%98JAVA%E5%BC%80%E5%8F%91%E5%B2%97%E4%BD%8D%E6%95%B0%E6%8D%AE%E5%88%86%E6%9E%90/3-zl/pic2.png">
<p>从地图上可以看出，这个岗位基本分布在东部以及东南部，西部的数量大大少于东部。密集度最高的要数华北、长江三角洲、珠江三角洲，其中深圳市需求最多，有962个岗位，前五名依次是深圳、北京、成都、上海、武汉，据统计结果显示，有70%以上的岗位分布在一线城市。</p>
<br>
<h5>2.2公司规模及公司类型统计</h5>
<p>作为一个应届生，都是想先去大公司锻炼一下，那接下来就来看看JAVA分析这个岗位的公司类型及公司规模吧。</p>
<img src="https://github.com/CrazyForamenMagnum/lwy-p/blob/%E6%99%BA%E8%81%94%E6%8B%9B%E8%81%98JAVA%E5%BC%80%E5%8F%91%E5%B2%97%E4%BD%8D%E6%95%B0%E6%8D%AE%E5%88%86%E6%9E%90/3-zl/pic3.png">
<p>从饼图上可以看出，占比最多的是100-499人，其次就是500-999人，看来做JAVA产品的公司规模普遍都不算太小。<br>
<img src="https://github.com/CrazyForamenMagnum/lwy-p/blob/%E6%99%BA%E8%81%94%E6%8B%9B%E8%81%98JAVA%E5%BC%80%E5%8F%91%E5%B2%97%E4%BD%8D%E6%95%B0%E6%8D%AE%E5%88%86%E6%9E%90/3-zl/pic4.png">
公司类型主要还是集中在民营及股份制企业。</p>
<br>
<h5>2.3不同学历的职位数目</h5>
<img src="https://github.com/CrazyForamenMagnum/lwy-p/blob/%E6%99%BA%E8%81%94%E6%8B%9B%E8%81%98JAVA%E5%BC%80%E5%8F%91%E5%B2%97%E4%BD%8D%E6%95%B0%E6%8D%AE%E5%88%86%E6%9E%90/3-zl/pic5.png">
最低学历要求最多的还是大专，看来JAVA开发岗位招聘还是比较注重技术，学历也不是那么重要的。

<h5>2.4不同经验的岗位需求</h5>
<img src="https://github.com/CrazyForamenMagnum/lwy-p/blob/%E6%99%BA%E8%81%94%E6%8B%9B%E8%81%98JAVA%E5%BC%80%E5%8F%91%E5%B2%97%E4%BD%8D%E6%95%B0%E6%8D%AE%E5%88%86%E6%9E%90/3-zl/pic6.png">

<h5>2.5平均工资分布</h5>
<p>由于平均工资都是具体数值，直接统计太过复杂，先给它们分各组。在4K~20K之间分8组，间隔为2K，加上小于4K和大于20K一共有十个组，遍历平均工资列分组并计数之后即可做出图：</p>

```
def salary_div(salarylist):
    """先将工资分成9个区间"""
    s_4k = 0
    s_4_6k = 0
    s_6_8k = 0
    s_8_10k = 0
    s_10_12k = 0
    s_12_14k = 0
    s_14_16k = 0
    s_16_18k = 0
    s_18_20k = 0
    s_20k = 0
    df_salary_rank = pd.DataFrame(columns=['salary_rank', 'count'])
    df_salary_rank['salary_rank'] = ['<4K', '4~6K', '6~8K', '8~10K', '10~12K', '12~14K', '14~16K', '16~18K', '18~20K',
                                     '>20K']
    for s in salarylist:
        s = int(s)
        if s < 4000:
            s_4k += 1
        if s >= 4000 and s < 6000:
            s_4_6k += 1
        if s >= 6000 and s < 8000:
            s_6_8k += 1
        if s >= 8000 and s < 10000:
            s_8_10k += 1
        if s >= 10000 and s < 12000:
            s_10_12k += 1
        if s >= 12000 and s < 14000:
            s_12_14k += 1
        if s >= 14000 and s < 16000:
            s_14_16k += 1
        if s >= 16000 and s < 18000:
            s_16_18k += 1
        if s >= 18000 and s < 20000:
            s_18_20k += 1
        if s >= 20000:
            s_20k += 1
    df_salary_rank['count'] = [s_4k, s_4_6k, s_6_8k, s_8_10k, s_10_12k, s_12_14k, s_14_16k, s_16_18k, s_18_20k, s_20k]
    return df_salary_rank
```
<img src="https://github.com/CrazyForamenMagnum/lwy-p/blob/%E6%99%BA%E8%81%94%E6%8B%9B%E8%81%98JAVA%E5%BC%80%E5%8F%91%E5%B2%97%E4%BD%8D%E6%95%B0%E6%8D%AE%E5%88%86%E6%9E%90/3-zl/pic7.png">

<p>平均工资主要集中在4~8K，最高的能到20K以上，跨度还是比较大的。<br>
接下来将会针对工作薪酬这个口径做具体深入的分析。</p>
<br>
<h4>3 与工作薪酬相关的属性</h4>
<h5>3.1不同类型的公司的平均月薪</h5>
<p>国企、事业单位一直是大家很向往的工作单位，下面就来看看不同类型的公司的平均薪酬是多少吧。</p>
<img src="https://github.com/CrazyForamenMagnum/lwy-p/blob/%E6%99%BA%E8%81%94%E6%8B%9B%E8%81%98JAVA%E5%BC%80%E5%8F%91%E5%B2%97%E4%BD%8D%E6%95%B0%E6%8D%AE%E5%88%86%E6%9E%90/3-zl/pic8.png">

<p>平均工资最高的是社会团体，最低的是银行，大概是偶然现象吧，因为银行出现的招聘条录只有一条，不具有太大的意义，除去最低的那项，其它公司的平均工资相差都不是太大。</p>
<br>
<h5>3.2不同工作经验对应的平均月薪</h5>
<img src="https://github.com/CrazyForamenMagnum/lwy-p/blob/%E6%99%BA%E8%81%94%E6%8B%9B%E8%81%98JAVA%E5%BC%80%E5%8F%91%E5%B2%97%E4%BD%8D%E6%95%B0%E6%8D%AE%E5%88%86%E6%9E%90/3-zl/pic9.png">
<p>除去“不限”工作经验，平均月薪和工作经验之间有明显的正比例关系，工作经验越长，薪酬也越高。</p>
<p>再把盒图做出来：</p>
<img src="https://github.com/CrazyForamenMagnum/lwy-p/blob/%E6%99%BA%E8%81%94%E6%8B%9B%E8%81%98JAVA%E5%BC%80%E5%8F%91%E5%B2%97%E4%BD%8D%E6%95%B0%E6%8D%AE%E5%88%86%E6%9E%90/3-zl/pic10.png">
<p>此处的盒图有点奇怪，盒图的胡须上限应该是最大观测值，而不是最大值，以5-10年为例：<br>
最大观测值=Q3+1.5（Q3-Q1）=21500+1.5*（21500-14000）=32750，但是图中的胡须去到了60000，大于32750的数据应该用点标出，表示那是离群点。<br>
并且观察到一个比较严重的问题“无经验”的Q1、Q2、Q3是相等的，说明数据源可能存在严重的重复问题。查了原数据发现是有几个公司发了多条重复数据，影响了整个结果。（判断重复的标准：公司名相同、职位描述大同小异、工作地点一样）这里要做的处理是将这个公司的所有数据删除。<br>
有一个公司甚至有800条重复数据，严重影响了分析结果，所以我又将前面的图重新更新了一遍。<br>
之后的结果是这样的：</p>
<img src="https://github.com/CrazyForamenMagnum/lwy-p/blob/%E6%99%BA%E8%81%94%E6%8B%9B%E8%81%98JAVA%E5%BC%80%E5%8F%91%E5%B2%97%E4%BD%8D%E6%95%B0%E6%8D%AE%E5%88%86%E6%9E%90/3-zl/pic11.png">

<h5>3.3学历对月薪的影响</h5>
<img src="https://github.com/CrazyForamenMagnum/lwy-p/blob/%E6%99%BA%E8%81%94%E6%8B%9B%E8%81%98JAVA%E5%BC%80%E5%8F%91%E5%B2%97%E4%BD%8D%E6%95%B0%E6%8D%AE%E5%88%86%E6%9E%90/3-zl/pic12.png">
<p>这里出现了一条问题数据，月薪能高达125K，感觉有点问题，找出原数据看了下：<br>
查了一下这个公司在其他网站的招聘信息，发现是薪酬是10K-15K，是数据录入错误了，修正这条数据，又发现最低工资都是0（可能是NaN？），这里把这些数据都删除掉，以免影响结果。</p>

```
df_job = df_job[~df_job['avg_salary'].isin([125000])]
df_job = df_job[~df_job['avg_salary'].isin([0])]
```

OUTPUT：
<img src="https://github.com/CrazyForamenMagnum/lwy-p/blob/%E6%99%BA%E8%81%94%E6%8B%9B%E8%81%98JAVA%E5%BC%80%E5%8F%91%E5%B2%97%E4%BD%8D%E6%95%B0%E6%8D%AE%E5%88%86%E6%9E%90/3-zl/pic13.png">
<p>结果很耐人寻味，从平均值来看，大专和本科相差不是很大，但是总体来讲本科学历薪酬比大专高，在JAVA开发这个岗位上，硕士研究生的平均工资竟然比本科还要低，最低学历为硕士研究生的条录有8条，大概是因为还是没有足够的样本去进行比较吧。</p>
<p>再看看总体分布：</p>
<img src="https://github.com/CrazyForamenMagnum/lwy-p/blob/%E6%99%BA%E8%81%94%E6%8B%9B%E8%81%98JAVA%E5%BC%80%E5%8F%91%E5%B2%97%E4%BD%8D%E6%95%B0%E6%8D%AE%E5%88%86%E6%9E%90/3-zl/pic14.png">
<br>
<h5>3.4工作城市与月薪的关系</h5>
<img src="https://github.com/CrazyForamenMagnum/lwy-p/blob/%E6%99%BA%E8%81%94%E6%8B%9B%E8%81%98JAVA%E5%BC%80%E5%8F%91%E5%B2%97%E4%BD%8D%E6%95%B0%E6%8D%AE%E5%88%86%E6%9E%90/3-zl/pic15.png">
<p>最高工资的是日本，国内城市最高的是宜宾，比北京和上海还要高一点，接着就是湖州了，但是宜宾和湖州都只有一个岗位，不排除是偶发现象。接下来将国内岗位最多的前6个城市的月薪拿出来分析（深圳、北京、上海、成都、郑州、广州）：</p>
<img src="https://github.com/CrazyForamenMagnum/lwy-p/blob/%E6%99%BA%E8%81%94%E6%8B%9B%E8%81%98JAVA%E5%BC%80%E5%8F%91%E5%B2%97%E4%BD%8D%E6%95%B0%E6%8D%AE%E5%88%86%E6%9E%90/3-zl/pic16.png">
<p>北、上、广、深这四大一线城市的薪酬还是比一般的一线城市要高一点。</p>
<br>
<h5>3.5 学历、工作经验对月薪的影响</h5>
<p>探讨完单方面的因素与工作薪酬之间的关系，再来看看是不是学历高就不需要多工作经验也能有较高的薪酬。
以学历为横轴、工作经验为纵轴，以平均月薪为主要数据，画出热力图：</p>
<img src="https://github.com/CrazyForamenMagnum/lwy-p/blob/%E6%99%BA%E8%81%94%E6%8B%9B%E8%81%98JAVA%E5%BC%80%E5%8F%91%E5%B2%97%E4%BD%8D%E6%95%B0%E6%8D%AE%E5%88%86%E6%9E%90/3-zl/pic17.png">
<p>（中专、中技的数据分布不是足够的均匀，造成数据空缺）<br>
生成的图保存为html格式，可以在网页端打开，交互地显示数据，调整左下角的取值范围可以查看不同范围的数据分布情况：</p>
<img src="https://github.com/CrazyForamenMagnum/lwy-p/blob/%E6%99%BA%E8%81%94%E6%8B%9B%E8%81%98JAVA%E5%BC%80%E5%8F%91%E5%B2%97%E4%BD%8D%E6%95%B0%E6%8D%AE%E5%88%86%E6%9E%90/3-zl/pic18.png">
<p>这里选取了中等至高月薪的区间，很明显是分布在工作年限长、学历相对高的地方。但是不限学历、工作资历较老的招聘岗位月薪也很高。</p>

<h5>3.6 结论</h5>
<p>可以大概得出一个规则：
工作资历长、学历高、工作地点在“超一线城市”的求职者能找到高薪酬工作的几率要更大，公司类型对月薪影响不算大，但是外资公司的薪酬很可观。在JAVA开发这个岗位，如果学历没有优势，那么工作经验就非常重要。</p>

<h5>4 福利待遇</h5>
<p>拿到的数据格式很整齐，直接split分词后就可以计数画图了，由于截取的字段是“关键词”字段，所以会出现一些技能要求，也可以限制一下出现频数，将这些词过滤。</p>
<img src="https://github.com/CrazyForamenMagnum/lwy-p/blob/%E6%99%BA%E8%81%94%E6%8B%9B%E8%81%98JAVA%E5%BC%80%E5%8F%91%E5%B2%97%E4%BD%8D%E6%95%B0%E6%8D%AE%E5%88%86%E6%9E%90/3-zl/pic19.png">
<p>最基本的福利就是五险一金、节日福利、带薪年假、绩效奖金、周末双休。</p>
