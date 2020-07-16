
import tkinter as tk
import turtle
from PIL import Image, ImageTk
import numpy as np
import math
import tkinter.filedialog
import os
import json
from win32api import GetSystemMetrics
from collections import OrderedDict
from operator import *



'''
This part is to display, add and delete colors from the text file
'''

def ShowTxtColors():
    global popup
    popup = tk.Tk()
    popup.wm_title("Colors")
    
    container = tk.Frame(popup)
    global canvas,scrollbar,scrollable_frame
    canvas = tk.Canvas(container,width=320, height=200)
    scrollbar = tk.Scrollbar(container, orient="vertical", command=canvas.yview )

    scrollable_frame = tk.Frame(canvas,width=250, height=200)
    
    scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                    scrollregion=canvas.bbox('all')
                    
                    )
            )
        

    canvas.create_window((0, 0), window=scrollable_frame,anchor="nw")
    
    canvas.configure(yscrollcommand=scrollbar.set, scrollregion=canvas.bbox('all'))
    canvas.bind_all("<MouseWheel>", _on_mousewheel)

    
    
    Names=[]
    with open('colors.txt') as json_file: 
        data = json.load(json_file)

        count=0
        Row=1
        Col = 1
        for name in data:
            Names.append(name)
            
            con= tk.Frame(scrollable_frame)
            SectionLabel= tk.Label(con, text=name, width=8)
            SectionLabel.configure(font=("Times New Roman", 12))
            SectionLabel.grid(row=0,column=1)
            
            Col+=3
            for key in data[name]:
                R=key['R']
                G=key['G']
                B= key['B']
                #print(R,G,B)
                
                
                
                
                c = '#{:02x}{:02x}{:02x}'.format(R,G,B)
                frame = tk.Frame(con,width=40,height=40) #their units in pixels
                frame.grid_propagate(False) #disables resizing of frame
                frame.columnconfigure(0, weight=1) #enables button to fill frame
                frame.rowconfigure(0,weight=1) 
                frame.grid(row=0, column=0)#put frame where the button should be
                #frame.grid(row=0,column=1)
                Col+=3
                
                ColorLabel= tk.Label(frame, bg=c,width=8)
                ColorLabel.grid(row=0,column=0)
                

                RLabel=tk.Label(con,text=R,width=3, bg='red', fg='white')
                RLabel.grid(row=0,column=2,padx=5)
                Col+=1
                

                GLabel=tk.Label(con,text=G,width=3, bg='green', fg='white')
                GLabel.grid(row=0,column=3,padx=5)
                Col+=1
                

                BLabel=tk.Label(con,text=B,width=3, bg='blue', fg='white')
                BLabel.grid(row=0,column=4,padx=5)
                Col=1
                Row+=1
                
                DelBtn = tk.Button(con, text='Delete Color', command=lambda x=count: DelColorToTxt(Names[x]))
                DelBtn.grid(row=0,column=5,padx=5)
                
            
            con.pack(fill=tk.BOTH,expand=1)  
            count+=1
        json_file.close()
        

    
    container.pack()
    
    canvas.pack(side="left", expand=True)
    
    scrollbar.pack(side="right", fill="y")
    
    Button = tk.Button(popup,text='Add Color',command=lambda:displayColorPage())
    Button.pack()


def displayColorPage():
    popup.destroy()
    global ColorPage 
    ColorPage=tk.Tk()
    val = ColorPage.register(ValidateColor)
    ColorPage.wm_title("Add Color")
    
    RColor = tk.StringVar(ColorPage)
    GColor=tk.StringVar(ColorPage)
    BColor=tk.StringVar(ColorPage)
    
    RColor.set(0)
    GColor.set(0)
    BColor.set(0)
    
    
    ColorLabel=tk.Label(ColorPage,text ='Colors')
    ColorLabel.configure(font=("Times New Roman", 12, "bold","underline"))
    ColorLabel.grid(row=0,column=1,columnspan=5)
    
    
    RLabel= tk.Label(ColorPage, text='R :')
    RLabel.grid(row=1,column=0)
    RInput=tk.Entry(ColorPage,width=3,textvariable=RColor)
    RInput.configure(validate="key",vcmd=(val,"%P"))
    RInput.grid(row=1,column=1)
    
    
    
    GLabel= tk.Label(ColorPage, text='G :')
    GLabel.grid(row=1,column=2)
    GInput=tk.Entry(ColorPage,width=3,textvariable=GColor)
    GInput.configure(validate="key",vcmd=(val,"%P"))
    GInput.grid(row=1,column=3)
    
    
    BLabel= tk.Label(ColorPage, text='B :')
    BLabel.grid(row=1,column=4)
    BInput=tk.Entry(ColorPage,width=3,textvariable=BColor)
    BInput.configure(validate="key",vcmd=(val,"%P"))
    BInput.grid(row=1,column=5)
    
    

    
    SeeColorBtn = tk.Button(ColorPage, text='See Color', command = lambda: SeeColor(int(RColor.get()),int(GColor.get()),int(BColor.get())))
    SeeColorBtn.grid(row=1,column=6,padx=5)

# function to add to JSON 
def write_json(data, filename='colors.txt'): 
    with open(filename,'w') as f: 
        json.dump(data, f, indent=4) 

def AddColorToTxt(R,G,B,Name): 
    ColorPage.destroy()     
    with open('colors.txt') as json_file: 
        data = json.load(json_file)     
        data[Name] =[] 
        # appending data to emp_details  
        data[Name].append({
                'R': R,
                'G': G,
                'B': B,              
                })
      
    write_json(data)
    ShowTxtColors()
    
def DelColorToTxt(Name): 
    popup.destroy()     
    with open('colors.txt') as json_file: 
        data = json.load(json_file)     
        del data[Name]
        
    write_json(data)
    ShowTxtColors()


def SeeColor(R,G,B):
    
    if R == "":
        R=0
    if G == "":
        G=0
    if B == "":
        B=0
    
    SeeColorFrame= tk.Frame(ColorPage)
    SeeColorFrame.grid(row=2,column=0,columnspan=8)
    
    
    c = '#{:02x}{:02x}{:02x}'.format(R,G,B)
    frame = tk.Frame(SeeColorFrame, width=40, height=40) #their units in pixels
    frame.grid_propagate(False) #disables resizing of frame 
    frame.columnconfigure(0, weight=1) #enables button to fill frame
    frame.rowconfigure(0,weight=1) #any positive number would do the trick
    frame.grid(row=0, column=0,padx=5, pady=10)#put frame where the button should be
    
    
    ColorLabel= tk.Label(frame, bg=c)
    ColorLabel.grid(row=0,column=0,sticky="wens")
    
    NameLabel=tk.Label(SeeColorFrame, text='Name:').grid(row=0,column=1)
    
    NameVar = tk.StringVar(SeeColorFrame)
    NameInput = tk.Entry(SeeColorFrame,width=10,textvariable=NameVar)
    NameInput.grid(row=0,column=2,padx=5)
    
    
    AddColor = tk.Button(SeeColorFrame, text='Add Color', command=lambda: AddColorToTxt(R,G,B,str(NameVar.get())))
    AddColor.grid(row=0,column=3,padx=5)


def ValidateColor(inp):
    #print(inp)
    if inp.isnumeric() and int(inp) in range(0,256):
        return True
    elif inp == "":
        return True
    else:
        return False

'''
This part is for the setting which is stored in a text file called Settings.txt
'''


def displaySettings():
    global SettingsPage
    SettingsPage = tk.Tk()
    SettingsPage.wm_title("Settings")
    count=0
        
    var = []
    varCount=0
    
    with open('Settings.txt') as json_file:

        data = json.load(json_file)

        for d in data:
            SectionLabel= tk.Label(SettingsPage, text=d)
            SectionLabel.configure(font=("Times New Roman", 12, "bold","underline"))
            SectionLabel.grid(row=count,column=0,columnspan=2)
            count+=1
            for key in data[d]:

                for x in key.keys():
                    var.append(tk.StringVar(SettingsPage))
                    SectionLabel= tk.Label(SettingsPage, text=x+':')
                    SectionLabel.grid(row=count,column=0)
                    var[varCount].set(key[x])
                    #print(var[varCount].get())

                    
                    Input = tk.Entry(SettingsPage,width=10,textvariable=var[varCount])
                    #Input.insert(0, key[x])
                    Input.grid(row=count,column=1,padx=5)

                    
                    count+=1
                    varCount+=1

        
        SaveBtn = tk.Button(SettingsPage, text ='Save', command=lambda: SaveSettings(var))
        SaveBtn.grid(row = count, column=0,columnspan=2)

    json_file.close()


def SaveSettings(Settings):

    data = {}
    
    
    
    data['Rotation for color change']=[]
    data['Rotation for color change'].append({
            'Angle': str(Settings[0].get()),
            'CW/CCW': str(Settings[1].get()),
            'Feed rate': str(Settings[2].get()),
            'Time delay': str(Settings[3].get())
            })
        
    data['Rotation'] = []
    data['Rotation'].append({
            'Angle': str(Settings[4].get()),
            'CW/CCW': str(Settings[5].get()),
            'Feed rate': str(Settings[6].get()),
            'Time delay': str(Settings[7].get())
            })
    
    data['Z axis'] = []
    data['Z axis'].append({
            'Height': str(Settings[8].get()),
            'Feed rate': str(Settings[9].get()),
            })
    
    
    
    data['Pixel placer actuator'] = []
    data['Pixel placer actuator'].append({
            'Time valve stays open for': str(Settings[10].get()),
            })
    
    data['Pixel clearer actuator'] = []
    data['Pixel clearer actuator'].append({
            'Time valve stays open for': str(Settings[11].get())
            })
    
    
    
    data['Home function secondary'] = []
    data['Home function secondary'].append({
            'No of purges': str(Settings[12].get())

            })
    
    
    data['X & Y function'] = []
    data['X & Y function'].append({
            'Feed rate': str(Settings[13].get()),
            })
    

    data['Cartridge pixel limits'] = []
    data['Cartridge pixel limits'].append({
            'No of cartridges': str(Settings[14].get()),
            'No of pixels': str(Settings[15].get()),
            })
    
    data['Distances from origin'] = []
    data['Distances from origin'].append({
            'X distance': str(Settings[16].get()),
            'Y distance': str(Settings[17].get())
            })
    
    
    data['Distances from board'] = []
    data['Distances from board'].append({
            'Distance from edge of board to first peg': str(Settings[18].get()),
            'Center to center distance of pegs': str(Settings[19].get())
            })
    
    #print(data)
    with open('Settings.txt', 'w') as outfile:
        json.dump(data, outfile)
        print('Data saved')
        
    SettingsPage.destroy()


'''
This is where the user interface is created, the main body of the program
'''
class SelectPage(tk.Tk):
    #constructor
    def __init__(self,*args,**kwargs):
        global scrollable_frame,canvas
        tk.Tk.__init__(self,*args,**kwargs)
        self.state('zoomed')
        HEIGHT = GetSystemMetrics(1)
        WIDTH = (GetSystemMetrics(0)-20)
        
        

        container = tk.Frame(self)
        canvas = tk.Canvas(container)
        canvas.configure(height=HEIGHT,width=WIDTH)
        scrollbar = tk.Scrollbar(self, orient="vertical", command=canvas.yview)
        scrollbar.pack(side="right", fill="y")
        XScrollBar = tk.Scrollbar(self, orient="horizontal", command=canvas.xview)
        #SizeGrip = tk.Sizegrip(container)
        XScrollBar.pack(side='bottom', fill=tk.X)
        scrollable_frame = tk.Frame(canvas)
        
        scrollable_frame.pack(side='top', expand = True)
        
        scrollable_frame.bind(
                "<Configure>",
                lambda e: canvas.configure(
                        scrollregion=canvas.bbox("all")
                        )
                )
        

                
        canvas.create_window((WIDTH/2, 0), window=scrollable_frame)
                
        canvas.configure(yscrollcommand=scrollbar.set, xscrollcommand=XScrollBar.set)
        self.bind_all("<MouseWheel>", _on_mousewheel)
        
   
        container.pack(side='top',fill='both')
        canvas.pack(side='left', fill="both")
        
        
        
        
        #SizeGrip.pack(in_=XScrollBar, side = "bottom", anchor='se')
        
        
        #CreatePackFrame(self)
        container.bind_all("<MouseWheel>", _on_mousewheel)
        
        
        

        self.frames={}
        

            
        frame = StartPage(container,self)
            
        self.frames[StartPage] = frame
            


        frame.pack()
        self.show_frame(StartPage)
        menubar = tk.Menu(self)
        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label="New", command=lambda:CreateName(self))
        filemenu.add_separator()
        filemenu.add_command(label="Edit Colors", command=lambda:ShowTxtColors())
        filemenu.add_separator()
        filemenu.add_command(label="Settings", command=lambda:displaySettings())
        menubar.add_cascade(label="File", menu=filemenu)
        self.config(menu=menubar)
        
        
    def show_frame(self,cont):
        
        frame = self.frames[cont]
        frame.tkraise()
        
        



class StartPage(tk.Frame):
    def __init__(self,parent,controller):
        tk.Frame.__init__(self,parent)
        CreateName(self)      
        
def CreateName(self):
    count = 0  
    for widget in scrollable_frame.winfo_children():
        widget.destroy()
 
    
    global NameLabel,NameInput,B1
    NameLabel = tk.Label(scrollable_frame, text='Enter name of project:')
    NameLabel.pack(side='top')
    #NameLabel.grid(row=0,column=0)
    global ProjectName
    ProjectName = tk.StringVar()
    NameInput = tk.Entry(scrollable_frame,width=10,textvariable=ProjectName)
    NameInput.pack(side='left',padx=10)
    #NameInput.grid(row=0,column=1)
    B1 = tk.Button(scrollable_frame, text="Okay",command=lambda:CreateSelctButton(self))
    #B1.grid(row=1,column=0,columnspan=2)
    B1.pack(side='left')     


def _on_mousewheel(event):
    try:
        canvas.yview_scroll(int(-1*(event.delta/120)), "units")
    except:
        pass






def CreateSelctButton(self):
    #Reset(self)
    #f=CreatePackFrame(self)
    if ProjectName != '':
        global dirName

        dirName=''+str(ProjectName.get())
        #print(name)
        
        try:
            
    # Create target Directory
            os.mkdir(dirName)
            print("Directory " , dirName ,  " Created ") 
        except FileExistsError:
            print("Directory " , dirName ,  " already exists")
        

    NameLabel.destroy()
    NameInput.destroy()
    B1.destroy()
    global SelectButton
    SelectImage(self)
    #SelectButton.grid(row=1, column=0)

    
def SelectImage(self, *args):
    global UndefinedData,OLDRGBS
    OLDRGBS=[] 
    #get file directory    
    #SelectButton.destroy()
    f = tkinter.filedialog.askopenfilename(   
    parent=self, initialdir='C:',
    title='Choose file',
    filetypes=[('png images', '.png'),
               ('gif images', '.gif'),
               ('jpg images', '.jpg')]
        )
        
    global OGImage,DefinedColors,TheseColors,OGImageSaveName
    TheseColors ={}
    DefinedColors = {}
    im = Image.open(f)
    OGImage = im
    OGImageSaveName = dirName+'/Original.png'
    OGImage.save(OGImageSaveName)
    display_OGimage(self,OGImage)
    
    DetermineColors(self,im)

def display_OGimage(self, *args, **keywds):

    im = args[0]

    global ImageArray, ROW, COL,XLength,YLength
    
    ImageArray = np.asarray(im)

    COL=1
    ROW=1
    XLength = len(ImageArray)
    YLength= len(ImageArray[0])
    
    if XLength%50==0 and YLength%40==0:
        im = im.rotate(90, expand=True)
        ImageArray = np.asarray(im)
        XLength = len(ImageArray)
        YLength= len(ImageArray[0])
        COL=int(XLength/40)
        ROW=int(YLength/50)
        print()
    
    if XLength%40==0 and YLength%50==0:
        COL=int(XLength/40)
        ROW=int(YLength/50)
    
        
        
    else:
       print('Image not right dimensions')
       pass
    CreateOGImageFrame(self)
    
    image = ImageTk.PhotoImage(im)
    
    OGLabel = tk.Label(OGImageFrame, text='Original Image: ')
    OGLabel.grid(row=0,column=0)
    l1 = tk.Label(OGImageFrame, image=image)
    l1.image = image
    l1.grid(row=0, column=1)



def DetermineColors(self, *args):
    global AllColors,AllColorsCount,ColSpan
    ColSpan=0
    AllColorsCount=[]
    AllColors = []
    lst = np.asarray(args[0])

    for y in range(len(lst)):
        for x in range (len(lst[y])):
            R = int(lst[y,x,0])
            G = int(lst[y,x,1])
            B = int(lst[y,x,2])
            RGB=(R,G,B)
            if RGB not in AllColors:
                AllColors.append(RGB)
                AllColorsCount.append(RGB)
                #print(RGB)
            
            yx=[int(x),int(y)]
    #print(AllColors)
    ColSpan=len(AllColorsCount)
    
    
    GetClosetColors(self)
    


def DisplayAllColors(self, *args):
    global Frame
    Frame = CreateAllColorFrame(self)
    i=1
    x=0
    for color in ColorComp:
        R,G,B = color
        c = '#{:02x}{:02x}{:02x}'.format(R,G,B)
        frame = tk.Frame(Frame, width=40, height=40) #their units in pixels
        frame.grid_propagate(False)#disables resizing of frame
        frame.columnconfigure(0, weight=1) #enables button to fill frame
        frame.rowconfigure(0,weight=1) #any positive number would do the trick
        frame.grid(row=0, column=i,padx=2,sticky="wens")#put frame where the button should be
        
        
        button = tk.Button(frame, bg = c, command = lambda c = x : DisplayColor(self,AllColors[c],int(len(AllColorsCount)) ))
        
        #command= lambda c= x: DisplayColor(self,c,colors[c][0],colors[c][1],colors[c][2],image,Coords[c])
        button.grid(column=0,sticky="wens",pady=10) #makes the button expand
        i=i+1
        x=x+1

        l=tk.Label(Frame,text='Undefined Colors:').grid(row=0,column=0,pady=10)

        #DisplayGCodeButton(self)

def DisplayColor(self, *args, **keywds):
    try:
        ColorInputFrame.destroy()
        
    except NameError:
        pass
    # args [R,G,B]

    R,G,B = args[0]
    #print(R,G,B)
    colSpan=args[1]

    c = '#{:02x}{:02x}{:02x}'.format(R,G,B)


    CreateColorInputFrame(self,colSpan)
    

    
   
    PickColor = tk.Button(ColorInputFrame,text='Pick Color',command= lambda: PickTxtColor(self,R,G,B))


    
    frame = tk.Frame(ColorInputFrame, width=45, height=40) #their units in pixels
    frame.pack_propagate(False) #disables resizing of frame
    frame.columnconfigure(0, weight=1) #enables button to fill frame
    frame.rowconfigure(0,weight=1) #any positive number would do the trick
    frame.pack(side = tk.LEFT)#put frame where the button should be

    
    ColorLabel= tk.Label(frame, bg=c,width=5,height=2)
    ColorLabel.pack(expand=1,padx=5)
    
    RVal=tk.Label(ColorInputFrame,text=R, bg='red', fg='white',width=3).pack(side = tk.LEFT)
    GVal=tk.Label(ColorInputFrame,text=G, bg='green', fg='white',width=3).pack(side = tk.LEFT)
    BVal=tk.Label(ColorInputFrame,text=B, bg='blue', fg='white',width=3).pack(side = tk.LEFT)

    PickColor.pack(side=tk.LEFT)


def PickTxtColor(self,OldR,OldG,OldB):

    global popup,canvas
    popup = tk.Tk()
    popup.wm_title("Colors")
    #print(Coord)
    container = tk.Frame(popup)
    canvas = tk.Canvas(container,width=350, height=200)
    scrollbar = tk.Scrollbar(container, orient="vertical", command=canvas.yview)
    scrollable_frame = tk.Frame(canvas,width=350, height=200)

    scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                    scrollregion=canvas.bbox('all')
                    )
            )

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw" )
    
    canvas.configure(yscrollcommand=scrollbar.set)
    canvas.bind_all("<MouseWheel>", _on_mousewheel)
    

        
    container.pack()
    canvas.pack(side="left", expand=True)
    scrollbar.pack(side="right", fill="y")
    
    
    with open('colors.txt') as json_file: 
        data = json.load(json_file)
        json_file.close()
        
    Names =[]
    SortedData={}
    count=0
    Diffs = []
    for name in data:        
        for key in data[name]:
            R=key['R']
            G=key['G']
            B=key['B']
            Diff = math.sqrt((OldR-R)**2 + (OldG-G)**2 +(OldB-B)**2)
            if Diff not in Diffs:
                Diffs.append(Diff)
            key['Diff']=Diff

   
    SortedDiff=sorted(Diffs)
    SortedData = {}
    for d in SortedDiff:
        for name in data:
            for key in data[name]:
                R=key['R']
                G=key['G']
                B=key['B']
                #print(R,G,B)
                if d == key['Diff']:
                    SortedData[name]=[]
                    SortedData[name].append({
                            'R': R,
                            'G': G,
                            'B': B,                    
                            })
                    #print()
    Col=0
    Row=0
    Rs=[]
    Gs=[]
    Bs=[]
    global con
    for name in SortedData:
            Names.append(name)
            con= tk.Frame(scrollable_frame)
            SectionLabel= tk.Label(con, text=name, width=8)
            SectionLabel.configure(font=("Times New Roman", 12))
            SectionLabel.grid(row=0,column=1)
            
            Col+=3
            for key in SortedData[name]:
                R=key['R']
                G=key['G']
                B= key['B']
                Rs.append(R)
                Gs.append(G)
                Bs.append(B)
                #print(R,G,B)
                
                
                
                
                c = '#{:02x}{:02x}{:02x}'.format(R,G,B)
                frame = tk.Frame(con,width=40,height=40) #their units in pixels
                frame.grid_propagate(False) #disables resizing of frame
                frame.columnconfigure(0, weight=1) #enables button to fill frame
                frame.rowconfigure(0,weight=1) 
                frame.grid(row=0, column=0)#put frame where the button should be
                #frame.grid(row=0,column=1)
                Col+=3
                
                ColorLabel= tk.Label(frame, bg=c,width=8)
                ColorLabel.grid(row=0,column=0)
                

                RLabel=tk.Label(con,text=R,width=3, bg='red', fg='white')
                RLabel.grid(row=0,column=2,padx=5)
                Col+=1
                

                GLabel=tk.Label(con,text=G,width=3, bg='green', fg='white')
                GLabel.grid(row=0,column=3,padx=5)
                Col+=1
                

                BLabel=tk.Label(con,text=B,width=3, bg='blue', fg='white')
                BLabel.grid(row=0,column=4,padx=5)
                Col=1
                Row+=1
                
                DelBtn = tk.Button(con, text='Pick Color', command=lambda i=count: ChangeOGColors(self,OldR,OldG,OldB,Rs[i],Gs[i],Bs[i],Names[i]))
           
                DelBtn.grid(row=0,column=5,padx=5)
            
            con.pack(fill=tk.BOTH,expand=1)
            count+=1


def ChangeOGColors(self,OldR,OldG,OldB,R,G,B,Name):

    ColorInputFrame.destroy()

    popup.destroy()
    image = OGImage
    OLDRGB = (OldR,OldG,OldB)
    RGB=(R,G,B)
    ColorComp[OLDRGB][0]=Name
    ColorComp[OLDRGB][1]=RGB
    print('0')
    DelImage(self)
    ChangePx(self,ColorComp)

    DisplayTheseColors(self)





def GetClosetColors(self):
    global ColorComp
    ColorComp = {}
    with open('colors.txt') as json_file: 
            data = json.load(json_file)
            json_file.close()
            
    for color in AllColors:
        #print(color)
        OldR,OldG,OldB = color
        
        Names =[]
        SortedData={}
        count=0
        Diffs = []
        for name in data:        
            for key in data[name]:
                R=key['R']
                G=key['G']
                B=key['B']
                Diff = math.sqrt((OldR-R)**2 + (OldG-G)**2 +(OldB-B)**2)

                print(Diff)
                if Diff not in Diffs:
                    Diffs.append(Diff)
                    key['Diff']=Diff

   
        SortedDiff=sorted(Diffs)
        SortedData = {}

        for d in SortedDiff:
            
            for name in data:
                for key in data[name]:
                    R=key['R']
                    G=key['G']
                    B=key['B']

                    
                    if SortedDiff[0] == key['Diff']:
                        ColorComp[color]=[]
                        
                        TheseColors[name]=[]
                        TheseColors[name].append({
                                'R': int(R),
                                'G': int(G),
                                'B': int(B),                    
                                })
                        RGB = (R,G,B)
                        ColorComp[color].append(name)
                        ColorComp[color].append(RGB)
    print('Changing Pixels')
                  
    #DisplayAllColors(self)
    DisplayTheseColors(self)
    #
    print(ColorComp)
                       
    
    
    #print(TheseColors)
    DefinedColors=TheseColors 

    
    
def DisplayTheseColors(self):
  
    try:
        Frame.destroy()
        Btn.destroy()
    except:
        pass
    i=1
    x=0
    colors=[]
    count=0
    DisplayAllColors(self)
    DefinedFrame = CreateDefinedColorFrame(self,int(len(AllColorsCount)))
    
    
    l=tk.Label(Frame,text='Defined Colors:').grid(row=1,column=0,pady=10)
    tk.Label(Frame, text='No Of Pixels:').grid(row=2,column=0)
    for OLDRGB in ColorComp:
        print( ColorComp[OLDRGB][1])
        R,G,B = ColorComp[OLDRGB][1]
        RGB=ColorComp[OLDRGB][1]
        
        colors.append((R,G,B))

        color = ColorComp[OLDRGB][0]
        
        c = '#{:02x}{:02x}{:02x}'.format(R,G,B)

        #colors.append(ColorComp[OLDRGB][1])
        frame = tk.Frame(Frame, width=40, height=40) #their units in pixels
        frame.grid_propagate(False)#disables resizing of frame
        frame.columnconfigure(0, weight=1) #enables button to fill frame
        frame.rowconfigure(0,weight=1) #any positive number would do the trick
        frame.grid(row=1, column=i,padx=2,sticky="wens")#put frame where the button should be
        NameL = tk.Label(Frame, text= color).grid(row=2,column=i)
        
    
        button =tk.Button(frame, bg = c)
    
        button.grid(column=0,sticky="wens",pady=10) #makes the button expand
        i=i+1
        x=x+1
        count=count+1
    
    ChangePx(self,ColorComp)  


def MachineColors(self):
    l=tk.Label(self,text='Colors in the machine:').grid(row=7,column=0,pady=10)


def DelImage(self):
    try:
        ImageFrame.destroy()
    except NameError:
        pass

def ChangePx(self, *args):
    #Reset(self)
    try:
        ImageFrame.destroy()
    except NameError:
        pass
    try:
        GBtnFrame.destroy()
        MachineFrame.destroy()
    except:
        pass
    print('Changing PX')
    
    image = Image.open(OGImageSaveName)
    #image.show()
    ColorComp = args[0]

    for OldColor in ColorComp:
        OldR,OldG,OldB = OldColor

        
        NewR,NewG,NewB = ColorComp[OldColor][1]


        pixdata = image.load()
        for y in range(image.size[1]):
            for x in range(image.size[0]):
                if pixdata[x,y][0] == OldR  and pixdata[x,y][1] == OldG  and pixdata[x,y][2] == OldB:
                        r,g,b,a = pixdata[x,y]
                        pixdata[x,y] = (NewR,NewG,NewB,int(a))
                        #print(OldR,OldG,OldB, '=>',NewR,NewG,NewB)
    #image.show()
    display_image(self, image)
    EditedImageSaveName = dirName+'/Edited.png'
    image.save(EditedImageSaveName)
    DisplayGCodeButton(self)
    




def display_image(self, *args, **keywds):
    try:
        ImageFrame.destroy()
    except NameError:
        pass
        
    im = args[0]

    global ImageArray, ROW, COL,XLength,YLength
    
    ImageArray = np.asarray(im)

    COL=1
    ROW=1
    XLength = len(ImageArray)
    YLength= len(ImageArray[0])
    
    if XLength%50==0 and YLength%40==0:
        im = im.rotate(90, expand=True)
        ImageArray = np.asarray(im)
        XLength = len(ImageArray)
        YLength= len(ImageArray[0])

        COL=int(XLength/40)
        ROW=int(YLength/50)

    
    if XLength%40==0 and YLength%50==0:
        COL=int(XLength/40)
        ROW=int(YLength/50)
    
        
        
    else:
        print(XLength%40,YLength%50)
        
    
    
    #CreateColorFrame(self)  
    CreateImageFrame(self)
    
    image = ImageTk.PhotoImage(im)
    label = tk.Label(ImageFrame, text ='Edited Image: ').grid(row=0, column=0)
    l1 = tk.Label(ImageFrame, image=image)
    l1.image = image
    l1.grid(row=0, column=1)

    global coord, colors
    
    cropImage(self,im)


def cropImage(self,*args):
    print('Crop Images')
    im=args[0]
    global Images
    Images=[]
    count = 0
    row = ROW+1
    col = 0
    Y = int(math.ceil(COL/3))
    X = int(math.ceil(ROW/3))
    top =0
    left = 0
    if X==0 and Y ==0:
        
        right=left +50

            
        
        bottom = top+40
            
        im1 = im.crop((left, top, right, bottom)) 
        Images.append(im1)
    else:
        for y in range (Y):

            for x in range(X):
                left = x*50
                right=left +50

                
                bottom = top+40
            

                im1 = im.crop((left, top, right, bottom))
                Images.append(im1)

    CreateButtonFrame(self)
    x=10+1
    y=0

    c=0
    counts=1
    for i in Images:
        image = ImageTk.PhotoImage(i)
        l1 = tk.Button(ButtonFrame, image=image, command= lambda x=c: cropBoard(self, Images[x],counts))
    
        l1.image = image
        
        text='Print '+str(counts)+':'
        counts=counts+1
        l=tk.Label(ButtonFrame, text= text).grid(row=y,column=x)
        x=x+1
        l1.grid(row=y, column=x)
        count=count+1
        x=x+1
        c=c+1
        if count==X:
            count=0
            x=10+1
            y=y+1





def cropBoard(self,*args):
    CreatePrintFrame(self)
    global boards 
    boards=[]
    image=args[0]
    count=args[1]
    ImArray=np.asarray(image)

    im = ImageTk.PhotoImage(image)
    text='Print '+str(count)+':'
    l = tk.Label(PrintFrame, text=text).grid(row=0, column=0,rowspan=2)
    l1 = tk.Label(PrintFrame, image=im)
    l1.image = im
    l1.grid(row=0,column=1,rowspan=3)

    
    for y in range(int(len(ImArray[0])/50)):
        for x in range (int(len(ImArray)/(40))):
            left=x*50
            right = left+50
            top = y*40
            bottom=top+40
            im1 = image.crop((left, top, right, bottom)) 
            boards.append(im1)
    count=1
    col=2
    Row=0 
    
    for board in boards:
        im = ImageTk.PhotoImage(board)
        text = 'Board '+str(count)+':'
        l1 = tk.Label(PrintFrame, text=text).grid(row=Row,column=col)
        count=count+1
        col=col+1
        l1 = tk.Label(PrintFrame, image=im)
        l1.image = im
        l1.grid(row=Row, column=col)
        
        col=col+1
        if count%3==1:
            col=2
            Row=Row+1


'''
This is where the gcode is generated
'''
def GetDefinedColors():
    global DefinedColors
    DefinedColors = {}
    for OGColor in ColorComp:
        DefColorName = ColorComp[OGColor][0]
        Color = ColorComp[OGColor][1]
        print(Color)
        DefinedColors[DefColorName]=[]
        DefinedColors[DefColorName].append(Color)
    print('----------------------')
    print(DefinedColors)
    
def GenGCode():
    GetDefinedColors()
    global GCodeData
    GCodeData = {}
    printNo = 0
    print('Length of images')
    print(len(Images))
    for image in Images:
        print(image.size)
        getXYCoordinates(image,printNo)
        printNo = printNo+1
        
        
    print(len(Images))
    
    
def getXYCoordinates(Image,printNo):
    #Image.show()
    PrintNo ='Print '+str(printNo)
    GCodeData[printNo] ={}
    lst = np.asarray(Image)
    print(lst.shape)
    for color in DefinedColors:
        print(color)
        GCodeData[printNo][color]=[]
        
        for DefRGB in DefinedColors[color]:
            for y in range(len(lst)):
                
                for x in range (len(lst[y])):
                   
                    
                    #print(x)
                    R = int(lst[y,x,0])
                    G = int(lst[y,x,1])
                    B = int(lst[y,x,2])
                    RGB=(R,G,B)
                    
                    if RGB == DefRGB:
                        xy =[int(x),int(y)]
                        GCodeData[printNo][color].append(xy)
            
    
    
    NoOfPixelsPerColor()


def NoOfPixelsPerColor():
    NoOfPixels = {}
    for No in GCodeData:
        for color in GCodeData[No]:
            NoOfPixels[color] =[]
            NoOfPixels[color].append(len(GCodeData[No][color]))
            print('||||||||||||||||||||||||||')
            print(NoOfPixels)
    

def WriteGCode(GCodeData):
    DefineSettings()
    colorCount = 0
    count=0
    ReturnHome = 'G0 X0 Y0 Z0'
    
    RoatateNewCart= 'G01 F'+str(ColorChangeFeedRate)+' A'+str(float(ColorChangeAngle)*0.0625)+'\n'
                    
    RoatateNewCartDelay = 'G4 P'+str(ColorChangeTimeDelay)+'\n'
    #print(GCodeData)
    for Print in GCodeData:
        tempDir = dirName+'/Print '+str(Print+1)
        FileName = tempDir+'/Gcode.txt'
        
        
        
        try:
            # Create target Directory
            os.mkdir(tempDir)
            print("Directory " , tempDir ,  " Created ") 
        except FileExistsError:
            print("Directory " , tempDir ,  " already exists")
        
        for color in GCodeData[Print]:
            colorCount+=1
            print(color)
            text_file = open(FileName, "a")
            
            if (colorCount >1):
                text_file.writelines('\n')   
                text_file.writelines('Purging now\n')    
                for i in range(int(NoOfPurges)):
                        text_file.writelines(RoatationGCode)
                        text_file.writelines(RoatationDelay)
                        text_file.writelines('M8\n')
                        text_file.writelines(TimeDelay)
                        text_file.writelines('M9\n')
                text_file.writelines('\n')
                text_file.writelines('This is a new color\n')    
                text_file.writelines(RoatateNewCart)
                text_file.writelines(RoatateNewCartDelay)
                
            else:
                text_file.writelines('G90\n')               
                text_file.writelines('G21\n')

            for xy in GCodeData[Print][color]:
                count+=1
                if count< int(PixelLimit):
                    
                    x,y=xy
                    z= 1.266+2.56
                #print(z)
                    XCoord = float(DistanceFromBoardToPeg) + float(CenterToCenter)*x
                    XCoord=round(XCoord, 3)
                    
                    YCoord = float(DistanceFromBoardToPeg) + float(CenterToCenter)*y
                    YCoord=round(YCoord, 3)
                
                #if Z1CW == 'CCW':
                    #Z1RotationDistance=-Z1RotationDistance
                    
                    RoatationGCode = 'G01 F'+str(RotationFeedRate)+' A'+str(float(Angle)*0.0625)+'\n'
                    
                    RoatationDelay = 'G4 P'+str(RoationTimeDelay)+'\n'
                    
                    GCodeCord='G01 F'+str(XYFeedRate)+' X'+str(XCoord)+' Y'+str(YCoord)+'\n'
                    
                    ZGCodeDown='G01 F'+str(ZAxisFeedRate)+' Z'+str(ZAxisHeight)+'\n'
                    
                    ZGCodeUp='G01 F'+str(ZAxisFeedRate)+' Z'+str(0)+'\n'
                    
                    TimeDelay = 'G4 P'+str(PixelPlacerTime)+'\n'
                    
                    
                    
                    
                    text_file.writelines('G91\n')
                    text_file.writelines(RoatationGCode)
                    text_file.writelines(RoatationDelay)
                    text_file.writelines('G90\n')
                    text_file.writelines(GCodeCord)
                    
                    #M8 turns on pin D10
                    #M7 turns on pin D9
                    #M9 turns off both
                    
                    text_file.writelines(ZGCodeDown)
                    text_file.writelines('M8\n')
                    text_file.writelines(TimeDelay)
                    text_file.writelines('M9\n')
                    
                    
                    text_file.writelines(ZGCodeUp)
                    text_file.writelines('M8\n')
                    text_file.writelines(TimeDelay)
                    text_file.writelines('M9\n')
                    
                    
                    text_file.writelines('M07\n')
                    text_file.writelines(TimeDelay)
                    text_file.writelines('M09\n')
                    
                    
                    
                    
                if count == int(PixelLimit):
                    text_file.writelines(ReturnHome)
                    for i in range(int(NoOfPurges)):
                        text_file.writelines(RoatationGCode)
                        text_file.writelines(RoatationDelay)
                        text_file.writelines('M8\n')
                        text_file.writelines(TimeDelay)
                        text_file.writelines('M9\n')
                        
                        
                    count = 0
 
            
            
            if len(GCodeData[Print][color]) >0:
                text_file.writelines(ReturnHome)
                
            try:
                text_file.close()
            except:
                pass
    
    
    
    
    
    
    
def DefineSettings():
    global ColorChangeAngle,ColorChangeDir,NoOfCart,ColorChangeFeedRate,ColorChangeTimeDelay,Angle,RotationCw,RotationFeedRate,RoationTimeDelay,ZAxisHeight,ZAxisFeedRate,PixelPlacerTime,PixelClearerTime,PixelLimit,DistanceFromBoardToPeg,CenterToCenter,XYFeedRate,NoOfPurges
    with open('Settings.txt') as json_file:

        data = json.load(json_file)
        print(data)
        ColorChangeAngle = data['Rotation for color change'][0]['Angle']
        ColorChangeDir = data['Rotation for color change'][0]['CW/CCW']
        
        ColorChangeFeedRate= data['Rotation for color change'][0]['Feed rate']
        ColorChangeTimeDelay = data['Rotation for color change'][0]['Time delay']
        
        Angle = data['Rotation'][0]['Angle']
        RotationCw = data['Rotation'][0]['CW/CCW']
        RotationFeedRate= data['Rotation'][0]['Feed rate']
        RoationTimeDelay = data['Rotation'][0]['Time delay']
        
        ZAxisHeight = data['Z axis'][0]['Height']
        ZAxisFeedRate = data['Z axis'][0]['Feed rate']
    
        PixelPlacerTime= data['Pixel placer actuator'][0]['Time valve stays open for']
        PixelClearerTime= data['Pixel clearer actuator'][0]['Time valve stays open for']
        
        
        PixelLimit = data['Cartridge pixel limits'][0]['No of pixels']
        NoOfCart = data['Cartridge pixel limits'][0]['No of cartridges']
        
        XYFeedRate = data['X & Y function'][0]['Feed rate']
        
        
        DistanceFromBoardToPeg = data['Distances from board'][0]['Distance from edge of board to first peg']
        CenterToCenter = data['Distances from board'][0]['Center to center distance of pegs']
        NoOfPurges = data ['Home function secondary'][0]['No of purges']

'''
This is where all the frames of the user interface are created
'''
def ShowMachineColors(self):
    DefineSettings()
    GenGCode()
    global MachineFrame
    try:
        MachineFrame.destroy()
    except NameError:
        pass
    MachineFrame = tk.Frame(scrollable_frame)
    MachineFrame.pack()
    MachineColorLabel = tk.Label(MachineFrame, text='Machine Colors:').grid(row=0,column=0)
    tk.Label(MachineFrame, text='No Of Pixels:').grid(row=2,column=0)
    i=1
    x=0
    colors=[]
    count=0
    print('[[[[[[[[[[[[[[[[[[[[[]]]]]]]]]]]]]]')
    print(ColorComp)
    
   
    for OLDRGB in ColorComp:
        print( ColorComp[OLDRGB][1])
        R,G,B = ColorComp[OLDRGB][1]
        RGB=ColorComp[OLDRGB][1]
        
        colors.append((R,G,B))

        color = ColorComp[OLDRGB][0]
     
        if color not in ColorOrder:
            ColorOrder.append(color)
            c = '#{:02x}{:02x}{:02x}'.format(R,G,B)

        #colors.append(ColorComp[OLDRGB][1])
        
            frame = tk.Frame(MachineFrame, width=40, height=40) #their units in pixels
            frame.grid_propagate(False)#disables resizing of frame
            frame.columnconfigure(0, weight=1) #enables button to fill frame
            frame.rowconfigure(0,weight=1) #any positive number would do the trick
            frame.grid(row=0, column=i,padx=2,sticky="wens")#put frame where the button should be
            NameL = tk.Label(MachineFrame, text= color).grid(row=1,column=i)
            button =tk.Button(frame, bg = c)
            button.grid(column=0,sticky="wens",pady=10)
            
            for No in GCodeData:
                for Color in GCodeData[No]:
                    if (Color ==color ):
                        NoL = tk.Label(Frame, text= len(GCodeData[No][color])).grid(row=3,column=i)
                        
                        if (len(GCodeData[No][color]) > int(PixelLimit)):
                            ColorOrder.append(color)
                            
                            for x in range( int(len(GCodeData[No][color])/int(PixelLimit))):
                                print('==========================')
                                print(x)

                                    
                                
                                NameL = tk.Label(MachineFrame, text= color).grid(row=1,column=i)
                                frame = tk.Frame(MachineFrame, width=40, height=40) #their units in pixels
                                frame.grid_propagate(False)#disables resizing of frame
                                frame.columnconfigure(0, weight=1) #enables button to fill frame
                                frame.rowconfigure(0,weight=1) #any positive number would do the trick
                                frame.grid(row=0, column=i,padx=2,sticky="wens")#put frame where the button should be
                                LeftOverPixels =str(len(GCodeData[No][color])%int(PixelLimit))
                                #NoL1 = tk.Label(Frame, text= LeftOverPixels).grid(row=3,column=i)
                                button =tk.Button(frame, bg = c)
                                button.grid(column=0,sticky="wens",pady=10)
                                

                                
                        else:
                            tk.Label(MachineFrame, text= len(GCodeData[No][color])).grid(row=2,column=i)
                            button =tk.Button(frame, bg = c)
                            button.grid(column=0,sticky="wens",pady=10) #makes the button expand
                            
            i=i+1
            x=x+1
            count=count+1



    print("Color Order: ", ColorOrder)


def UpdateColorOrder(self,No,Color):
    count = 0
    
    for FinalColor in FinalColorOrder:
        
        color = FinalColor.get()
        FinalColors.append(FinalColor.get())
        print(color,ColorOrder[count],count)
        if color != ColorOrder[count]:
            print(color,ColorOrder[count])
            ColorOrder[ColorOrder.index(color)] =ColorOrder[count]
            
            ColorOrder[count] = color
            print(ColorOrder)
            ShowChangeColorOrder(self)
            
            
            break
        count+=1
        
        
def ShowUpdatedMachineColors():
    i = 1
    
    global MachineFrame
    try:
        MachineFrame.destroy()
    except NameError:
        pass
    MachineFrame = tk.Frame(scrollable_frame)
    MachineFrame.pack()
    MachineColorLabel = tk.Label(MachineFrame, text='Machine Colors:').grid(row=0,column=0)
    #tk.Label(MachineFrame, text='No Of Pixels:').grid(row=2,column=0)
    print(ColorComp)
    for color in ColorOrder:
        for OLDRGB in ColorComp:
            #print( ColorComp[OLDRGB][1])
            R,G,B = ColorComp[OLDRGB][1]
            RGB=ColorComp[OLDRGB][1]
        
            #colors.append((R,G,B))

            Color = ColorComp[OLDRGB][0]
            
            if Color == color:
                c = '#{:02x}{:02x}{:02x}'.format(R,G,B)

        #colors.append(ColorComp[OLDRGB][1])
        
                frame = tk.Frame(MachineFrame, width=40, height=40) #their units in pixels
                frame.grid_propagate(False)#disables resizing of frame
                frame.columnconfigure(0, weight=1) #enables button to fill frame
                frame.rowconfigure(0,weight=1) #any positive number would do the trick
                frame.grid(row=0, column=i,padx=2,sticky="wens")#put frame where the button should be
                NameL = tk.Label(MachineFrame, text= color).grid(row=1,column=i)
                button =tk.Button(frame, bg = c)
                button.grid(column=0,sticky="wens",pady=10)
                i = i+1
        #print(color)
    

    



def ShowChangeColorOrder(self):
    ShowUpdatedMachineColors()
    global MachineOrderFrame,GBtnFrame
    try:
        MachineOrderFrame.destroy()
        GBtnFrame.destroy()

    except NameError:
        pass
    MachineOrderFrame = tk.Frame(scrollable_frame)
    MachineOrderFrame.pack()

    global FinalColorOrder,FinalColors
    FinalColors= []
    FinalColorOrder = []
    xi=0
    count = 0
    for OrderNo in ColorOrder:

        var = tk.StringVar()
        var.set(ColorOrder[xi])
        FinalColorOrder.append(var)
        xi+=1
    
    for c in FinalColorOrder:
        w = tk.OptionMenu(MachineOrderFrame, FinalColorOrder[count],*(ColorOrder), command= lambda x = count: UpdateColorOrder(self,ColorOrder.index(x),x))
        w.grid(row=5,column=count+1)
        
        count+=1
    
    GBtnFrame = tk.Frame(scrollable_frame)
    GBtnFrame.pack()
    Btn=tk.Button(GBtnFrame,text='Generate G-Code', command = lambda: WriteGCode(GCodeData)).pack()
    


def DisplayGCodeButton(self):
    print('DsplayGcode')
    global GBtnFrame,MachineFrame, ColorOrder
    ColorOrder=[]
    ShowMachineColors(self)
    ShowChangeColorOrder(self)

    
    
    
    
def CreateOGImageFrame(self):
    global OGImageFrame
    OGImageFrame = tk.Frame(scrollable_frame)
    OGImageFrame.pack()
    print('OG Image Created')
    return OGImageFrame


def CreateAllColorFrame(self, *args):
    
    global AllColorFrame
    AllColorFrame = tk.Frame(scrollable_frame)
    AllColorFrame.pack()

    return AllColorFrame

def CreatePackFrame(self):
    global packFrame
    print('Pack Frame Created')
    packFrame=tk.Frame(scrollable_frame)
    packFrame.pack(fill="both", expand=True)
    return packFrame


def CreateDefinedColorFrame(self,*args):
    global DefColorFrame
    DefColorFrame = tk.Frame(scrollable_frame)
    DefColorFrame.pack()
    return DefColorFrame

def CreateImageFrame(self):
    global ImageFrame
    ImageFrame = tk.Frame(scrollable_frame)
    ImageFrame.pack()
    return ImageFrame

def CreateButtonFrame(self):
    global ButtonFrame
    ButtonFrame = tk.Frame(ImageFrame)
    ButtonFrame.grid(row=0, column=3)
    print('Button Frame Created')
    return ButtonFrame

def CreatePrintFrame(self):
    global PrintFrame
    PrintFrame = tk.Frame(ImageFrame)
    PrintFrame.grid(row=0, column=4)
    print('Button Frame Created')
    return PrintFrame

def CreateColorInputFrame(self, *args):
    #COLUMSPAN=args[0]
    global ColorInputFrame
    ColorInputFrame = tk.Frame(scrollable_frame)
    ColorInputFrame.pack()
    print('Color Input Frame Created')
    #ColorInputFrame.grid(row=ROW+13,column=0, columnspan = COLUMSPAN)
    #,highlightbackground="Blue",highlightthickness=5
app = SelectPage()

app.mainloop()





