from Spider.models import *
link1=Link.objects(visited=False)
print(link1.to_json())
print(link1.delete())