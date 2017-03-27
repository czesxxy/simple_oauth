import redis
r = redis.Redis(host='localhost', port=6379)


def getExpert(domain):
    id_list = r.lrange('domain:'+domain, 0, -1)
    id_h = dict()
    for id in id_list:
        id_h[id] = r.get(id+':hi')
        id_h[id] = int(id_h[id])

    id_h = sorted(id_h.items(), key = lambda d:d[1], reverse = True)
    
    expert_list = []
    for person in id_h:
        p = dict()
        index = person[0]
        p['index'] = unicode(index)
        p['hi'] = unicode(r.get(index+':hi'))
        p['name'] = unicode(r.get(index+':n'), "utf-8")
        expert_list.append(p)
    return expert_list

def getCoauthor(author):
    id_list = r.smembers(author+':coauthor')
    id_time = dict()
    for id in id_list:
        id_time[id] = r.get(author+':coauthor:'+id)
        id_time[id] = int(id_time[id])
    id_time = sorted(id_time.items(), key = lambda d:d[1], reverse = True)
  
    coauthor_list = []
    for person in id_time:
        p = dict()
        index = person[0]
        p['index'] = index
        p['name'] = unicode(r.get(index+':n'), "utf-8")
        p['time'] = person[1]
        coauthor_list.append(p)
    return coauthor_list
