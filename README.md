# 🦾 CNC 3D Modelling Controller

**Software desenvolvido para automação e controlo de máquinas industriais de modelação 3D.**
*Projeto desenvolvido durante estágio curricular na Optima (Grupo Tecmacal).*

## 📖 Sobre o Projeto
Este software foi criado para resolver o problema de controlar uma máquina CNC para esculpir moldes 3D através de pinos. O desafio principal foi traduzir coordenadas virtuais (modelos 3D) em movimentos mecânicos precisos.

## 🧠 Desafios Técnicos & Soluções (A Lógica)
* **Cálculos Matemáticos:** Implementação de algoritmos de **Trigonometria** e **Distância Euclidiana** para calcular a trajetória exata da ferramenta de corte.
* **Interpretação de G-Code:** Parsing de ficheiros NCP e logs da máquina para comunicação em tempo real.
* **Mapeamento de Eixos:** Conversão lógica entre o referencial da peça (molde) e o referencial da máquina (Eixos XYZ).
* **Interface Gráfica (GUI):** Painel de controlo para o operador visualizar o processo e calibrar a máquina.

## 🛠️ Tecnologias Usadas
* **Linguagem:** Python 3.x
* **Bibliotecas:** Tkinter, PyQt, Numpy, Math, Serial/PySerial, ...
* **Conceitos:** Automação Industrial, Geometria Analítica, I/O de Ficheiros.

## ⚠️ Nota
Este repositório contém uma demonstração da lógica desenvolvida. Algumas funcionalidades específicas de hardware proprietário foram removidas por questões de confidencialidade.
