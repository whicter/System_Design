# Design A URL Shortener

## Step 1 - Understand the problem and establish design scope
### Bsic use cases:

1.URL shortening: given a long URL => return a much shorter URL

2.URL redirecting: given a shorter URL => redirect to the original URL

3.High availability, scalability, and fault tolerance considerations

### Back of the envelope estimation
- Write operation: 100 million URLs are generated per day.
 * Write operation per second: 100 million / 24 /3600 = 1160
- Read operation: Assuming ratio of read operation to write operation is 10:1, read operation per second: 1160 * 10 = 11,600
- Assuming the URL shortener service will run for 10 years, this means we must support 100 million * 365 * 10 = 365 billion records.
- Assume average URL length is 100.
 * Storage requirement over 10 years: 365 billion * 100 bytes = 36.5 TB
 
## Step 2 - Propose high-level design and get buy-in
### API Endpoints
1. URL shortening. To create a new short URL, a client sends a POST request, which contains one parameter: the original long URL. The API looks like this: **_POST api/v1/data/shorten_**
 * request parameter: {longUrl: longURLString}
 * return shortURL
2. URL redirecting. To redirect a short URL to the corresponding long URL, a client sends a GET request. The API looks like this: **_GET api/v1/shortUrl_**
 * Return longURL for HTTP redirection

