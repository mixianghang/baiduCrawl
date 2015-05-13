# baiduSearch.py
This script is used to browse the results returned by Baidu Search Engine in terminal. It takes the user_input as the keywords.
该脚本能在命令行动态查询百度搜索结果，关键词需要用户手动输入。

# baiduGetFile.py
This script is used to search and write all the searching results into local txt files for further research such as Natural Language Processing.
脚本用于抓取百度搜索引擎针对每个“手机对比关键词”查询到的摘要信息，这些数据用于process.py脚本中的比较句抽取。

# coutinue.py
This script is used to contine writing certain pages which is interrupted in the baiduGetFile.py by the Baidu Server.
It takes three parameter as arguments in the terminal. (lastPageNum,lastPageUrl,localFile).
该脚本用于断点抓取百度搜索结果摘要，有效应对百度服务器的屏蔽。

# process.py
该脚本用于从抓取的摘要中抽取比较句，过程中使用了规则匹配方法，并对产品词、比较词进行替换。

#featureScore.py
该脚本用于将竞争产品的比较句按4个“共同特征”和“独有特征”分类，依次计算竞争产品在不同特征下的得分，计分过程使用的情感词典见dict.txt文件。

# dict.txt
该文件是论文《基于比较句的网络用户情感分析》用到的情感词典，数据来源于网络和个人整理。
