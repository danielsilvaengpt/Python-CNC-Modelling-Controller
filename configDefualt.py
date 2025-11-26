import configparser
import os
from tkinter import Tk
from tkinter.filedialog import askopenfilename

def atualizarDados(x_max, y_max, z_max, dim, pin_spacing, angle, filencp):
    config_file = 'config.ini'
    # Criar um objeto ConfigParser
    config = configparser.ConfigParser()
    # Verificar se o arquivo de configuração existe
    if os.path.exists(config_file):
        # Ler o arquivo de configuração existente
        config.read(config_file)

        # Converter os valores para strings antes de atribuí-los aos campos de configuração
        config['DEFAULT']['maximox'] = str(x_max)
        config['DEFAULT']['maximoy'] = str(y_max)
        config['DEFAULT']['maximoz'] = str(z_max)
        config['DEFAULT']['diamtropino'] = str(dim)
        config['DEFAULT']['espaçoentrepinos'] = str(pin_spacing)
        config['DEFAULT']['angulopino'] = str(angle)
        config['DEFAULT']['filencp'] = filencp

        with open(config_file, 'w') as f:
            config.write(f)


def VerificarConfig():
    # Caminho do arquivo de configuração
    config_file = 'config.ini'
    int_X = 0
    int_Y = 0
    int_Z = 0
    int_Dim = 0
    int_PS =  0
    int_Angle = 0
    int_File = 0


    # Criar um objeto ConfigParser
    config = configparser.ConfigParser()

    # Verificar se o arquivo de configuração existe
    if os.path.exists(config_file):
        # Ler o arquivo de configuração existente
        config.read(config_file)

        # Acessar os valores da seção "DEFAULT"
        x_max = config['DEFAULT'].getint('maximox')
        y_max = config['DEFAULT'].getint('maximoy')
        z_max = config['DEFAULT'].getfloat('maximoz')
        dim = config['DEFAULT'].getfloat('diamtropino')
        pin_spacing = config['DEFAULT'].getfloat('espaçoentrepinos')
        angle = config['DEFAULT'].getint('angulopino')
        filencp = config['DEFAULT']['filencp']

        if filencp == '' or x_max == 0 or y_max == 0 or z_max == 0.0 or dim == 0.0 or pin_spacing == 0.0 or angle == 0:
            if filencp == '':
                int_File = 1
                #root = Tk()
                #root.withdraw()
                #filencp = askopenfilename(filetypes=[("ncp files", "*.ncp")])

            if x_max == 0:
                #x_max = input("Enter the maximum X value (mm): ")
                int_X = 1

            if y_max == 0:
                #y_max = input("Enter the maximum Y value (mm): ")
                int_Y = 1

            if z_max == 0.0:
                #z_max = input("Enter the maximum Z value (mm): ")
                int_Z = 1

            if dim == 0.0:
                #dim = input("Enter the pin diameter (mm): ")
                int_Dim = 1

            if pin_spacing == 0.0:
                #pin_spacing = input("Enter the pin spacing (mm): ")
                int_PS = 1

            if angle == 0:
                #angle = input("Enter an angle: ")
                int_Angle = 1

            # Atualizar os valores no arquivo de configuração
            #config['DEFAULT']['maximox'] = x_max
            #config['DEFAULT']['maximoy'] = y_max
            #config['DEFAULT']['maximoz'] = z_max
            #config['DEFAULT']['diamtropino'] = dim
            #config['DEFAULT']['espaçoentrepinos'] = pin_spacing
            #config['DEFAULT']['angulopino'] = angle
            #config['DEFAULT']['filencp'] = filencp

            #with open(config_file, 'w') as f:
                #config.write(f)

    else:
        # Criar um arquivo de configuração com os valores padrão
        config['DEFAULT'] = {
            'maximox': 0,
            'maximoy': 0,
            'maximoz': 0.0,
            'diamtropino': 0.0,
            'espaçoentrepinos': 0.0,
            'angulopino': 0,
            'filencp': ''
        }

        with open(config_file, 'w') as f:
            config.write(f)

        print('Arquivo de configuração criado com valores padrão.')

        return VerificarConfig()

    return int_X, int_Y, int_Z, int_Dim, int_PS, int_Angle, int_File


def ValoresConfig():
    config_file = 'config.ini'
    config = configparser.ConfigParser()
    if os.path.exists(config_file):
        config.read(config_file)

        x_max = config['DEFAULT'].getint('maximox')
        y_max = config['DEFAULT'].getint('maximoy')
        z_max = config['DEFAULT'].getfloat('maximoz')
        dim = config['DEFAULT'].getfloat('diamtropino')
        pin_spacing = config['DEFAULT'].getfloat('espaçoentrepinos')

        # Verificar se o valor para 'angulopino' é um número inteiro válido
        try:
            angle = config['DEFAULT'].getint('angulopino')
        except ValueError:
            angle = 0  # Valor padrão caso não seja um número inteiro válido

        filencp = config['DEFAULT'].get('filencp')

        return x_max, y_max, z_max, dim, pin_spacing, angle, filencp

    return None