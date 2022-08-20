# 460. LFU Cache

### 题目描述

> Design and implement a data structure for Least Frequently Used (LFU) cache. It should support the following operations: get and put.
<br>`get(key)` - Get the value (will always be positive) of the key if the key exists in the cache, otherwise return -1.
<br>`put(key, value)` - Set or insert the value if the key is not already present. When the cache reaches its capacity, it should invalidate the least frequently used item before inserting a new item. For the purpose of this problem, when there is a tie (i.e., two or more keys that have the same frequency), the least recently used key would be evicted.


**Follow up:**
Could you do both operations in O(1) time complexity?

[原题链接](https://leetcode.com/problems/lfu-cache/)

### 解题思路

- 需要存key `<->` value pair那需要HashMap来保存这组对应
- 需要知道frequency，因此需要HashMap来保存key和count的关系
- 由于可能有多个key有同一个frequency，因此需要HashMap来保存count `<->` ListOfKeys。需要注意的是此处的list需要用LinkedHashSet，因为如果frequency相同需要去除least used. 同时HashSet的remove操作也是O(1)
- 同时还需要min variable来维护当前最小的frequency

#### Java代码实现：

```java
class LFUCache {
    HashMap<Integer, Integer> keyVals; //cache K and V
    HashMap<Integer, Integer> keyCounts; //K and counters
    HashMap<Integer, LinkedHashSet<Integer>> countKeySets; //Counter and item list
    int capacity;
    int minUsageCount;

    public LFUCache(int capacity) {
        this.capacity = capacity;
        this.minUsageCount = -1;
        keyVals = new HashMap<Integer, Integer>();
        keyCounts = new HashMap<Integer, Integer>();
        countKeySets = new HashMap<Integer, LinkedHashSet<Integer>>();
        countKeySets.put(1, new LinkedHashSet<Integer>());
    }
    
    public int get(int key) {
        if (!keyVals.containsKey(key)) {
            return -1;
        }
        // Get the count from counts map
        int count = keyCounts.get(key);
        
        // increase the counter     
        keyCounts.put(key, count + 1);
        
        // remove the element from the counter to linkedhashset   
        countKeySets.get(count).remove(key);
        
        // when current minUsageCount does not have any data, next one would be the minUsageCount
        if (count == minUsageCount && countKeySets.get(count).size() == 0) {
            minUsageCount++;
        }
        
        if (!countKeySets.containsKey(count + 1)) {
            countKeySets.put(count + 1, new LinkedHashSet<Integer>());
        }
        
        countKeySets.get(count + 1).add(key);
        
        return keyVals.get(key);
    }
    
    public void put(int key, int value) {
        if (capacity <= 0) {
            return;
        }
        
        // If key does exist, we are returning from here
        if (keyVals.containsKey(key)) {
            keyVals.put(key, value);
            get(key);
            return;
        }
        
        if (keyVals.size() >= capacity) {
            int leastFreq = countKeySets.get(minUsageCount).iterator().next();
            keyVals.remove(leastFreq);
            keyCounts.remove(leastFreq);
            countKeySets.get(minUsageCount).remove(leastFreq);
        }
        
        // If the key is new, insert the value and current minUsageCount should be 1 of course
        keyVals.put(key, value);
        keyCounts.put(key, 1);
        countKeySets.get(1).add(key);
        minUsageCount = 1;
    }
}

/**
 * Your LFUCache object will be instantiated and called as such:
 * LFUCache obj = new LFUCache(capacity);
 * int param_1 = obj.get(key);
 * obj.put(key,value);
 */
```

