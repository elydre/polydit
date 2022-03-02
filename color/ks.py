def get_colors(ligne): # sourcery no-metrics
    colors = []

    in_string = False
    debut_string = 0

    in_comment = False
    
    in_var = False
    debut_var = 0

    theme = {
        "comment": "green",
        "string": "#c66421",
        "push": "#e1d600",
        "keyword": "#c73fe5",
        "var": "#86eaee",
        "number": "#90d7b8",
        "operator": "#928a8a",
    }
    
    for i in range(len(ligne)):
        car = ligne[i]

        if car == '"' and in_string:
            colors.append([[debut_string, i+1], theme["string"]])

        if car == '"':
            in_string = not in_string
            if in_string:
                debut_string = i

        elif i > 0 and car == '/' and ligne[i-1] == '/':
            in_comment = True
            break

        elif car == ">" and not in_string:
            colors.append([[i, i+1], theme["push"]])
        
        elif car in list("+-*/%=^") and not in_string:
            colors.append([[i, i+1], theme["operator"]])

        elif car == "$" and not in_string:
            in_var = True
            debut_var = i

        elif car == " " and in_var:
            in_var = False
            colors.append([[debut_var, i], theme["var"]])

        elif car in list("0123456789") and not in_string:
            colors.append([[i, i+1], theme["number"]])

    if in_comment:
        colors.append([[0, len(ligne)], theme["comment"]])
    
    if in_string:
        colors.append([[debut_string, len(ligne)], theme["string"]])

    if in_var:
        colors.append([[debut_var, len(ligne)], theme["var"]])

    for mot in ["IF", "END", "LOOP", "RETURN", "FUNC"]:
        if mot in ligne:
            colors.append([[ligne.find(mot), ligne.find(mot)+len(mot)], theme["keyword"]])

    return colors