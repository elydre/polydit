import config
import tkinter as tk
from tkinter.filedialog import asksaveasfile
from tkinter import filedialog

global old_dim
geometry = "1050x700"
old_dim = iter(geometry.split("x"))


fenetre = tk.Tk()
fenetre.geometry(geometry)
fenetre.title("polydit")
fenetre.configure(background="#000000")

get_dimensions = lambda: [fenetre.winfo_width(), fenetre.winfo_height()]

def push():
    global chemin
    print(chemin)
    if chemin == "...":
        return save_file()
    with open(chemin, "w") as fichier:
        fichier.write(ZCODE.get("1.0", tk.END))

def save_file():
    global chemin
    fichier = asksaveasfile(filetypes = files, defaultextension = files)
    if fichier is not None:
        chemin = fichier.name
        fichier.write(ZCODE.get("1.0", tk.END))
        fichier.close()

def open_file():
    global chemin
    temp = filedialog.askopenfilename(filetypes = files, defaultextension = files)
    if temp != "":
        chemin = temp
        with open(chemin, "r") as fichier:
            ZCODE.delete("1.0", tk.END)
            ZCODE.insert("1.0", fichier.read())

def refr():
    with open(chemin, "r") as fichier:
        ZCODE.delete("1.0", tk.END)
        ZCODE.insert("1.0", fichier.read())
    if do_actu:
        fenetre.after(config.interval_actu, refr)

def bool_refr():
    global do_actu
    if chemin != "...":
        do_actu = not do_actu
        if do_actu:
            refr()
            BT_REFR.configure(background="#006600")
        else:
            BT_REFR.configure(background="#12172B")
    else:
        print("Pas de fichier chargé")


def setup_editor():
    global ZCODE, BT_LOAD, BT_SAVE, BT_PUSH, BT_REFR, LB_NAME, chemin, files, list_tag, do_actu
    list_tag = []
    do_actu = False
    chemin = "..."
    files = config.files
    ZCODE = tk.Text(fenetre, bg="#0C0F1D", fg="#FFFFFF", insertbackground=config.curseur_color, font=config.main_font)

    BT_SAVE = tk.Button(fenetre, bg="#12172B", fg="#FFFFFF", text="SAVE AS", command=save_file)
    BT_PUSH = tk.Button(fenetre, bg="#12172B", fg="#FFFFFF", text="SAVE",    command=push)
    BT_LOAD = tk.Button(fenetre, bg="#12172B", fg="#FFFFFF", text="LOAD",    command=open_file)
    BT_REFR = tk.Button(fenetre, bg="#12172B", fg="#FFFFFF", text="REFRESH", command=bool_refr)
    LB_NAME =  tk.Label(fenetre, bg="#12172B", fg="#FFFFFF", text="", anchor="w", font=config.main_font)
    place_editor()

def kill_editor():
    ZCODE.destroy()

def place_editor():
    x, y = get_dimensions()

    ZCODE.place(x=0, y=30, width=x, height=y-30)
    BT_SAVE.place(x=0, y=0, width=100, height=30)
    BT_PUSH.place(x=100, y=0, width=100, height=30)
    BT_LOAD.place(x=200, y=0, width=100, height=30)
    BT_REFR.place(x=300, y=0, width=100, height=30)
    LB_NAME.place(x=400, y=0, width=x-300, height=30)


def get_text():
    return list(ZCODE.get("1.0", tk.END).split("\n")[:-1])



def actu():
    global old_dim, list_tag
    new_dim = get_dimensions()

    if old_dim != new_dim:
        print("Dimensions changées", new_dim)
        place_editor()
        old_dim = new_dim

    for tag in list_tag:
        ZCODE.tag_delete(tag)

    if config.get_colors("", chemin.split(".")[-1]) is not False:
        LB_NAME.configure(text=f" •  {chemin}  •  {chemin.split('.')[-1]}")
        for l in range(len(get_text())):
            ligne = get_text()[l]
            liste_color = config.get_colors(ligne, chemin.split(".")[-1])
            if liste_color is not None:
                for e in liste_color:
                    ZCODE.tag_add(e[1], f"{l+1}.{e[0][0]}", f"{l+1}.{e[0][1]}")
                    list_tag.append(e[1])
                    ZCODE.tag_configure(e[1], foreground=e[1])
    else:
        LB_NAME.configure(text=f" •  {chemin}  •  pas de module")

    fenetre.after(250, actu)
setup_editor()
actu()

fenetre.mainloop()