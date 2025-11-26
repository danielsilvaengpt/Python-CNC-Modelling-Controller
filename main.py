import glob
import threading
import time
import os
import sys
from tkinter import Tk
from tkinter.filedialog import askopenfilename

from PyQt6.QtCore import Qt, QSize, QTimer
from PyQt6.QtGui import QFont, QIcon
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QTabWidget, QApplication, QPushButton, QGridLayout, QLabel, QLineEdit,
    QHBoxLayout, QFormLayout, QMessageBox, QTextEdit, QDial, QFrame,
    QGroupBox, QScrollArea
)
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
from matplotlib.figure import Figure
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer

import Log
import PointsManager
import configDefualt


class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.i = 0
        self.j = 0
        self.k = 0
        self.setWindowTitle("MorphingTech Optima")
        self.resize(1750, 1000)

        self.configX = 0
        self.configY = 0
        self.configZ = 0
        self.configDim = 0
        self.configEsp = 0
        self.configAngle = 0
        self.configFile = 0
        self.filencp = ""
        self.modelo_path = None

        # Create a top-level layout
        mainLayout = QVBoxLayout()
        self.setLayout(mainLayout)

        # Create a scroll area
        scrollArea = QScrollArea()
        scrollArea.setWidgetResizable(True)

        # Create a widget for the scroll area
        scrollWidget = QWidget()
        scrollLayout = QVBoxLayout(scrollWidget)
        scrollLayout.setContentsMargins(0, 0, 0, 0)
        scrollArea.setStyleSheet("QScrollArea { border:none; }")

        # Add the scroll widget to the scroll area
        scrollArea.setWidget(scrollWidget)

        # Create the tab widget with two tabs
        tabs = QTabWidget()

        # Set the style sheet for the tab widget
        tabs.setStyleSheet("QWidget { background-color: #151515;"
                           "border-radius: 5px; }"
                           "QTabBar::tab { height: 30px;"
                           "border-radius: 5px;"
                           "color: white;"
                           "width: 120px;"
                           "margin: 13px;"
                           "font-size: 16px;"
                           "font-weight: bold}"
                           "QTabBar::tab:selected {background-color: #d22e2e;}")

        tabs.addTab(self.InitialTabUI(), "Pagina Inicial")
        tabs.addTab(self.ConfigurationsTabUI(), "Configurações")

        # Add the tabs to the scroll layout
        scrollLayout.addWidget(tabs)

        # Add the scroll area to the main layout
        mainLayout.addWidget(tabs)

    def InitialTabUI(self):
        """Create the General page UI."""
        generalTab = QWidget()
        layout = QGridLayout()
        generalTab.setLayout(layout)

        self.button = QPushButton("Selecionar Molde")

        self.button.setStyleSheet("QPushButton { background-color: grey;"
                                  "color: #d22e2e;"
                                  "border-radius: 5px;"
                                  "padding: 10px;"
                                  "font-size: 25px;"
                                  "font-weight: bold;"
                                  "width: 300px;}"
                                  "QPushButton:hover { background-color: black; }"
                                  "QPushButton:pressed { background-color: #b33636;"
                                  "color: black; }")

        self.button.setFixedWidth(350)

        self.buttonPower = QPushButton()
        self.buttonPower.setIconSize(QSize(55, 55))
        self.buttonPower.setIcon(
            QIcon("powerOff-button.png"))  # Substitua "powerOff-button.png" pelo caminho correto da imagem
        self.buttonPower.setStyleSheet(
            "QPushButton { background-color: transparent;"  # Alteração: Plano de fundo transparente
            "border: none;"  # Alteração: Sem borda
            "padding: 0px;"
            "margin-top:10px;"
            "margin-right:10px;}"  # Alteração: Sem preenchimento
            "QPushButton:hover { background-color: transparent; }"
            "QPushButton:pressed { background-color: transparent; }")

        self.toggle2 = QPushButton()
        self.toggle2.setIconSize(QSize(55, 55))
        self.toggle2.setIcon(QIcon("auto_off.png"))  # Substitua "powerOff-button.png" pelo caminho correto da imagem
        self.toggle2.setStyleSheet(
            "QPushButton { background-color: transparent;"  # Alteração: Plano de fundo transparente
            "border: none;"  # Alteração: Sem borda
            "padding: 0px;"
            "margin-top:10px;"
            "margin-right:10px;}"  # Alteração: Sem preenchimento
            "QPushButton:hover { background-color: transparent; }"
            "QPushButton:pressed { background-color: transparent; }")

        self.reset = QPushButton()
        self.reset.setIconSize(QSize(55, 55))
        self.reset.setIcon(QIcon("reset.png"))  # Substitua "powerOff-button.png" pelo caminho correto da imagem
        self.reset.setStyleSheet(
            "QPushButton { background-color: transparent;"  # Alteração: Plano de fundo transparente
            "border: none;"  # Alteração: Sem borda
            "padding: 0px;"
            "margin-top:10px;"
            "margin-right:10px;}"  # Alteração: Sem preenchimento
            "QPushButton:hover { background-color: transparent; }"
            "QPushButton:pressed { background-color: transparent; }")

        buttonRepair = QPushButton()
        buttonRepair.setIconSize(QSize(45, 45))
        buttonRepair.setIcon(QIcon("repair_off.png"))  # Substitua "powerOff-button.png" pelo caminho correto da imagem
        buttonRepair.setStyleSheet(
            "QPushButton { background-color: transparent;"  # Alteração: Plano de fundo transparente
            "border: none;"  # Alteração: Sem borda
            "padding: 0px;"
            "margin-top:10px;"
            "margin-right:10px}"  # Alteração: Sem preenchimento
            "QPushButton:hover { background-color: transparent; }"
            "QPushButton:pressed { background-color: transparent; }")

        self.ButtonPino = QPushButton("OK")
        self.ButtonPino.setStyleSheet("QPushButton { background-color: grey;"
                                      "color: #d22e2e;"
                                      "border-radius: 5px;"
                                      "padding: 10px;"
                                      "font-size: 15px;"
                                      "font-weight: bold;"
                                      "width: 300px;"
                                      "margin-top:5px;}"
                                      "QPushButton:hover { background-color: darkgreen; }"
                                      "QPushButton:pressed { background-color: #b33636;"
                                      "color: black; }")

        self.ButtonPino.setFixedWidth(50)
        self.ButtonPino.setFixedHeight(50)

        # Criar a QLabel vazia
        label_file = QLabel()
        label_file.setStyleSheet("color: white; font-size: 15px;")

        label_escorregamento = QLabel("NºEscorregamento")
        label_escorregamento.setStyleSheet(
            "color: white; font-size: 15px;font-weight:bold; margin-left:0px; margin-top:20px;")

        self.input_pino = QLineEdit()
        self.input_pino.setStyleSheet(
            "background-color: black; border:2px solid grey;color: white; margin-left:5px; margin-top:5px;")
        self.input_pino.setAlignment(Qt.AlignmentFlag.AlignCenter)  # Centraliza o texto
        self.input_pino.setFont(QFont("Arial", 14))  # Define o tamanho da fonte
        self.input_pino.setFixedHeight(50)  # Define a altura desejada
        self.input_pino.setFixedWidth(100)  # Define a altura desejada
        self.input_pino.setVisible(True)
        self.input_pino.setEnabled(False)

        input_valorEscorregamento = QLineEdit()
        input_valorEscorregamento.setStyleSheet(
            "background-color: black; border:2px solid grey;color: white; margin-left:0px; margin-top:5px;")
        input_valorEscorregamento.setAlignment(Qt.AlignmentFlag.AlignCenter)  # Centraliza o texto
        input_valorEscorregamento.setFont(QFont("Arial", 14))  # Define o tamanho da fonte
        input_valorEscorregamento.setFixedHeight(50)  # Define a altura desejada
        input_valorEscorregamento.setFixedWidth(190)  # Define a altura desejada
        input_valorEscorregamento.setVisible(True)
        input_valorEscorregamento.setEnabled(False)

        model_widget = QWidget()
        model_widget.setStyleSheet("background-color:#151515;")
        model_widget.setFixedWidth(500)
        model_widget.setFixedHeight(500)

        dial = QDial()
        dial.setRange(0, 1000)
        dial.setValue(0)
        dial.setWrapping(False)
        dial.setNotchesVisible(True)
        dial.setFixedSize(150, 150)
        dial.setNotchTarget(5)

        dial2 = QDial()
        dial2.setRange(0, 1000)
        dial2.setValue(0)
        dial2.setWrapping(False)
        dial2.setNotchesVisible(True)
        dial2.setFixedSize(150, 150)
        dial2.setNotchTarget(5)

        self.label2 = QLabel("0")
        self.label2.setStyleSheet(
            "color: white; font-size: 13px;border-radius:None; background-color:black; font-weight:bold;")
        # Connect the dial's valueChanged signal to update the label
        dial.valueChanged.connect(lambda value: self.label2.setText(f"{value}"))

        self.label3 = QLabel("0")
        self.label3.setStyleSheet(
            "color: white; font-size: 13px;border-radius:None; background-color: black; font-weight:bold;")
        # Connect the dial's valueChanged signal to update the label
        dial2.valueChanged.connect(lambda value: self.label3.setText(f"{value}"))

        CoordenadasDoMolde_label = QLabel("Coordenadas Molde - Valor a atingir")
        CoordenadasDoMolde_label.setStyleSheet("border:None; color: white; font-size:13px; font-weight:bold;")
        CoordenadasDoMolde_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        CoordenadasDoMolde_labelX = QLabel("X")
        CoordenadasDoMolde_labelX.setStyleSheet("border:None; color: white; font-size:12px; font-weight:bold;")
        CoordenadasDoMolde_labelX.setAlignment(Qt.AlignmentFlag.AlignCenter)

        CoordenadasDoMolde_labelY = QLabel("Y")
        CoordenadasDoMolde_labelY.setStyleSheet("border:None; color: white; font-size:12px; font-weight:bold;")
        CoordenadasDoMolde_labelY.setAlignment(Qt.AlignmentFlag.AlignCenter)

        CoordenadasDoMolde_labelZ = QLabel("Z")
        CoordenadasDoMolde_labelZ.setStyleSheet("border:None; color: white; font-size:12px; font-weight:bold;")
        CoordenadasDoMolde_labelZ.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.CoordenadasDoMolde_labelXX = QLabel("0")
        self.CoordenadasDoMolde_labelXX.setStyleSheet("border:None; color: white; font-size:12px;")
        self.CoordenadasDoMolde_labelXX.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.CoordenadasDoMolde_labelYY = QLabel("0")
        self.CoordenadasDoMolde_labelYY.setStyleSheet("border:None; color: white; font-size:12px;")
        self.CoordenadasDoMolde_labelYY.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.CoordenadasDoMolde_labelZZ = QLabel("0.000")
        self.CoordenadasDoMolde_labelZZ.setStyleSheet("border:None; color: white; font-size:12px;")
        self.CoordenadasDoMolde_labelZZ.setAlignment(Qt.AlignmentFlag.AlignCenter)

        CoordenadasReais_label = QLabel("Coordenadas reais - Sistema Visão")
        CoordenadasReais_label.setStyleSheet("border:None; color: white; font-size:13px; font-weight:bold;")
        CoordenadasReais_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        CoordenadasReais_labelX = QLabel("X")
        CoordenadasReais_labelX.setStyleSheet("border:None; color: white; font-size:12px; font-weight:bold;")
        CoordenadasReais_labelX.setAlignment(Qt.AlignmentFlag.AlignCenter)

        CoordenadasReais_labelY = QLabel("Y")
        CoordenadasReais_labelY.setStyleSheet("border:None; color: white; font-size:12px; font-weight:bold;")
        CoordenadasReais_labelY.setAlignment(Qt.AlignmentFlag.AlignCenter)

        CoordenadasReais_labelZ = QLabel("Z")
        CoordenadasReais_labelZ.setStyleSheet("border:None; color: white; font-size:12px; font-weight:bold;")
        CoordenadasReais_labelZ.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.CoordenadasReais_labelXX = QLabel("0")
        self.CoordenadasReais_labelXX.setStyleSheet("border:None; color: white; font-size:12px;")
        self.CoordenadasReais_labelXX.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.CoordenadasReais_labelYY = QLabel("0")
        self.CoordenadasReais_labelYY.setStyleSheet("border:None; color: white; font-size:12px;")
        self.CoordenadasReais_labelYY.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.CoordenadasReais_labelZZ = QLabel("0.000")
        self.CoordenadasReais_labelZZ.setStyleSheet("border:None; color: white; font-size:12px;")
        self.CoordenadasReais_labelZZ.setAlignment(Qt.AlignmentFlag.AlignCenter)

        CoordenadasOpti_label = QLabel("Coordenadas OptiCNC")
        CoordenadasOpti_label.setStyleSheet("border:None; color: white; font-size:13px; font-weight:bold;")
        CoordenadasOpti_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        CoordenadasOpti_labelX = QLabel("X")
        CoordenadasOpti_labelX.setStyleSheet("border:None; color: white; font-size:12px; font-weight:bold;")
        CoordenadasOpti_labelX.setAlignment(Qt.AlignmentFlag.AlignCenter)

        CoordenadasOpti_labelY = QLabel("Y")
        CoordenadasOpti_labelY.setStyleSheet("border:None; color: white; font-size:12px; font-weight:bold;")
        CoordenadasOpti_labelY.setAlignment(Qt.AlignmentFlag.AlignCenter)

        CoordenadasOpti_labelZ = QLabel("Z")
        CoordenadasOpti_labelZ.setStyleSheet("border:None; color: white; font-size:12px; font-weight:bold;")
        CoordenadasOpti_labelZ.setAlignment(Qt.AlignmentFlag.AlignCenter)

        CoordenadasOpti_labelB = QLabel("B")
        CoordenadasOpti_labelB.setStyleSheet("border:None; color: white; font-size:12px; font-weight:bold;")
        CoordenadasOpti_labelB.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.CoordenadasOpti_labelXX = QLabel("0")
        self.CoordenadasOpti_labelXX.setStyleSheet("border:None; color: white; font-size:12px;")
        self.CoordenadasOpti_labelXX.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.CoordenadasOpti_labelYY = QLabel("0")
        self.CoordenadasOpti_labelYY.setStyleSheet("border:None; color: white; font-size:12px;")
        self.CoordenadasOpti_labelYY.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.CoordenadasOpti_labelZZ = QLabel("0")
        self.CoordenadasOpti_labelZZ.setStyleSheet("border:None; color: white; font-size:12px;")
        self.CoordenadasOpti_labelZZ.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.CoordenadasOpti_labelBB = QLabel("0.000")
        self.CoordenadasOpti_labelBB.setStyleSheet("border:None; color: white; font-size:12px;")
        self.CoordenadasOpti_labelBB.setAlignment(Qt.AlignmentFlag.AlignCenter)

        fig = Figure(figsize=(5, 5))
        fig.set_facecolor('#151515')
        canvas = FigureCanvasQTAgg(fig)

        ax = fig.add_subplot(111, projection='3d')

        self.filePath = None

        def update_model_widget():
            diretorio_atual = os.getcwd()
            root = Tk()
            root.withdraw()
            os.chdir(
                r'C:\Users\Daniel\documents')
            file_path = askopenfilename(filetypes=[("STL files", "*.stl")])
            os.chdir(diretorio_atual)

            if file_path:
                self.modelo_path = file_path
                self.filePath = file_path
                Name_File = file_path.rsplit("/", 1)
                Name_File = Name_File[-1]
                # Criar a QLabel para exibir o Name_File
                label_file.setText(Name_File)

                x_max, y_max, z_max, dim, pin_spacing, angle, filencp = configDefualt.ValoresConfig()
                linesAT, modelo_x, modelo_y, modelo_z, x_max, y_max, df = PointsManager.principal(x_max, y_max, dim,
                                                                                                  pin_spacing, angle,
                                                                                                  self.modelo_path,
                                                                                                  z_max)

                # Limpar os eixos do gráfico
                ax.cla()

                PointsManager.plotarCoordenadasPinos(modelo_x, modelo_y, modelo_z, df, x_max, y_max, ax)
                # Redesenhar o gráfico
                canvas.draw()

                # Adicione o canvas à área de exibição do modelo
                layout = QVBoxLayout()
                layout.addWidget(canvas)
                model_widget.setLayout(layout)

        self.button.clicked.connect(update_model_widget)

        def show_popup(message):
            msg_box = QMessageBox()
            msg_box.setWindowTitle("Parametros em Falta")
            msg_box.setText(message)
            msg_box.setIcon(QMessageBox.Icon.Information)

            # Set custom style sheet for the message box
            msg_box.setStyleSheet("""
                QMessageBox {
                    background-color:#1C1C1C;
                    color: white;
                    font-size: 16px;
                }
                QLabel {
                    color: white;
                    font-size: 15px;
                    font-weight: bold;
                }
                QPushButton {
                    background-color: grey;
                    color: #d22e2e;
                    border-radius: 5px;
                    padding: 10px;
                    font-size: 16px;
                    font-weight:bold;
                }
                QPushButton:hover {
                    background-color: black;
                }
                QPushButton:pressed {
                    background-color: #b33636;
                    color: black;
                }
            """)

            msg_box.exec()

        self.button.setEnabled(False)

        self.ButtonPino.setEnabled(False)
        self.reset.setEnabled(False)

        def PowerButton():
            self.configX, self.configY, self.configZ, self.configDim, self.configEsp, self.configAngle, self.configFile = configDefualt.VerificarConfig()
            if self.configX == 0 and self.configY == 0 and self.configZ == 0 and self.configDim == 0 and self.configEsp == 0 and self.configAngle == 0 and self.configFile == 0:
                if self.i == 0:
                    self.buttonPower.setIcon(QIcon("power-button.png"))
                    self.i = 1
                    self.toggle2.setEnabled(True)
                    self.input_pino.setEnabled(True)
                    self.ButtonPino.setEnabled(True)
                    self.button.setEnabled(True)
                    self.reset.setEnabled(True)

                else:
                    self.buttonPower.setIcon(QIcon("powerOff-button.png"))
                    self.i = 0
                    self.j = 1
                    AutoButton()
                    self.input_pino.setText("0")
                    self.input_pino.setEnabled(False)
                    self.toggle2.setEnabled(False)
                    self.ButtonPino.setEnabled(False)
                    self.button.setEnabled(False)
                    self.reset.setEnabled(False)
            else:
                # Exemplo de uso
                if self.configX == 1:
                    show_popup("Insira o valor máximo de X -> Configurações")

                if self.configY == 1:
                    show_popup("Insira o valor máximo de Y -> Configurações")

                if self.configZ == 1:
                    show_popup("Insira o valor máximo de Z -> Configurações")

                if self.configDim == 1:
                    show_popup("Insira o diâmetro do pino -> Configurações")

                if self.configEsp == 1:
                    show_popup("Insira o espaçamento entre pinos -> Configurações")

                if self.configAngle == 1:
                    show_popup("Insira o ângulo -> Configurações")

                if self.configFile == 1:
                    show_popup("Insira o arquivo NCP -> Configurações")

        self.input_pino.setText("0")
        self.buttonPower.clicked.connect(PowerButton)

        def AutoButton():
            if self.j == 0:
                self.toggle2.setIcon(QIcon("auto_on.png"))
                start_input_thread_auto()
                self.j = 1
            else:
                self.toggle2.setIcon(QIcon("auto_off.png"))
                self.j = 0


        self.l = 0
        def ResetButton():
            if self.l == 0:
                msg_box = QMessageBox()
                msg_box.setIcon(QMessageBox.Icon.Question)
                msg_box.setText("Deseja fazer o reset ?         ")
                msg_box.setWindowTitle("Pergunta")
                msg_box.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
                msg_box.setDefaultButton(QMessageBox.StandardButton.No)
                msg_box.setStyleSheet("""
                                    QMessageBox {
                                        background-color:#1C1C1C;
                                        color: white;
                                        font-size: 16px;
                                    }
                                    QLabel {
                                        color: white;
                                        font-size: 15px;
                                        font-weight: bold;
                                    }
                                    QPushButton {
                                        background-color: grey;
                                        color: #d22e2e;
                                        border-radius: 5px;
                                        padding: 10px;
                                        font-size: 16px;
                                        font-weight:bold;
                                    }
                                    QPushButton:hover {
                                        background-color: black;
                                    }
                                    QPushButton:pressed {
                                        background-color: #b33636;
                                        color: black;
                                    }
                                """)

                # Exibir o pop-up e obter o resultado
                result = msg_box.exec()

                if result == QMessageBox.StandardButton.Yes:
                    self.reset.setIcon(QIcon("reset_on.png"))
                    start_input_thread_autoReset()
                    self.l= 1
                else:
                    self.reset.setIcon(QIcon("reset.png"))
                    self.l=0
            else:
                self.reset.setIcon(QIcon("reset.png"))
                self.l = 0

        self.reset.clicked.connect(ResetButton)

        self.toggle2.setEnabled(False)  # Desabilita o botão AutoButton inicialmente
        self.toggle2.clicked.connect(AutoButton)

        def RepairButton():
            if self.k == 0:
                buttonRepair.setIcon(QIcon("repair_on.png"))
                self.k = 1
            else:
                buttonRepair.setIcon(QIcon("repair_off.png"))
                self.k = 0

        input_valorEscorregamento.setText("0")
        buttonRepair.setEnabled(False)
        buttonRepair.clicked.connect(RepairButton)

        def add_dial_labels(dial):
            # Remove rótulos existentes
            for child in dial.children():
                if isinstance(child, QLabel):
                    child.deleteLater()

            # Lista com os quatro valores a serem exibidos nos rótulos
            label_values = [dial.minimum(), dial.maximum()]

            # Adiciona os rótulos numéricos
            for value in label_values:
                # Cria o rótulo com o número
                label = QLabel(str(value), dial)
                # label.setAlignment(Qt.AlignCenter)
                label.setStyleSheet("color: white; font-size: 13px;font-weight:bold;")

            # Define a posição dos rótulos
            dial_width = dial.width()
            dial_height = dial.height()
            label_positions = [(dial_width * 0.19, dial_height * 0.91),  # Posição superior
                               (dial_width * 0.74, dial_height * 0.91)]

            for label, position in zip(dial.children(), label_positions):
                label.move(int(position[0]), int(position[1]))

        add_dial_labels(dial)
        add_dial_labels(dial2)

        self.NPino = 0

        def buttonPino():
            self.NPino = int(self.input_pino.text())
            start_input_thread_manual()

        self.ButtonPino.clicked.connect(buttonPino)

        # ---------------------------------Posicionamento dos layouts-------------------------------------------#
        # Define os widgets
        self.text_Manual = QLabel("Manual")
        self.text_Manual.setStyleSheet("color: white; font-size: 15px; margin-left: 0px; font-weight:bold; margin-top:20px;")

        # Define os layouts
        checkbox_layout2 = QHBoxLayout()
        checkbox_layout2.addWidget(self.buttonPower)
        checkbox_layout2.addWidget(self.toggle2)
        checkbox_layout2.addWidget(buttonRepair)

        # Define o layout horizontal para as labels
        labels_layout = QHBoxLayout()
        labels_layout.addWidget(self.text_Manual)
        labels_layout.addWidget(label_escorregamento)

        # Define o layout horizontal para os inputs

        formBP = QHBoxLayout()
        formBP.addWidget(self.input_pino)
        formBP.addSpacing(0)
        formBP.addWidget(self.ButtonPino)
        formBP.addSpacing(20)

        inputs_layout = QHBoxLayout()
        inputs_layout.addLayout(formBP)
        inputs_layout.addWidget(input_valorEscorregamento)

        # Define o layout vertical
        vertical_layout = QVBoxLayout()
        vertical_layout.addLayout(checkbox_layout2)
        vertical_layout.addLayout(labels_layout)
        vertical_layout.addLayout(inputs_layout)
        checkbox_layout2.setContentsMargins(10, 0, 0, 10)

        # Define o layout da janela principal
        form_layout = QFormLayout()
        form_layout.addRow(vertical_layout)

        BackgroundXYZ_layout = QFrame()
        BackgroundXYZ_layout.setStyleSheet(
            "background-color: #1C1C1C; margin-left:10px; margin-top:20px; border:3px solid grey")
        BackgroundXYZ_layout.setFixedSize(380, 430)

        form_layout_labels_CoordenadasMoldeXYZXYZ = QHBoxLayout()
        form_layout_labels_CoordenadasMoldeXYZXYZ.addSpacing(30)
        form_layout_labels_CoordenadasMoldeXYZXYZ.addWidget(self.CoordenadasDoMolde_labelXX)
        form_layout_labels_CoordenadasMoldeXYZXYZ.addSpacing(80)
        form_layout_labels_CoordenadasMoldeXYZXYZ.addWidget(self.CoordenadasDoMolde_labelYY)
        form_layout_labels_CoordenadasMoldeXYZXYZ.addSpacing(75)
        form_layout_labels_CoordenadasMoldeXYZXYZ.addWidget(self.CoordenadasDoMolde_labelZZ)
        form_layout_labels_CoordenadasMoldeXYZXYZ.setAlignment(Qt.AlignmentFlag.AlignCenter)

        form_layout_labels_CoordenadasMoldeXYZ = QHBoxLayout()
        form_layout_labels_CoordenadasMoldeXYZ.addWidget(CoordenadasDoMolde_labelX)
        form_layout_labels_CoordenadasMoldeXYZ.addSpacing(80)
        form_layout_labels_CoordenadasMoldeXYZ.addWidget(CoordenadasDoMolde_labelY)
        form_layout_labels_CoordenadasMoldeXYZ.addSpacing(80)
        form_layout_labels_CoordenadasMoldeXYZ.addWidget(CoordenadasDoMolde_labelZ)
        form_layout_labels_CoordenadasMoldeXYZ.setAlignment(Qt.AlignmentFlag.AlignCenter)

        form_layout_labels_CoordenadasReaisXYZXYZ = QHBoxLayout()
        form_layout_labels_CoordenadasReaisXYZXYZ.addSpacing(25)
        form_layout_labels_CoordenadasReaisXYZXYZ.addWidget(self.CoordenadasReais_labelXX)
        form_layout_labels_CoordenadasReaisXYZXYZ.addSpacing(85)
        form_layout_labels_CoordenadasReaisXYZXYZ.addWidget(self.CoordenadasReais_labelYY)
        form_layout_labels_CoordenadasReaisXYZXYZ.addSpacing(75)
        form_layout_labels_CoordenadasReaisXYZXYZ.addWidget(self.CoordenadasReais_labelZZ)
        form_layout_labels_CoordenadasReaisXYZXYZ.setAlignment(Qt.AlignmentFlag.AlignCenter)

        form_layout_labels_CoordenadasReaisXYZ = QHBoxLayout()
        form_layout_labels_CoordenadasReaisXYZ.addWidget(CoordenadasReais_labelX)
        form_layout_labels_CoordenadasReaisXYZ.addSpacing(80)
        form_layout_labels_CoordenadasReaisXYZ.addWidget(CoordenadasReais_labelY)
        form_layout_labels_CoordenadasReaisXYZ.addSpacing(80)
        form_layout_labels_CoordenadasReaisXYZ.addWidget(CoordenadasReais_labelZ)
        form_layout_labels_CoordenadasReaisXYZ.setAlignment(Qt.AlignmentFlag.AlignCenter)

        form_layout_labels_CoordenadasOptiXYZXYZ = QHBoxLayout()
        form_layout_labels_CoordenadasOptiXYZXYZ.addSpacing(0)
        form_layout_labels_CoordenadasOptiXYZXYZ.addWidget(self.CoordenadasOpti_labelXX)
        form_layout_labels_CoordenadasOptiXYZXYZ.addWidget(self.CoordenadasOpti_labelYY)
        form_layout_labels_CoordenadasOptiXYZXYZ.addWidget(self.CoordenadasOpti_labelZZ)
        form_layout_labels_CoordenadasOptiXYZXYZ.addWidget(self.CoordenadasOpti_labelBB)

        form_layout_labels_CoordenadasOptiXYZ = QHBoxLayout()
        form_layout_labels_CoordenadasOptiXYZ.addWidget(CoordenadasOpti_labelX)
        form_layout_labels_CoordenadasOptiXYZ.addSpacing(60)
        form_layout_labels_CoordenadasOptiXYZ.addWidget(CoordenadasOpti_labelY)
        form_layout_labels_CoordenadasOptiXYZ.addSpacing(60)
        form_layout_labels_CoordenadasOptiXYZ.addWidget(CoordenadasOpti_labelZ)
        form_layout_labels_CoordenadasOptiXYZ.addSpacing(60)
        form_layout_labels_CoordenadasOptiXYZ.addWidget(CoordenadasOpti_labelB)
        form_layout_labels_CoordenadasOptiXYZ.setAlignment(Qt.AlignmentFlag.AlignCenter)

        LayoutXYZ_Background = QVBoxLayout(BackgroundXYZ_layout)
        LayoutXYZ_Background.setAlignment(Qt.AlignmentFlag.AlignTop)
        LayoutXYZ_Background.addWidget(CoordenadasDoMolde_label)
        LayoutXYZ_Background.addLayout(form_layout_labels_CoordenadasMoldeXYZ)
        LayoutXYZ_Background.addLayout(form_layout_labels_CoordenadasMoldeXYZXYZ)
        LayoutXYZ_Background.addSpacing(20)
        LayoutXYZ_Background.addWidget(CoordenadasReais_label)
        LayoutXYZ_Background.addLayout(form_layout_labels_CoordenadasReaisXYZ)
        LayoutXYZ_Background.addLayout(form_layout_labels_CoordenadasReaisXYZXYZ)
        LayoutXYZ_Background.addSpacing(20)
        LayoutXYZ_Background.addWidget(CoordenadasOpti_label)
        LayoutXYZ_Background.addLayout(form_layout_labels_CoordenadasOptiXYZ)
        LayoutXYZ_Background.addLayout(form_layout_labels_CoordenadasOptiXYZXYZ)

        form_layout.addRow(BackgroundXYZ_layout)

        self.text_box = QLineEdit()
        self.text_box.setStyleSheet(
            "background-color:#1C1C1C; color: white; font-size:15px; border:2px solid grey; border-radius: 5px;")
        self.text_box.setFixedHeight(60)
        self.text_box.setFixedWidth(450)
        self.text_box.setReadOnly(True)
        self.text_box.setContentsMargins(0, 0, 0, 0)

        self.text_box2 = QLineEdit()
        self.text_box2.setStyleSheet(
            "background-color:#1C1C1C; color: white; font-size:15px; border:2px solid grey;border-radius: 5px;")
        self.text_box2.setFixedHeight(40)
        self.text_box2.setFixedWidth(450)
        self.text_box2.setReadOnly(True)
        self.text_box2.setContentsMargins(0, 0, 0, 0)

        container_layout = QVBoxLayout()
        container_layout.addWidget(self.text_box)

        container_layout2 = QVBoxLayout()
        container_layout2.addWidget(self.text_box2)

        text_CA = QLabel("Código Atual")
        text_CA.setStyleSheet("color: white; font-size: 15px;font-weight:bold;")
        text_A = QLabel("Acontecimento")
        text_A.setStyleSheet("color: white; font-size: 15px;font-weight:bold;")

        model_widget_layout = QVBoxLayout()
        model_widget_layout.addWidget(model_widget)
        model_widget_layout.addWidget(text_CA)
        model_widget_layout.addWidget(self.text_box)
        model_widget_layout.addWidget(text_A)
        model_widget_layout.addWidget(self.text_box2)
        model_widget_layout.addSpacing(10)
        model_widget_layout.setContentsMargins(50, 0, 0, 0)

        # Criar a caixa
        box = QGroupBox()
        box_layout = QVBoxLayout()
        label2_layout = QVBoxLayout()
        label2_layout.addWidget(self.label2)
        box_layout.addLayout(label2_layout)
        box.setLayout(box_layout)
        box.setStyleSheet("QGroupBox { border: 2px solid grey;"
                          "margin-top: 10px; "
                          "padding: 5px; "
                          "margin-left:100px;"
                          "margin-right:180px;"
                          "border-radius: 10px;"
                          "background-color:black;}")

        # Criar a caixa
        box2 = QGroupBox()
        box_layout2 = QVBoxLayout()
        label3_layout = QVBoxLayout()
        label3_layout.addWidget(self.label3)
        box_layout2.addLayout(label3_layout)
        box2.setLayout(box_layout2)
        box2.setStyleSheet("QGroupBox { border: 2px solid grey; "
                           "margin-top: 10px; "
                           "padding: 5px; "
                           "margin-left:100px;"
                           "margin-right:180px;"
                           "border-radius: 10px;"
                           "background-color:black;}")

        dial1_layout = QVBoxLayout()  # Layout principal
        dial1_layout.addWidget(dial)
        dial1_layout.setContentsMargins(60, 0, 0, 0)

        dial2_layout = QVBoxLayout()  # Layout principal
        dial2_layout.addWidget(dial2)
        dial2_layout.setContentsMargins(60, 0, 0, 0)

        P = QLabel("P (mm/min)")
        P.setStyleSheet("color: white; font-size: 13px; margin-left: 60px;font-weight:bold;")
        P.setContentsMargins(95, 0, 0, 0)
        F = QLabel("F (mm/min)")
        F.setStyleSheet("color: white; font-size: 13px; margin-left: 60px;font-weight:bold;")
        F.setContentsMargins(95, 0, 0, 0)

        button_layout = QVBoxLayout()  # Layout principal
        button_layout.addWidget(self.button)
        button_layout.addWidget(label_file)
        button_layout.addSpacing(30)
        button_layout.addWidget(P)
        button_layout.addLayout(dial1_layout)
        button_layout.addWidget(box)
        button_layout.addSpacing(20)
        button_layout.addWidget(F)
        button_layout.addLayout(dial2_layout)
        button_layout.addWidget(box2)
        button_layout.setContentsMargins(20, 10, 10, 0)  # Define as margens do layout

        main_layout = QHBoxLayout()
        main_layout.addLayout(button_layout)
        main_layout.addLayout(form_layout)

        layout.addLayout(main_layout, 0, 0, alignment=Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
        layout.addLayout(model_widget_layout, 0, 1, alignment=Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
        layout.addWidget(self.reset , 0 , 1 ,alignment=Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignRight )

        return generalTab

    # ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
    def ConfigurationsTabUI(self):
        """Create the Network page UI."""
        networkTab = QWidget()
        layout = QVBoxLayout()
        networkTab.setLayout(layout)
        # Define the login button click handler
        is_logged_in = False  # Variável para controlar se o usuário está logado ou não
        login_layout_added = False

        # Create a container widget to hold the login form components
        login_container = QWidget()
        login_container.setStyleSheet("background-color: #1C1C1C; padding: 20px; border-radius: 10px; ")
        login_container.setFixedWidth(400)
        login_container.setFixedHeight(500)

        username_label = QLabel("Username:")
        username_label.setStyleSheet("QLabel { color: white; font-size: 20px; font-weight:bold;}")

        username_input = QLineEdit()
        username_input.setStyleSheet(
            "QLineEdit { background-color:#d22e2e; color: white; margin-left:20px; margin-bottom:30px;  }")
        username_input.setFixedWidth(400)

        password_label = QLabel("Password:")
        password_label.setStyleSheet("QLabel { color: white; font-size: 20px; font-weight:bold;}")

        password_input = QLineEdit()
        password_input.setEchoMode(QLineEdit.EchoMode.Password)
        password_input.setStyleSheet("QLineEdit { background-color:#d22e2e; color: white; margin-left:20px; }")
        password_input.setFixedWidth(400)

        login_button = QPushButton("Entrar")
        login_button.setStyleSheet(
            "QPushButton { background-color: grey; color: #d22e2e; border-radius: 5px; padding: 10px; font-size: 20px; margin-top:40px; font-weight: bold;}"
            "QPushButton:hover { background-color: black; }"
            "QPushButton:pressed { background-color: #b33636; color: black; }")
        login_button.setFixedWidth(100)

        # Create a grid layout for the login form components
        login_layout = QGridLayout()
        login_layout.addWidget(username_label, 0, 0, 1, 2)
        login_layout.addWidget(username_input, 1, 0, 1, 2)
        login_layout.addWidget(password_label, 2, 0, 1, 2)
        login_layout.addWidget(password_input, 3, 0, 1, 2)
        login_layout.addWidget(login_button, 4, 1, 1, 1,
                               alignment=Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignBottom)

        # Set the login form layout for the login container widget
        login_container.setLayout(login_layout)

        # Add the login container widget to the main layout
        layout.addWidget(login_container, alignment=Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignCenter)

        def login():

            username = username_input.text()
            password = password_input.text()
            if username == "admin" and password == "admin":

                username_input.clear()
                password_input.clear()
                # Remove the login container widget from the main layout
                layout.removeWidget(login_container)

                # TODO: Replace with the logic for handling successful login
                print("Login successful")
                with open('config.ini', "r") as file:
                    text_content = file.read()

                X_MAX, Y_MAX, Z_MAX, DIM, PIN_SPACING, ANGLE, FILENCP = configDefualt.ValoresConfig()
                self.filencp = FILENCP
                # Create a container widget for the text box
                text_container = QFrame()
                text_container.setStyleSheet(
                    "background-color: #1C1C1C; border-radius: 10px; border: 5px solid #DCDCDC")
                text_container.setFixedSize(600, 600)

                # Create the text box
                text_box = QTextEdit()
                text_box.setStyleSheet(
                    "background-color: #1C1C1C; color: white; font-size:20px;border:None;")
                text_box.setPlainText(text_content)
                text_box.setReadOnly(True)

                # Create a layout for the text container
                container_layout = QVBoxLayout(text_container)
                container_layout.addWidget(text_box)

                # Linha 1
                line_layout1 = QHBoxLayout()
                label_MaximoX = QLabel("Maximo Valor de X")
                label_MaximoX.setStyleSheet("color:white; font-weight:bold; font-size:18px;border: None")
                input_MaximoX = QLineEdit()
                input_MaximoX.setStyleSheet("background: black; border:2px solid grey;color:white;font-size:18px;")
                input_MaximoX.setText(str(X_MAX))

                input_MaximoX.setFixedSize(150, 50)
                input_MaximoX.setAlignment(Qt.AlignmentFlag.AlignCenter)
                line_layout1.addWidget(label_MaximoX)
                line_layout1.addWidget(input_MaximoX)

                # Linha 2
                line_layout2 = QHBoxLayout()
                label_MaximoY = QLabel("Maximo Valor de Y")
                label_MaximoY.setStyleSheet("color:white; font-weight:bold; font-size:18px;border: None")
                input_MaximoY = QLineEdit()
                input_MaximoY.setStyleSheet("background: black; border:2px solid grey;color:white;font-size:18px;")
                input_MaximoY.setText(str(Y_MAX))
                input_MaximoY.setAlignment(Qt.AlignmentFlag.AlignCenter)
                input_MaximoY.setFixedSize(150, 50)
                line_layout2.addWidget(label_MaximoY)
                line_layout2.addWidget(input_MaximoY)

                # Linha 3
                line_layout3 = QHBoxLayout()
                label_MaximoZ = QLabel("Maximo Valor de Z")
                label_MaximoZ.setStyleSheet("color:white; font-weight:bold; font-size:18px;border: None")
                input_MaximoZ = QLineEdit()
                input_MaximoZ.setStyleSheet("background: black; border:2px solid grey;color:white;font-size:18px;")
                input_MaximoZ.setAlignment(Qt.AlignmentFlag.AlignCenter)
                input_MaximoZ.setText(str(Z_MAX))
                input_MaximoZ.setFixedSize(150, 50)
                line_layout3.addWidget(label_MaximoZ)
                line_layout3.addWidget(input_MaximoZ)

                # Linha 4
                line_layout4 = QHBoxLayout()
                label_MaximoDim = QLabel("Diametro do Pino")
                label_MaximoDim.setStyleSheet("color:white; font-weight:bold; font-size:18px;border: None;")
                input_MaximoDim = QLineEdit()
                input_MaximoDim.setStyleSheet("background: black; border:2px solid grey;color:white;font-size:18px;")
                input_MaximoDim.setAlignment(Qt.AlignmentFlag.AlignCenter)
                input_MaximoDim.setText(str(DIM))
                input_MaximoDim.setFixedSize(150, 50)
                line_layout4.addWidget(label_MaximoDim)
                line_layout4.addWidget(input_MaximoDim)

                # Linha 5
                line_layout5 = QHBoxLayout()
                label_MaximoEspPino = QLabel("Espaçamento entre os Pinos")
                label_MaximoEspPino.setStyleSheet("color:white; font-weight:bold; font-size:18px;border: None")
                input_MaximoEspPino = QLineEdit()
                input_MaximoEspPino.setStyleSheet(
                    "background: black; border:2px solid grey;color:white;font-size:18px;")
                input_MaximoEspPino.setAlignment(Qt.AlignmentFlag.AlignCenter)
                input_MaximoEspPino.setText(str(PIN_SPACING))
                input_MaximoEspPino.setFixedSize(150, 50)
                line_layout5.addWidget(label_MaximoEspPino)
                line_layout5.addWidget(input_MaximoEspPino)

                # Linha 6
                line_layout6 = QHBoxLayout()
                label_MaximoAng = QLabel("Angulo dos Pinos")
                label_MaximoAng.setStyleSheet("color:white; font-weight:bold; font-size:18px;border: None")
                input_MaximoAng = QLineEdit()
                input_MaximoAng.setStyleSheet("background: black; border:2px solid grey;color:white;font-size:18px;")
                input_MaximoAng.setText(str(ANGLE))
                input_MaximoAng.setAlignment(Qt.AlignmentFlag.AlignCenter)
                input_MaximoAng.setFixedSize(150, 50)
                line_layout6.addWidget(label_MaximoAng)
                line_layout6.addWidget(input_MaximoAng)

                # Linha 6
                line_layout7 = QHBoxLayout()
                label_FileNCP = QLabel("Ficheiro NCP")
                label_FileNCP.setStyleSheet("color:white; font-weight:bold; font-size:18px;border: None")
                button_FileNCP = QPushButton("Selecionar Ficheiro NCP")
                button_FileNCP.setStyleSheet("QPushButton { background-color: black;"
                                             "color: grey;"
                                             "border-radius: 5px;"
                                             "border:2px solid grey;"
                                             "padding: 10px;"
                                             "font-size: 15px;"
                                             "font-weight: bold;}"
                                             "QPushButton:hover { background-color: grey; color:black; border: 2px solid black; }")

                button_FileNCP.setFixedWidth(300)
                button_FileNCP.setFixedHeight(50)
                line_layout7.addWidget(label_FileNCP)
                line_layout7.addWidget(button_FileNCP)

                Form_layout_Buttons = QFormLayout()
                line_layout8 = QHBoxLayout()
                button1 = QPushButton("Salvar")
                button1.setStyleSheet(
                    "QPushButton { background-color: black; color: white ; border-radius: 5px; border: 2px solid green; "
                    "padding: 10px; font-size: 18px; font-weight: bold; margin-bottom: 50px;}"
                    "QPushButton:pressed { background-color: green; color: black; border:5px solid black}"
                )

                button2 = QPushButton("Cancelar")
                button2.setStyleSheet(
                    "QPushButton { background-color: black; color: white; border-radius: 5px; border: 2px solid red; "
                    "padding: 10px; font-size: 18px; font-weight: bold; }"
                    "QPushButton:pressed { background-color: red; color: black; border: 5px solid black; }"
                )

                Form_layout_Buttons.addRow(button1)
                Form_layout_Buttons.addRow(button2)
                line_layout8.addLayout(Form_layout_Buttons)
                line_layout8.setContentsMargins(10, 200, 10, 0)

                container_inputs = QVBoxLayout()
                # Adicionar as linhas ao layout vertical
                container_inputs.addLayout(line_layout1)
                container_inputs.addSpacing(50)
                container_inputs.addLayout(line_layout2)
                container_inputs.addSpacing(50)
                container_inputs.addLayout(line_layout3)
                container_inputs.addSpacing(50)
                container_inputs.addLayout(line_layout4)
                container_inputs.addSpacing(50)
                container_inputs.addLayout(line_layout5)
                container_inputs.addSpacing(50)
                container_inputs.addLayout(line_layout6)
                container_inputs.addSpacing(50)
                container_inputs.addLayout(line_layout7)

                container_inputs.setContentsMargins(50, 10, 50, 20)

                frame = QFrame()
                frame.setLayout(container_inputs)
                frame.setStyleSheet("border: 5px solid #DCDCDC; margin-top:0px;")
                frame.setFixedHeight(600)

                self.username_input = username_input
                self.password_input = password_input

                # Create a layout for the main container
                main_layout = QHBoxLayout()
                main_layout.addWidget(frame)
                main_layout.addLayout(line_layout8)
                main_layout.addWidget(text_container)
                main_layout.setAlignment(text_container, Qt.AlignmentFlag.AlignRight)
                main_layout.setAlignment(frame, Qt.AlignmentFlag.AlignTop)

                # Create a container widget for the main layout
                main_container = QWidget()
                main_container.setLayout(main_layout)

                # Add the main container widget to the main layout
                layout.addWidget(main_container)

                def FileNCP_Button():
                    root = Tk()
                    root.withdraw()
                    self.filencp = askopenfilename(filetypes=[("ncp files", "*.ncp")])

                button_FileNCP.clicked.connect(FileNCP_Button)

                def reset_page():
                    # Limpar os campos de QLineEdit
                    input_MaximoX.clear()
                    input_MaximoY.clear()
                    input_MaximoZ.clear()
                    input_MaximoDim.clear()
                    input_MaximoEspPino.clear()
                    input_MaximoAng.clear()

                    # Remover todos os widgets do layout
                    while layout.count():
                        item = layout.takeAt(0)
                        widget = item.widget()
                        if widget:
                            widget.deleteLater()

                    # Desconectar o sinal login_button.clicked da função login()
                    login_button.clicked.disconnect(login)
                    layout.addWidget(login_container,
                                     alignment=Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignCenter)
                    login_button.clicked.connect(login)

                button2.clicked.connect(reset_page)

                def save_page():
                    X_MAX = int(input_MaximoX.text())
                    Y_MAX = int(input_MaximoY.text())
                    Z_MAX = float(input_MaximoZ.text())
                    DIM = float(input_MaximoDim.text())
                    PIN_SPACING = float(input_MaximoEspPino.text())
                    ANGLE = int(input_MaximoAng.text())
                    FILENCP = self.filencp

                    with open('config.ini', "r") as file:
                        text_content = file.read()

                    text_box.setPlainText(text_content)

                    configDefualt.atualizarDados(X_MAX, Y_MAX, Z_MAX, DIM, PIN_SPACING, ANGLE, FILENCP)
                    with open("Sistema_Visao.txt", 'w') as fileSystemVision:
                        fileSystemVision.write("")

                button1.clicked.connect(save_page)

            else:
                # Show a pop-up message for incorrect username or password
                # Show a styled pop-up message for incorrect username or password
                msg_box = QMessageBox()
                msg_box.setWindowTitle("Erro de Login")
                msg_box.setText("Nome de utilizador ou senha incorretos.")
                msg_box.setIcon(QMessageBox.Icon.Warning)

                # Set custom style sheet for the message box
                msg_box.setStyleSheet("""
                            QMessageBox {
                                background-color:#1C1C1C;
                                color: white;
                                font-size: 16px;
                            }
                            QLabel {
                                color: white;
                                font-size: 15px;
                                font-weight: bold;
                            }
                            QPushButton {
                                background-color: grey;
                                color: #d22e2e;
                                border-radius: 5px;
                                padding: 10px;
                                font-size: 16px;
                                font-weight:bold;
                            }
                            QPushButton:hover {
                                background-color: black;
                            }
                            QPushButton:pressed {
                                background-color: #b33636;
                                color: black;
                            }
                        """)

                # Execute the message box and store the result
                msg_box.exec()

        login_button.clicked.connect(login)

        return networkTab

    # def update_value(self, value):
    # self.label7.setText(str(value))

    # def update_value2(self, value):
    # self.label8.setText(str(value))

    def update_labels(self, x, y, z):
        self.CoordenadasDoMolde_labelXX.setText(str(x))
        self.CoordenadasDoMolde_labelYY.setText(str(y))
        self.CoordenadasDoMolde_labelZZ.setText(str(z))

    def update_labels_CR(self, x, y, z):
        self.CoordenadasReais_labelXX.setText(str(x))
        self.CoordenadasReais_labelYY.setText(str(y))
        self.CoordenadasReais_labelZZ.setText(str(z))

    def update_labels_Opti(self, x, y, z, b):
        self.CoordenadasOpti_labelXX.setText(str(x))
        self.CoordenadasOpti_labelYY.setText(str(y))
        self.CoordenadasOpti_labelZZ.setText(str(z))
        self.CoordenadasOpti_labelBB.setText(str(b))

    def Acontecimento(self, text):
        self.text_box2.setText(text)

    def ReturnQDial(self):
        return self.label2.text()

    def ReturnQDial2(self):
        return self.label3.text()

    def filepath(self):
        return self.filePath

    def iC(self):
        return self.i

    def jC(self):
        return self.j

    def lC(self):
        return self.l

    def StopGroupReset(self):
        self.toggle2.setEnabled(False)
        self.input_pino.setEnabled(False)
        self.ButtonPino.setEnabled(False)

    def WorkGroupReset(self):
        self.toggle2.setEnabled(True)
        self.input_pino.setEnabled(True)
        self.ButtonPino.setEnabled(True)

    def modify_powerButton(self):
        self.buttonPower.setIcon(QIcon("powerOff-button.png"))
        self.i = 0

    def modify_autoButton(self):
        self.toggle2.setIcon(QIcon("auto_off.png"))
        self.j = 0
        self.input_pino.setEnabled(True)

    def Notenable_autoButton(self):
        self.toggle2.setEnabled(False)

    def Enable_Button(self):
        self.button.setEnabled(True)

    def Notenable_Button(self):
        self.button.setEnabled(False)

    def Enable_autoButton(self):
        self.toggle2.setEnabled(True)

    def write_textBox(self):
        with open(r'C:\Users\lenovo\Documents\Tecmacal\OPTIMACNCGRAF7.1\AutoRunCode.ncp', 'r') as file:
            text_content = file.read()
            self.text_box.setText(text_content)

    def NPinoManual(self):
        return self.NPino

    def StopButtonPino(self):
        self.input_pino.setEnabled(False)
        self.ButtonPino.setEnabled(False)

    def WorkButtonPino(self):
        self.input_pino.setEnabled(True)
        self.ButtonPino.setEnabled(True)

    def PinoExecucaoself(self , Pino):
        self.input_pino.setText(str(Pino))
        print(Pino)

    def TextLabelManual(self):
        self.text_Manual.setText("Manual")

    def TextLabelPinoExecucao(self):
        self.text_Manual.setText("Pino Em Execução")

    def InputPinoDefault(self):
        self.input_pino.setText("0")

    def StopAuto_Buttons(self):
        self.input_pino.setEnabled(False)
        self.ButtonPino.setEnabled(False)
        self.reset.setEnabled(False)

    def WorkAuto_Buttons(self):
        self.input_pino.setEnabled(True)
        self.ButtonPino.setEnabled(True)
        self.reset.setEnabled(True)


    def StopButtonReset(self):
        self.reset.setEnabled(False)

    def WorkButtonReset(self):
        self.reset.setEnabled(True)

    def show_popup_Error(self):
        message_box = QMessageBox()
        message_box.setIcon(QMessageBox.Icon.Warning)
        message_box.setWindowTitle("Aviso")
        message_box.setText("Verifique se o ficheiro STL e as velocidades foram inseridos!")
        message_box.exec()
def input_thread_func_auto(window):

    # Pasta que contém os logs
    logs_folder = r'C:\Users\lenovo\Documents\Tecmacal\OPTIMACNCGRAF7.1\log'
    # Encontrar o arquivo de log mais recente na pasta
    log_files = glob.glob(os.path.join(logs_folder, '*.txt'))
    recent_log_file = max(log_files, key=os.path.getmtime)
    modelo_path = window.filepath()
    print(modelo_path)
    FP1 = int(window.ReturnQDial())
    FP2 = int(window.ReturnQDial2())
    # if modelo_path is not None:
    if modelo_path is not None and FP1 > 0 and FP2 > 0:
        window.StopAuto_Buttons()
        x_max, y_max, z_max, dim, pin_spacing, angle, filencp = configDefualt.ValoresConfig()
        df, modelo_x, modelo_y, modelo_z, x_max, y_max, df = PointsManager.principal(x_max, y_max, dim,
                                                                                     pin_spacing, angle,
                                                                                     modelo_path, z_max)
        window.TextLabelPinoExecucao()
        window.Notenable_Button()
        with open('Sistema_Visao.txt', 'r') as file:
            lines_CR = file.readlines()

            class LogFileEventHandler(FileSystemEventHandler):
                def __init__(self):
                    self.primeiros_elementos = None
                    self.lineDigite = ""
                    self.VetorLineDigite = []
                    self.LimparLog10Registos = 0
                    self.Coordenadasreais = lines_CR
                    self.i = 0
                    self.string_procurada = "Job finish, ready"
                    self.z_CR = 0
                    self.P = window.ReturnQDial()
                    self.F = window.ReturnQDial2()
                    self.j = 0
                    self.o = 0
                    self.g =0
                    self.resultado = None
                    Log.Escrever0(filencp, self.P)
                    self.iC = window.iC()
                    self.jC = window.jC()
                    window.Acontecimento("Regresso ao Ponto Origem.")
                    window.write_textBox()
                    window.PinoExecucaoself(0)

                def on_modified(self, event):
                    if not event.is_directory and event.src_path == recent_log_file:
                        with open(recent_log_file, 'r') as file:
                            linesOC = file.readlines()

                        if linesOC:
                            last_line = linesOC[-1].strip()
                            last_line_split = last_line.split()
                            last_line_splitFloat = last_line.split(".")

                            if last_line_split[0].isdigit() or last_line_splitFloat[0].isdigit():
                                # window.update_labels_Opti(0, 0, 0 , 0)
                                self.lineDigite = last_line.split()
                                self.resultado = self.lineDigite[:5]

                            if self.string_procurada.lower() in last_line.lower():
                                if self.iC == 1 and self.jC == 1:

                                    if self.i == 0:
                                        self.x = df.iloc[self.i]["X"]
                                        self.y = df.iloc[self.i]["Y"]
                                        self.z = round(df.iloc[self.i]["Z"], 3)
                                        window.PinoExecucaoself(self.i + 1)
                                        print("\nCoordenadas do molde:\n", self.x, self.y, self.z)
                                        self.z_CR = round(float(lines_CR[self.i].split()[1]), 3)
                                        print("Coordenadas reais:\n", self.x, self.y, self.z_CR)
                                        window.update_labels(self.x, self.y, self.z)
                                        window.update_labels_CR(self.x, self.y, self.z_CR)
                                        time.sleep(0.5)
                                        Log.EscreverZ0(filencp, self.P, self.x, self.y)
                                        window.Acontecimento("Deslocamento ás coordenadas do pino.")
                                        print("Coordenadas OptiCNC:")
                                        window.write_textBox()
                                        self.i += 1

                                    elif self.i < len(df['X']) and self.i > 0:
                                        # print(self.resultado, "\n")
                                        if self.j == 0:
                                            resultX = round(float(self.resultado[0]), 2)
                                            resultY = round(float(self.resultado[1]), 2)
                                            resultZ = round(float(self.resultado[3]), 3)
                                            resultB = round(float(self.resultado[4]), 3)
                                            window.update_labels_Opti(resultX, resultY, resultZ, resultB)
                                            time.sleep(0.5)
                                            Log.EscreverZ(filencp, self.P, self.x, self.y, self.z_CR)
                                            window.Acontecimento("Subida de Z do pino")

                                            window.write_textBox()

                                            self.j = 1
                                        elif self.j == 1:
                                            resultX = round(float(self.resultado[0]), 2)
                                            resultY = round(float(self.resultado[1]), 2)
                                            resultZ = round(float(self.resultado[3]), 3)
                                            resultB = round(float(self.resultado[4]), 3)
                                            window.update_labels_Opti(resultX, resultY, resultZ, resultB)
                                            time.sleep(0.5)
                                            Log.EscreverZB(filencp, self.F, self.x, self.y, self.z, self.z_CR)
                                            window.Acontecimento("Rotação do pino")
                                            window.write_textBox()

                                            self.j = 2

                                        elif self.j == 2:
                                            resultX = round(float(self.resultado[0]), 2)
                                            resultY = round(float(self.resultado[1]), 2)
                                            resultZ = round(float(self.resultado[3]), 3)
                                            resultB = round(float(self.resultado[4]), 3)
                                            window.update_labels_Opti(resultX, resultY, resultZ, resultB)
                                            time.sleep(0.5)
                                            Log.EscreverPZ0(filencp, self.P, self.x, self.y)
                                            window.Acontecimento("Descida de Z do pino")
                                            window.write_textBox()
                                            self.j = 3
                                        elif self.j == 3:
                                            resultX = round(float(self.resultado[0]), 2)
                                            resultY = round(float(self.resultado[1]), 2)
                                            resultZ = round(float(self.resultado[3]), 3)
                                            resultB = round(float(self.resultado[4]), 3)
                                            window.update_labels_Opti(resultX, resultY, resultZ, resultB)
                                            time.sleep(0.5)
                                            Log.EscreverPB0(filencp, self.x, self.y)
                                            window.Acontecimento("Rotacionando ponto inicial B do pino")
                                            window.write_textBox()
                                            self.j = 4
                                        elif self.j == 4:
                                            resultX = round(float(self.resultado[0]), 2)
                                            resultY = round(float(self.resultado[1]), 2)
                                            resultZ = round(float(self.resultado[3]), 3)
                                            resultB = round(float(self.resultado[4]), 3)
                                            window.update_labels_Opti(resultX, resultY, resultZ, resultB)
                                            window.write_textBox()

                                            self.iC = window.iC()
                                            self.jC = window.jC()

                                            if self.iC == 1 and self.jC == 1:
                                                self.P = window.ReturnQDial()
                                                self.F = window.ReturnQDial2()

                                                print("\nCoordenadas do molde:\n", self.x, self.y, self.z)
                                                self.z_CR = round(float(lines_CR[self.i].split()[1]), 3)
                                                print("Coordenadas reais:\n", self.x, self.y, self.z_CR)

                                                self.x = df.iloc[self.i]["X"]
                                                self.y = df.iloc[self.i]["Y"]
                                                self.z = round(df.iloc[self.i]["Z"], 3)
                                                window.update_labels(self.x, self.y, self.z)
                                                window.update_labels_CR(self.x, self.y, self.z_CR)

                                                time.sleep(0.5)
                                                Log.EscreverZ0(filencp, self.P, self.x, self.y)
                                                window.Acontecimento("Deslocamento ás coordenadas do pino.")
                                                window.write_textBox()

                                                print("Coordenadas OptiCNC:")
                                                window.PinoExecucaoself(self.i + 1)
                                                self.LimparLog10Registos += 1
                                                self.i += 1
                                                self.j = 0
                                            else:
                                                if self.g ==0:

                                                    time.sleep(0.5)
                                                    Log.Escrever0(filencp, self.P)
                                                    window.Acontecimento("Regresso ao Ponto de Origem.")
                                                    window.write_textBox()
                                                    self.g = 1
                                                elif self.g == 1:
                                                    resultX = round(float(self.resultado[0]), 2)
                                                    resultY = round(float(self.resultado[1]), 2)
                                                    resultZ = round(float(self.resultado[3]), 3)
                                                    resultB = round(float(self.resultado[4]), 3)
                                                    window.update_labels_Opti(resultX, resultY, resultZ, resultB)
                                                    window.WorkAuto_Buttons()
                                                    window.TextLabelManual()
                                                    window.InputPinoDefault()
                                                    sys.exit(0)

                                        if self.LimparLog10Registos == 10:
                                            with open(recent_log_file, 'w') as file:
                                                file.write('')
                                            self.LimparLog10Registos = 0

                                    elif self.i == len(df['X']):
                                        if self.j == 0:
                                            resultX = round(float(self.resultado[0]), 2)
                                            resultY = round(float(self.resultado[1]), 2)
                                            resultZ = round(float(self.resultado[3]), 3)
                                            resultB = round(float(self.resultado[4]), 3)
                                            window.update_labels_Opti(resultX, resultY, resultZ, resultB)
                                            time.sleep(0.5)
                                            Log.EscreverZ(filencp, self.P, self.x, self.y, self.z_CR)
                                            window.Acontecimento("Subida de Z do pino")
                                            window.write_textBox()
                                            self.j = 1
                                        elif self.j == 1:
                                            resultX = round(float(self.resultado[0]), 2)
                                            resultY = round(float(self.resultado[1]), 2)
                                            resultZ = round(float(self.resultado[3]), 3)
                                            resultB = round(float(self.resultado[4]), 3)
                                            window.update_labels_Opti(resultX, resultY, resultZ, resultB)
                                            time.sleep(0.5)
                                            Log.EscreverZB(filencp, self.F, self.x, self.y, self.z,self.z_CR)
                                            window.Acontecimento("Rotação do pino")
                                            window.write_textBox()
                                            self.j = 2

                                        elif self.j == 2:

                                            resultX = round(float(self.resultado[0]), 2)
                                            resultY = round(float(self.resultado[1]), 2)
                                            resultZ = round(float(self.resultado[3]), 3)
                                            resultB = round(float(self.resultado[4]), 3)
                                            window.update_labels_Opti(resultX, resultY, resultZ, resultB)
                                            time.sleep(0.5)
                                            Log.EscreverPZ0(filencp, self.P, self.x, self.y)
                                            window.Acontecimento("Descida de Z do pino")
                                            window.write_textBox()
                                            self.j = 3
                                        elif self.j == 3:
                                            resultX = round(float(self.resultado[0]), 2)
                                            resultY = round(float(self.resultado[1]), 2)
                                            resultZ = round(float(self.resultado[3]), 3)
                                            resultB = round(float(self.resultado[4]), 3)
                                            window.update_labels_Opti(resultX, resultY, resultZ, resultB)
                                            time.sleep(0.5)
                                            Log.EscreverPB0(filencp, self.x, self.y)
                                            window.Acontecimento("Rotacionando ponto inicial B do pino")
                                            window.write_textBox()
                                            self.j = 4
                                        elif self.j == 4:
                                            resultX = round(float(self.resultado[0]), 2)
                                            resultY = round(float(self.resultado[1]), 2)
                                            resultZ = round(float(self.resultado[3]), 3)
                                            resultB = round(float(self.resultado[4]), 3)
                                            window.update_labels_Opti(resultX, resultY, resultZ, resultB)
                                            time.sleep(0.5)
                                            Log.Escrever0(filencp, self.P)
                                            window.Acontecimento("Regresso ao Ponto de Origem.")
                                            window.write_textBox()
                                            self.j = 5
                                        elif self.j == 5:
                                            resultX = round(float(self.resultado[0]), 2)
                                            resultY = round(float(self.resultado[1]), 2)
                                            resultZ = round(float(self.resultado[3]), 3)
                                            resultB = round(float(self.resultado[4]), 3)
                                            window.update_labels_Opti(resultX, resultY, resultZ, resultB)
                                            with open(recent_log_file, 'w') as file:
                                                file.write('')
                                            self.LimparLog10Registos = 0
                                            # window.modify_powerButton()
                                            window.modify_autoButton()
                                            window.WorkButtonPino()
                                            window.Enable_Button()
                                            window.TextLabelManual()
                                            window.InputPinoDefault()
                                            self.i = 0
                                            observer.stop()
                                            sys.exit(0)

                                else:
                                    if self.o == 0:
                                        resultX = round(float(self.resultado[0]), 2)
                                        resultY = round(float(self.resultado[1]), 2)
                                        resultZ = round(float(self.resultado[3]), 3)
                                        resultB = round(float(self.resultado[4]), 3)
                                        window.update_labels_Opti(resultX, resultY, resultZ, resultB)
                                        time.sleep(0.5)
                                        Log.Escrever0(filencp, self.P)
                                        window.Acontecimento("Regresso ao Ponto de Origem.")
                                        window.write_textBox()
                                        self.o = 1
                                    elif self.o == 1:
                                        resultX = round(float(self.resultado[0]), 2)
                                        resultY = round(float(self.resultado[1]), 2)
                                        resultZ = round(float(self.resultado[3]), 3)
                                        resultB = round(float(self.resultado[4]), 3)
                                        window.update_labels_Opti(resultX, resultY, resultZ, resultB)
                                        window.Enable_Button()
                                        window.TextLabelManual()
                                        window.InputPinoDefault()
                                        window.WorkAuto_Buttons()
                                        self.o = 0
                                        sys.exit(0)

            # Criar o observador para monitorar as mudanças no arquivo de log
            observer = Observer()
            event_handler = LogFileEventHandler()

            # Iniciar o observador e o loop de verificação
            observer.schedule(event_handler, logs_folder, recursive=False)
            observer.start()

            try:
                observer.join()
            except KeyboardInterrupt:
                observer.stop()

            observer.join()
    else:
        QTimer.singleShot(0, window.show_popup_Error)
        window.modify_autoButton()

# -----------------------------------------------------------------------------------------------------------------------------------------------------#


def input_thread_func_manual(window):
    indice = window.NPinoManual()
    # Pasta que contém os logs
    logs_folder = r'C:\\Users\lenovo\Documents\Tecmacal\OPTIMACNCGRAF7.1\log'
    # Encontrar o arquivo de log mais recente na pasta
    log_files = glob.glob(os.path.join(logs_folder, '*.txt'))
    recent_log_file = max(log_files, key=os.path.getmtime)
    modelo_path = window.filepath()
    print(modelo_path)
    print(recent_log_file)
    FP1 = int(window.ReturnQDial())
    FP2 = int(window.ReturnQDial2())

    # if modelo_path is not None:
    if modelo_path is not None and FP1 > 0 and FP2 > 0:
        window.StopButtonReset()
        x_max, y_max, z_max, dim, pin_spacing, angle, filencp = configDefualt.ValoresConfig()
        df, modelo_x, modelo_y, modelo_z, x_max, y_max, df = PointsManager.principal(x_max, y_max, dim,
                                                                                     pin_spacing, angle,
                                                                                     modelo_path, z_max)
        window.TextLabelManual()
        window.StopButtonPino()
        window.Notenable_autoButton()
        window.Notenable_Button()
        with open('Sistema_Visao.txt', 'r') as file:
            lines_CR = file.readlines()

        if indice >= 0 and indice <= len(df['X']):

            class LogFileEventHandler(FileSystemEventHandler):
                def __init__(self):
                    self.primeiros_elementos = None
                    self.lineDigite = ""
                    self.VetorLineDigite = []
                    self.LimparLog10Registos = 0
                    self.Coordenadasreais = lines_CR
                    self.string_procurada = "Job finish, ready"
                    self.z_CR = 0
                    self.i = indice - 1
                    self.P = window.ReturnQDial()
                    self.F = window.ReturnQDial2()
                    self.j = 0
                    self.resultado = None
                    self.p = 0

                    self.iC = window.iC()
                    self.jC = window.jC()

                    self.x = df.iloc[self.i]["X"]
                    self.y = df.iloc[self.i]["Y"]
                    self.z = round(df.iloc[self.i]["Z"], 3)

                    if self.i > -1:
                        print("\nCoordenadas do molde:\n", self.x, self.y, self.z)
                        self.z_CR = round(float(lines_CR[self.i].split()[1]), 3)
                        print("Coordenadas reais:\n", self.x, self.y, self.z_CR)
                        window.update_labels(self.x, self.y, self.z)
                        window.update_labels_CR(self.x, self.y, self.z_CR)
                        Log.EscreverZ0(filencp, self.P, self.x, self.y)
                        window.Acontecimento("Deslocamento á ccoordenadas do pino.")
                        print("Coordenadas OptiCNC:")
                        window.write_textBox()
                    elif self.i == -1:
                        Log.Escrever0(filencp, self.P)
                        window.Acontecimento("Regresso ao Ponto de Origem.")

                        window.write_textBox()

                def on_modified(self, event):
                    if not event.is_directory and event.src_path == recent_log_file:
                        with open(recent_log_file, 'r') as file:
                            linesOC = file.readlines()

                        if linesOC:
                            last_line = linesOC[-1].strip()
                            last_line_split = last_line.split()
                            last_line_splitFloat = last_line.split(".")

                            if last_line_split[0].isdigit() or last_line_splitFloat[0].isdigit():
                                # window.update_labels_Opti(0, 0, 0 , 0)
                                self.lineDigite = last_line.split()
                                self.resultado = self.lineDigite[:5]

                            if self.string_procurada.lower() in last_line.lower():
                                if self.iC == 1 and self.jC == 0:

                                    if self.i == 0:
                                        self.i += 1

                                    if self.i <= len(df['X']) and self.i >= 0:
                                        # print(self.resultado, "\n")
                                        if self.j == 0:
                                            resultX = round(float(self.resultado[0]), 2)
                                            resultY = round(float(self.resultado[1]), 2)
                                            resultZ = round(float(self.resultado[3]), 3)
                                            resultB = round(float(self.resultado[4]), 3)
                                            window.update_labels_Opti(resultX, resultY, resultZ, resultB)
                                            time.sleep(0.5)
                                            Log.EscreverZ(filencp, self.P, self.x, self.y, self.z_CR)
                                            window.Acontecimento("Subida do Z do pino.")

                                            window.write_textBox()

                                            self.j = 1
                                        elif self.j == 1:
                                            resultX = round(float(self.resultado[0]), 2)
                                            resultY = round(float(self.resultado[1]), 2)
                                            resultZ = round(float(self.resultado[3]), 3)
                                            resultB = round(float(self.resultado[4]), 3)
                                            window.update_labels_Opti(resultX, resultY, resultZ, resultB)
                                            time.sleep(0.5)
                                            Log.EscreverZB(filencp, self.F, self.x, self.y, self.z,self.z_CR)
                                            window.Acontecimento("Rotação do pino.")
                                            window.write_textBox()

                                            self.j = 2

                                        elif self.j == 2:
                                            resultX = round(float(self.resultado[0]), 2)
                                            resultY = round(float(self.resultado[1]), 2)
                                            resultZ = round(float(self.resultado[3]), 3)
                                            resultB = round(float(self.resultado[4]), 3)
                                            window.update_labels_Opti(resultX, resultY, resultZ, resultB)
                                            time.sleep(0.5)
                                            Log.EscreverPZ0(filencp, self.P, self.x, self.y)
                                            window.Acontecimento("Descida de Z do pino")
                                            window.write_textBox()
                                            self.j = 3
                                        elif self.j == 3:
                                            resultX = round(float(self.resultado[0]), 2)
                                            resultY = round(float(self.resultado[1]), 2)
                                            resultZ = round(float(self.resultado[3]), 3)
                                            resultB = round(float(self.resultado[4]), 3)
                                            window.update_labels_Opti(resultX, resultY, resultZ, resultB)
                                            time.sleep(0.5)
                                            Log.EscreverPB0(filencp, self.x, self.y)
                                            window.Acontecimento("Rotacionando ponto inicial B do pino")
                                            window.write_textBox()
                                            self.j = 4
                                        elif self.j == 4:
                                            resultX = round(float(self.resultado[0]), 2)
                                            resultY = round(float(self.resultado[1]), 2)
                                            resultZ = round(float(self.resultado[3]), 3)
                                            resultB = round(float(self.resultado[4]), 3)
                                            window.update_labels_Opti(resultX, resultY, resultZ, resultB)
                                            window.write_textBox()
                                            self.P = window.ReturnQDial()
                                            self.F = window.ReturnQDial2()
                                            # Log.Escrever0(filencp, self.P)
                                            resultX = round(float(self.resultado[0]), 2)
                                            resultY = round(float(self.resultado[1]), 2)
                                            resultZ = round(float(self.resultado[3]), 3)
                                            resultB = round(float(self.resultado[4]), 3)
                                            window.update_labels_Opti(resultX, resultY, resultZ, resultB)
                                            window.WorkButtonPino()
                                            window.Enable_autoButton()
                                            window.Enable_Button()
                                            window.WorkButtonReset()
                                            sys.exit(0)
                                    elif self.i == -1:
                                        resultX = round(float(self.resultado[0]), 2)
                                        resultY = round(float(self.resultado[1]), 2)
                                        resultZ = round(float(self.resultado[3]), 3)
                                        resultB = round(float(self.resultado[4]), 3)
                                        window.update_labels_Opti(resultX, resultY, resultZ, resultB)
                                        self.p = 1
                                        window.WorkButtonPino()
                                        window.Enable_autoButton()
                                        window.Enable_Button()
                                        window.WorkButtonReset()
                                        sys.exit(0)

            # Criar o observador para monitorar as mudanças no arquivo de log
            observer = Observer()
            event_handler = LogFileEventHandler()

            # Iniciar o observador e o loop de verificação
            observer.schedule(event_handler, logs_folder, recursive=False)
            observer.start()

            try:
                observer.join()
            except KeyboardInterrupt:
                observer.stop()

            observer.join()
        else:
            window.WorkButtonPino()
    else:
        QTimer.singleShot(0, window.show_popup_Error)


#-----------------------------------------------------------------------------------------------------------------#

def input_thread_func_autoReset(window):
    # Pasta que contém os logs
    logs_folder = r'C:\Users\lenovo\Documents\Tecmacal\OPTIMACNCGRAF7.1\log'
    # Encontrar o arquivo de log mais recente na pasta
    log_files = glob.glob(os.path.join(logs_folder, '*.txt'))
    recent_log_file = max(log_files, key=os.path.getmtime)
    modelo_path = window.filepath()
    print(modelo_path)
    FP1 = int(window.ReturnQDial())
    FP2 = int(window.ReturnQDial2())
    # if modelo_path is not None:
    if modelo_path is not None and FP1 > 0 and FP2 > 0:
        window.StopGroupReset()
        x_max, y_max, z_max, dim, pin_spacing, angle, filencp = configDefualt.ValoresConfig()
        df, modelo_x, modelo_y, modelo_z, x_max, y_max, df = PointsManager.principal(x_max, y_max, dim,
                                                                                     pin_spacing, angle,
                                                                                     modelo_path, z_max)
        window.TextLabelPinoExecucao()
        window.Notenable_Button()
        with open('Sistema_Visao.txt', 'r') as file:
            lines_CR = file.readlines()

            class LogFileEventHandler(FileSystemEventHandler):
                def __init__(self):
                    self.primeiros_elementos = None
                    self.lineDigite = ""
                    self.VetorLineDigite = []
                    self.LimparLog10Registos = 0
                    self.Coordenadasreais = lines_CR
                    self.i = 0
                    self.o = 0
                    self.string_procurada = "Job finish, ready"
                    self.z_CR = 0
                    self.P = window.ReturnQDial()
                    self.F = window.ReturnQDial2()
                    self.j = 0
                    self.g=0
                    self.resultado = None
                    Log.Escrever0(filencp, self.P)
                    self.iC = window.iC()
                    self.jC = window.jC()
                    self.lC = window.lC()
                    window.Acontecimento("Regresso ao Ponto Origem.")
                    window.write_textBox()
                    window.PinoExecucaoself(0)

                def on_modified(self, event):
                    if not event.is_directory and event.src_path == recent_log_file:
                        with open(recent_log_file, 'r') as file:
                            linesOC = file.readlines()

                        if linesOC:
                            last_line = linesOC[-1].strip()
                            last_line_split = last_line.split()
                            last_line_splitFloat = last_line.split(".")

                            if last_line_split[0].isdigit() or last_line_splitFloat[0].isdigit():
                                # window.update_labels_Opti(0, 0, 0 , 0)
                                self.lineDigite = last_line.split()
                                self.resultado = self.lineDigite[:5]

                            if self.string_procurada.lower() in last_line.lower():
                                if self.iC == 1 and self.jC == 0 and self.lC == 1:

                                    if self.i == 0:
                                        self.x = df.iloc[self.i]["X"]
                                        self.y = df.iloc[self.i]["Y"]
                                        self.z = round(df.iloc[self.i]["Z"], 3)
                                        window.PinoExecucaoself(self.i + 1)
                                        print("\nCoordenadas do molde:\n", self.x, self.y, self.z)
                                        self.z_CR = round(float(lines_CR[self.i].split()[1]), 3)
                                        print("Coordenadas reais:\n", self.x, self.y, self.z_CR)
                                        window.update_labels(self.x, self.y, self.z)
                                        window.update_labels_CR(self.x, self.y, self.z_CR)
                                        time.sleep(0.5)
                                        Log.EscreverZ0(filencp, self.P, self.x, self.y)
                                        window.Acontecimento("Deslocamento ás coordenadas do pino.")
                                        print("Coordenadas OptiCNC:")
                                        window.write_textBox()
                                        self.i += 1

                                    elif self.i < len(df['X']) and self.i > 0:
                                        # print(self.resultado, "\n")
                                        if self.j == 0:
                                            resultX = round(float(self.resultado[0]), 2)
                                            resultY = round(float(self.resultado[1]), 2)
                                            resultZ = round(float(self.resultado[3]), 3)
                                            resultB = round(float(self.resultado[4]), 3)
                                            window.update_labels_Opti(resultX, resultY, resultZ, resultB)
                                            time.sleep(0.5)
                                            Log.EscreverZReset(filencp, self.P, self.x, self.y, self.z , self.z_CR)
                                            window.Acontecimento("Subida de Z do pino")

                                            window.write_textBox()

                                            self.j = 1
                                        elif self.j == 1:
                                            resultX = round(float(self.resultado[0]), 2)
                                            resultY = round(float(self.resultado[1]), 2)
                                            resultZ = round(float(self.resultado[3]), 3)
                                            resultB = round(float(self.resultado[4]), 3)
                                            window.update_labels_Opti(resultX, resultY, resultZ, resultB)
                                            time.sleep(0.5)
                                            Log.EscreverZABReset(filencp, self.F, self.x, self.y, self.z , self.z_CR)
                                            window.Acontecimento("Rotação do pino")
                                            window.write_textBox()

                                            self.j = 2

                                        elif self.j == 2:
                                            resultX = round(float(self.resultado[0]), 2)
                                            resultY = round(float(self.resultado[1]), 2)
                                            resultZ = round(float(self.resultado[3]), 3)
                                            resultB = round(float(self.resultado[4]), 3)
                                            window.update_labels_Opti(resultX, resultY, resultZ, resultB)
                                            time.sleep(0.5)
                                            Log.EscreverZAReset(filencp, self.P, self.x, self.y)
                                            window.Acontecimento("Rotação do pino Sistema de visão")
                                            window.write_textBox()

                                            self.j = 3

                                        elif self.j == 3:
                                            resultX = round(float(self.resultado[0]), 2)
                                            resultY = round(float(self.resultado[1]), 2)
                                            resultZ = round(float(self.resultado[3]), 3)
                                            resultB = round(float(self.resultado[4]), 3)
                                            window.update_labels_Opti(resultX, resultY, resultZ, resultB)
                                            time.sleep(0.5)
                                            Log.EscreverZB0Reset(filencp, self.F, self.x, self.y)
                                            window.Acontecimento("Rotação do pino Sistema de visão")
                                            window.write_textBox()

                                            self.j = 4
                                        elif self.j == 4:
                                            resultX = round(float(self.resultado[0]), 2)
                                            resultY = round(float(self.resultado[1]), 2)
                                            resultZ = round(float(self.resultado[3]), 3)
                                            resultB = round(float(self.resultado[4]), 3)
                                            window.update_labels_Opti(resultX, resultY, resultZ, resultB)
                                            window.write_textBox()

                                            self.iC = window.iC()
                                            self.jC = window.jC()
                                            self.lC = window.lC()

                                            if self.iC == 1 and self.jC == 0 and self.lC == 1:
                                                self.P = window.ReturnQDial()
                                                self.F = window.ReturnQDial2()

                                                print("\nCoordenadas do molde:\n", self.x, self.y, self.z)
                                                self.z_CR = round(float(lines_CR[self.i].split()[1]), 3)
                                                print("Coordenadas reais:\n", self.x, self.y, self.z_CR)

                                                self.x = df.iloc[self.i]["X"]
                                                self.y = df.iloc[self.i]["Y"]
                                                self.z = round(df.iloc[self.i]["Z"], 3)
                                                window.update_labels(self.x, self.y, self.z)
                                                window.update_labels_CR(self.x, self.y, self.z_CR)

                                                time.sleep(0.5)
                                                Log.EscreverZ0(filencp, self.P, self.x, self.y)
                                                window.Acontecimento("Deslocamento ás coordenadas do pino.")
                                                window.write_textBox()

                                                print("Coordenadas OptiCNC:")
                                                window.PinoExecucaoself(self.i + 1)
                                                self.LimparLog10Registos += 1
                                                self.i += 1
                                                self.j = 0
                                            else:
                                                if self.g == 0:

                                                    time.sleep(0.5)
                                                    Log.Escrever0(filencp, self.P)
                                                    window.Acontecimento("Regresso ao Ponto de Origem.")
                                                    window.write_textBox()
                                                    self.g = 1
                                                elif self.g == 1:
                                                    resultX = round(float(self.resultado[0]), 2)
                                                    resultY = round(float(self.resultado[1]), 2)
                                                    resultZ = round(float(self.resultado[3]), 3)
                                                    resultB = round(float(self.resultado[4]), 3)
                                                    window.update_labels_Opti(resultX, resultY, resultZ, resultB)
                                                    window.WorkGroupReset()
                                                    window.TextLabelManual()
                                                    window.InputPinoDefault()
                                                    sys.exit(0)

                                        if self.LimparLog10Registos == 10:
                                            with open(recent_log_file, 'w') as file:
                                                file.write('')
                                            self.LimparLog10Registos = 0

                                    elif self.i == len(df['X']):
                                        if self.j == 0:
                                            resultX = round(float(self.resultado[0]), 2)
                                            resultY = round(float(self.resultado[1]), 2)
                                            resultZ = round(float(self.resultado[3]), 3)
                                            resultB = round(float(self.resultado[4]), 3)
                                            window.update_labels_Opti(resultX, resultY, resultZ, resultB)
                                            time.sleep(0.5)
                                            Log.EscreverZReset(filencp, self.P, self.x, self.y, self.z , self.z_CR)
                                            window.Acontecimento("Subida de Z do pino")
                                            window.write_textBox()
                                            self.j = 1
                                        elif self.j == 1:
                                            resultX = round(float(self.resultado[0]), 2)
                                            resultY = round(float(self.resultado[1]), 2)
                                            resultZ = round(float(self.resultado[3]), 3)
                                            resultB = round(float(self.resultado[4]), 3)
                                            window.update_labels_Opti(resultX, resultY, resultZ, resultB)
                                            time.sleep(0.5)
                                            Log.EscreverZABReset(filencp, self.F, self.x, self.y, self.z , self.z_CR)
                                            window.Acontecimento("Rotação do pino")
                                            window.write_textBox()
                                            self.j = 2
                                        elif self.j == 2:
                                            resultX = round(float(self.resultado[0]), 2)
                                            resultY = round(float(self.resultado[1]), 2)
                                            resultZ = round(float(self.resultado[3]), 3)
                                            resultB = round(float(self.resultado[4]), 3)
                                            window.update_labels_Opti(resultX, resultY, resultZ, resultB)
                                            time.sleep(0.5)
                                            Log.EscreverZAReset(filencp, self.P, self.x, self.y)
                                            window.Acontecimento("Rotação do pino Sistema de visão")
                                            window.write_textBox()

                                            self.j = 3

                                        elif self.j == 3:
                                            resultX = round(float(self.resultado[0]), 2)
                                            resultY = round(float(self.resultado[1]), 2)
                                            resultZ = round(float(self.resultado[3]), 3)
                                            resultB = round(float(self.resultado[4]), 3)
                                            window.update_labels_Opti(resultX, resultY, resultZ, resultB)
                                            time.sleep(0.5)
                                            Log.EscreverZB0Reset(filencp, self.F, self.x, self.y)
                                            window.Acontecimento("Rotação do pino Sistema de visão")
                                            window.write_textBox()

                                            self.j = 4

                                        elif self.j == 4:
                                            resultX = round(float(self.resultado[0]), 2)
                                            resultY = round(float(self.resultado[1]), 2)
                                            resultZ = round(float(self.resultado[3]), 3)
                                            resultB = round(float(self.resultado[4]), 3)
                                            window.update_labels_Opti(resultX, resultY, resultZ, resultB)
                                            time.sleep(0.5)
                                            Log.Escrever0(filencp, self.P)
                                            window.Acontecimento("Regresso ao Ponto de Origem.")
                                            window.write_textBox()
                                            self.j = 5
                                        elif self.j == 5:
                                            resultX = round(float(self.resultado[0]), 2)
                                            resultY = round(float(self.resultado[1]), 2)
                                            resultZ = round(float(self.resultado[3]), 3)
                                            resultB = round(float(self.resultado[4]), 3)
                                            window.update_labels_Opti(resultX, resultY, resultZ, resultB)
                                            with open(recent_log_file, 'w') as file:
                                                file.write('')
                                            self.LimparLog10Registos = 0
                                            # window.modify_powerButton()
                                            window.modify_autoButton()
                                            window.WorkButtonPino()
                                            window.Enable_Button()
                                            window.TextLabelManual()
                                            window.InputPinoDefault()
                                            window.WorkGroupReset()
                                            self.i = 0
                                            observer.stop()
                                            sys.exit(0)

                                else:
                                    if self.o == 0:
                                        resultX = round(float(self.resultado[0]), 2)
                                        resultY = round(float(self.resultado[1]), 2)
                                        resultZ = round(float(self.resultado[3]), 3)
                                        resultB = round(float(self.resultado[4]), 3)
                                        window.update_labels_Opti(resultX, resultY, resultZ, resultB)
                                        window.Acontecimento("Regresso ao Ponto de Origem.")
                                        time.sleep(0.5)
                                        Log.Escrever0(filencp, self.P)
                                        window.write_textBox()
                                        self.o = 1
                                    elif self.o == 1:
                                        resultX = round(float(self.resultado[0]), 2)
                                        resultY = round(float(self.resultado[1]), 2)
                                        resultZ = round(float(self.resultado[3]), 3)
                                        resultB = round(float(self.resultado[4]), 3)
                                        window.update_labels_Opti(resultX, resultY, resultZ, resultB)
                                        window.Enable_Button()
                                        window.TextLabelManual()
                                        window.WorkGroupReset()
                                        window.InputPinoDefault()
                                        self.o = 0
                                        sys.exit(0)

            # Criar o observador para monitorar as mudanças no arquivo de log
            observer = Observer()
            event_handler = LogFileEventHandler()

            # Iniciar o observador e o loop de verificação
            observer.schedule(event_handler, logs_folder, recursive=False)
            observer.start()

            try:
                observer.join()
            except KeyboardInterrupt:
                observer.stop()

            observer.join()
    else:
        QTimer.singleShot(0, window.show_popup_Error)

def start_input_thread_auto():
    input_thread = threading.Thread(target=input_thread_func_auto, args=(window,), daemon=True)
    input_thread.start()


def start_input_thread_manual():
    input_thread = threading.Thread(target=input_thread_func_manual, args=(window,), daemon=True)
    input_thread.start()

def start_input_thread_autoReset():

    input_thread = threading.Thread(target=input_thread_func_autoReset, args=(window,), daemon=True)
    input_thread.start()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec())
