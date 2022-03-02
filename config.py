import color.ks as ks

# fichier dans l'explorateur
files = [
    ('All Files', '*.*'),
    ('KEA stream', '*.ks'),
    ('KEA', '*.KEA'),
    ('Text', '*.txt'),
]

curseur_color = "#f3934b"

main_font = ("consolas", 12)


def get_colors(ligne, extension):
    """
    la fonction doit renvoyer une coordonnée de
    début et de fin avec la couleur correspondante
    exemple:
    [(0, 5, 'red'), (9, 10, 'blue')]
    du caractère 0 à 5  -> couleur rouge
    du caractère 9 à 10 -> couleur bleu
    """

    mod4color = {
        "ks": ks.get_colors
    }

    return mod4color[extension](ligne) if extension in mod4color else False