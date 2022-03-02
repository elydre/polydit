def get_colors(ligne): # sourcery no-metrics
    colors = []

    in_comment = False
    autre_lettre = False

    theme = {
        "comment": "green",
        "keyword": "#c73fe5",
        "number": "#90d7b8",
        "operator": "#928a8a",
    }
    
    for i in range(len(ligne)):
        car = ligne[i]

        if i > 0 and car == '/' and ligne[i-1] == '/':
            in_comment = True
            break
        
        elif car in list("+-*/%=^<>"):
            colors.append([[i, i+1], theme["operator"]])

        elif car in list("0123456789"):
            colors.append([[i, i+1], theme["number"]])

        elif car in list("#ABCDEFHILRSTVXZ") and not autre_lettre:
            colors.append([[i, i+1], theme["keyword"]])

        if car not in [" ", "\t"]:
            autre_lettre = True

    if in_comment:
        colors.append([[0, len(ligne)], theme["comment"]])

    for mot in ["IF", "END", "LOOP", "RETURN", "FUNC"]:
        if mot in ligne:
            colors.append([[ligne.find(mot), ligne.find(mot)+len(mot)], theme["keyword"]])

    return colors