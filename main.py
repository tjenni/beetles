import tkinter as tk
from helper import ScrollbarFrame
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
    
    
        
        
    
    

class App(tk.Tk):
    
    def __init__(self, world):
        super().__init__()
        
        self.title('Beetle v1.0')
        
        self.resizable(True, True)
        
        
        
        self.world = world
        
        self.active_beetle = None
        
        
        
        
        self.geometry('800x400')
        
        
        
        # init frames
        
        self.frame_left = tk.Frame(self, bg="white")
        self.frame_left.grid(row=0, column=0, sticky='nsew')
       
        self.frame_right = tk.Frame(self, bg="white")
        self.frame_right.grid(row=0, column=1, sticky='nsew')
        
        self.grid_rowconfigure(0, minsize=400, weight=1)
        self.grid_columnconfigure(0, minsize=400, weight=1)
        self.grid_columnconfigure(1, minsize=400,weight=1)
       
        
        
        
        
    
        # init canvas
        self.canvas_inner_pad = 10
        
        self.canvas = tk.Canvas(self.frame_left, highlightthickness=1, highlightbackground="black")
        self.canvas.bind("<Configure>", self.resize_canvas)
        self.canvas.bind("<Button-1>", self.canvas_clicked)
        self.canvas.pack(fill="x",anchor=tk.NW, expand=True, padx=10,pady=10)
        
       
        
        
        self.frame_button = tk.Frame(self.frame_right, bg="white")
        self.frame_right.columnconfigure(0, weight=1)
        self.frame_right.rowconfigure(3, weight=1)
        self.frame_button.grid(row=0, column=0, sticky='nw')
        
        

        self.button_run = tk.Button(self.frame_button,
            text="run",
            width=5,
            height=1,
            activeforeground="#f00",
            command=self.run_clicked)
        
        self.button_run.pack(side=tk.LEFT, anchor=tk.NW, padx=10, pady=10)
        
        self.button_stop = tk.Button(self.frame_button,
            text="step",
            width=5,
            height=1,
            activeforeground="#f00",
            command=self.step_clicked)
        
        self.button_stop.pack(side=tk.LEFT, anchor=tk.NW, padx=10, pady=10)
        
        
        
        # Info Frame
        
        
        
        self.frame_info = tk.Frame(self.frame_right, bg="white")
        self.frame_info.grid(row=1, column=0, sticky='nw')
        
        
        self.label_time = tk.Label(self.frame_info, text="Zeit: 100", font = ('Helvetica', 12, 'bold'))
        self.label_time.grid(row=0, column=0, sticky="W")
        
        self.label_n_beetles = tk.Label(self.frame_info, text="Anzahl Käfer: 100", font = ('Helvetica', 12, 'bold'))
        self.label_n_beetles.grid(row=1, column=0, sticky="W")
        
        self.label_n_generation = tk.Label(self.frame_info, text="Generationen: 100", font = ('Helvetica', 12, 'bold'))
        self.label_n_generation.grid(row=2, column=0, sticky="W")
        
        
        
        
        
        
        # Genome Frame
        
        label = tk.Label(self.frame_right, text="Genom", font = ('Helvetica', 12, 'bold'))
        label.grid(row=2, column=0, sticky="W")
                
        
        self.frame_genome = ScrollbarFrame(self.frame_right, highlightthickness=1, highlightbackground="black")
        self.frame_genome.grid(row=3, column=0, sticky='nswe', padx=10, pady=10)
        
        scrolled_frame = self.frame_genome.scrolled_frame
        
        # init genome table
        self.genome_table = []
        
        
        
        for i in range(32):

            cols = []

            for j in range(8):
                label = tk.Label(scrolled_frame, text="",  width=4, anchor="e")
                
                label.grid(row=i+1, column=j)
                
                cols.append(label)

            self.genome_table.append(cols)
        
        

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
            
            self.show_genome()
            self.update_canvas()
            
            
            
            
    def show_genome(self):
        
        genome = self.active_beetle.genome
        n = len(genome)
        
        i = 0
        for row in self.genome_table:
            for col in row:
                
                if i < n:
                    col['text'] = genome[i]
                else:
                    col['text'] = ""
                    
                i += 1
            
        
        
        
        
        
        
    def run_clicked(self):
        print("run")
        
    
        
        
    
    def step_clicked(self):
        print("stop")
    




if __name__ == "__main__":
    App(world).mainloop()
    
    
