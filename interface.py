# -*- coding: utf-8 -*-
import main
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5 import *
import sys
import numpy as np

DISPLAY_CITY =["Moscow", "Kazan","Vladivostok", "Sochi", "Yekaterinburg", "Belgorod"]
color = 'black'
rows = [("Newton", "1643-01-04", "Classical mechanics"),
        ("Einstein", "1879-03-14", "Relativity"),
        ("Darwin", "1809-02-12", "Evolution")]


def make_zeros(number):
    return [0] * number

CITIES = dict.fromkeys(DISPLAY_CITY,make_zeros(6))
CITIES_UPD = dict.fromkeys(DISPLAY_CITY,make_zeros(6))
CITIES_RES= dict.fromkeys(DISPLAY_CITY,make_zeros(4))


class MyForm(QDialog):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.a=0
        self.ui.cities.currentIndexChanged.connect(self.changed_values)
        self.ui.savebutton.clicked.connect(self.on_button_clicked)
        self.ui.runbutton.clicked.connect(self.on_button_clicked_2)
        self.ui.stepbutton.clicked.connect(self.load_data)
        self.ui.exitbutton.clicked.connect(self.close)  
        self.ui.w = None

    def __del__(self):
        sys.stdout = sys.__stdout__


    def changed_values(self):
        for city in CITIES:
                firstParameter = self.ui.cities.currentText()
                if firstParameter == city:
                        lst = CITIES.get(city)
                        self.ui.population.setValue(lst[0]*100)
                        self.ui.vaccinerate.setValue(lst[1]*100)
                        self.ui.virusrate.setValue(lst[2]*100)
                        self.ui.recoveryrate.setValue(lst[3]*100)
                        self.ui.transportrate.setValue(lst[4]*100)

    def on_button_clicked(self):
        people = int(self.ui.population.text())
        alpha = int(self.ui.vaccinerate.text())
        beta = int(self.ui.virusrate.text())
        gamma = int(self.ui.recoveryrate.text())
        phi = int(self.ui.transportrate.text())
        alphaper = alpha / 100
        betaper = beta / 100
        gammaper = gamma / 100
        phiper = phi / 100
        alert = QMessageBox()
        if (alphaper > betaper) and (alphaper - betaper > 0.4):
                delta = 0.015
        elif (alphaper < betaper) and (betaper - alphaper > 0.4):
                delta = 0.035
        else:
                delta = 0.025
        CITIES.update({self.ui.cities.currentText(): 
                [people,
                alphaper,
                betaper,
                gammaper,
                phiper,
                delta]
           })
        alert.setText('Your data was saved!')
        alert.exec_()
        

    def on_button_clicked_2(self):
        alert = QMessageBox()
        time = int(self.ui.modeltime.text())
        val = time - 1 
        self.ui.table.setHorizontalHeaderLabels(["Step", "City", "Population", "Suspected", "Vaccine", "Virus", "Dead"])
        self.ui.table.setColumnCount(7)
        if time > 0:
                for city in CITIES:
                        lst = CITIES.get(city)
                        (a,b,c,d) = main.start(lst[0],time,lst[1],lst[2],lst[3],lst[4],lst[5])
                        CITIES_RES.update({city: (a[val],b[val],c[val],d[val])})
                        rowPosition = self.ui.table.rowCount()
                        self.ui.table.insertRow(rowPosition)
                        self.ui.table.setItem(rowPosition , 0, QStandardItem(str("RESULT")))
                        self.ui.table.setItem(rowPosition , 1, QStandardItem(city))
                        self.ui.table.setItem(rowPosition , 2, QStandardItem(str(lst[0])))
                        self.ui.table.setItem(rowPosition , 3, QStandardItem(str(a[val])))
                        self.ui.table.setItem(rowPosition , 4, QStandardItem(str(b[val])))
                        self.ui.table.setItem(rowPosition , 5, QStandardItem(str(c[val])))
                        self.ui.table.setItem(rowPosition , 6, QStandardItem(str(d[val])))
                        rowPosition = self.ui.table.rowCount()
                for i in range(7):
                        self.ui.table.setItem(rowPosition , i, QStandardItem(str("--------------")))
                x = 0 
                y = 0
                z = 0
                w = 0
                for city in CITIES_RES:
                        lst_2 = CITIES_RES.get(city)
                        x += lst_2[0] # Симптомы
                        y += lst_2[1] # Инфецированы
                        z += lst_2[2] # Вакцинированы
                        w += lst_2[3] # Смертность
                self.ui.susceptibleCount.setText(str(x))
                self.ui.infectedCount.setText(str(y))
                self.ui.vaccineCount.setText(str(z))
                self.ui.deathsCount.setText(str(w))
        else:
                alert.setText('Warning! Set duration time for your model')
                alert.exec_()

    def load_data(self):
        alert = QMessageBox()
        time = int(self.ui.modeltime.text()) 
        self.ui.table.setHorizontalHeaderLabels(["Step", "City", "Population", "Suspected", "Vaccine", "Virus", "Dead"])
        self.ui.table.setColumnCount(7)
        if self.a < time:
                for city in CITIES:
                        numlist = []
                        lst_of_city = CITIES.get(city)
                        (a,b,c,d) = main.start(lst_of_city[0],time,lst_of_city[1],lst_of_city[2],lst_of_city[3],lst_of_city[4],lst_of_city[5])
                        CITIES_UPD.update({city: (a,b,c,d)})
                        value_list = CITIES_UPD.get(city)
                        for i in range(len(value_list)):
                                a  = value_list[i]
                                numlist.append(a[self.a])
                        rowPosition = self.ui.table.rowCount()
                        self.ui.table.insertRow(rowPosition)
                        self.ui.table.setItem(rowPosition , 0, QStandardItem(str(self.a+1)))
                        self.ui.table.setItem(rowPosition , 1, QStandardItem(city))
                        print(city)
                        self.ui.table.setItem(rowPosition , 2, QStandardItem(str(lst_of_city[0])))
                        self.ui.table.setItem(rowPosition , 3, QStandardItem(str(numlist[0])))
                        self.ui.table.setItem(rowPosition , 4, QStandardItem(str(numlist[1])))
                        self.ui.table.setItem(rowPosition , 5, QStandardItem(str(numlist[2])))
                        self.ui.table.setItem(rowPosition , 6, QStandardItem(str(numlist[3])))
                        rowPosition = self.ui.table.rowCount()
                for i in range(7):
                        self.ui.table.setItem(rowPosition , i, QStandardItem(str("--------------")))
                self.a+=1
        elif self.a == time and time > 0:
                alert.setText('Simulating has finished')
                alert.exec_()
                self.ui.table.clear()
        else:
                alert.setText('Warning! Set duration time for your model')
                alert.exec_()
                
             
class Ui_Dialog(object):
    def setupUi(self, Virus):
        Virus.setObjectName("Virus")
        Virus.resize(1360, 430)
        Virus.setStyleSheet("QDialog {\n"
"    background-color: white;\n"
"}")
        self.bg = QtWidgets.QFrame(Virus)
        self.bg.setGeometry(QtCore.QRect(20, 150, 381, 245))
        self.bg.setStyleSheet("#bg {\n"
"    background-color: rgb(71,63,151);\n"
"border-radius: 20px\n"
"        \n"
"}")
        self.bg.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.bg.setFrameShadow(QtWidgets.QFrame.Raised)
        self.bg.setObjectName("bg")
        self.frame_infected = QtWidgets.QFrame(self.bg)
        self.frame_infected.setGeometry(QtCore.QRect(10, 130, 181, 101))
        self.frame_infected.setStyleSheet("#frame_infected {\n"
"background-color: #FFB259;\n"
"    border-radius: 20px;\n"
"}\n"
"")
        self.frame_infected.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_infected.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_infected.setObjectName("frame_infected")
        self.infected = QtWidgets.QLabel(self.frame_infected)
        self.infected.setGeometry(QtCore.QRect(20, 10, 81, 41))
        font = QtGui.QFont()
        font.setFamily("Montserrat")
        font.setPointSize(19)
        font.setBold(True)
        font.setWeight(75)
        self.infected.setFont(font)
        self.infected.setStyleSheet("color: rgb(255, 255, 255);")
        self.infected.setObjectName("Infected")
        self.infectedCount = QtWidgets.QLabel(self.frame_infected)
        self.infectedCount.setGeometry(QtCore.QRect(20, 50, 141, 41))
        font = QtGui.QFont()
        font.setFamily("Montserrat")
        font.setPointSize(28)
        font.setBold(True)
        font.setWeight(75)
        self.infectedCount.setFont(font)
        self.infectedCount.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.infectedCount.setStyleSheet("color: rgb(255, 255, 255);")
        self.infectedCount.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.infectedCount.setObjectName("infectedCount")
        self.frame_affected = QtWidgets.QFrame(self.bg)
        self.frame_affected.setGeometry(QtCore.QRect(10, 10, 181, 111))
        self.frame_affected.setStyleSheet("#frame_affected {\n"
"    background-color: rgb(76, 217, 123);\n"
"    border-radius: 20px;\n"
"}")
        self.frame_affected.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_affected.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_affected.setObjectName("frame_affected")
        self.susceptible = QtWidgets.QLabel(self.frame_affected)
        self.susceptible.setGeometry(QtCore.QRect(20, 10, 111, 41))
        font = QtGui.QFont()
        font.setFamily("Montserrat")
        font.setPointSize(19)
        font.setBold(True)
        font.setWeight(75)
        self.susceptible.setFont(font)
        self.susceptible.setStyleSheet("color: rgb(255, 255, 255);")
        self.susceptible.setObjectName("Susceptible")
        self.susceptibleCount = QtWidgets.QLabel(self.frame_affected)
        self.susceptibleCount.setGeometry(QtCore.QRect(10, 60, 161, 41))
        font = QtGui.QFont()
        font.setFamily("Montserrat")
        font.setPointSize(28)
        font.setBold(True)
        font.setWeight(75)
        self.susceptibleCount.setFont(font)
        self.susceptibleCount.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.susceptibleCount.setStyleSheet("color: rgb(255, 255, 255);")
        self.susceptibleCount.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.susceptibleCount.setObjectName("SusceptibleCount")
        self.frame_deaths = QtWidgets.QFrame(self.bg)
        self.frame_deaths.setGeometry(QtCore.QRect(200, 10, 171, 111))
        self.frame_deaths.setStyleSheet("background-color: rgb(255, 89, 89);\n"
"    border-radius: 20px;")
        self.frame_deaths.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_deaths.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_deaths.setObjectName("frame_deaths")
        self.deaths = QtWidgets.QLabel(self.frame_deaths)
        self.deaths.setGeometry(QtCore.QRect(20, 10, 71, 41))
        font = QtGui.QFont()
        font.setFamily("Montserrat")
        font.setPointSize(19)
        font.setBold(True)
        font.setWeight(75)
        self.deaths.setFont(font)
        self.deaths.setStyleSheet("color: rgb(255, 255, 255);")
        self.deaths.setObjectName("deaths")
        self.deathsCount = QtWidgets.QLabel(self.frame_deaths)
        self.deathsCount.setGeometry(QtCore.QRect(10, 60, 141, 41))
        font = QtGui.QFont()
        font.setFamily("Montserrat")
        font.setPointSize(28)
        font.setBold(True)
        font.setWeight(75)
        self.deathsCount.setFont(font)
        self.deathsCount.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.deathsCount.setStyleSheet("color: rgb(255, 255, 255);")
        self.deathsCount.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.deathsCount.setObjectName("deathsCount")
        self.frame_vaccinated = QtWidgets.QFrame(self.bg)
        self.frame_vaccinated.setGeometry(QtCore.QRect(200, 130, 171, 101))
        self.frame_vaccinated.setStyleSheet("\n"
"background-color: rgb(76, 181, 255);\n"
"    border-radius: 20px;")
        self.frame_vaccinated.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_vaccinated.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_vaccinated.setObjectName("frame_vaccinated")
        self.vaccine = QtWidgets.QLabel(self.frame_vaccinated)
        self.vaccine.setGeometry(QtCore.QRect(20, 10, 121, 41))
        font = QtGui.QFont()
        font.setFamily("Montserrat")
        font.setPointSize(19)
        font.setBold(True)
        font.setWeight(75)
        self.vaccine.setFont(font)
        self.vaccine.setStyleSheet("color: rgb(255, 255, 255);")
        self.vaccine.setObjectName("vaccine")
        self.vaccineCount = QtWidgets.QLabel(self.frame_vaccinated)
        self.vaccineCount.setGeometry(QtCore.QRect(20, 50, 141, 41))
        font = QtGui.QFont()
        font.setFamily("Montserrat")
        font.setPointSize(28)
        font.setBold(True)
        font.setWeight(75)
        self.vaccineCount.setFont(font)
        self.vaccineCount.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.vaccineCount.setStyleSheet("color: rgb(255, 255, 255);")
        self.vaccineCount.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.vaccineCount.setObjectName("vaccineCount")
        self.virustxt = QtWidgets.QLabel(Virus)
        self.virustxt.setGeometry(QtCore.QRect(120, 35, 181, 41))
        font = QtGui.QFont()
        font.setFamily("Montserrat Black")
        font.setPointSize(35)
        font.setItalic(True)
        self.virustxt.setFont(font)
        self.virustxt.setStyleSheet("color: rgb(143, 143, 143);")
        self.virustxt.setObjectName("virustxt")
        self.spreadtxt = QtWidgets.QLabel(Virus)
        self.spreadtxt.setGeometry(QtCore.QRect(160, 65, 181, 41))
        font = QtGui.QFont()
        font.setFamily("Montserrat Black")
        font.setPointSize(37)
        font.setItalic(True)
        self.spreadtxt.setFont(font)
        self.spreadtxt.setStyleSheet("color: rgb(206, 0, 0);")
        self.spreadtxt.setObjectName("spreadtxt")

        self.cities = QtWidgets.QComboBox(Virus)
        self.cities.setCurrentText("Moscow")
        self.base_city = DISPLAY_CITY
        self.cities.addItems(self.base_city)
        self.cities.setGeometry(QtCore.QRect(440, 65, 161, 31))
        self.cities.setObjectName("cities")
        self.cities.setStyleSheet("QComboBox:editable{{ color: {} }}".format(color))
        self.population = QtWidgets.QSpinBox(Virus)
        self.population.setGeometry(QtCore.QRect(530, 115, 131, 31))
        self.population.setMinimum(0) 
        self.population.setMaximum(15000000)
        self.population.setSingleStep(1)
        self.population.setValue(0)
        self.population.setStyleSheet("border-color: rgb(143, 143, 143);")
        self.population.setObjectName("population")

        self.vaccinerate = QtWidgets.QSpinBox(Virus)
        self.vaccinerate.setGeometry(QtCore.QRect(555, 155, 81, 31))
        self.vaccinerate.setMinimum(0) 
        self.vaccinerate.setMaximum(100)
        self.vaccinerate.setSingleStep(1)
        self.vaccinerate.setValue(0)
        self.vaccinerate.setStyleSheet("border-color: rgb(143, 143, 143);")
        self.vaccinerate.setObjectName("vaccinerate")
        self.virusrate = QtWidgets.QSpinBox(Virus)
        self.virusrate.setGeometry(QtCore.QRect(555, 195, 81, 31))
        self.virusrate.setMinimum(0) 
        self.virusrate.setMaximum(100)
        self.virusrate.setSingleStep(1)
        self.virusrate.setValue(0)
        self.virusrate.setStyleSheet("border-color: rgb(143, 143, 143);")
        self.virusrate.setObjectName("virusrate")
        self.recoveryrate = QtWidgets.QSpinBox(Virus)
        self.recoveryrate.setGeometry(QtCore.QRect(555, 235, 81, 31))
        self.recoveryrate.setMinimum(0) 
        self.recoveryrate.setMaximum(100)
        self.recoveryrate.setSingleStep(1)
        self.recoveryrate.setValue(0)
        self.recoveryrate.setStyleSheet("border-color: rgb(143, 143, 143);")
        self.recoveryrate.setObjectName("recoveryrate")
        self.transportrate = QtWidgets.QSpinBox(Virus)
        self.transportrate.setGeometry(QtCore.QRect(555, 275, 81, 31))
        self.transportrate.setMinimum(0) 
        self.transportrate.setMaximum(50)
        self.transportrate.setSingleStep(1)
        self.transportrate.setValue(0)
        self.transportrate.setStyleSheet("border-color: rgb(143, 143, 143);")
        self.transportrate.setObjectName("transportrate")
        
        self.whichCity = QtWidgets.QLabel(Virus)
        self.whichCity.setGeometry(QtCore.QRect(465, 35, 111, 31))
        font = QtGui.QFont()
        font.setFamily("Montserrat Black")
        font.setPointSize(14)
        font.setItalic(True)
        self.whichCity.setFont(font)
        self.whichCity.setStyleSheet("color: rgb(143, 143, 143);")
        self.whichCity.setObjectName("whichCity")

        self.amountPopulation = QtWidgets.QLabel(Virus)
        self.amountPopulation.setGeometry(QtCore.QRect(420, 115, 81, 31))
        font = QtGui.QFont()
        font.setFamily("Montserrat Black")
        font.setPointSize(14)
        font.setItalic(True)
        self.amountPopulation.setFont(font)
        self.amountPopulation.setStyleSheet("color: rgb(143, 143, 143);")
        self.amountPopulation.setObjectName("amountPopulation")

        self.amountVaccine = QtWidgets.QLabel(Virus)
        self.amountVaccine.setGeometry(QtCore.QRect(420, 155, 111, 31))
        font = QtGui.QFont()
        font.setFamily("Montserrat Black")
        font.setPointSize(14)
        font.setItalic(True)
        self.amountVaccine.setFont(font)
        self.amountVaccine.setStyleSheet("color: rgb(143, 143, 143);")
        self.amountVaccine.setObjectName("amountVaccine")

        self.amountVirus = QtWidgets.QLabel(Virus)
        self.amountVirus.setGeometry(QtCore.QRect(420, 195, 111, 31))
        font = QtGui.QFont()
        font.setFamily("Montserrat Black")
        font.setPointSize(14)
        font.setItalic(True)
        self.amountVirus.setFont(font)
        self.amountVirus.setStyleSheet("color: rgb(143, 143, 143);")
        self.amountVirus.setObjectName("amountVirus")

        self.amountRecovery = QtWidgets.QLabel(Virus)
        self.amountRecovery.setGeometry(QtCore.QRect(420, 235, 121, 31))
        font = QtGui.QFont()
        font.setFamily("Montserrat Black")
        font.setPointSize(14)
        font.setItalic(True)
        self.amountRecovery.setFont(font)
        self.amountRecovery.setStyleSheet("color: rgb(143, 143, 143);")
        self.amountRecovery.setObjectName("amountRecovery")

        self.amountTransport = QtWidgets.QLabel(Virus)
        self.amountTransport.setGeometry(QtCore.QRect(420, 275, 131, 31))
        font = QtGui.QFont()
        font.setFamily("Montserrat Black")
        font.setPointSize(14)
        font.setItalic(True)
        self.amountTransport.setFont(font)
        self.amountTransport.setStyleSheet("color: rgb(143, 143, 143);")
        self.amountTransport.setObjectName("amountTransport")

        self.frame_savebutton = QtWidgets.QFrame(Virus)
        self.frame_savebutton.setGeometry(QtCore.QRect(440, 330, 195, 80))
        self.frame_savebutton.setStyleSheet("background-color: rgb(255, 165, 0);\n"
"    border-radius: 15px;")
        self.frame_savebutton.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_savebutton.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_savebutton.setObjectName("frame_savebutton")
        self.savebutton = QtWidgets.QPushButton(self.frame_savebutton)
        self.savebutton.setGeometry(QtCore.QRect(55, 10, 91, 61))
        font = QtGui.QFont()
        font.setFamily("Montserrat Black")
        font.setPointSize(23)
        font.setBold(True)
        font.setWeight(75)
        self.savebutton.setFont(font)
        self.savebutton.setStyleSheet("color: rgb(235, 97, 35);")
        self.savebutton.setObjectName("savebutton")

        self.modeltime = QtWidgets.QSpinBox(Virus)
        self.modeltime.setGeometry(QtCore.QRect(640, 55, 61, 31))
        self.modeltime.setMinimum(0) 
        self.modeltime.setMaximum(10000)
        self.modeltime.setSingleStep(1)
        self.modeltime.setValue(0)
        self.modeltime.setStyleSheet("border-color: rgb(143, 143, 143);")
        self.modeltime.setObjectName("modeltime")
        self.amountTime = QtWidgets.QLabel(Virus)
        self.amountTime.setGeometry(QtCore.QRect(710, 55, 81, 31))
        font = QtGui.QFont()
        font.setFamily("Montserrat Black")
        font.setPointSize(14)
        font.setItalic(True)
        self.amountTime.setFont(font)
        self.amountTime.setStyleSheet("color: rgb(143, 143, 143);")
        self.amountTime.setObjectName("amountTime")

        self.frame_runbutton = QtWidgets.QFrame(Virus)
        self.frame_runbutton.setGeometry(QtCore.QRect(800, 20, 111, 80))
        self.frame_runbutton.setStyleSheet("background-color: rgb(119, 221, 119);\n"
"    border-radius: 15px;")
        self.frame_runbutton.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_runbutton.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_runbutton.setObjectName("frame_runbutton")
        self.runbutton = QtWidgets.QPushButton(self.frame_runbutton)
        self.runbutton.setGeometry(QtCore.QRect(10, 10, 91, 61))
        font = QtGui.QFont()
        font.setFamily("Montserrat Black")
        font.setPointSize(18)
        font.setBold(True)
        font.setWeight(75)
        self.runbutton.setFont(font)
        self.runbutton.setStyleSheet("color: rgb(0, 128, 130);")
        self.runbutton.setObjectName("runbutton")

        self.frame_stepbutton = QtWidgets.QFrame(Virus)
        self.frame_stepbutton.setGeometry(QtCore.QRect(975, 20, 111, 80))
        self.frame_stepbutton.setStyleSheet("background-color: rgb(180, 255, 255);\n"
"    border-radius: 15px;")
        self.frame_stepbutton.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_stepbutton.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_stepbutton.setObjectName("frame_stepbutton ")
        self.stepbutton = QtWidgets.QPushButton(self.frame_stepbutton)
        self.stepbutton.setGeometry(QtCore.QRect(10, 10, 91, 61))
        font = QtGui.QFont()
        font.setFamily("Montserrat Black")
        font.setPointSize(18)
        font.setBold(True)
        font.setWeight(75)
        self.stepbutton.setFont(font)
        self.stepbutton.setStyleSheet("color: rgb(48, 213, 200);")
        self.stepbutton.setObjectName("stepbutton")

        self.frame_exitbutton = QtWidgets.QFrame(Virus)
        self.frame_exitbutton.setGeometry(QtCore.QRect(1140, 20, 111, 80))
        self.frame_exitbutton.setStyleSheet("background-color: rgb(255, 89, 89);\n"
"    border-radius: 15px;")
        self.frame_exitbutton.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_exitbutton.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_exitbutton.setObjectName("frame_exitbutton ")
        self.exitbutton = QtWidgets.QPushButton(self.frame_exitbutton )
        self.exitbutton.setGeometry(QtCore.QRect(10, 10, 91, 61))
        font = QtGui.QFont()
        font.setFamily("Montserrat Black")
        font.setPointSize(18)
        font.setBold(True)
        font.setWeight(75)
        self.exitbutton.setFont(font)
        self.exitbutton.setStyleSheet("color: rgb(155, 17, 30);")
        self.exitbutton.setObjectName("exitbutton")

        self.resulttable = QtWidgets.QTableView(Virus)
        self.table = QStandardItemModel()
        self.resulttable.setModel(self.table)
        self.resulttable.setGeometry(QtCore.QRect(675, 120, 680, 290))
        # self.resulttable.setStyleSheet("background-color: white;")
        self.resulttable.setObjectName("resulttable")


        self.retranslateUi(Virus)
        QtCore.QMetaObject.connectSlotsByName(Virus)

    def retranslateUi(self, Virus):
        _translate = QtCore.QCoreApplication.translate
        Virus.setWindowTitle(_translate("Virus", "Virus"))
        self.infected.setText(_translate("Virus", "Infected"))
        self.infectedCount.setText(_translate("Virus", "0"))
        self.susceptible.setText(_translate("Virus", "Susceptible"))
        self.susceptibleCount.setText(_translate("Virus", "0"))
        self.deaths.setText(_translate("Virus", "Deaths"))
        self.deathsCount.setText(_translate("Virus", "0"))
        self.vaccine.setText(_translate("Virus", "Vaccinated"))
        self.vaccineCount.setText(_translate("Virus", "0")) 
        self.virustxt.setText(_translate("Virus", "Virus"))
        self.spreadtxt.setText(_translate("Virus", "Spreading"))
        self.whichCity.setText(_translate("Virus", "Choose the City"))
        self.amountPopulation.setText(_translate("Virus", "Population"))
        self.stepbutton.setText(_translate("Virus", "STEP"))
        self.amountVirus.setText(_translate("Virus", "Virus Rate (%)"))
        self.amountVaccine.setText(_translate("Virus", "Vaccine Rate (%)"))
        self.amountRecovery.setText(_translate("Virus", "Recovery Rate (%)"))
        self.amountTransport.setText(_translate("Virus", "Transport Rate (%)"))
        self.savebutton.setText(_translate("Virus", "SAVE"))
        self.amountTime.setText(_translate("Virus", "Duration"))
        self.runbutton.setText(_translate("Virus", "RUN"))
        self.exitbutton.setText(_translate("Virus", "EXIT"))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    myapp = MyForm()
    myapp.show()
    sys.exit(app.exec_())

