# Creates ColorScheme objects to store the colors of the game
from tkinter import *

class LightsOutTheme:
    def __init__(self, 
                 num_colors, 
                 lightcolors=None, 
                 solcolors=None,
                 themelightsconfig=None,
                 themewidgetconfig=None,
                 themebackgroundconfig=None):
        self.num_colors=num_colors
        if lightcolors is None:
            self.lightcolors = LightsOutTheme.defaultcolors(num_colors)
        else:
            self.lightcolors = lightcolors
        if solcolors is None:
            self.solcolors = LightsOutTheme.defaultsolcolors(num_colors)
        else:
            self.solcolors = solcolors
        if themelightsconfig is None:
            self.themelightsconfig = LightsOutTheme.defaultlightconfig()
        else:
            self.themelightsconfig = themelightsconfig
        if themewidgetconfig is None:
            self.themewidgetconfig = LightsOutTheme.defaultwidgetconfig()
        else:
            self.themewidgetconfig = themewidgetconfig
        if themebackgroundconfig is None:
            self.themebackgroundconfig = LightsOutTheme.defaultbackgroundconfig()
        else:
            self.themebackgroundconfig = themebackgroundconfig

    @staticmethod
    def defaultcolors(n):  # Returns the default color scheme for n colors. The default color scheme when
        # there are n colors are just n approximately evenly spaced shades of gray
        colors = ["#000000"]  # List containing only the black color
        for i in range(1, n):
            j = format(int(255 * i / (n - 1)), "02x")
            s = f"#{j}{j}{j}"
            colors.append(s)
        return colors
    
    @staticmethod
    def defaultsolcolors(n):  # Returns the default color scheme for n colors. The default color scheme when
        # there are n colors are just n approximately evenly spaced shades of gray
        colors = ["#000000"]  # List containing only the black color
        for i in range(1, n):
            j = format(int(255 * i / (n - 1)), "02x")
            s = f"#00{j}00"
            colors.append(s)
        return colors
    
    @staticmethod
    def defaultlightconfig():
        dlcdictionary = {}
        dlcdictionary.update({"fg":"#007F00"})
        dlcdictionary.update({"width":3})
        dlcdictionary.update({"height":1})
        dlcdictionary.update({"font":("Calibri",18)})
        return dlcdictionary
        
    @staticmethod
    def defaultwidgetconfig():
        dwcdictionary = {}
        dwcdictionary.update({"bg":"#CCCCCC"})
        dwcdictionary.update({"lheight": 2})
        dwcdictionary.update({"sheight": 1})
        dwcdictionary.update({"width": 15})
        dwcdictionary.update({"bd": 4})
        dwcdictionary.update({"relief": RAISED})
        dwcdictionary.update({"lfont": ("Calibri, 30")})
        dwcdictionary.update({"sfont": ("Calibri, 18")})
        dwcdictionary.update({"padx": 20})
        dwcdictionary.update({"pady": 5})
        dwcdictionary.update({"ebg": "#FF9999"})  # Background color for widget when improper input is given.
        dwcdictionary.update({"twidth": 27}) # Width of textbox when displayed
        dwcdictionary.update({"theight": 10})  # Width of textbox when displayed
        return dwcdictionary

    @staticmethod
    def defaultbackgroundconfig():
        dbcdictionary = {}
        dbcdictionary.update({"bg": "#999999"})
        dbcdictionary.update({"mmpadx": 50})
        dbcdictionary.update({"pady": 20})
        dbcdictionary.update({"owpadx": 20})
        return dbcdictionary

    def themelabel(self, parent, t, size="s"):
        label = Label(parent,
                     text=t,
                     width=self.themewidgetconfig.get("width"),
                     bg=self.themewidgetconfig.get("bg"),
                     bd=self.themewidgetconfig.get("bd"),
                     relief=self.themewidgetconfig.get("relief"),
                     font=self.themewidgetconfig.get("font"))
        if size=="s":
            label.configure(font=self.themewidgetconfig.get("sfont"))
            label.configure(height=self.themewidgetconfig.get("sheight"))
        elif size=="l":
            label.configure(font=self.themewidgetconfig.get("lfont"))
            label.configure(height=self.themewidgetconfig.get("lheight"))
        return label
    
    def themeentry(self, parent, size="s"):
        entry = Entry(parent,
                     width=self.themewidgetconfig.get("width"),
                     bg=self.themewidgetconfig.get("bg"),
                     bd=self.themewidgetconfig.get("bd"),
                     relief=self.themewidgetconfig.get("relief"))
        if size=="s":
            entry.configure(font=self.themewidgetconfig.get("sfont"))
        elif size=="l":
            entry.configure(font=self.themewidgetconfig.get("lfont"))
        return entry
    
    def themebutton(self, parent, t, c=None, size="s"):
        button = Button(parent,
                      text=t,
                      command=c,
                      height=self.themewidgetconfig.get("height"),
                      width=self.themewidgetconfig.get("width"),
                      bg=self.themewidgetconfig.get("bg"),
                      bd=self.themewidgetconfig.get("bd"),
                      relief=self.themewidgetconfig.get("relief"),
                      font=self.themewidgetconfig.get("font"))
        if size=="s":
            button.configure(font=self.themewidgetconfig.get("sfont"))
            button.configure(height=self.themewidgetconfig.get("sheight"))
        elif size=="l":
            button.configure(font=self.themewidgetconfig.get("lfont"))
            button.configure(height=self.themewidgetconfig.get("lheight"))
        return button
    
    def themelightbutton(self, parent, bg):
        lightbutton = Button(parent,
                             bg=bg,
                             fg=self.themelightsconfig.get("fg"),
                             width=self.themelightsconfig.get("width"),
                             height=self.themelightsconfig.get("height"),
                             font=self.themelightsconfig.get("font"))
        return lightbutton

    def themetextbox(self, parent):
        textbox = Text(parent,
                       wrap=WORD,
                       bg=self.themewidgetconfig.get("bg"),
                       bd=self.themewidgetconfig.get("bd"),
                       relief=self.themewidgetconfig.get("relief"),
                       fg=self.themewidgetconfig.get("fg"),
                       width=self.themewidgetconfig.get("twidth"),
                       height=self.themewidgetconfig.get("theight"),
                       font=self.themewidgetconfig.get("sfont"))
        return textbox