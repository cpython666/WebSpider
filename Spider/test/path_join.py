import os
from urllib.parse import urlparse
from urllib.parse import urljoin

if __name__ == '__main__':
    print(urljoin('https://www.huxiu.com/', '/channel/10.html'))
    print('-'*20)
    url = "https://www.example.com/path/to/file.html?query1=value1&query2=value2"
    parsed_url = urlparse(url)

    print("Scheme:", parsed_url.scheme)  # 输出 "https"
    print("Netloc:", parsed_url.netloc)  # 输出 "www.example.com"
    print("Path:", parsed_url.path)  # 输出 "/path/to/file.html"
    print("Query:", parsed_url.query)  # 输出 "query1=value1&query2=value2"

