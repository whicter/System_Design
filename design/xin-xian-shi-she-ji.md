# 新鲜事
## QPS Analysis
- QPS = 100  
	* 用你的笔记本做 Web 服务器就好了
- QPS=1k
	* 用一台好点的 Web 服务器就差不多了
	* 需要考虑 Single Point Failure
    
- QPS=1m
	* 需要建设一个1000台 Web 服务器的集群
	* 需要考虑如何 Maintainance(某一台挂了怎么办)

- QPS和 Web Server (服务器) / Database (数据库) 之间的关系
	* 一台 Web Server 约承受量是 1k 的 QPS (考虑到逻辑处理时间以及数据库查询的瓶颈)
	* 一台 SQL Database 约承受量是 1k 的 QPS(如果 JOIN 和 INDEX query比较多的话，这个值会更小)
	*  一台 NoSQL Database (Memcached) 约承受量是 1M 的 QPS
	* 
## Pull Mode
- 算法
	* 在用户查看News Feed时，获取每个好友的前100条Tweets，合并出前100条News Feed • K路归并算法 Merge K Sorted Arrays

- 复杂度分析  
	* News Feed => 假如有N个关注对象，则为N次DB Reads的时间 + N路归并时间(可忽略) 
	* Postatweet=>1次DBWrite的时间

- Pseudo code
	* getNewsFeed(request)  
		* followings=DB.getFollowings(user=request.user) 
		* news_feed=empty  
		* for follow in followings:
			* tweets = DB.getTweets(follow.to_user, 100)
			* news_feed.merge(tweets)
		* sort(news_feed)  r
		* return news_feed[:100]#返回前100条
		
	* postTweet(request, tweet)  
		* DB.insertTweet(request.user,tweet)
		* return success


![](/assets/pull原理.png)
	
![](/assets/News Feed Table.jpg)  

![](/assets/push 原理.png)

- Pseudo Code
	* getNewsFeed(request)
		* returnDB.getNewsFeed(request.user)
	
	* postTweet(request, tweet_info)   Async Process
		* tweet=DB.insertTweet(request.user,tweet_info) 
		* AsyncService.fanoutTweet(request.user,tweet)  
		* return success
	
	* AsyncService::fanoutTweet(user, tweet) 
		* followers=DB.getFollowers(user)  
		* for follower in followers:
			* DB.insertNewsFeed(tweet, follower)
			* Follower 数目可能很大