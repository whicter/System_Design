## Resource
https://segmentfault.com/a/1190000006165097

## SNAKE分析法
#### Scenario
哪些功能？Feature/Interface?

#### Needs
多强的系统？Constrains/Hypothesis/QPS/DAU

#### Application
主要组成模块？Service/Module

#### Kilobyte
如何存储数据和访问？Data/Storage/SQL vs. NoSQL/File System/Schema

#### Evolve
如何进化，解决缺陷，处理问题？Optimize/Special Case

## Design a Twitter
-----------------------------------------------------------------

### Scenario
-----------------------------------------------------------------

#### Step 1 -- Enumerate 罗列功能

- Register/Login
- User Profile Display/Edit
- Upload Image/Video
- Search
- Post/Share a tweet
- Timeline/News Feed
- Follow/Unfollow a user

#### Step 2 -- Sort 选出核心功能

- Post a tweet
- Timeline
- News Feed
- Follow/Unfollow
- Register/Login

-----------------------------------------------------------------
### Needs
-----------------------------------------------------------------
#### Step 1 -- Ask

- DAU -- Daily Active Users -- 日活跃用户数量 -- 评价系统牛逼的标准
- Twitter: MAU 320M, DAU ~150M+
- Read More: http://bit.ly/1Knl0M7

#### Step 2 -- Predict

- Concurrent Users -- 并发用户
    - Avg Concurrent Users = 日活跃用户数量 * 每个用户平均请求次数 / 一天多少秒 = 150M * 60 / 86400 ~= 100k
    - 峰值：Peak Users = Avg Concurrent Users * 3 ~ 300k
    - 快速增长的产品：Fast Growing = Peak Users * 2 ~ 600k
- Read QPS(Queries Per Second) 读频率：300k
- Write QPS(Queries Per Second) 写频率：5k

-----------------------------------------------------------------
### Application -- Service/Module
-----------------------------------------------------------------
#### Receptionist

1. User Service: Register/Login
2. Tweet Service: Post a tweet/News Feed/Timeline
3. Media Service: Upload Picture/Video
4. Friendship Service: Follow/Unfollow

#### Replay -- 重放需求

#### Merge -- 归并需求

-----------------------------------------------------------------
### Kilobyte -- Data/Storage
-----------------------------------------------------------------
#### 基本知识

**关系型数据库 SQL Database：**User Table
**非关系型数据库 NoSQL Database：Tweets, Social Graph (Followers)**
**文件系统 File System: **Images, Videos, other media files

程序 = 算法 + 数据结构
系统 = 服务 + 数据存储

1. User Service: SQL
2. Tweet Service: NoSQL
3. Media Service: File System
4. Friendship Service: SQL/NoSQL

#### Select

- 为每个App/Service选择合适的存储结构

#### Schema

- 细化Database结构

#### Please Design Schema

| User Table         |
| ---------| ------- |
| userId   | integer |   
| username | varchar |
| email    | varchar |
| password | varchar |

-----------------------------------------------------------------

|       Friendship Table         |
| -----------------| ----------- |
| relationshipId   | integer     |   
| from_userId      | foreign key |
| to_userId        | foreign key |

-----------------------------------------------------------------

|      Tweet Table      |
| --------| ----------- |
| tweetId | integer     |
| userId  | foreign key |
| time    | timestamp   |
| content | text        | 

<br>
### News Feed 如何存取？
### Pull vs. Push （明星问题、僵尸粉问题）
#### Pull Model

- 获取每个好友的前k条tweets，合并出k条news feed
    - K路归并算法：Merge K sorted arrays
- 假设有N个好友，则时间为 ==>
    - N次DB Read的时间 + K路归并时间（可忽略）
- Post a tweet ==>
    - 1次DB Write的时间

##### Pull Work Flow 原理图

    Client ---->send get News Feed request to----> Server
    Server <----get Following from----> Friendship Table
    Server <----get Tweets of Followings from----> Tweet Table
    Server ---->Merge Tweets and return to----> Client

##### Pull模型的缺陷

读取慢（N次DB Reads，非常慢）
发生在用户获得News Feed的请求过程中，有延迟

#### Push Model

#### 算法

- 为每个用户建一个List存储他的News Feed；
- 当他post一个tweet的时候，将该推文逐个推送（Fanout）到每个Follower的List中；
- 当他查看News Feed时，从List中读取最新的100条即可

#### 复杂度

- 每次News Feed，只用一次DB Read；
- 每次Post Tweet，会Fanout到N个Follower，需要N次DB Writes；
- 不过对于Post Tweet，可以用异步任务后台执行，用户无须等待

``` java
postTweet(POST, tweet_info) {
    tweet = DB.insertTweet(userId, tweet_info); //userId对应这个用户的News Feed List
    AsyncService.fanoutTweet(userId, tweet);
    return success;
}
AsyncService::fanoutTweet(userId, tweet) {
    followers = DB.getFollowers(userId);
    for (follower: followers) {
        DB.insertNewsFeed(follower.userId, tweet);
    }
}
```

#### Push Model的缺陷

postTweet()的异步执行；而fanoutTweet()可能遇到followers数目太大的问题。

### Push和Pull的比较

Facebook	Pull
Twitter	Pull
Instagram	Pull + Push

-----------------------------------------------------------------

### Evolve 优化：Optimize/Maintenance
-----------------------------------------------------------------


#### Step 1: Optimize

- Solve Problems: Push vs. Pull; Normalize vs. De-normalize
- More Features: Edit; Delete; Media; Ads
- Special Cases: 大V，热推，不活跃用户

#### Step 2: Maintenance

- Robust 鲁棒性：如果有一台server/DB挂了怎么处理
- Scalability 扩展性：如果有流量暴增，如何扩展

### 解决Pull的缺陷 DB Reads
- 在访问DB之前加入Cache；
- Cache每个用户的Timeline
    - N次DB Reads，所以Cache最近的100条
- Cache每个用户的News Feed
    - 最近没有Cache过News Feed的用户：归并N个好友每人最近的100条Tweets，取出前100条；
    - 最近Cache过的用户：归并某个时间戳之后的tweets

### 解决Push的缺陷
- 浪费更多Disk存储空间
    与Pull模型存在Memory中相比，虽然Disk很便宜
- 其实对于实时性要求而言，Push的效果不如Pull
- 所以对于不活跃用户，可以采用粉丝排序
- follower数目远大于following数目时，加几台push任务的机器
- 如果加server无法解决：针对长期的fast growing，进行评估，转换push模型为pull模型
- Tradeoff：对于明星用户，采用pull；对于普通用户，采用push(朋友圈)；

### 如何实现Follow和Unfollow
Follow之后：异步将他的Timeline合并到你的News Feed中
Unfollow之后：异步将他的Tweets从你的News Feed中移除

异步的好处：用户迅速得到反馈，以为succeess了，无须等待异步操作的真正完成
异步的坏处：如果unfollow之后刷新，发现他的Tweets还在

如何存储Likes
标准化操作：Normalize：两个tables，使用Join操作，时间更多
所以，使用去标准化操作：De-normalize

## 大V发一条tweet之后的问题
对于同一条数据短时间出现大量请求：

- load balancer, sharing, consistent hashing都不是很有效；
- 加入cache可以完美解决；

Follow Up 1:

- Like, Retweet, Comment都会改变该tweet的基本信息，如何更新？
    Write through; Write back; Look aside

Follow Up 2:

- Cache失效怎么办，例如内存不够或者Cache决策失误，导致tweet
- Answer: http://www.cs.utah.edu/~stuts...

While building, maintaining, and evolving our system we have learned the following lessons. (1) Separating cache and persistent storage sys- tems allows us to independently scale them. (2) Features that improve monitoring, debugging and operational ef- ficiency are as important as performance. (3) Managing stateful components is operationally more complex than stateless ones. As a result keeping logic in a stateless client helps iterate on features and minimize disruption. (4) The system must support gradual rollout and roll- back of new features even if it leads to temporary het- erogeneity of feature sets. (5) Simplicity is vital.