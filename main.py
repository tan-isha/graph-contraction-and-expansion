import folium
import webbrowser
import csv
import math
import tkinter as tk
from tkinter import *
  
#initialize
my_map1 = folium.Map(location = [100, 100], 
                                        zoom_start = 0 ) 



x11=[]
y11=[]
city=[]

def enter():
    with open('F:\cities.csv', newline='') as csvfile:
        data = csv.DictReader(csvfile)
        for row in data:
            if( row['City']== c1.get() ):
                    lat1=float(row['Lat'])
                    long1=float(row['Long'])
            if( row['City']== c2.get() ):
                lat2=float(row['Lat'])
                long2=float(row['Long'])
    print(lat1,long1,long2,lat2)
    #a=[lat1,long1,lat2,long2]
    minlat=min(lat1,lat2)
    maxlat=max(lat1,lat2)
    minlong=min(long1,long2)
    maxlong=max(long1,long2)
    m=int(long2-long1)/int(lat2-lat1) #slope of line for determining shortest distance of cities under 150km near the path from source to destination
    #determining constant of the line
    c=long1-m*lat1                       
    a=[[lat1,long1],[long2,lat2]]
    city=[]
    #marking on map
    folium.Marker([lat1,long1], 
              popup = c1.get()).add_to(my_map1) 
  
    folium.Marker([lat2,long2], 
              popup = c2.get()).add_to(my_map1) 
  

  
    folium.PolyLine(locations = [[lat1,long1], [lat2,long2]], 
                line_opacity = 0.5).add_to(my_map1)
            
    #creation of city array
    with open('F:\cities.csv', newline='') as csvfile:
        data = csv.DictReader(csvfile)
        for row in data:
            x=float(row['Lat'])
            y=float(row['Long'])

            shortest_distance(x, y, m, -1, c,minlat,maxlat,minlong,maxlong)
            n=len(x11)
            for i in range(0,n):
            
                if(x11[i]==float(row['Lat']) and y11[i]==float(row['Long'])):
                    city.append(row['City'])

    my_map1.save('E:\\map.html')
    webbrowser.open('E:\\map.html')

    

#function for determining whether city on the line(not used in program)
def pointIsOnLine(m, c, x, y,lat1,long1,long2,lat2): 
      

    if (y == ((m * x) + c)):
        a.append([x,y])
#function for determining shortest distance of cities under 150km near the path from source to destination
def shortest_distance(x1, y1, a, b, c,minlat,maxlat,minlong,maxlong):  
       
    d = abs((a * x1 + b * y1 + c)) / (math.sqrt(a * a + b * b))
    if(d<=1 and minlat<=x1 and maxlat>=x1 and minlong<=y1 and maxlong>=y1 ):
        print([x1,y1])
        x11.append(x1)
        y11.append(y1)


        
    

#here graph expansion takes place. With every zoomin 1 city is added in the path from source to destination
def zoomin():
    with open('F:\cities.csv', newline='') as csvfile:
        data = csv.DictReader(csvfile)
        for row in data:
            x=float(row['Lat'])
            y=float(row['Long'])

      
            n=len(x11)
            for i in range(0,n):
            
                if(x11[i]==float(row['Lat']) and y11[i]==float(row['Long'])):
                    city.append(row['City'])
    zoom.set(zoom.get()+1)
    my_map1 = folium.Map(location = [20, 80], 
                                        zoom_start = zoom.get() ) 
    for i in range(0,zoom.get()):
        
    
    
            
        folium.Marker([x11[i],y11[i]], popup=city[i]).add_to(my_map1)
    s.set(s.get()+city[zoom.get()-1]+' ')
    my_map1.save('E:\\map.html')
    webbrowser.open('E:\\map.html')
    

#here graph expansion takes place. With every zoomin 1 city is deleted from the path from source to destination
def zoomout():

    
    with open('F:\cities.csv', newline='') as csvfile:
        data = csv.DictReader(csvfile)
        for row in data:
            x=float(row['Lat'])
            y=float(row['Long'])

        
            n=len(x11)
            for i in range(0,n):
            
                if(x11[i]==float(row['Lat']) and y11[i]==float(row['Long'])):
                    city.append(row['City'])
    zoom.set(zoom.get()-1)
    my_map1 = folium.Map(location = [20, 80], 
                                        zoom_start = zoom.get() )
    s.set("")
    
    for i in range(0,zoom.get()):
        s.set(s.get()+city[i]+" ")
        
   
    
    
            
        folium.Marker([x11[i],y11[i]], popup=city[i]).add_to(my_map1)
    
    my_map1.save('E:\\map.html')
    webbrowser.open('E:\\map.html')
    

# user interface

master = tk.Tk()
master.geometry('550x500')
zoom= IntVar()
s=StringVar()
s.set("cities : \n")
#my_font = font(family="Times New Roman", size=16, weight="bold", slant="italic")
#my_font1 = font(family="Times New Roman", size=24, weight="bold")
l=Label(master, text="Graph Contraction and Expansion")
l.config(font =("Courier", 14,"bold"))
l.grid(row=0)
T = Text(master, height = 4, width = 22)
T.insert(tk.END, "Tanisha Agrawal 13 A")
T.grid(row=1)

tk.Label(master, text="Source").grid(row=3,column=0)
tk.Label(master, text="Destination").grid(row=4,column=0)

c1 = tk.Entry(master)
c2 = tk.Entry(master)
c1.grid(row=3, column=1)
c2.grid(row=4, column=1)
   
tk.Button(master,text='+', command=zoomin,height=2,width=2).grid(row=8,column=0,sticky=tk.W,pady=4)
tk.Label(master, text="<=expansion").grid(row=8,column=1,sticky=tk.W,pady=4)
tk.Button(master,text='-', command=zoomout,height=2,width=2).grid(row=9,column=0,sticky=tk.W,pady=4)
tk.Label(master, text="<=contraction").grid(row=9,column=1,sticky=tk.W,pady=4)
tk.Button(master, text='Enter', command=enter,height=2,width=10).grid(row=7,column=1, sticky=tk.W, pady=4)
tk.Label(master,textvariable=s).grid(row=10,column=0,sticky=tk.W,pady=4)
tk.Button(master, text='Quit', command=exit,height=2,width=10).grid(row=20,column=3, sticky=tk.W, pady=4)


tk.mainloop()
