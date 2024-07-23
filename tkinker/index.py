import tkinter as tk
import tkinter as tk

# Création de la fenêtre principale
fenetre = tk.Tk()

# Frame 1
Frame1 = tk.Frame(fenetre, width=300, height=1000, bg='lightblue')
Frame1.pack_propagate(False) 
Frame1.pack(side=tk.LEFT, padx=10, pady=0)

# Frame 2
Frame2 = tk.Frame(fenetre, width=300, height=500,bg="red")
Frame1.pack_propagate(False) 
Frame2.pack(side=tk.RIGHT, padx=0, pady=0)


# Frame 3 dans Frame 2
# Ajout de labels
# Lancer la boucle principale
fenetre.mainloop()
