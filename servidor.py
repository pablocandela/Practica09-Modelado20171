import sys
from PyQt4 import QtGui, QtCore, uic
from random import randint 

class Vivora():
    
    def __init__(self, red, green, blue):
        self.color = (red, green, blue)
        self.casillas = [[3,0],[4,0],[5,0], [6,0],[7,0]] 
        self.direccion = "Abajo" 
        
class Servidor(QtGui.QMainWindow):

    def __init__(self):
        super(Servidor, self).__init__() 
        uic.loadUi('servidor.ui', self) 
        self.terminar.hide() 
        self.iniciar = False 
        self.pausar = False
        self.timer = 0 
        self.vivoras = [] 
        self.agrandar_cuadros() 
        self.llenar_tabla()
        self.tableWidget.setSelectionMode(QtGui.QTableWidget.NoSelection)
        self.spinBox_2.valueChanged.connect(self.actualiza_tabla) 
        self.spinBox_3.valueChanged.connect(self.actualiza_tabla)
        self.spinBox.valueChanged.connect(self.actualizar_timer)
        self.iniciar_pausar.clicked.connect(self.comenzar_juego) 
        self.terminar.clicked.connect(self.terminar_juego)
        self.show() 
    
    def comenzar_juego(self):
        if not self.iniciar:
            self.terminar.show()
            vivora = Vivora(161,191,50)  
            self.vivoras.append(vivora)
            self.iniciar_pausar.setText("Pausar Juego") 
            self.dibujar_vivoras()
            self.timer = QtCore.QTimer(self) 
            self.timer.timeout.connect(self.mover_vivoras)
            self.timer.start(100)
            self.tableWidget.installEventFilter(self) 
            self.iniciar = True 
        elif self.iniciar and self.pausar == False: 
            self.timer.stop() 
            self.pausar = True 
            self.iniciar_pausar.setText("Reanudar el Juego") 
        elif self.pausar: 
            self.timer.start() 
            self.pausar = False 
            self.iniciar_pausar.setText("Pausar Juego") 

    def terminar_juego(self):
        self.vivoras = [] 
        self.timer.stop()
        self.iniciar = False 
        self.terminar.hide()
        self.iniciar_pausar.setText("Iniciar Juego")  
        self.llenar_tabla() 

    def actualizar_timer(self):
        valor = self.spinBox.value()
        self.timer.setInterval(valor)

    def eventFilter(self, source, event):
        if (event.type() == QtCore.QEvent.KeyPress and
            source is self.tableWidget): 
                key = event.key() 
                if (key == QtCore.Qt.Key_Up and source is self.tableWidget):
                    for vivora in self.vivoras:
                        if vivora.direccion is not "Abajo":
                            vivora.direccion = "Arriba"
                elif (key == QtCore.Qt.Key_Down and source is self.tableWidget):
                    for vivora in self.vivoras:
                        if vivora.direccion is not "Arriba": vivora.direccion = "Abajo"
                elif (key == QtCore.Qt.Key_Right and source is self.tableWidget):
                    for vivora in self.vivoras:
                        if vivora.direccion is not "Izquierda": vivora.direccion = "Derecha"
                elif (key == QtCore.Qt.Key_Left and source is self.tableWidget):
                    for vivora in self.vivoras:
                        if vivora.direccion is not "Derecha": vivora.direccion = "Izquierda"
        return QtGui.QMainWindow.eventFilter(self, source, event) 

    def dibujar_vivoras(self):
        for vivora in self.vivoras:
            for parte_vivora in vivora.casillas:
                self.tableWidget.item(parte_vivora[0], parte_vivora[1]).setBackground(QtGui.QColor(vivora.color[0], vivora.color[1], vivora.color[2]))
    
    def se_comio(self, vivora):    
        for parte_de_vivora in vivora.casillas[0:len(vivora.casillas)-2]:           
            if vivora.casillas[-1][0] == parte_de_vivora[0] and vivora.casillas[-1][1] == parte_de_vivora[1]: return True
        return False

    def mover_vivoras(self):
        for vivora in self.vivoras: 
            if self.se_comio(vivora): 
                self.vivoras.remove(vivora) 
                self.llenar_tabla() 
                r,g,b = randint(0,255),randint(0,255),randint(0,255) 
                vivora = Vivora(r,g,b)
                self.vivoras = [vivora]
            self.tableWidget.item(vivora.casillas[0][0],vivora.casillas[0][1]).setBackground(QtGui.QColor(82,130,135))
            x = 0 
            for tupla in vivora.casillas[0: len(vivora.casillas)-1]:
                x += 1
                tupla[0] = vivora.casillas[x][0]
                tupla[1] = vivora.casillas[x][1]
            if vivora.direccion == "Abajo":
                if vivora.casillas[-1][0] + 1 - self.tableWidget.rowCount() < 0: vivora.casillas[-1][0] += 1
                else:
                    vivora.casillas[-1][0] = 0
            if vivora.direccion == "Derecha":
                if vivora.casillas[-1][1] + 1 - self.tableWidget.columnCount() < 0: vivora.casillas[-1][1] += 1
                else:
                    vivora.casillas[-1][1] = 0
            if vivora.direccion == "Arriba":
                if vivora.casillas[-1][0] != 0: vivora.casillas[-1][0] -= 1
                else:
                    vivora.casillas[-1][0] = self.tableWidget.rowCount()-1
            if vivora.direccion == "Izquierda":
                if vivora.casillas[-1][1] != 0: vivora.casillas[-1][1] -= 1
                else:
                    vivora.casillas[-1][1] = self.tableWidget.columnCount()-1
        self.dibujar_vivoras() 

    def llenar_tabla(self):
        for i in range(self.tableWidget.rowCount()):
            for j in range(self.tableWidget.columnCount()):
                self.tableWidget.setItem(i,j, QtGui.QTableWidgetItem())
                self.tableWidget.item(i,j).setBackground(QtGui.QColor(80,134,134))

    def agrandar_cuadros(self):
        self.tableWidget.horizontalHeader().setResizeMode(QtGui.QHeaderView.Stretch)
        self.tableWidget.verticalHeader().setResizeMode(QtGui.QHeaderView.Stretch)

    def actualiza_tabla(self):
        filas = self.spinBox_2.value()
        columnas = self.spinBox_3.value()
        self.tableWidget.setRowCount(filas) 
        self.tableWidget.setColumnCount(columnas)
        self.llenar_tabla()


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv) 
    ventana = Servidor() 
    sys.exit(app.exec_()) 
