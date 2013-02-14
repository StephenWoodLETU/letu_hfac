# A collection of utilities related to electrical engineering

def Vswr(roe):
        "Returnd the VSWR of a certain absolute value of roe."
        return (1 + float(abs(roe))) / (1 - float(abs(roe)))

def tooComplex(form):
        "Converts a execl style formula to a complex number"
        parts=form.split("(")[1].split(")")[0].split(",")
        return complex(float(parts[0]),float(parts[1]))
        
