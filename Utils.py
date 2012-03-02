# A collection of utilities related to electrical engineering

def Vswr(roe):
	"Returnd the VSWR of a certain absolute value of roe."
	return (1 + float(abs(roe))) / (1 - float(abs(roe)))

