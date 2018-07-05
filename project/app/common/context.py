

map = {}

def set(key, value):
    map[key] = value

def remove(key):
    try:
        del map[key]
    except KeyError:
        print("key:'"+str(key)+"'  不存在")

def get(key):
    try:
        if key in "all":
            return map
        return map[key]
    except KeyError as e:
        print("key:'"+str(key)+"'  不存在")
        return False


