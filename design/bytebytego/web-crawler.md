# Design A Web Crawler
## Step 1 - Understand the problem and establish design scope
The basic algorithm of a web crawler is simple:
1. Given a set of URLs, download all the web pages addressed by the URLs.
2. Extract URLs from these web pages
3. Add new URLs to the list of URLs to be downloaded. Repeat these 3 steps.

### Back of the envelope estimation
The following estimations are based on many assumptions, and it is important to communicate with the interviewer to be on the same page.

- Assume 1 billion web pages are downloaded every month.
- QPS: 1,000,000,000 / 30 days / 24 hours / 3600 seconds = ~400 pages per second.
    * Peak QPS = 2 * QPS = 800
- Assume the average web page size is 500k.
    * 1-billion-page x 500k = 500 TB storage per month. 
- Assuming data are stored for five years, 
    * 500 TB * 12 months * 5 years = 30 PB. A 30 PB storage is needed to store five-year content.
    
## Step 2 - Propose high-level design and get buy-in

![](/assets/simple_web_crawler_workflow.png)
Step 1: Add seed URLs to the URL Frontier

Step 2: HTML Downloader fetches a list of URLs from URL Frontier.

Step 3: HTML Downloader gets IP addresses of URLs from DNS resolver and starts downloading.

Step 4: Content Parser parses HTML pages and checks if pages are malformed.

Step 5: After content is parsed and validated, it is passed to the “Content Seen?” component.

Step 6: “Content Seen” component checks if a HTML page is already in the storage.

    * If it is in the storage, this means the same content in a different URL has already been processed. In this case, the HTML page is discarded.
    * If it is not in the storage, the system has not processed the same content before. The content is passed to Link Extractor.
Step 7: Link extractor extracts links from HTML pages.

Step 8: Extracted links are passed to the URL filter.

Step 9: After links are filtered, they are passed to the “URL Seen?” component.

Step 10: “URL Seen” component checks if a URL is already in the storage, if yes, it is processed before, and nothing needs to be done.

Step 11: If a URL has not been processed before, it is added to the URL Frontier.

### Step 3 - Design deep dive
### DFS vs BFS
You can think of the web as a directed graph where web pages serve as nodes and hyperlinks (URLs) as edges. DFS is usually not a good choice because the depth of DFS can be very deep.

BFS is commonly used by web crawlers and is implemented by a first-in-first-out (FIFO) queue. In a FIFO queue, URLs are dequeued in the order they are enqueued. However, this implementation has two problems:

### URL frontier
URL frontier helps to address these problems. A URL frontier is a data structure that stores URLs to be downloaded. The URL frontier is an important component to ensure politeness, URL prioritization, and freshness.

#### Politeness

Most links from the same web page are linked back to the same host.When the crawler tries to download web pages in parallel, Wikipedia servers will be flooded with requests. This is considered as “impolite”.

Sending too many requests is considered as “impolite” or even treated as denial-of-service (DOS) attack. 

The general idea of enforcing politeness is to download one page at a time from the same host. A delay can be added between two download tasks. 

- The politeness constraint is implemented by maintain a mapping from website hostnames to download (worker) threads. Each downloader thread has a separate FIFO queue and only 
![](/assets/politeness.png)
    * Queue router: It ensures that each queue (b1, b2, … bn) only contains URLs from the same host.
    * Mapping table: It maps each host to a queue.
    * FIFO queues b1, b2 to bn: Each queue contains URLs from the same host.
    * Queue selector: Each worker thread is mapped to a FIFO queue, and it only downloads URLs from that queue. The queue selection logic is done by the Queue selector.
    * Worker thread 1 to N. A worker thread downloads web pages one by one from the same host. A delay can be added between two download tasks.

- Another way to do it is to have a scheduler
![](/assets/politeness2.png)


### HTML Downloader
#### Performance optimization
- Distributed crawl
![](/assets/distributed_crawl.png)





