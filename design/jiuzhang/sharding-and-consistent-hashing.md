# 8 Sharding & Consistant Hashing

## Simple horisontal sharding
- 对机器数目取模
- e.g. 3 台数据库的机器, from_user_id % 3 进行拆分
- 问题： 新加机器， 原来的%3，就变成了%4， 所有数据要迁移
- % n 的方法是一种最简单的 Hash 算法  
	* 但是这种方法在 n 变成 n+1 的时候，每个 key % n和 % (n+1) 结果基本上都不一样 
	*  这个 Hash 算法可以称之为:不一致 hash
![](/assets/Simple_hashing_rehashing.png)
  
## Consistant Hashing

## 一个简单的一致性Hash算法  
- 将 key 模一个很大的数，比如 360  
- 将 360 分配给 n 台机器，每个机器负责一段区间  
	* 区间分配信息记录为一张表存在 Web Server 上  
- 新加一台机器的时候，在表中选择一个位置插入，匀走相邻两台机器的一部分数据
	* 比如n从2变化到3，只有1/3的数据移动

![](/assets/improved_simple_hashing.png)

- 缺陷1 数据分布不均匀 因为算法是“将数据最多的相邻两台机器均匀分为三台”
	* 比如，3台机器变4台机器时，无法做到4台机器均匀分布
- 缺陷2 迁移压力大 
	* 新机器的数据只从两台老机器上获取导致这两台老机器负载过大

## 更完美的一致性哈希算法

-   将取模的底数从 360 拓展到 2^64
-   将 0~2^64-1 看做一个很大的圆环(Ring)
-   将数据和机器都通过 hash function 换算到环上的一个点
	* 数据取 key / row_key 作为 hash key  
	* 机器取MAC地址，或者机器固定名字如database01，或者固定的 IP 地址  
- 每个数据放在哪台机器上，取决于在Consistent Hash Ring 上顺时针碰到的 下一个机器节点

![](/assets/consistent_hashing.png)
## Virtual Nodes
-   一个实体机器(Real node) 对应若干虚拟机器(Virtual Node)
	* 通常是 1000 个  
	* 分身的KEY可以用实体机器的KEY+后缀的形式
		* 如 database01-0001  
		* 好处是直接按格式去掉后缀就可以得到实体机器
- 用一个数据结构存储这些 virtual nodes
	* 支持快􏰀的查询比某个数大的最小数 
	* 即顺时针碰到的下一个 virtual nodes

![](/assets/virtual_nodes.png)