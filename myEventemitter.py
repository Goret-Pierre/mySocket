class Eventemmiter():
    def __init__(self,**kargs):
        self.listenners = {}
        self.generate_exeptions = kargs.get("generate_exeptions",True)
        self.max_listenners = kargs.get("max_listenner",-1) 
    
    def on(self,event_name, f = None):
        def _on(f): 
            if not hasattr(f,"__call__"):
                raise TypeError("Function is not callable")
            self.add_listenner(event_name,f)
            return f       
        if f is not None:
            if hasattr(f,"__call__"):
                self.add_listenner(event_name,f)
        else:
            return _on

    def add_listenner(self,event_name,f):
        if event_name not in self.listenners:
            self.listenners[event_name] = [] 
        if self.max_listenners == -1 or len(self.listenners) < self.max_listenners :
            self.listenners[event_name].append(f)
        elif self.generate_exeptions:
             raise NameError("nombre max de listenners dépassé !")
    
    def remove_listenner(self,event_name,function):
        if event_name in self.listenners:
            if function in self.listenners[event_name]:
                self.listenners[event_name].remove(function)
                if(self.listenners[event_name] == []):
                    del self.listenners[event_name] 
            elif self.generate_exeptions:
                raise KeyError('function "{}" is not in event list "{}"'.format(function,event_name))

        elif self.generate_exeptions:
            raise KeyError("{} is not in event list".format(event_name))
    
    def remove_all_listenners(self,event_name = None):
        if event_name == None:
            self.listenners = {}  
        elif event_name in self.listenners:
            del self.listenners[event_name]
        elif self.generate_exeptions:
            raise KeyError("{} is not in event list".format(event_name))
    
    def emit(self,event_name,*args,**kargs):
        if event_name in self.listenners:
            for f in self.listenners[event_name]:  
                # if args == () and kargs == {}:
                #     f()
                # elif args == () and kargs != {}:
                #     f(**kargs) 
                # elif args != () and kargs == {}:
                #     f(*args)
                # elif args != () and kargs != {}:
                #     f(*args,**kargs)
                f(*args,**kargs)
        elif self.generate_exeptions:
            raise KeyError("{} is not in event list".format(event_name))

if __name__ ==  "__main__":
    event = Eventemmiter()
    @event.on("salut")
    def bjr(name = None):
        print("Bonjour {} ! :)".format(name))

    a = bjr
    event.on("bonjour",a)
    
    event.emit("bonjour","Pierre")
    event.remove_all_listenners("bonjour")
    print(event.listenners)
    # event.emit("bonjour")


