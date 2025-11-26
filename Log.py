
def EscreverZ0(FileNCP , P , x , y):

        PontoReferenciaX = 0
        PontoReferenciaY = 0

        Px = x + PontoReferenciaX
        Py = y + PontoReferenciaY

        with open(FileNCP, 'w') as file:
            file.write("M71")
            file.write("\n")
            file.write("G00" + " X" + str(Px) + " Y" + str(Py) + " A0")
            file.write(" F"+P)


def EscreverZ(FileNCP, F, x , y , z_CR):

    PontoReferenciaZ = 0
    Diferenca =  8.128 + 19.5
    PontoReferenciaX = 0
    PontoReferenciaY = 0

    Px = x + PontoReferenciaX
    Py = y + PontoReferenciaY

    PZ = z_CR + PontoReferenciaZ + Diferenca
    with open(FileNCP, 'w') as file:
        file.write("M71")
        file.write("\n")
        file.write("G01" + " X" + str(Px) + " Y" + str(Py) + " A" + str(PZ))
        file.write(" F" + F)


def EscreverZB(FileNCP, F,x,y,z,z_Cr):
    PontoReferenciaZ = 0
    Diferenca = 8.128 + 19.5
    PontoReferenciaX = 0
    PontoReferenciaY = 0

    Px = x + PontoReferenciaX
    Py = y + PontoReferenciaY

    DifZ_ZCR = z - z_Cr

    PZ = z_Cr + PontoReferenciaZ + Diferenca + DifZ_ZCR
    with open(FileNCP, 'w') as file:
        file.write("M70")
        file.write("\n")
        file.write("G01" + " X" + str(Px) + " Y" + str(Py) + " A" + str(PZ) + " B" + str(DifZ_ZCR) + " F" + F)
        #file.write(" F" + F)

def EscreverPZ0(FileNCP, F, x , y):
    PontoReferenciaX = 0
    PontoReferenciaY = 0

    Px = x + PontoReferenciaX
    Py = y + PontoReferenciaY
    with open(FileNCP, 'w') as file:
        file.write("M71")
        file.write("\n")
        file.write("G01" + " X" + str(Px) + " Y" + str(Py) + " A0" + " F" + F)

def EscreverPB0(FileNCP, x , y):
    PontoReferenciaX = 0
    PontoReferenciaY = 0

    Px = x + PontoReferenciaX
    Py = y + PontoReferenciaY
    with open(FileNCP, 'w') as file:
        file.write("M71")
        file.write("\n")
        file.write("G00" + " X" + str(Px) + " Y" + str(Py) + " A0" + " B0")

def Escrever0(FileNCP, F):
    with open(FileNCP, 'w') as file:
        file.write("M71")
        file.write("\n")
        file.write("G00 X0 Y0")
        file.write(" F" + F)

def EscreverZReset(FileNCP, F, x , y , z , z_CR):
    PontoReferenciaZ = 0
    Diferenca = 8.128 + 19.5
    PontoReferenciaX = 0
    PontoReferenciaY = 0

    Px = x + PontoReferenciaX
    Py = y + PontoReferenciaY

    PZ = z_CR + PontoReferenciaZ + Diferenca

    with open(FileNCP, 'w') as file:
        file.write("M71")
        file.write("\n")
        file.write("G01" + " X" + str(Px) + " Y" + str(Py) + " A" + str(PZ))
        file.write(" F" + F)


def EscreverZABReset(FileNCP, F, x, y, z, z_CR):
    PontoReferenciaZ = 0
    Diferenca = 8.128 + 19.5
    PontoReferenciaX = 0
    PontoReferenciaY = 0

    Px = x + PontoReferenciaX
    Py = y + PontoReferenciaY

    with open(FileNCP, 'w') as file:
        file.write("M70")
        file.write("\n")
        file.write("G01" + " X" + str(Px) + " Y" + str(Py) + " A" + str(Diferenca) + " B-"+ str(z_CR))
        file.write(" F" + F)

def EscreverZAReset(FileNCP, F, x, y):

    PontoReferenciaX = 0
    PontoReferenciaY = 0

    Px = x + PontoReferenciaX
    Py = y + PontoReferenciaY

    with open(FileNCP, 'w') as file:
        file.write("M71")
        file.write("\n")
        file.write("G01" + " X" + str(Px) + " Y" + str(Py) + " A0")
        file.write(" F" + F)


def EscreverZB0Reset(FileNCP, F, x, y):

    PontoReferenciaX = 0
    PontoReferenciaY = 0

    Px = x + PontoReferenciaX
    Py = y + PontoReferenciaY

    with open(FileNCP, 'w') as file:
        file.write("M71")
        file.write("\n")
        file.write("G00" + " X" + str(Px) + " Y" + str(Py) + " A0" + " B0")
