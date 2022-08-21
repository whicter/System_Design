## Database Replication
![](/assets/master_slave_db_cluster.svg)

### Load balancer and database replication.
![](/assets/lb_with_db_replica.webp)

## Cache
### CDN
- A CDN is a network of geographically dispersed servers used to deliver static content. CDN servers cache static content like images, videos, CSS, JavaScript files, etc.
![](/assets/CDN_workflow.webp)

### CDN with Cache
![](/assets/CDN_with_Cache.webp)

## Data Center
![](/assets/data_center.webp)

## Database Scaling
Sharding is a great technique to scale the database but it is far from a perfect solution. It introduces complexities and new challenges to the system:

- **Resharding data**: Resharding data is needed when 1) a single shard could no longer hold more data due to rapid growth. 2) Certain shards might experience shard exhaustion faster than others due to uneven data distribution. When shard exhaustion happens, it requires updating the sharding function and moving data around. Consistent hashing is a commonly used technique to solve this problem.

- **Celebrity problem**: This is also called a hotspot key problem. Excessive access to a specific shard could cause server overload. Imagine data for Katy Perry, Justin Bieber, and Lady Gaga all end up on the same shard. For social applications, that shard will be overwhelmed with read operations. To solve this problem, we may need to allocate a shard for each celebrity. Each shard might even require further partition.

- **Join and de-normalization**: Once a database has been sharded across multiple servers, it is hard to perform join operations across database shards. A common workaround is to de-normalize the database so that queries can be performed in a single table.

![](/assets/complete_design.webp)