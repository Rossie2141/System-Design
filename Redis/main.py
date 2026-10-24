import time

class Redis:
    def __init__(self):
        self.store = {}
        self.expiry = {}

    def set(self, key, value, ttl=None):
        self.store[key] = value

        if ttl:
            self.expiry[key] = time.time() + ttl
        

    def get(self, key):
        if key in self.expiry:
            if time.time() > self.expiry[key]:
                del self.store[key]
                del self.expiry[key]
                return None

        return self.store.get(key)
    
    def exists(self, key):
        if key not in self.store:
            return False

        if key in self.expiry:
            if time.time() > self.expiry[key]:
                self.store.pop(key, None)
                self.expiry.pop(key, None)
                return False

        return True
    
    def ttl(self,key):
        if key not in self.store:
            return -2
        elif key not in self.expiry:
            return -1
        elif time.time()>self.expiry[key]:
            self.delete(key)
            return -2
        else:
            return self.expiry[key]-time.time()
        
    def incr(self,key):
        if key not in self.store:
            self.set(key,1)
            return 1
        if isinstance(self.store[key],int):
            self.store[key]+=1
            return self.store[key]
        else:
            raise TypeError("Value must be an integer")
        
    def decr(self,key):
        if key not in self.store:
            self.set(key,-1)
            return -1
        if isinstance(self.store[key],int):
            self.store[key]-=1
            return self.store[key]
        else:
            raise TypeError("Value must be an integer")
            

    def delete(self,key):
        self.store.pop(key,None)
        self.expiry.pop(key,None)


redis=Redis()
redis.set("session", "abc")

time.sleep(3)

print(redis.ttl("session"))


