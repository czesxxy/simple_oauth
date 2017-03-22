import redis
r = redis.Redis(host='localhost', port=6379)
r.flushall()

file = open('AMiner-Author.txt')
data = file.read()

people = data.split('\n\n')
print len(people)

cnt = 10;
for person in people:

    if cnt < 0:
        bre
    info = person.split('#')
    for entry in info:
        if entry == '':
            continue
        d = entry.split(' ', 1)
        if len(d) < 1:
            continue
        if d[0] == 'index':
            index = d[1]
        else:
            if len(d) > 1:
                content = d[1]
            else:
                content = ''
            r.set(index+':'+d[0], content)
            if d[0] == 't':
                if len(d) < 2:
                    continue
                domains = d[1].split(';')
                for domain in domains:
                    r.rpush('domain:'+domain, index)
        
        
