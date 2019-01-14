<h1>北京积分落户人员信息分析</h1>
<h5>1整理数据</h5>
<p>早前得到一份北京积分落户的信息（并不涉及特别敏感的信息），包括每个“新北京人”的姓名、籍贯省份、身份证前十位、积分总分、当前就业的单位。<br>
虽然这些信息看似没什么特别，但是能分析的东西还是挺多的。<br>
首先身份证前十位包括了其具体的地区、出生年份，我们要做的第一步就是将他的出生年份及祖籍所在地整理出来。</p>
<br>
<h4>1.1出生年份及年龄</h4>
<p>出生年份就是第7~10位，直接将身份证号的列遍历一遍再切片就可以了，此处不赘述。<br>
年龄=当前的年份-出生年份，也是很简单的逻辑。</p>
<br>
<h4>1.2籍贯所在地</h4>
<p>这个做起来可能比较费劲，先去下载一份身份证前六位对应地区的文件或者sql格式的文件，再通过嵌套遍历即可得到籍贯所在地：</p>

```
city_list = []
idNum = df_score['idCard'].values.tolist()
for id in idNum:
    city = 'null'
    for index, row in df_idCard.iterrows():
        if int(id[0: 6]) != row['num']:
            continue
        if int(id[0: 6]) == row['num']:
            city = row['areazone']

    if city == 'null':
        city = '其它'
    city_list.append(city)
    print(city)
df_score['city'] = city_list
```

<p>新增两列dataframe再存储到一个新的csv文件中，方便后续的分析工作。</p>
<br>
<h4>2.1年龄组成的分析统计</h4>
<p>想知道积分落户的人员年龄的组成，并且运用可视化工具pyecharts得出直观的统计结果。<br>
第一步先将分散的年龄遍历一遍，放进统一的年龄段，为了方便统计这次分了五个年龄段：35岁以下、35~40岁、40~45岁、45~50岁、50岁以上。</p>

```
def age_division(agelist):
    '''年龄分段'''
    count_list=[]
    df_age_division = pd.DataFrame(columns=['age_zone', 'count'])
    a_35 = 0
    a_35_40 = 0
    a_40_45 = 0
    a_45_50 = 0
    a_50 = 0
    for a in agelist:
        if a < 35:
            a_35 += 1
        if a >= 35 and a < 40:
            a_35_40 += 1
        if a >= 40 and a < 45:
            a_40_45 += 1
        if a >= 45 and a < 50:
            a_45_50 += 1
        if a >= 50:
            a_50 += 1
    df_age_division['age_zone'] = ['35岁以下', '35~40岁', '40~45岁', '45~50岁', '50岁以上']
    df_age_division['count'] = [a_35, a_35_40, a_40_45, a_45_50, a_50]
    return df_age_division
```

<p>然后通过这组数据画出饼图，但是还想了解具体每个年龄的人数，为了结果更加直观，我又加上了具体年龄分布的条形统计图。</p>
<img src="https://github.com/CrazyForamenMagnum/lwy-s/blob/master/Desktop/%E5%9B%BE%E7%89%87/2-bjr/pic1.png"/>
<p>可以发现，人数最多的是40~45岁这个年龄段的人，占了61.95%，其中43岁的人数最多，有813人，占了总人数的13.51%。
查了一下北京积分落户的申请要求：</p>

```
第四条 申请人申请积分落户应同时符合下列条件：
(一)持有本市居住证；(二)不超过法定退休年龄；(三)在京连续缴纳社会保险7年及以上；(四)无刑事犯罪记录。
第五条 积分落户指标体系由合法稳定就业、合法稳定住所以及教育背景、职住区域、创新创业、纳税、年龄、荣誉表彰、守法记录指标组成。总积分为各项指标的累计得分。
(七)年龄指标及分值
申请人年龄不超过45周岁的，加20分。
（来自百度百科）
```

<p>这么看来40~45岁这个年龄段的人最多也是很合情理了。</p>
<br>
<h4>2.2籍贯省份</h4>
<p>哪个地方的人最热衷于落户北京？</p>
<img src="https://github.com/CrazyForamenMagnum/lwy-s/blob/master/Desktop/%E5%9B%BE%E7%89%87/2-bjr/pic2.png"/>
<p>有一个问题让人很费解：原本是北京户口的97个北京人为何要参加积分落户，这个问题本人暂时无法查证。</p>
<br>

<h4>2.3 各企业人数统计</h4>
<p>在这里由于存在许多出现频数太少的公司，将出现频数少于10次的去掉了：</p>

```
company_group = df.groupby('unit')['id'].agg({"计数": np.size})
for index, row in company_group.iterrows():
    if row['计数'] < 10:
        company_group = company_group.drop(index)
```

<img src="https://github.com/CrazyForamenMagnum/lwy-s/blob/master/Desktop/%E5%9B%BE%E7%89%87/2-bjr/pic3.png"/>

<p>华为可谓独领风骚，以高出第二名近一倍的数量稳居第一，像中央电视台、首钢建设集团、百度、联想的人数也是不少的。再抽出人数最多的前10家公司看看年龄组成：</p>
<img src="https://github.com/CrazyForamenMagnum/lwy-s/blob/master/Desktop/%E5%9B%BE%E7%89%87/2-bjr/pic4.png"/>
<p>平均年龄最高的是北京首钢建设集团，最低的是百度，这10个公司里年龄最低的出现在北京华为。</p>
<br>
<h4>2.4行业组成分析</h4>
<p>
分析完籍贯省份，再来看看行业组成。<br>
由于并没有明确指出行业，只能从公司名称进行猜测，首先对公司名称进行分词，限制出现频率较高的词，例如“公司”、“有限公司”、“股份集团”等等，这些词汇没有统计意义。<br>
然后，做出词云图：
</p>
<img src="https://github.com/CrazyForamenMagnum/lwy-s/blob/master/Desktop/%E5%9B%BE%E7%89%87/2-bjr/pic5.png"/>
<p>可以看到，频次最高的词就是“信息技术”，换言之，在积分落户的人员中，最多的是信息技术行业的。点击统计图旁边的第三个图标（如上图高亮）可以看到频数统计：</p>
<img src="https://github.com/CrazyForamenMagnum/lwy-s/blob/master/Desktop/%E5%9B%BE%E7%89%87/2-bjr/pic6.png"/>

<p>接下来需要手工抽取一些出现频次较高，并且能标志一个行业的词汇并包含在一个list中：</p>

```
inside = ['电气', '咨询', '制药', '银行', '建筑', '装饰', '工程', '信息技术', '人力资源', '新能源', '电子', '生物',
          '房地产', '电力', '证券', '资产管理', '建材', '贸易', '金融', '保险', '建设', '设计', '通信', '汽车', '公关',
          '软件', '投资', '会计']
接下来同样的对公司名称的字段进行分词，将分词结果存在一个名为segs的list中，再遍历这个list，并新建一个dataframe去存放它：
for seg in segs:
    if len(seg) > 1 and seg !='\r\n' and seg in inside:
        segments.append(seg)
words_df = pd.DataFrame({"segment": segments})
```

<p>然后就可以以这些数据画出条形统计图了：</p>
<img src="https://github.com/CrazyForamenMagnum/lwy-s/blob/master/Desktop/%E5%9B%BE%E7%89%87/2-bjr/pic7.png"/>
<p>但是这样的分析结果还是存在冗余的，譬如，建筑、建设、装饰这几个相似的词汇可以合并成一个列，总体来讲，行业分析在此处只能作为较为模糊的分析，但是还是可以明显看出，信息技术、咨询、工程、建设、投资、软件这些行业的人占比是明显高于其他行业的。</p>
<p>在这里贴上一个来自百度的数据来结束本次的数据分析实验吧：</p>

```
59.2%——来自高新企业、拥有奖项的与高分段人数占比
据媒体公布的数据，这次积100分及以上的高分段人员中，35.8%来自高新企业，23.4%获得创新创业奖项，12人获评省部级以上劳动模范。
```
