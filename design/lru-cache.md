# 146. LRU Cache

### 题目描述

> Design and implement a data structure for Least Recently Used (LRU) cache. It should support the following operations: get and put.
<br> `get(key)` - Get the value (will always be positive) of the key if the key exists in the cache, otherwise return -1.
<br>`put(key, value)` - Set or insert the value if the key is not already present. When the cache reached its capacity, it should invalidate the least recently used item before inserting a new item.
<br> The cache is initialized with a positive capacity.

**Follow up:**
Could you do both operations in O(1) time complexity?

[原题链接](https://leetcode.com/problems/lru-cache/)

### 解题思路

需要存key <-> value pair那首先想到的是HashMap，同时HashMap的get操作也是O(1)
由于需要在超过capacity的时候把最少用的entry去掉，因此这就需要我们的entry是有序的。为了能够实现O(1)操作，考虑使用双向列表。这样可以实现顺序的更新.

因此我们新建一个Node class, 作为链表的节点，同时包括key value的信息 （其实key的信息都可以不用包括在内）

#### Java代码实现：

```java
class Node {
    int key;
    int value;
    Node prev;
    Node next;
 
    public Node(int key, int value){
        this.key = key;
        this.value = value;
    }
}
class LRUCache {
    Node head;
    Node tail;
    Map<Integer, Node> map = null;
    int cap = 0;
 
    public LRUCache(int capacity) {
        this.cap = capacity;
        this.map = new HashMap<Integer, Node>();
    }
 
    public int get(int key) {
        if (map.get(key) == null){
            return -1;
        }
 
        //move to tail
        Node t = map.get(key);
 
        removeNode(t);
        offerNode(t);
 
        return t.value;
    }
 
    public void put(int key, int value) {
        if (map.containsKey(key)){
            Node t = map.get(key);
            t.value = value;
 
            //move to tail
            removeNode(t); 
            offerNode(t);
            
        } else {
            if (map.size() >= cap) {
                //delete head
                map.remove(head.key);
                removeNode(head);
            }
 
            Node node = new Node(key, value);
            //add to tail
            offerNode(node);
            map.put(key, node);
        }
    }
 
    private void removeNode(Node n) {
        if (n.prev!=null) {
            n.prev.next = n.next;
        } else {
            head = n.next;
        }
 
        if (n.next != null){
            n.next.prev = n.prev;
        } else {
            tail = n.prev;
        }
    }
 
    private void offerNode(Node n) {
        if (tail != null){
            tail.next = n;
        }
 
        n.prev = tail;
        n.next = null;
        tail = n;
 
        if (head == null) {
            head = tail;   
        }
    }
}



/**
 * Your LRUCache object will be instantiated and called as such:
 * LRUCache obj = new LRUCache(capacity);
 * int param_1 = obj.get(key);
 * obj.put(key,value);
 */

```

