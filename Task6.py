import math


class Vertices(object):
    def __init__(self, n, dots, h):
        self.n=n
        self.dots=dots
        self.h=h
    def Get_n(self):
        return self.n
    def Get_h(self):
        return self.h    
    def Get_dot(self, i):
        return self.dots[i]  
    def Get_dots(self):
        return self.dots  
    
    
class Sides(object):
    def __init__(self, s, n):
        self.n=n
        self.s=s
    def Get_n(self):
        return self.n        
    def Get_sides(self):
        return self.s   
    def Get_side(self, i):
        return self.s[i]     
    
    
def Get_int(opened_file):
    f=0
    s=0
    x='0'
    while (x!=''):
        x=opened_file.read(1)
        if (x==' ' or x=='' or x=='\n') and (f!=0):
            return s*f
        if (x==''):
            return 'end'        
        if (x!=' '):
            try:
                x=int(x)
                s=s*10+x
                if (f==0):
                    f=1            
            except:
                if (x=='-'):
                    f=-1
                elif(x!='\n'):
                    print("Wrong data\n")
                    exit()


def Get_dots(opened_file):
    s=[]
    h=0
    a=Get_int(opened_file)
    if(a=='end'):
        print("Empty file\n")
        exit()
    b=Get_int(opened_file)
    if(b=='end'):
        print("Wrong data\n")
        exit()
    s.append([a,b])
    k=1
    while(a!='end'):
        a=Get_int(opened_file)
        if(a!='end'):
            b=Get_int(opened_file)
            if(b=='end'):
                h=a
                a='end'
            else:
                s.append([a,b]) 
                k+=1
    if(h==0):
        print("Wrong data\n")
        exit()                
    V = Vertices(k, s, h)   
    return V


def Line(dot1, dot2):
    if(dot1[0]==dot2[0] and dot1[1]==dot2[1]):
        print("The same dots")
        exit()        
    a=math.atan2(dot2[1]-dot1[1],dot2[0]-dot1[0])
    pi=math.atan2(0,-1)
    if(abs(a)>0.5*pi):
        a=pi-abs(a)
    if(dot1[0]==dot2[0]):
            b=dot1[0]          
    else:
        b=(dot2[1]*dot1[0] - dot1[1]*dot2[0])/(dot1[0]-dot2[0])
    return [a,b]


def Get_sides(V):
    S=[]
    n=V.Get_n()
    W=V.Get_dots()
    for i in range(0,n-1):
        h=Line(W[i],W[i+1])
        S.append(h)
    h=Line(W[0],W[n-1])
    S.append(h) 
    U=Sides(S, n)
    return U


def Angle(dot1, dot2, dot3):
    a=math.atan2(dot1[1]-dot2[1],dot1[0]-dot2[0])
    b=math.atan2(dot3[1]-dot2[1],dot3[0]-dot2[0])
    pi=math.atan2(0,-1)
    if(abs(a-b)>pi):
        return (2*pi-abs(a-b))
    return abs(a-b)


def Get_vectors(V):
    fv=[]
    n=V.Get_n()
    W=V.Get_dots()
    for i in range(0,n-1):
        a=W[i+1][0]-W[i][0]
        b=W[i+1][1]-W[i][1]
        fv.append([a,b])
    a=W[0][0]-W[n-1][0]
    b=W[0][1]-W[n-1][1]
    fv.append([a,b])    
    return fv    
        
        
def Normals(V):
    n=V.Get_n()        
    ns=Get_vectors(V)
    for i in range(0,n):  
        c=ns[i][1]
        ns[i][1]=ns[i][0]
        ns[i][0]=(-1)*c
        p=math.sqrt((ns[i][1])**2+(ns[i][0])**2)
        ns[i][1]=ns[i][1]/p
        ns[i][0]=ns[i][0]/p
    return ns   


def Move(S, ns, h):
    n=S.Get_n()
    ss=S.Get_sides()
    hpi=0.5*math.atan2(0,-1)
    for i in range(0,n): 
        if(ss[i][0]==hpi or ss[i][0]==(-1)*hpi):
            ss[i][1]+=h*ns[i][0]
        else:
            b=h*ns[i][1]/(math.cos(ss[i][0])**2)
            ss[i][1]+=b
    C=Sides(ss, n) 
    return C


def New_dots(S):
    ds=[]
    n=S.Get_n()
    ss=S.Get_sides()
    hpi=0.5*math.atan2(0,-1)
    if(ss[0][0]==hpi or ss[0][0]==(-1)*hpi):
        x=ss[0][1]
        t=math.tan(ss[n-1][0])
        y=t*x + ss[n-1][1]
        ds.append([x,y])
    elif(ss[n-1][0]==hpi or ss[n-1][0]==(-1)*hpi):
        x=ss[n-1][1]
        t=math.tan(ss[0][0])
        y=t*x + ss[0][1]
        ds.append([x,y])
    else:
        t1=math.tan(ss[0][0])
        tn=math.tan(ss[0][0])
        x=(ss[0][1]-ss[n-1][1])/(tn - t1)
        y=(ss[0][1]*tn - ss[n-1][1]*t1)/(tn - t1)
        ds.append([x,y])
        
    for i in range(0,n-1):
        if(ss[i][0]==hpi or ss[i][0]==(-1)*hpi):
            x=ss[i][1]
            t=math.tan(ss[i+1][0])
            y=t*x + ss[i+1][1]
            ds.append([x,y])
        elif(ss[i+1][0]==hpi or ss[i+1][0]==(-1)*hpi):
            x=ss[i+1][1]
            t=math.tan(ss[i][0])
            y=t*x + ss[i][1]
            ds.append([x,y]) 
        else:
            t1=math.tan(ss[i][0])
            tn=math.tan(ss[i+1][0])
            x=(ss[i][1]-ss[i+1][1])/(tn - t1)
            y=(ss[i][1]*tn - ss[i+1][1]*t1)/(tn - t1)
            ds.append([x,y])
    return ds
 
 
def Autotest():
    dots=[[1,1],[1,2],[2,2],[2,1]]
    n=4
    V=Vertices(n, dots, 1)
    S=Get_sides(V)
    Z=S.Get_sides()
    if(Z[0][1]!=1 or Z[1][1]!=2 or Z[2][1]!=2 or Z[3][1]!=1):
        print("Autotest failed")
        exit()
    ns=Normals(V)
    if(ns[0][0]!=-1 or ns[1][0]!=0 or ns[2][0]!=1 or ns[3][0]!=0 or
       ns[0][1]!=0 or ns[1][1]!=1 or ns[2][1]!=0 or ns[3][1]!=-1):
        print("Autotest failed")
        exit()    
    C=Move(S, ns, 1)
    Z=C.Get_sides()
    if(Z[0][1]!=0 or Z[1][1]!=3 or Z[2][1]!=3 or Z[3][1]!=0):
        print("Autotest failed")
        exit()    
    ns=New_dots(C)
    if(ns[0][0]!=0 or ns[1][0]!=0 or ns[2][0]!=3 or ns[3][0]!=3 or
       ns[0][1]!=0 or ns[1][1]!=3 or ns[2][1]!=3 or ns[3][1]!=0):
        print("Autotest failed")
        exit()    
    print("Autotest passed")
        

try:
    file = open("data.txt", "r")
except:
    print("Cannot open file")
    exit()

Autotest()
V = Get_dots(file)
n=V.Get_n()
if(n<3):
    print("Add more dots")
    file.close()
    exit()
h=V.Get_h()
S=Get_sides(V)
ns=Normals(V)
C=Move(S, ns, h)
W=New_dots(C)
print("New dots are")
for i in range(0,n):
    print("( ", W[i][0], " , ", W[i][1], " )")