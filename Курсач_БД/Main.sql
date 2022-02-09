





CREATE TABLE Aviapark(
	[ID_Авиапарка] [int] PRIMARY KEY IDENTITY(1,1) NOT NULL,
	[Название компании] [nvarchar](50) NOT NULL,
	[Местонахождение] nvarchar(50) not null
) 


CREATE TABLE Рейс(
	ID_Рейса int PRIMARY KEY IDENTITY(1,1) NOT NULL,
	Flight_Number int not null,
	[Откуда вылетает] nvarchar(50) not null,
	[Куда летит] nvarchar(50) not null,
	[Дата вылета] date not null,
	[Дата приземления] date not null,
	[Компания самолета] [nvarchar](50) NOT NULL,
	[ID_Авиапарка] [int] NOT NULL,
	FOREIGN KEY (ID_Авиапарка) REFERENCES dbo.Aviapark(ID_Авиапарка)
)


CREATE TABLE Сопоставление(
	ID_Рейса int  not null,
	ID_Пассажира int not null,
	FOREIGN KEY (ID_Рейса) REFERENCES dbo.Рейс(ID_Рейса),
	FOREIGN KEY (ID_Пассажира) REFERENCES dbo.Пассажир(ID_Пассажира)
	)


CREATE TABLE Пассажир(
	[ID_Пассажира] [int] PRIMARY KEY IDENTITY(1,1) NOT NULL,
	[Имя] [nvarchar](50) NOT NULL,
	[Фамилия] [nvarchar](50) NOT NULL,
	[Отчество] [nvarchar](50) NULL,
	PasportNumber int 
)
 ALTER TABLE Пассажир ADD  Price int 









SELECT Flight_Number AS Номер_рейса, [Имя], [Фамилия], CASE WHEN [Отчество] IS NULL THEN 'Нет отчества' ELSE Отчество END [Отчество], PasportNumber FROM Пассажир JOIN Сопоставление ON Сопоставление.ID_Пассажира = Пассажир.ID_Пассажира JOIN Рейс ON Рейс.ID_Рейса = Сопоставление.ID_Рейса WHERE Flight_Number = 322;


SELECT Рейс.Flight_Number as Номер_рейса, avg(Пассажир.Price) as Средння_Цена FROM Пассажир JOIN Сопоставление ON Пассажир.ID_Пассажира = Сопоставление.ID_Пассажира JOIN Рейс ON Рейс.ID_Рейса = Сопоставление.ID_Рейса GROUP BY Flight_Number HAVING  AVG(Price) > 20000

SELECT  Имя, Фамилия, Отчество, Price FROM Пассажир WHERE ID_Пассажира = ALL(SELECT ID_Пассажира FROM Сопоставление WHERE ID_Рейса = ALL(SELECT ID_Рейса FROM Рейс))

--------------------------/ View /-------------------------

CREATE VIEW Passenger AS SELECT ID_Пассажира, [Имя], [Фамилия], CASE WHEN [Отчество] IS NULL THEN 'Нет отчетсва' ELSE [Отчество] END [Отчетсво], PasportNumber, Price FROM Пассажир 

CREATE VIEW Flight AS SELECT * FROM Рейс





CREATE PROCEDURE insert_Aviapark (@[Название компании] nvarchar , @[Местонахождение] nvarchar)
AS
BEGIN 
INSERT INTO Aviapark([Название компании], [Местонахождение]) VALUES (@[Название компании], @[Местонахождение]) END;






CREATE PROCEDURE Insert_Aviapark (@Name nvarchar(50), @Place [nvarchar](50))
AS
BEGIN 
INSERT INTO Aviapark ([Название компании], [Местонахождение]) VALUES (@Name, @Place) END;

EXEC Insert_Aviapark @Name = 'Россия', @Place = 'Волгоград'


---------------------/ индексы /------------------
create index pass on Пассажир(ID_Пассажира, Фамилия)
create index Flight on Рейс(ID_Рейса, Flight_Number)
create index Avia on Aviapark(ID_Авиапарка)
create index rav on Сопоставление(ID_Рейса, ID_Пассажира)




----------------/ Откат /-------------------
CREATE PROCEDURE Trans(@id int, @Name INT, @Place nvarchar(50))
AS
BEGIN
BEGIN TRANSACTION
INSERT INTO Aviapark([Название компании], [Местонахождение] VALUES (@Name, @Place);
IF @Name = @Place
ROLLBACK
COMMIT TRANSACTION
END


 



 -----------------/ Курсор /------------------
 CREATE PROCEDURE Cur_Update_Aviapark(@update_id INT, @update_name nvarchar(50), @update_place nvarchar (50)) AS
 BEGIN
 declare cur CURSOR
 FOR SELECT ID_Авиапарка FROM Aviapark;
 OPEN cur
 DECLARE @id int;
 FETCH NEXT FROM cur INTO @id;
 WHILE @@FETCH_STATUS = 0
 BEGIN 
 IF @update_id = @id
 UPDATE Aviapark 
 SET [Название компании] = '', Местонахождение = ''
 WHERE ID_Авиапарка = @update_id
 FETCH NEXT FROM cur INTO @id
 END
 CLOSE cur
 DEALLOCATE cur;
 END;



 
 ---------------------/ Процедуры на добавление /-------------------------------------------------------

 CREATE PROCEDURE Select_Flight (@FlightNumber int)
AS
SELECT * FROM Рейс


CREATE PROCEDURE Select_Passenger (@Last_Name nvarchar(50))
AS
SELECT Flight_Number AS Номер_рейса, [Имя], [Фамилия], CASE WHEN [Отчество] IS NULL THEN 'Нет отчества' ELSE Отчество END [Отчество], PasportNumber, Price FROM Пассажир JOIN Сопоставление ON Сопоставление.ID_Пассажира = Пассажир.ID_Пассажира JOIN Рейс ON Рейс.ID_Рейса = Сопоставление.ID_Рейса WHERE Фамилия = @Last_Name;



 CREATE FUNCTION Select_from_Fligt(@FlightNumber int)
 RETURNS
 TABLE
 AS
 RETURN
 SELECT Flight_Number AS Номер_рейса, [Имя], [Фамилия], CASE WHEN [Отчество] IS NULL THEN 'Нет отчества' ELSE Отчество END [Отчество], PasportNumber FROM Пассажир JOIN Сопоставление ON Сопоставление.ID_Пассажира = Пассажир.ID_Пассажира JOIN Рейс ON Рейс.ID_Рейса = Сопоставление.ID_Рейса WHERE Flight_Number = @FlightNumber;


 CREATE PROCEDURE Select_from_Flight(@Last_Name1 nvarchar (50))
 AS
 BEGIN
 EXEC Select_Passenger @Last_Name1
 END


 -----------------/ Процедура на обновление /-----------
 CREATE PROCEDURE Update_Aviapark (@id int, @Name nvarchar(50), @Place nvarchar(50))
AS
BEGIN
UPDATE Aviapark SET [Название компании] = @Name, [Местонахождение] = @Place WHERE ID_Авиапарка = @id
END;


-------------------/ Процедура на удаление /-----------------

CREATE PROCEDURE Delete_Aviapark (@id int)
AS
BEGIN
DELETE FROM Aviapark WHERE ID_Авиапарка = @id END;


 -----------------------/ Триггеры /------------------------

 CREATE TRIGGER delete_passenger ON Пассажир INSTEAD OF DELETE AS
    BEGIN
        DELETE FROM Сопоставление WHERE ID_Пассажира=(
            SELECT ID_Пассажира FROM deleted)
		DELETE FROM Пассажир WHERE ID_Пассажира = (
			SELECT ID_Пассажира FROM deleted)
    END;

CREATE TRIGGER delete_flight ON Рейс INSTEAD OF DELETE AS
    BEGIN
		DELETE FROM Сопоставление WHERE ID_Рейса = (
			SELECT ID_Рейса FROM deleted)
		DELETE FROM Рейс WHERE ID_Рейса = (
			SELECT ID_Рейса FROM deleted)
	END;





---------------------/ Распределение прав /--------------------
CREATE ROLE test;
 GRANT SELECT TO test;
 CREATE LOGIN tester WITH PASSWORD = '12345';
 CREATE USER tester FOR LOGIN tester
 EXEC sp_addrolemember 'test','tester';

 CREATE ROLE root;
 GRANT SELECT, INSERT, DELETE, EXECUTE to root;
 CREATE LOGIN root WITH PASSWORD = 'admin'
 CREATE USER root FOR LOGIN root
 EXEC sp_addrolemember 'root','root';




SELECT ID FROM Taken WHERE Date_return < ANY(SELECT Date_return FROM Taken WHERE Book_ID =
(SELECT ID FROM Book WHERE Book.Name = ‘Название No1’));

SELECT ID_Рейса FROM Рейс WHERE Flight_Number < (SELECT Flight_Number FROM Рейс WHERE  ID_Авиапарка = (SELECT ID_Авиапарка FROM Aviapark WHERE [Местонахождение] = 'Владивосток'))



SELECT * FROM (SELECT ID_Пассажира FROM Пассажир WHERE Price >= 20000) AS Pas JOIN Пассажир ON Pas.ID_Пассажира =
Пассажир.ID_Пассажира;

SELECT * FROM (SELECT Фамилия, Price AS Pr1 FROM Пассажир) AS Pr2 WHERE Pr1 > 15000;


SELECT Av.*, (SELECT Flight_Number FROM Рейс AS R WHERE R.ID_Авиапарка = Av.ID_Авиапарка) AS 'Номер рейса' FROM Aviapark AS
Av;
SELECT R.Flight_Number, (SELECT Count(*) FROM Aviapark WHERE ID_Авиапарка = R.ID_Авиапарка) AS 'Количество' FROM Рейс AS R;


