
from PyQt5 import QtCore
from PyQt5.QtWidgets import *
import sys
from Main import Ui_Form
import pyodbc
from admin import Ui_Administration

class Administration(QMainWindow, Ui_Administration):


    def __init__(self):
        super(Administration, self).__init__()
        self.setupUi(self)
        self.Connect.clicked.connect(self.login)

    def login(self):
        login = str(self.lineEdit.text())
        password = str(self.lineEdit_2.text())
        try:
            parameters = "DRIVER=ODBC Driver 17 for SQL Server;\
                            Server=DESKTOP-8NRUDO3;\
                            Database=Kursach;\
                            UID={};\
                            PWD={};\
                            Trusted_connection=no;".format(login, password)
            connection = pyodbc.connect(parameters)
            cursor = connection.cursor()
            self.window = Ui(cursor, login, password)
            self.window.show()
            self.close()
        except:
            QMessageBox(QMessageBox.Critical, "Ошибка", "Неправильный логин или пароль").exec()









class Ui(QMainWindow, Ui_Form):

    editItems = False
    currentValue = 0
    cursor = 0
    def __init__(self, cursor, login, password):
        super(Ui, self).__init__()
        self.cursor = cursor
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        if (login != 'root' and password != 'admin'):
            self.ui.Add.setDisabled(True)
            self.ui.Del.setDisabled(True)
            self.ui.Change.setDisabled(True)
        self.errorbox = QMessageBox()
        self.errorbox.setWindowTitle("Critical error")
        self.errorbox.setText("Данные не были введены!")
        self.errorbox.setIcon(QMessageBox.Critical)
        self.complete = QMessageBox()
        self.complete.setWindowTitle("Information")
        self.complete.setText("Данные успешно введены!")
        self.complete.setIcon(QMessageBox.Information)
        self.ui.AddAviapark.clicked.connect(self.get_Aviapark)
        self.ui.AddFlight.clicked.connect(self.get_Flight)
        self.ui.Add_Passenger_Button.clicked.connect(self.Add_Passenger)
        self.ui.Add_Passenger_on_board_Button.clicked.connect(self.Passenger_on_board)
        self.ui.Show_Aviapark_Button.clicked.connect(self.set_Aviapark)
        self.ui.Show_Passenger_Button.clicked.connect(self.set_Passenger)
        self.ui.Show_Flight_Button.clicked.connect(self.set_Flight)
        self.ui.Show_Passenger_Board_Button.clicked.connect(self.set_Passenger_on_Board)
        self.ui.Show_Del_Passenger.clicked.connect(self.Show_to_Delete_Passenger)
        self.ui.Delete_Passenger_Button.clicked.connect(self.Delete_Passenger)
        self.ui.Show_Del_Flight.clicked.connect(self.Show_to_Delete_Flight)
        self.ui.Delete_Flight_Button.clicked.connect(self.Delete_Flight)
        self.ui.Switch_Button.clicked.connect(self.Print_Table)
        self.ui.Change_Table.itemDoubleClicked.connect(self.Changed)


    # /-------------------------------------------------------------------------------------------------/
    def get_Aviapark(self): #Добавление данных
        column_conteiner=[]
        try:
            for x in range(0, self.ui.AviaparkAdd.rowCount()):
                (column_conteiner.append(self.ui.AviaparkAdd.item(x,0).text()))

            self.cursor.execute("INSERT INTO Aviapark ([Название компании], [Местонахождение]) VALUES (?,?);", (column_conteiner[0], column_conteiner[1]))
            self.complete.exec()
            self.ui.AviaparkAdd.setItem(1, 0, QTableWidgetItem(""))
            self.ui.AviaparkAdd.setItem(0, 0, QTableWidgetItem(""))
            self.cursor.commit()
        except:
            self.errorbox.exec()

 #/-------------------------------------------------------------------------------------------------/
    def get_Flight(self): #Добавление данных
        column_conteiner = []
        try:
            for x in range(0,self.ui.FlightAdd.rowCount()):
                column_conteiner.append(self.ui.FlightAdd.item(x,0).text())
            self.cursor.execute(
                    "INSERT INTO Рейс (Flight_Number, [Откуда вылетает], [Куда летит], [Дата вылета], [Дата приземления], [Компания самолета], [ID_Авиапарка]) VALUES (?, ?, ?, ?, ?, ?, ?);",
                    (column_conteiner[0], column_conteiner[1], column_conteiner[2], column_conteiner[3],
                     column_conteiner[4], column_conteiner[5], column_conteiner[6]))
            self.complete.exec()
            for i in range (self.ui.FlightAdd.rowCount()):
                self.ui.FlightAdd.setItem(i, 0, QTableWidgetItem(""))
            self.cursor.commit()

        except:
            self.errorbox.exec()

    # /-------------------------------------------------------------------------------------------------/
    def Add_Passenger(self):
        column_conteiner = []

        try:
            for x in range(0, self.ui.AddPassenger.rowCount()):
                column_conteiner.append(self.ui.AddPassenger.item(x, 0).text())
            self.cursor.execute("INSERT INTO Пассажир ([Имя], [Фамилия], [Отчество], PasportNumber, Price) VALUES (?, ?, ?, ?, ?);",(column_conteiner[0], column_conteiner[1], column_conteiner[2], column_conteiner[3], column_conteiner[4]))
            self.complete.exec()
            for i in range (self.ui.AddPassenger.rowCount()):
                self.ui.AddPassenger.setItem(i, 0, QTableWidgetItem(""))
            self.cursor.commit()
        except:
            self.errorbox.exec()


    def Passenger_on_board(self):
        try:

            self.cursor.execute("INSERT INTO Сопоставление (ID_Рейса, ID_Пассажира) VALUES (?,?)",(self.ui.Add_on_Flight.item(0, 0).text(), self.ui.Add_on_Flight.item(1, 0).text()))
            self.complete.exec()
            for i in range(self.ui.Add_on_Flight.rowCount()):
                self.ui.Add_on_Flight.setItem(i, 0, QTableWidgetItem(""))
            self.cursor.commit()
        except:
            self.errorbox.exec()

    def set_Aviapark(self):
        self.ui.Show_Aviapark.setRowCount(len(self.cursor.execute("SELECT [Название компании], [Местонахождение] FROM Aviapark").fetchall()))
        for i in range (len(self.cursor.execute("SELECT [Название компании], [Местонахождение] FROM Aviapark").fetchall())):
            self.ui.Show_Aviapark.setItem(i, 0, QTableWidgetItem(str(self.cursor.execute("SELECT [Название компании], [Местонахождение] FROM Aviapark").fetchall()[i][0])))
            self.ui.Show_Aviapark.setItem(i, 1, QTableWidgetItem(self.cursor.execute("SELECT [Название компании], [Местонахождение] FROM Aviapark").fetchall()[i][1]))



    def set_Passenger(self):
        LastName_Passenger = str(self.ui.get_ID_Passenger.text())
        self.ui.Show_Passenger.setColumnCount(len(self.cursor.execute("SELECT Flight_Number AS Номер_рейса, [Имя], [Фамилия], CASE WHEN [Отчество] IS NULL THEN 'Нет отчества' ELSE Отчество END [Отчество], PasportNumber, Price FROM Пассажир JOIN Сопоставление ON Сопоставление.ID_Пассажира = Пассажир.ID_Пассажира JOIN Рейс ON Рейс.ID_Рейса = Сопоставление.ID_Рейса WHERE [Фамилия] = (?);", (LastName_Passenger)).fetchall()))
        for i in range(len(self.cursor.execute("SELECT Flight_Number AS Номер_рейса, [Имя], [Фамилия], CASE WHEN [Отчество] IS NULL THEN 'Нет фамилии' ELSE Отчество END [Отчество], PasportNumber, Price FROM Пассажир JOIN Сопоставление ON Сопоставление.ID_Пассажира = Пассажир.ID_Пассажира JOIN Рейс ON Рейс.ID_Рейса = Сопоставление.ID_Рейса WHERE [Фамилия] = (?)", (LastName_Passenger)).fetchall())):
            self.ui.Show_Passenger.setItem(0, i, QTableWidgetItem(str(self.cursor.execute("SELECT Flight_Number AS Номер_рейса, [Имя], [Фамилия], CASE WHEN [Отчество] IS NULL THEN 'Нет фамилии' ELSE Отчество END [Отчество], PasportNumber, Price FROM Пассажир JOIN Сопоставление ON Сопоставление.ID_Пассажира = Пассажир.ID_Пассажира JOIN Рейс ON Рейс.ID_Рейса = Сопоставление.ID_Рейса WHERE [Фамилия] = (?);", (LastName_Passenger)).fetchall()[i][0])))
            self.ui.Show_Passenger.setItem(1, i, QTableWidgetItem(self.cursor.execute("SELECT Flight_Number AS Номер_рейса, [Имя], [Фамилия], CASE WHEN [Отчество] IS NULL THEN 'Нет фамилии' ELSE Отчество END [Отчество], PasportNumber, Price FROM Пассажир JOIN Сопоставление ON Сопоставление.ID_Пассажира = Пассажир.ID_Пассажира JOIN Рейс ON Рейс.ID_Рейса = Сопоставление.ID_Рейса WHERE [Фамилия] = (?);", (LastName_Passenger)).fetchall()[i][1]))
            self.ui.Show_Passenger.setItem(2, i, QTableWidgetItem(self.cursor.execute("SELECT Flight_Number AS Номер_рейса, [Имя], [Фамилия], CASE WHEN [Отчество] IS NULL THEN 'Нет фамилии' ELSE Отчество END [Отчество], PasportNumber, Price FROM Пассажир JOIN Сопоставление ON Сопоставление.ID_Пассажира = Пассажир.ID_Пассажира JOIN Рейс ON Рейс.ID_Рейса = Сопоставление.ID_Рейса WHERE [Фамилия] = (?);", (LastName_Passenger)).fetchall()[i][2]))
            self.ui.Show_Passenger.setItem(3, i, QTableWidgetItem(self.cursor.execute("SELECT Flight_Number AS Номер_рейса, [Имя], [Фамилия], CASE WHEN [Отчество] IS NULL THEN 'Нет фамилии' ELSE Отчество END [Отчество], PasportNumber, Price FROM Пассажир JOIN Сопоставление ON Сопоставление.ID_Пассажира = Пассажир.ID_Пассажира JOIN Рейс ON Рейс.ID_Рейса = Сопоставление.ID_Рейса WHERE [Фамилия] = (?);", (LastName_Passenger)).fetchall()[i][3]))
            self.ui.Show_Passenger.setItem(4, i, QTableWidgetItem(str(self.cursor.execute("SELECT Flight_Number AS Номер_рейса, [Имя], [Фамилия], CASE WHEN [Отчество] IS NULL THEN 'Нет фамилии' ELSE Отчество END [Отчество], PasportNumber, Price FROM Пассажир JOIN Сопоставление ON Сопоставление.ID_Пассажира = Пассажир.ID_Пассажира JOIN Рейс ON Рейс.ID_Рейса = Сопоставление.ID_Рейса WHERE [Фамилия] = (?);", (LastName_Passenger)).fetchall()[i][4])))
            self.ui.Show_Passenger.setItem(5, i, QTableWidgetItem(str(self.cursor.execute("SELECT Flight_Number AS Номер_рейса, [Имя], [Фамилия], CASE WHEN [Отчество] IS NULL THEN 'Нет фамилии' ELSE Отчество END [Отчество], PasportNumber, Price FROM Пассажир JOIN Сопоставление ON Сопоставление.ID_Пассажира = Пассажир.ID_Пассажира JOIN Рейс ON Рейс.ID_Рейса = Сопоставление.ID_Рейса WHERE [Фамилия] = (?);", (LastName_Passenger)).fetchall()[i][5])))

    def set_Flight(self):
        Flight_Number = int(self.ui.get_ID_Flight.text())
        Flight = self.cursor.execute("SELECT * FROM [Рейс] WHERE Flight_Number = (?);", (Flight_Number)).fetchall()
        self.ui.Show_Flight.setItem(0, 0, QTableWidgetItem(str(Flight[0][2])))
        self.ui.Show_Flight.setItem(1, 0, QTableWidgetItem(str(Flight[0][3])))
        self.ui.Show_Flight.setItem(2, 0, QTableWidgetItem(str(Flight[0][4])))
        self.ui.Show_Flight.setItem(3, 0, QTableWidgetItem(str(Flight[0][5])))
        self.ui.Show_Flight.setItem(4, 0, QTableWidgetItem(str(Flight[0][6])))
        self.ui.Show_Flight.setItem(5, 0, QTableWidgetItem(str(Flight[0][7])))


    def set_Passenger_on_Board(self):
        set_Passanger = str(self.ui.Show_Passenger_Edit.text())
        self.ui.Show_Passenger_Board.setColumnCount(len(self.cursor.execute("SELECT Flight_Number AS Номер_рейса, [Имя], [Фамилия], CASE WHEN [Отчество] IS NULL THEN 'Нет отчества' ELSE Отчество END [Отчество], PasportNumber, Price FROM Пассажир JOIN Сопоставление ON Сопоставление.ID_Пассажира = Пассажир.ID_Пассажира JOIN Рейс ON Рейс.ID_Рейса = Сопоставление.ID_Рейса WHERE Flight_Number = (?);", (set_Passanger)).fetchall()))
        for i in range (len(self.cursor.execute("SELECT Flight_Number AS Номер_рейса, [Имя], [Фамилия], CASE WHEN [Отчество] IS NULL THEN 'Нет отчества' ELSE Отчество END [Отчество], PasportNumber, Price FROM Пассажир JOIN Сопоставление ON Сопоставление.ID_Пассажира = Пассажир.ID_Пассажира JOIN Рейс ON Рейс.ID_Рейса = Сопоставление.ID_Рейса WHERE Flight_Number = (?)", (set_Passanger)).fetchall())):
            self.ui.Show_Passenger_Board.setItem(0, i, QTableWidgetItem(str(self.cursor.execute("SELECT Flight_Number AS Номер_рейса, [Имя], [Фамилия], CASE WHEN [Отчество] IS NULL THEN 'Нет отчества' ELSE Отчество END [Отчество], PasportNumber, Price FROM Пассажир JOIN Сопоставление ON Сопоставление.ID_Пассажира = Пассажир.ID_Пассажира JOIN Рейс ON Рейс.ID_Рейса = Сопоставление.ID_Рейса WHERE Flight_Number = (?)", (set_Passanger)).fetchall()[i][0])))
            self.ui.Show_Passenger_Board.setItem(1, i, QTableWidgetItem(str(self.cursor.execute("SELECT Flight_Number AS Номер_рейса, [Имя], [Фамилия], CASE WHEN [Отчество] IS NULL THEN 'Нет отчества' ELSE Отчество END [Отчество], PasportNumber, Price FROM Пассажир JOIN Сопоставление ON Сопоставление.ID_Пассажира = Пассажир.ID_Пассажира JOIN Рейс ON Рейс.ID_Рейса = Сопоставление.ID_Рейса WHERE Flight_Number = (?)", (set_Passanger)).fetchall()[i][1])))
            self.ui.Show_Passenger_Board.setItem(2, i, QTableWidgetItem(str(self.cursor.execute("SELECT Flight_Number AS Номер_рейса, [Имя], [Фамилия], CASE WHEN [Отчество] IS NULL THEN 'Нет отчества' ELSE Отчество END [Отчество], PasportNumber, Price FROM Пассажир JOIN Сопоставление ON Сопоставление.ID_Пассажира = Пассажир.ID_Пассажира JOIN Рейс ON Рейс.ID_Рейса = Сопоставление.ID_Рейса WHERE Flight_Number = (?)", (set_Passanger)).fetchall()[i][2])))
            self.ui.Show_Passenger_Board.setItem(3, i, QTableWidgetItem(str(self.cursor.execute("SELECT Flight_Number AS Номер_рейса, [Имя], [Фамилия], CASE WHEN [Отчество] IS NULL THEN 'Нет отчества' ELSE Отчество END [Отчество], PasportNumber, Price FROM Пассажир JOIN Сопоставление ON Сопоставление.ID_Пассажира = Пассажир.ID_Пассажира JOIN Рейс ON Рейс.ID_Рейса = Сопоставление.ID_Рейса WHERE Flight_Number = (?);", (set_Passanger)).fetchall()[i][3])))
            self.ui.Show_Passenger_Board.setItem(4, i, QTableWidgetItem(str(self.cursor.execute("SELECT Flight_Number AS Номер_рейса, [Имя], [Фамилия], CASE WHEN [Отчество] IS NULL THEN 'Нет отчества' ELSE Отчество END [Отчество], PasportNumber, Price FROM Пассажир JOIN Сопоставление ON Сопоставление.ID_Пассажира = Пассажир.ID_Пассажира JOIN Рейс ON Рейс.ID_Рейса = Сопоставление.ID_Рейса WHERE Flight_Number = (?);", (set_Passanger)).fetchall()[i][4])))
            self.ui.Show_Passenger_Board.setItem(5, i, QTableWidgetItem(str(self.cursor.execute("SELECT Flight_Number AS Номер_рейса, [Имя], [Фамилия], CASE WHEN [Отчество] IS NULL THEN 'Нет отчества' ELSE Отчество END [Отчество], PasportNumber, Price FROM Пассажир JOIN Сопоставление ON Сопоставление.ID_Пассажира = Пассажир.ID_Пассажира JOIN Рейс ON Рейс.ID_Рейса = Сопоставление.ID_Рейса WHERE Flight_Number = (?);" ,(set_Passanger)).fetchall()[i][5])))

    def Show_to_Delete_Passenger(self):
        self.ui.Delete_Passenger.setColumnCount(len(self.cursor.execute("SELECT * FROM Passenger ORDER BY Price").fetchall()))
        for i in range (len(self.cursor.execute("SELECT * FROM Passenger ORDER BY Price").fetchall())):
            self.ui.Delete_Passenger.setItem(0, i, QTableWidgetItem(str(self.cursor.execute("SELECT * FROM Passenger ORDER BY Price").fetchall()[i][0])))
            self.ui.Delete_Passenger.setItem(1, i, QTableWidgetItem(str(self.cursor.execute("SELECT * FROM Passenger ORDER BY Price").fetchall()[i][1])))
            self.ui.Delete_Passenger.setItem(2, i, QTableWidgetItem(str(self.cursor.execute("SELECT * FROM Passenger ORDER BY Price").fetchall()[i][2])))
            self.ui.Delete_Passenger.setItem(3, i, QTableWidgetItem(str(self.cursor.execute("SELECT * FROM Passenger ORDER BY Price").fetchall()[i][3])))
            self.ui.Delete_Passenger.setItem(4, i, QTableWidgetItem(str(self.cursor.execute("SELECT * FROM Passenger ORDER BY Price").fetchall()[i][4])))
            self.ui.Delete_Passenger.setItem(5, i, QTableWidgetItem(str(self.cursor.execute("SELECT * FROM Passenger ORDER BY Price").fetchall()[i][5])))
        for i in range (5):
            for j in range (len(self.cursor.execute("SELECT * FROM Passenger ORDER BY Price").fetchall())):
                self.ui.Delete_Passenger.item(i, j).setFlags(QtCore.Qt.ItemIsEnabled)

    def Delete_Passenger(self):
        Del_Passenger = self.ui.Delete_ID_Passenger.text()
        self.cursor.execute("DELETE FROM Пассажир WHERE [ID_Пассажира] = (?);", (Del_Passenger))
        self.cursor.commit()

    def Show_to_Delete_Flight(self):
        self.ui.Delete_Flight.setColumnCount(len(self.cursor.execute("SELECT * FROM Рейс").fetchall()))
        for i in range(len(self.cursor.execute("SELECT * FROM Рейс").fetchall())):
            self.ui.Delete_Flight.setItem(0, i, QTableWidgetItem(str(self.cursor.execute("SELECT * FROM Рейс").fetchall()[i][0])))
            self.ui.Delete_Flight.setItem(1, i, QTableWidgetItem(str(self.cursor.execute("SELECT * FROM Рейс").fetchall()[i][1])))
            self.ui.Delete_Flight.setItem(2, i, QTableWidgetItem(str(self.cursor.execute("SELECT * FROM Рейс").fetchall()[i][2])))
            self.ui.Delete_Flight.setItem(3, i, QTableWidgetItem(str(self.cursor.execute("SELECT * FROM Рейс").fetchall()[i][3])))
            self.ui.Delete_Flight.setItem(4, i, QTableWidgetItem(str(self.cursor.execute("SELECT * FROM Рейс").fetchall()[i][4])))
            self.ui.Delete_Flight.setItem(5, i, QTableWidgetItem(str(self.cursor.execute("SELECT * FROM Рейс").fetchall()[i][5])))
            self.ui.Delete_Flight.setItem(6, i, QTableWidgetItem(str(self.cursor.execute("SELECT * FROM Рейс").fetchall()[i][6])))
            self.ui.Delete_Flight.setItem(7, i, QTableWidgetItem(str(self.cursor.execute("SELECT * FROM Рейс").fetchall()[i][7])))

    def Delete_Flight(self):
        ID_Flight = self.ui.Delete_ID_Flight.text()
        self.cursor.execute("DELETE FROM Рейс WHERE ID_Рейса = (?);", (ID_Flight))
        self.cursor.commit()

    def Print_Table(self):
        Show_table = int(self.ui.Switch_Edit.text())
        if (Show_table == 1):
            self.ui.Change_Table.setRowCount(2)
            self.ui.Change_Table.setColumnCount(len(self.cursor.execute("SELECT [Название компании], [Местонахождение] FROM Aviapark").fetchall()))
            for i in range (len(self.cursor.execute("SELECT [Название компании], [Местонахождение] FROM Aviapark;").fetchall())):
                self.ui.Change_Table.setItem(i, 0, QTableWidgetItem(self.cursor.execute("SELECT [Название компании], [Местонахождение] FROM Aviapark;").fetchall()[i][0]))
                self.ui.Change_Table.setItem(i, 1, QTableWidgetItem(self.cursor.execute("SELECT [Название компании], [Местонахождение] FROM Aviapark;").fetchall()[i][1]))
        elif (Show_table == 2):
            self.ui.Change_Table.setRowCount(7)
            self.ui.Change_Table.setColumnCount(len(self.cursor.execute("SELECT Flight_Number, [Откуда вылетает], [Куда летит], [Дата вылета], [Дата приземления], [Компания самолета], [ID_Авиапарка] FROM Рейс").fetchall()))
            for i in range (len(self.cursor.execute("SELECT Flight_Number, [Откуда вылетает], [Куда летит], [Дата вылета], [Дата приземления], [Компания самолета], [ID_Авиапарка] FROM Рейс").fetchall())):
                self.ui.Change_Table.setItem(0, i, QTableWidgetItem(str(self.cursor.execute("SELECT Flight_Number, [Откуда вылетает], [Куда летит], [Дата вылета], [Дата приземления], [Компания самолета], [ID_Авиапарка] FROM Рейс").fetchall()[i][0])))
                self.ui.Change_Table.setItem(1, i, QTableWidgetItem(self.cursor.execute("SELECT Flight_Number, [Откуда вылетает], [Куда летит], [Дата вылета], [Дата приземления], [Компания самолета], [ID_Авиапарка] FROM Рейс").fetchall()[i][1]))
                self.ui.Change_Table.setItem(2, i, QTableWidgetItem(self.cursor.execute("SELECT Flight_Number, [Откуда вылетает], [Куда летит], [Дата вылета], [Дата приземления], [Компания самолета], [ID_Авиапарка] FROM Рейс").fetchall()[i][2]))
                self.ui.Change_Table.setItem(3, i, QTableWidgetItem(str(self.cursor.execute("SELECT Flight_Number, [Откуда вылетает], [Куда летит], [Дата вылета], [Дата приземления], [Компания самолета], [ID_Авиапарка] FROM Рейс").fetchall()[i][3])))
                self.ui.Change_Table.setItem(4, i, QTableWidgetItem(str(self.cursor.execute("SELECT Flight_Number, [Откуда вылетает], [Куда летит], [Дата вылета], [Дата приземления], [Компания самолета], [ID_Авиапарка] FROM Рейс").fetchall()[i][4])))
                self.ui.Change_Table.setItem(5, i, QTableWidgetItem(str(self.cursor.execute("SELECT Flight_Number, [Откуда вылетает], [Куда летит], [Дата вылета], [Дата приземления], [Компания самолета], [ID_Авиапарка] FROM Рейс").fetchall()[i][5])))
                self.ui.Change_Table.setItem(6, i, QTableWidgetItem(str(self.cursor.execute("SELECT Flight_Number, [Откуда вылетает], [Куда летит], [Дата вылета], [Дата приземления], [Компания самолета], [ID_Авиапарка] FROM Рейс").fetchall()[i][6])))
        elif (Show_table == 3):
            self.ui.Change_Table.setRowCount(5)
            self.ui.Change_Table.setColumnCount(len(self.cursor.execute("SELECT * FROM Passenger").fetchall()))
            for i in range (len(self.cursor.execute("SELECT * FROM Passenger").fetchall())):
                self.ui.Change_Table.setItem(0, i, QTableWidgetItem(self.cursor.execute("SELECT * FROM Passenger;").fetchall()[i][1]))
                self.ui.Change_Table.setItem(1, i, QTableWidgetItem(self.cursor.execute("SELECT * FROM Passenger;").fetchall()[i][2]))
                self.ui.Change_Table.setItem(2, i, QTableWidgetItem(self.cursor.execute("SELECT * FROM Passenger;").fetchall()[i][3]))
                self.ui.Change_Table.setItem(3, i, QTableWidgetItem(str(self.cursor.execute("SELECT * FROM Passenger;").fetchall()[i][4])))
                self.ui.Change_Table.setItem(4, i, QTableWidgetItem(str(self.cursor.execute("SELECT * FROM Passenger;").fetchall()[i][5])))
        if (Show_table != 1 and Show_table != 2 and Show_table != 3 ):
            QMessageBox(QMessageBox.Critical, "Ошибка", 'Такой таблицы не существует').exec()

    def Changed(self):
        self.currentValue = self.ui.Change_Table.currentItem().text()
        if not self.editItems:
            self.ui.Change_Table.itemChanged.connect(self.Changed1)
            self.editItems = True

    def Changed1(self, item):
        Show_table = int(self.ui.Switch_Edit.text())
        value = item.text()
        count_column = item.column()
        count_row = item.row()
        mass_Id = []
        if Show_table == 1:
            mass_Id = self.cursor.execute("SELECT * FROM Aviapark").fetchall()
            if (count_column == 0):
                self.cursor.execute("UPDATE Aviapark SET [Название компании] = (?) WHERE [ID_Авиапарка] = (?);", (value, mass_Id[count_row][0]))
            elif (count_column == 1):
                self.cursor.execute("UPDATE Aviapark SET [Местонахождение] = (?) WHERE [ID_Авиапарка] = (?);", (value, mass_Id[count_row][0]))
            self.cursor.commit()
        elif Show_table == 2:
            mass_Id = self.cursor.execute("SELECT ID_Рейса FROM Рейс").fetchall()
            if count_row == 0:
                self.cursor.execute("UPDATE Рейс SET Flight_Number = (?) WHERE [ID_Рейса] = (?);", (value, mass_Id[count_column][0]))
            elif count_row == 1:
                self.cursor.execute("UPDATE Рейс SET [Откуда вылетает] = (?) WHERE [ID_Рейса] = (?);", (value, mass_Id[count_column][0]))
            elif count_row == 2:
                self.cursor.execute("UPDATE Рейс SET [Куда летит] = (?) WHERE [ID_Рейса] = (?);", (value, mass_Id[count_column][0]))
            elif count_row == 3:
                self.cursor.execute("UPDATE Рейс SET [Дата вылета] = (?) WHERE [ID_Рейса] = (?);", (str(value), mass_Id[count_column][0]))
            elif count_row == 4:
                self.cursor.execute("UPDATE Рейс SET [Дата приземления] = (?) WHERE [ID_РЕйса] = (?);", (str(value), mass_Id[count_column][0]))
            elif count_row == 5:
                self.cursor.execute("UPDATE Рейса SET [Компания самолета] = (?) WHERE [ID_Рейса] = (?);", (str(value), mass_Id[count_column][0]))
            elif count_row == 6:
                self.cursor.execute("UPDATE Рейса SET [ID_Авиапарка] = (?) WHERE [ID_Рейса] = (?);", (int(value), mass_Id[count_column][0]))
            self.cursor.commit()
        elif Show_table == 3:
            mass_Id = self.cursor.execute("SELECT [ID_Пассажира] FROM Пассажир").fetchall()
            if count_row == 0:
                self.cursor.execute("UPDATE Пассажир SET [Имя] = (?) WHERE [ID_Пассажира] = (?);", (value, mass_Id[count_column][0]))
            elif count_row == 1:
                self.cursor.execute("UPDATE Пассажир SET [Фамилия] = (?) WHERE [ID_Пассажира] = (?);", (value, mass_Id[count_column][0]))
            elif count_row == 2:
                self.cursor.execute("UPDATE Пассажир SET [Отчество] = (?) WHERE [ID_Пассажира] = (?);", (value, mass_Id[count_column][0]))
            elif count_row == 3:
                self.cursor.execute("UPDATE Пассажир SET PasportNumber = (?) WHERE [ID_Пассажира] = (?);", (value, mass_Id[count_column][0]))
            elif count_row == 4:
                self.cursor.execute("UPDATE Пассажир SET Price = (?) WHERE [ID_Пассажира] = (?);", value, mass_Id[count_column][0])
            self.cursor.commit()

        self.ui.Change_Table.itemChanged.disconnect(self.Changed1)
        self.editItems = False
        self.cursor.commit()

def main():
    app = QApplication(sys.argv)
    application1 = Administration()
    application1.show()
    app.exec_()

if __name__ == '__main__':
    main()
