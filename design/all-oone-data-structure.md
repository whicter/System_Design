# 432. All O`one Data Structure

### 题目描述

> Implement a data structure supporting the following operations:

> 1. Inc(Key) - Inserts a new key with value 1. Or increments an existing key by 1. Key is guaranteed to be a non-empty string.
2. Dec(Key) - If Key's value is 1, remove it from the data structure. Otherwise decrements an existing key by 1. If the key does not exist, this function does nothing. Key is guaranteed to be a non-empty string.
4. GetMaxKey() - Returns one of the keys with maximal value. If no element exists, return an empty string "".
4. GetMinKey() - Returns one of the keys with minimal value. If no element exists, return an empty string "".
Challenge: Perform all these in O(1) time complexity.

[原题链接](https://leetcode.com/problems/all-oone-data-structure/)

### 解题思路

由于需要常数级的时间复杂度，我们首先反应就是要用哈希表来做。不仅如此，我们肯定还需要用list来保存所有的key，那么哈希表就是建立count和list of key的映射，这个机制和LRU Cache很类似

因此我们建立Bucket的结构体来保存次数以及保存key值的。并建立双向列表。
在具体实现插入和删除的操作中，我们需要分类讨论情况

#### 插入操作
- 如果我们插入一个新的key，则加入后次数一定为1。此时又有两种情况：
    如果list中没有val为1的这一行，那么我们需要新建bucket
    如果已经有了val为1的这行，我们直接将key加入对应的bucket

- 如果我们插入了一个已存在的key，个数增加后该key值肯定不能在当前bucket继续待下去了,需要到新的bucket里去。那么这里就有两种情况了：
    如果该key要升到的bucket不存在，我们需要手动添；
    如果那一行存在，我们之间将key加入集合中，并且将原来行中的key值删掉。

#### 删除操作
dec函数如何实现思路大致一样

- 如果我们要删除的key不存在，那么直接返回即可。

- 如果我们要删除的key存在，那么我们看其val值是否为1。
    - 如果为1的话，那么直接在删除bucket
    - 如果key的次数val不为1的话，我们要考虑降级问题，跟之前的升bucket很类。 同理：
        - 如果要降级的行不存在，我们手动添加上
        - 如果存在，则直接将key值添加到keys集合中即可。

当我们搞懂了inc和dec的实现方法，那么getMaxKey()和getMinKey()简直就是福利啊，不要太简单啊，直接返回首层和尾层的key值即可，参见代码如下：

#### Java代码实现：

```java
public class AllOne {
    Bucket head;
    Bucket tail;
    Map<String, Integer> keyCount;
    Map<Integer, Bucket> countBucket;
    
    /** Initialize your data structure here. */
    public AllOne() {
        head = new Bucket(-1);
        tail = new Bucket(-1);
        head.next = tail;
        tail.pre = head;
        keyCount = new HashMap<String, Integer>();
        countBucket = new HashMap<Integer, Bucket>();
    }
    
    /** Inserts a new key <Key> with value 1. Or increments an existing key by 1. */
    public void inc(String key) {
        if (keyCount.containsKey(key)) {
            moveKey(key, 1);
        } else {
            keyCount.put(key, 1);
            if (head.next.count != 1) {
                addBucketAfter(new Bucket(1), head);
            }
            head.next.keySet.add(key);
            countBucket.put(1, head.next);
        }
    }
    
    /** Decrements an existing key by 1. If Key's value is 1, remove it from the data structure. */
    public void dec(String key) {
        if (keyCount.containsKey(key)) {
            int count = keyCount.get(key);
            if (count == 1) {
                keyCount.remove(key);
                removeKeyFromBucket(countBucket.get(count), key);
            } else {
                moveKey(key, -1);
            }
        }
    }
    
    /** Returns one of the keys with maximal value. */
    public String getMaxKey() {
        return tail.pre == head ? "" : tail.pre.keySet.iterator().next();
    }
    
    /** Returns one of the keys with Minimal value. */
    public String getMinKey() {
        return head.next == tail ? "" : head.next.keySet.iterator().next();
    }
    
    private void moveKey(String key, int offset) {
        int count = keyCount.get(key);
        keyCount.put(key, count + offset);
        Bucket cur = countBucket.get(count);
        Bucket moveToBucket;
        
        if (countBucket.containsKey(count + offset)) {
            moveToBucket = countBucket.get(count + offset);
        } else {
            moveToBucket = new Bucket(count + offset);
            countBucket.put(count + offset, moveToBucket);
            addBucketAfter(moveToBucket, offset == 1 ? cur : cur.pre);
        }
        
        moveToBucket.keySet.add(key);
        removeKeyFromBucket(cur, key);
    }
    
    private void addBucketAfter(Bucket newBucket, Bucket preBucket) {
        newBucket.next = preBucket.next;
        newBucket.pre = preBucket;
        preBucket.next.pre = newBucket;
        preBucket.next = newBucket;
    }
    
    private void removeKeyFromBucket(Bucket cur, String key) {
        cur.keySet.remove(key);
        // no key within the bucket, remove it
        if (cur.keySet.size() == 0) {
            countBucket.remove(cur.count);
            cur.pre.next = cur.next;
            cur.next.pre = cur.pre;
        }
    }
}

class Bucket{
    int count;
    Set<String> keySet;
    Bucket pre;
    Bucket next;
    
    public Bucket(int count) {
        this.count = count;
        keySet = new LinkedHashSet<String>();
    }
}

/**
 * Your AllOne object will be instantiated and called as such:
 * AllOne obj = new AllOne();
 * obj.inc(key);
 * obj.dec(key);
 * String param_3 = obj.getMaxKey();
 * String param_4 = obj.getMinKey();
 */
```

