# https://stackoverflow.com/questions/3085696/adding-a-scrollbar-to-a-group-of-widgets-in-tkinter/3092341#3092341
'''
class App(tk.Tk):
    def __init__(self):
        super().__init__()

        sbf = ScrollbarFrame(self)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        sbf.grid(row=0, column=0, sticky='nsew')
        # sbf.pack(side="top", fill="both", expand=True)

        # Some data, layout into the sbf.scrolled_frame
        frame = sbf.scrolled_frame
        for row in range(50):
            text = "%s" % row
            tk.Label(frame, text=text,
                     width=3, borderwidth="1", relief="solid") \
                .grid(row=row, column=0)

            text = "this is the second column for row %s" % row
            tk.Label(frame, text=text,
                     background=sbf.scrolled_frame.cget('bg')) \
                .grid(row=row, column=1)


if __name__ == "__main__":
    App().mainloop()
'''

import tkinter as tk

class ScrollbarFrame(tk.Frame):
    """
    Extends class tk.Frame to support a scrollable Frame 
    This class is independent from the widgets to be scrolled and 
    can be used to replace a standard tk.Frame
    """
    def __init__(self, parent, **kwargs):
        tk.Frame.__init__(self, parent, **kwargs)

        # The Scrollbar, layout to the right
        vsb = tk.Scrollbar(self, orient="vertical")
        vsb.pack(side="right", fill="y")

        # The Canvas which supports the Scrollbar Interface, layout to the left
        self.canvas = tk.Canvas(self, borderwidth=0, background="#ffffff")
        self.canvas.pack(side="left", fill="both", expand=True)

        # Bind the Scrollbar to the self.canvas Scrollbar Interface
        self.canvas.configure(yscrollcommand=vsb.set)
        vsb.configure(command=self.canvas.yview)

        # The Frame to be scrolled, layout into the canvas
        # All widgets to be scrolled have to use this Frame as parent
        self.scrolled_frame = tk.Frame(self.canvas, background=self.canvas.cget('bg'))
        self.canvas.create_window((4, 4), window=self.scrolled_frame, anchor="nw")

        # Configures the scrollregion of the Canvas dynamically
        self.scrolled_frame.bind("<Configure>", self.on_configure)
        
        self.offset_y = 0
        self.scroll_y = 0
        
        self.scrolled_frame.bind_all('<Button-1>', self.on_press)
        self.scrolled_frame.bind_all('<B1-Motion>', self.on_touch_scroll)


    def on_configure(self, event):
        """Set the scroll region to encompass the scrolled frame"""
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
    
    def on_press(self, event):
        self.offset_y = event.y_root + self.canvas.canvasy(0)
        
    def on_touch_scroll(self, event):
        dy = event.y_root - self.offset_y
        height = self.scrolled_frame.winfo_height() 
        
        self.canvas.yview_moveto(-dy/height)
        
