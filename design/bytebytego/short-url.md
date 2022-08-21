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

## Step 3 - Design deep dive
### URL shortening deep dive
![](/assets/url_shortener_workflow.png)

### Base 62 conversion

Base conversion is another approach commonly used for URL shorteners. Base conversion helps to convert the same number between its different number representation systems. Base 62 conversion is used as there are 62 possible characters for hashValue. Let us use an example to explain how the conversion works: convert 1115710 to base 62 representation (1115710 represents 11157 in a base 10 system).

From its name, base 62 is a way of using 62 characters for encoding. The mappings are: 0-0, ..., 9-9, 10-a, 11-b, ..., 35-z, 36-A, ..., 61-Z, where ‘a’ stands for 10, ‘Z’ stands for 61, etc.
1115710 = 2 x 622 + 55 x 621 + 59 x 620 = [2, 55, 59] -> [2, T, X] in base 62 representation. 

![](/assets/base_62_conversion.png)

### Data model
id, shortURL, longURL.

### Example

- Assuming the input longURL is: https://en.wikipedia.org/wiki/Systems_design
- Unique ID generator returns ID: 2009215674938.
- Convert the ID to shortURL using the base 62 conversion. ID (2009215674938) is converted to “zn9edcu”.
- Save ID, shortURL, and longURL to the database

### URL redirecting deep dive
![](/assets/url_redirecting_design.png)



