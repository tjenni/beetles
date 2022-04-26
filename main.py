import tkinter as tk
import random



class World:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.beetles = []
        self.positions = [] 
        
        
    
    def add_beetle(self, beetle, position):
        if beetle in self.beetles:
            raise Exception("Beetle is already in world.")
        
        if position in self.positions:
            raise Exception("There is another Beetle at this position.")
        
        self.beetles.append(beetle)
        self.positions.append(position)
        
        beetle.position = position
        
        
    def is_empty(self, position):
        if position == None:
            return False
        
        return not( position in self.positions )

    
class Beetle:
    start_energy = 100
    genome_length = 255
    
    def __init__(self, beetle=None):
        
        self.energy = Beetle.start_energy
        
        self.position = None
        
        self.direction = random.randint(0,3)
        self.speed = 0
        
        self.counter = 0
        self.color = [random.randint(100, 200) for i in range(3)]
        
        
        
        
        # create genome
        if beetle is None:
            self.genome = [random.randint(0, 255) for i in range(Beetle.genome_length)]
        else:
            self.genome = beetle.genome.copy()
    
    
    




world = World(100,100)

for i in range(100):
    position = None
    while not world.is_empty(position):
        position = ( random.randint(0, world.width+1), random.randint(0, world.height+1) )
    
    b = Beetle()
    world.add_beetle(b,position)

b = Beetle()
world.add_beetle(b,(0,0))

b = Beetle()
world.add_beetle(b,(100,100))
    
    
        
        
    
    


class App:
    
    def __init__(self, t, world):
        
        t.title('Beetle v1.0')
        
        t.resizable(True, True)
        
        
        
        self.world = world
        
        self.active_beetle = None
        
        
        
        
        t.geometry('800x500')
        
        
        
        # init frames
        
        self.frame_left = tk.Frame(t, bg="white")
        self.frame_left.grid(row=0, column=0, sticky='nsew')
       
        self.frame_right = tk.Frame(t, bg="white")
        self.frame_right.grid(row=0, column=1, sticky='nsew')
        
        t.grid_rowconfigure(0, minsize=500, weight=1)
        t.grid_columnconfigure(0, minsize=400, weight=1)
        t.grid_columnconfigure(1, minsize=400,weight=1)
       
        
        
        
        
    
        # init canvas
        self.canvas_inner_pad = 10
        
        self.canvas = tk.Canvas(self.frame_left, highlightthickness=1, highlightbackground="black")
        self.canvas.bind("<Configure>", self.resize_canvas)
        self.canvas.bind("<Button-1>", self.canvas_clicked)
        self.canvas.pack(fill="x",anchor=tk.NW, expand=True, padx=10,pady=10)
        
       
        
        
        self.frame_button = tk.Frame(self.frame_right, bg="white")
        self.frame_button.grid(row=0, column=0, sticky='nw')
        
        

        self.button_run = tk.Button(self.frame_button,
            text="run",
            width=10,
            height=2,
            activeforeground="#f00",
            command=self.run_clicked)
        
        self.button_run.pack(side=tk.LEFT, anchor=tk.NW, padx=10, pady=10)
        
        self.button_stop = tk.Button(self.frame_button,
            text="step",
            width=10,
            height=2,
            activeforeground="#f00",
            command=self.step_clicked)
        
        self.button_stop.pack(side=tk.LEFT, anchor=tk.NW, padx=10, pady=10)
        
        
        
        # init table
        self.genome_table = tk.ttk.Treeview(self.frame_right)
        self.genome_table['columns'] = ('0', '1', '2', '3', '4', '5', '6', '7', '8')
        


        self.genome_table.column("#0", width=0,  stretch=tk.NO)
        self.genome_table.column("0",anchor=tk.CENTER, width=20)
        self.genome_table.column("1",anchor=tk.CENTER, width=20)
        self.genome_table.column("2",anchor=tk.CENTER, width=20)
        self.genome_table.column("3",anchor=tk.CENTER, width=20)
        self.genome_table.column("4",anchor=tk.CENTER, width=20)
        self.genome_table.column("5",anchor=tk.CENTER, width=20)
        self.genome_table.column("6",anchor=tk.CENTER, width=20)
        self.genome_table.column("7",anchor=tk.CENTER, width=20)
        self.genome_table.column("8",anchor=tk.CENTER, width=20)
        
        
        

        self.genome_table.grid(row=1, column=0, sticky='nw', padx=10, pady=10)
        
    
    def resize_canvas(self, event):
        size = event.width
        self.canvas.config(width=size, height=size)
        
        self.update_canvas()
    
    
    def update_canvas(self):
        self.canvas.delete("all")
        
        pad = self.canvas_inner_pad
        
        size = self.canvas.winfo_width() - 2*pad
        
        self.photoimage = tk.PhotoImage(width=size, height=size)
        self.photoimage.put("#FFFFFF",(0,0,size,size))
        
        k = size / self.world.width
        k2 = int(k/2)
        
        # draw beetles
        for beetle in self.world.beetles:
            position = beetle.position
            
            x, y = int(position[0]*k)+pad, int(position[1]*k)+pad
            color = "#%02x%02x%02x" % tuple(beetle.color)
            
            self.photoimage.put(color,(x - k2, y - k2, x + k2, y + k2))
          
        self.canvas.create_image(0, 0, image = self.photoimage, anchor=tk.NW)
        
        # draw active beetle
        if not (self.active_beetle is None):
            position = self.active_beetle.position
            
            x = int(position[0] * k) + pad
            y = int(position[1] * k) + pad
        
            self.canvas.create_rectangle(x - k2 - 2, y - k2 - 2, x + k2 + 2, y + k2 + 2, outline="red", width=2)
        
        
        
        
        
        
        
    def canvas_clicked(self, event):
        pad = self.canvas_inner_pad
        size = self.canvas.winfo_width() - 2*pad
        
        k = size / self.world.width
        k2 = k/2
        
        x = int((event.x-pad+k2) / k)
        y = int((event.y-pad+k2) / k)
        
        if (x,y) in self.world.positions:
            i = self.world.positions.index((x,y))
            
            self.active_beetle = self.world.beetles[i]
            
            self.update_canvas()
            
    
        
        
    def run_clicked(self):
        print("run")
        
    
        
        
    
    def step_clicked(self):
        print("stop")
    


t = tk.Tk()
a = App(t, world)    
t.mainloop()

