import json
file = open('test.txt')

file = file.read()

data = json.loads(file)

for article in data['articles']:
    print(article['title'],article['content'])
    print()