

class T:
    
    def __init__(self, t,): 
        self.t = t


    def convert_slug(self):
       self.t = self.t.replace(" ", "_") 


x = T("This is a test")
print(x.t)
x.convert_slug()
print(x.t)

