import redis
r = redis.Redis(host='localhost', port=6379)

file = open('AMiner-Coauthor.txt')
data = file.read()

pairs = data.split('#')
print len(pairs)

for pair in pairs:
    p = pair.split()
    if len(p) < 1:
        continue
    a = p[0]
    b = p[1]
    time = p[2]
    r.sadd(a+':coauthor', b)
    r.sadd(b+':coauthor', a)
    r.set(a+':coauthor:'+b, time)
    r.set(b+':coauthor:'+a, time)
