# -*- coding: utf-8 -*-
#Aleix Leon

#imports
from mpcpy_aleon import * #albums, playlists
from mpc import *

#tkinter ______________________________________________
from tkinter import *
import tkinter.font as font
import tkinter.ttk as ttk
import tkinter as tk

#per gif animat
from PIL import Image, ImageTk
from itertools import count, cycle

#per intèrval
import time


#constants ______________________________________________

#classes objecte ______________________________________________
#interfície gràfica
class Reproductor():
    def __init__(self):

        #ini reproductor_aleon
        self.albums = albums
        self.playlists = llegeix_playlists()
        self.generes = llegeix_generes(albums)
        self.autors = llegeix_autors(albums)
        self.anys = llegeix_anys(albums)
        self.anys.sort()
        self.cops = llegeix_cops(albums)
        self.cops.sort()
        self.noms_albums = llegeix_noms_albums(albums)

        #var
        self.criteris = ['Gènere','Autor','Anys','Reproduccions']
        self.tipus = "" #per tipus playlist

        #objecte mpc
        self.mpc = MPC()

        #objecte tk
        self.arrel = Tk()

        # set the dimensions of the screen 
        # and where it is placed
        self.geo = self.geometria()
        self.arrel.geometry(self.geo)
        
        #finestra mida fixa
        self.arrel.resizable(0, 0)

        #títol
        self.arrel.title("WINAMP v2022 by Aleon")
        
        #font
        #https://www.geeksforgeeks.org/how-to-set-font-for-text-in-tkinter/
        
        # Create an object of type Font from tkinter.
        self.font1 = font.Font( family = "Consolas", 
                                        size = 20, 
                                        weight = "bold")
        
        #frame info
        self.frame_info = Frame(self.arrel, bg = "white", bd = 0, highlightbackground = "black", highlightcolor = "black", highlightthickness = 0)
        self.frame_info.pack(side = TOP, padx=5, pady=5)
        #self.frame_info.pack(expand=1)
       
        # info (Text)
        #self.input_info = Entry(self.frame_info, width=100 ,font = ('Consolas', 22, 'bold'), textvariable = self.input_text, bg = "white", bd = 0, justify = RIGHT, state='disabled', disabledbackground="white", disabledforeground="black", relief=tk.RAISED, borderwidth=1)
        self.text_info = Text(self.frame_info, width=100 , height=10 ,font = ('Consolas', 24, 'bold'), bg = "white", bd = 0, relief=tk.RAISED, borderwidth=1)
        self.text_info.grid(row = 0, column = 0) #posició en grid
        #self.text_info.pack(ipady = 15) #altura

        #inserto funció que retorna str
        self.text_info.insert(tk.INSERT, str_info(albums))
        self.text_info.config(state='disabled')
        
        # schedule an update every 1 second
        #amb 'after' crida funció 'update_info' al cap d'1 segon
        #a dins funció, hi ha un 2n after que torna a cridar funció cada segon,
        #i així va fent el loop
        self.text_info.after(1000, self.update_interval)

        #test frames
        #self.frame1 = Frame(master=self.arrel, width= 50, height=50, bg="red")
        #self.frame1.pack(fill=tk.X)
        #self.frame2 = Frame(master=self.arrel, width=100, bg="yellow")
        #self.frame2.pack(fill=tk.Y, side=tk.LEFT)

        #imatges
        # Creating a photoimage object to use image
        #subsample redimensiona
        self.img_play = PhotoImage(file = "./img/PLAY.png").subsample(4,4)
        self.img_stop = PhotoImage(file = "./img/STOP.png").subsample(4,4)
        self.img_prev = PhotoImage(file = "./img/PREV.png").subsample(4,4)
        self.img_next = PhotoImage(file = "./img/NEXT.png").subsample(4,4)
        self.img_rand = PhotoImage(file = "./img/RANDOM.png").subsample(4,4)
        
        self.img_album = PhotoImage(file = "./img/ALBUMS.png").subsample(4,4)
        self.img_load = PhotoImage(file = "./img/PLAYLIST.png").subsample(4,4)
        self.img_crea = PhotoImage(file = "./img/CREAR.png").subsample(4,4)
        self.img_reset = PhotoImage(file = "./img/RESET.png").subsample(4,4)
        self.img_exit = PhotoImage(file = "./img/SORTIR.png").subsample(4,4)

        #frame eq (eq + volum)
        self.eq_frame = Frame(self.arrel, width=100, bg = "white")
        self.eq_frame.pack(fill=tk.X, padx=5, pady=5)
        
        #eq gif animat
        self.lbl = ImageLabel(self.eq_frame)
        self.lbl.grid(row = 1, column = 0, padx = 10, pady = 1)
        
        #control parar gif animat, si playing o no
        if len(self.playlists) > 0:
            self.lbl.load('./img/EQ_.gif')
        else:
            self.lbl.load('./img/EQ_OFF.gif')

        #self.volum = 30
        #volum, "value" = valor escala, ja es passa a funció onMove
        self.barra_volum = tk.Scale(self.eq_frame, label='Volum ',
            command=self.onMove,
            #command = lambda: self.onMove(self.volum),
            #variable=self.volum,
            from_=0, to=100,
            length=500, tickinterval=25,
            showvalue='yes', 
            orient='horizontal',
            font = self.font1,
            bg = 'white',
            width = 32
            )
        self.barra_volum.grid(row = 1, column = 1, columnspan = 2, padx = 10, pady = 1)
        
        #assignar valor per defecte a barra
        self.barra_volum.set(30)
        
        #frame butons
        self.btns_frame = Frame(self.arrel, width=100, bg = "white")
        self.btns_frame.pack(fill=tk.X, padx=5, pady=5)
  
        #1a filera 5 butons
        self.bplay = Button(self.btns_frame, image=self.img_play, width = 200, fg = "black", bg = "white", activebackground="#eee", activeforeground="#fff", bd = 0, cursor = "hand2", command = self.play ).grid(row = 0, column = 0, padx = 1, pady = 1)
        self.bstop = Button(self.btns_frame, image=self.img_stop, width = 200, fg = "black", bg = "white", activebackground="#eee", activeforeground="#fff", bd = 0, cursor = "hand2", command = self.pause).grid(row = 0, column = 1, padx = 1, pady = 1)
        self.bprev = Button(self.btns_frame, image=self.img_prev, width = 200, fg = "black", bg = "white", activebackground="#eee", activeforeground="#fff", bd = 0, cursor = "hand2", command = self.prev ).grid(row = 0, column = 2, padx = 1, pady = 1)
        self.bnext = Button(self.btns_frame, image=self.img_next, width = 200, fg = "black", bg = "white", activebackground="#eee", activeforeground="#fff", bd = 0, cursor = "hand2", command = self.next ).grid(row = 0, column = 3, padx = 1, pady = 1)
        self.brand = Button(self.btns_frame, image=self.img_rand, width = 200, fg = "black", bg = "white", activebackground="#eee", activeforeground="#fff", bd = 0, cursor = "hand2", command = self.rand ).grid(row = 0, column = 4, padx = 1, pady = 1)
       
        #labels 1a fila
        self.l1 = Label(self.btns_frame,text="PLAY", font = self.font1, bg='white').grid(row = 1, column = 0, padx = 1, pady = 1)
        self.l2 = Label(self.btns_frame,text="PAUSE", font = self.font1, bg='white').grid(row = 1, column = 1, padx = 1, pady = 1)
        self.l3 = Label(self.btns_frame,text="PREV", font = self.font1, bg='white').grid(row = 1, column = 2, padx = 1, pady = 1)
        self.l4 = Label(self.btns_frame,text="NEXT", font = self.font1, bg='white').grid(row = 1, column = 3, padx = 1, pady = 1)
        self.l5 = Label(self.btns_frame,text="RANDOM", font = self.font1, bg='white').grid(row = 1, column = 4, padx = 1, pady = 1)

        #opcions
        self.bload = Button(self.btns_frame, image=self.img_load, width = 200, fg = "black", bg = "white", activebackground="#eee", activeforeground="#fff", bd = 0, cursor = "hand2", command = self.window_load_playlist ).grid(row = 2, column = 0, padx = 1, pady = 1)
        self.bcrea = Button(self.btns_frame, image=self.img_crea, width = 200, fg = "black", bg = "white", activebackground="#eee", activeforeground="#fff", bd = 0, cursor = "hand2", command = self.window_add_playlist ).grid(row = 2, column = 1, padx = 1, pady = 1)
        self.balbum = Button(self.btns_frame, image=self.img_album, width = 200, fg = "black", bg = "white", activebackground="#eee", activeforeground="#fff", bd = 0, cursor = "hand2", command = self.window_albums ).grid(row = 2, column = 2, padx = 1, pady = 1)
        self.breset = Button(self.btns_frame, image=self.img_reset, width = 200, fg = "black", bg = "white", activebackground="#eee", activeforeground="#fff", bd = 0, cursor = "hand2", command = self.reset ).grid(row = 2, column = 3, padx = 1, pady = 1)
        self.bexit = Button(self.btns_frame, image=self.img_exit, width = 200, fg = "black", bg = "white", activebackground="#eee", activeforeground="#fff", bd = 0, cursor = "hand2", command = self.exit ).grid(row = 2, column = 4, padx = 1, pady = 1)

        #labels fila opcions
        self.l6 = Label(self.btns_frame,text="LOAD", font = self.font1, bg='white').grid(row = 3, column = 0, padx = 1, pady = 1)
        self.l7 = Label(self.btns_frame,text="ADD+", font = self.font1, bg='white').grid(row = 3, column = 1, padx = 1, pady = 1)
        self.l8 = Label(self.btns_frame,text="ALBUM", font = self.font1, bg='white').grid(row = 3, column = 2, padx = 1, pady = 1)
        self.l9 = Label(self.btns_frame,text="RESET", font = self.font1, bg='white').grid(row = 3, column = 3, padx = 1, pady = 1)
        self.l0 = Label(self.btns_frame,text="EXIT", font = self.font1, bg='white').grid(row = 3, column = 4, padx = 1, pady = 1)

        #ampliem frame
        #self.btns_frame.pack(expand=1)

        #Disable the Close Window Control Icon
        self.arrel.protocol("WM_DELETE_WINDOW", self.disable_event)

        #loop finestra activa
        self.arrel.mainloop()

    def geometria(self, tipus = 'ARREL'):
        #mides
        if tipus == 'ARREL':
            w = 1050 # width for the Tk root
            h = 850 # height for the Tk root
        elif tipus == 'ALBUMS':
            w = 1850
            h = 850 

        # get screen width and height
        ws = self.arrel.winfo_screenwidth() # width of the screen
        hs = self.arrel.winfo_screenheight() # height of the screen

        # calculate x and y coordinates for the Tk root window
        x = (ws/2) - (w/2)
        y = (hs/2) - (h/2)

        return '%dx%d+%d+%d' % (w, h, x, y)

    #FINESTRA load playlist_____________________________________
    def window_load_playlist(self):
        self.wplaylist = tk.Toplevel(self.arrel)    
        self.wplaylist.geometry("400x400")
        self.wplaylist.resizable(0, 0) #finestra mida fixa
        self.wplaylist.title("* PLAYLISTS *") #títol
        #self.canvas = tk.Canvas(self.new, height=self.h, width=self.w)
        #self.canvas.pack()
        self.wplaylist.grab_set() #manté focus a finestra

        #listbox
        self.lb = Listbox(self.wplaylist, font = self.font1, width=100)
        
        #for per insertar list a listbox
        for i in self.playlists:
            self.lb.insert(END, i)

        self.lb.bind("<<ListboxSelect>>", self.onSelectPlaylist)
        self.lb.pack()

        #botó tancar
        self.tanca = Button(self.wplaylist, text='TANCAR', 
            font = self.font1, width = 100, 
            fg = "black", bg = "#727bff", 
            activebackground="#b6bbfc", activeforeground="#fff", 
            bd = 0, cursor = "hand2", command = self.wplaylist.destroy )
        self.tanca.pack()

    #en seleccionar item listbox, s'envia 'event'
    def onSelectPlaylist(self, event):   

        # get selected indices
        selected_i = self.lb.curselection()
        
        # get selected items
        selected_v = ",".join([self.lb.get(i) for i in selected_i])
        
        print(f'You selected: {selected_v} index: {selected_i}')
        print(selected_i[0])

        #funció reproductor_aleon
        load_playlist(self.playlists[int(selected_i[0])], albums)

        #play
        self.play()

        #update info
        self.update_info()

    #FINESTRA add playlist_____________________________________
    def window_add_playlist(self):
        self.wplaylist = tk.Toplevel(self.arrel)    
        self.wplaylist.geometry(self.geo) #mida arrel
        self.wplaylist.resizable(0, 0) #finestra mida fixa
        self.wplaylist.title("* ADD PLAYLIST *") #títol
        self.wplaylist.grab_set() #manté focus a finestra

        #listbox 1: criteris
        self.lb = Listbox(self.wplaylist, font = self.font1, width=100, height=5)
        for i in self.criteris:
            self.lb.insert(END, i)
        self.lb.bind("<<ListboxSelect>>", self.on_select_lb1)
        self.lb.pack()

        #listbox 2: consulta segons criteris
        self.lb2 = Listbox(self.wplaylist, font = self.font1, width=100, height=18)
        #self.lb2.bind("<Double-1>", self.on_select_lb2) #doble-click
        self.lb2.bind("<<ListboxSelect>>", self.on_select_lb2)
        self.lb2.pack()

        #missatge
        self.playlist_ok = Text(self.wplaylist, width=100, height=2,font = ('Consolas', 24, 'bold'), bg = "white", fg ="green", bd = 0, relief=tk.RAISED, borderwidth=1)
        self.playlist_ok.pack()

        #botó crear
        self.crea = Button(self.wplaylist, text='CREAR', 
            font = self.font1, width = 100, 
            fg = "black", bg = "#b8eab8", 
            activebackground="#b6bbfc", activeforeground="#fff", 
            bd = 0, cursor = "hand2", command = self.crea_playlist )
        self.crea.pack()

        #botó tancar
        self.tanca = Button(self.wplaylist, text='TANCAR', 
            font = self.font1, width = 100, 
            fg = "black", bg = "#727bff", 
            activebackground="#b6bbfc", activeforeground="#fff", 
            bd = 0, cursor = "hand2", command = self.wplaylist.destroy )
        self.tanca.pack()

    #en seleccionar item listbox, s'envia 'event'
    def on_select_lb1(self, event):

        #ini missatge
        self.playlist_ok.config(state='normal')
        self.playlist_ok.delete('1.0', END) 

        # get selected indices
        selected_i = self.lb.curselection()

        #si selecció
        if selected_i:
        
            # get selected items
            selected_v = ",".join([self.lb.get(i) for i in selected_i])
            
            print(f'You selected: {selected_v} index: {selected_i}')
            print(selected_i[0])

            #segons criteri carrega llista, canvia mode select
            if selected_i[0] == 0:
                self.tipus = "GEN"
                self.lb2.config(selectmode = "single")
                self.update_lb2(self.generes)
            
            elif selected_i[0] == 1:
                self.tipus = "AUTOR"
                self.lb2.config(selectmode = "single")
                self.update_lb2(self.autors)

            elif selected_i[0] == 2:
                self.tipus = "ANY"
                self.lb2.config(selectmode = "multiple")
                self.update_lb2(self.anys)

            elif selected_i[0] == 3:
                self.tipus = "COPS"
                self.lb2.config(selectmode = "multiple")
                self.update_lb2(self.cops)
            
            print(self.tipus)
        
    def update_lb2(self, file_list):
          # updates right listbox
          self.lb2.delete(0, END)
          for i in file_list:
            self.lb2.insert(END, i)

    #al fer click list box 2
    def on_select_lb2(self, event):
        #print('hola list box 2')

        #ini missatge
        self.playlist_ok.config(state='normal')
        self.playlist_ok.delete('1.0', END)

        items =  len( self.lb2.curselection() )
        print(items)
    
    #botó crear playlist
    def crea_playlist(self):

        # agafem selecció listbox 2
        selected_i = self.lb2.curselection()

        #si selecció
        if selected_i:
        
            # get selected items
            selected_v = ",".join([str(self.lb2.get(i)) for i in selected_i])
            print(f'You selected: {selected_v} index: {selected_i}')

            #crea_playlist(val,tipus): tipus = GEN, AUTOR, ...
            #segons tipus, fer llista
            if self.tipus == "GEN":
                crea_playlist(selected_v,'GEN',albums)
            elif self.tipus == "AUTOR":
                crea_playlist(selected_v,'AUTOR',albums)
            elif self.tipus == "ANY":
                #__listbox múltiple, min i max de listbox2 (intèrval)
                valors = str(self.anys[min(selected_i)]) + ' ' + str(self.anys[max(selected_i)])
                crea_playlist(valors,'ANY',albums)
            elif self.tipus == "COPS":
                #__listbox múltiple, min i max de listbox2 (intèrval)
                valors = str(self.cops[min(selected_i)]) + ' ' + str(self.cops[max(selected_i)])
                crea_playlist(valors,'COPS',albums)
            
            #update
            self.update()
            self.update_info

            #missatge
            self.playlist_ok.insert(tk.INSERT, '* PLAYLIST CREADA OK :)')
            self.playlist_ok.config(state='disabled')

            #tancar finestra
            #self.wplaylist.destroy()
    
    #FINESTRA albums_____________________________________
    def window_albums(self):
        self.walbums = tk.Toplevel(self.arrel)    
        self.walbums.geometry( self.geometria('ALBUMS')  ) #passo paràmetre
        self.walbums.resizable(0, 0) #finestra mida fixa
        self.walbums.title("* ALBUMS *") #títol
        self.walbums.grab_set() #manté focus a finestra

        #listbox albums
        self.lalbums = Listbox(self.walbums, font = self.font1, width=50, height=80)
        for i in self.noms_albums:
            self.lalbums.insert(END, i)
        self.lalbums.bind("<<ListboxSelect>>", self.on_select_album)
        self.lalbums.pack(fill=tk.Y, side=tk.LEFT)

        #listbox 2: consulta segons criteris
        self.linfo = Listbox(self.walbums, font = self.font1, width=50, height=80)
        self.linfo.bind("<<ListboxSelect>>", self.on_select_info)
        self.linfo.pack(fill=tk.Y, side=tk.RIGHT)

        #missatge
        self.album_ok = Text(self.walbums, width=100, height=20,font = ('Consolas', 24, 'bold'), bg = "white", fg ="green", bd = 0, relief=tk.RAISED, borderwidth=1)
        self.album_ok.pack()

        #botó del/add song
        self.del_song = Button(self.walbums, text='BORRAR SONG', 
            font = self.font1, width = 100, 
            fg = "black", bg = "#b8eab8", 
            activebackground="#b6bbfc", activeforeground="#fff", 
            bd = 0, cursor = "hand2", command = self.borra_song )
        self.del_song.pack()

        #botó tancar
        self.tanca = Button(self.walbums, text='TANCAR', 
            font = self.font1, width = 100, 
            fg = "black", bg = "#727bff", 
            activebackground="#b6bbfc", activeforeground="#fff", 
            bd = 0, cursor = "hand2", command = self.walbums.destroy )
        self.tanca.pack()

    def on_select_album(self):
        pass

    def on_select_info(self):
        pass

    def borra_song(self):
        pass
    
    #________________________________________________________________
    def update(self):
        #update
        self.albums = albums
        self.playlists = llegeix_playlists()
        self.generes = llegeix_generes(albums)
        self.autors = llegeix_autors(albums)
        self.anys = llegeix_anys(albums)
        self.anys.sort()
        self.cops = llegeix_cops(albums)
        self.cops.sort()
        self.noms_albums = llegeix_noms_albums(albums)

    #update text info, borrem i tornem a insertar
    def update_info(self):
        self.text_info.config(state='normal')
        self.text_info.delete('1.0', END)
        self.text_info.insert(tk.INSERT, str_info(albums))
        self.text_info.config(state='disabled')
        
    #update per intèrval
    def update_interval(self):
        self.text_info.config(state='normal')
        self.text_info.delete('1.0', END)
        self.text_info.insert(tk.INSERT, str_info(albums))
        self.text_info.config(state='disabled')
        
        # schedule an update every 1 second
        self.text_info.after(1000, self.update_interval)

    def play(self):
        #tornem a inicialitzar gif animat de label
        if len(self.playlists) > 0:
            del self.lbl
            self.lbl = ImageLabel(self.eq_frame)
            self.lbl.grid(row = 1, column = 0, padx = 10, pady = 1)
            self.lbl.load('./img/EQ_.gif')
            #play
            self.mpc.play()
            #update info
            self.update_info()
    
    def pause(self):
        #parem gif animat de label
        self.lbl.unload()
        del self.lbl
        self.lbl = ImageLabel(self.eq_frame)
        self.lbl.grid(row = 1, column = 0, padx = 10, pady = 1)
        #pause
        self.mpc.pause()
        #update info
        self.update_info()

    def prev(self):
        self.mpc.prev()
        self.play()
        self.update_info()
    
    def next(self):
        self.mpc.next()
        self.play()
        self.update_info()
    
    def rand(self):
        self.mpc.random()
        self.update_info()

    def reset(self):
        reset(albums)
        self.update()
        self.update_info()
        self.pause()

    def exit(self):
        sortir(albums)
        self.arrel.destroy()

    #per evitar tancar amb botó superior X finestra
    def disable_event():
        pass
        
    #value de la barra, es passa sense fer res
    #també s'obté amb self.barra_volum.get()
    def onMove(self, value):
        """ you can use value or self.scale1.get() """
        s = "Volum = %s" % value
        #show result in the title
        #self.arrel.title(s)
        self.barra_volum['label'] = s
        self.mpc.volum_set(value)
        self.update_info()
    

#per carregar el gif animat
class ImageLabel(tk.Label):
    """
    A Label that displays images, and plays them if they are gifs
    :im: A PIL Image instance or a string filename
    """
    def load(self, im):
        if isinstance(im, str):
            im = Image.open(im)
        frames = []
 
        try:
            for i in count(1):
                frames.append(ImageTk.PhotoImage(im.copy()))
                im.seek(i)
        except EOFError:
            pass
        self.frames = cycle(frames)
 
        try:
            self.delay = im.info['duration']
        except:
            self.delay = 100
 
        if len(frames) == 1:
            self.config(image=next(self.frames))
        else:
            self.next_frame()
 
    def unload(self):
        self.config(image=None)
        self.frames = None
 
    def next_frame(self):
        if self.frames:
            self.config(image=next(self.frames))
            self.after(self.delay, self.next_frame)

#test ______________________________________________________________
#main __________________________________________
#programa  ______________________________________________________________
if __name__ == "__main__":
    
    #inicialitzem
    albums = init()
    #print(albums)
  
    #ini gràfica
    app = Reproductor()



    
