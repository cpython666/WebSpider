from urllib.parse import urlparse

url = 'https://example.com:8080/path/to/page?param=value#fragment'
result = urlparse(url)

print(result.scheme)
print(result.netloc)
print(result.path)
print(result.query)
print(result.fragment)

# https
# example.com:8080
# /path/to/page
# param=value
# fragment