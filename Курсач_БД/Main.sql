





CREATE TABLE Aviapark(
	[ID_���������] [int] PRIMARY KEY IDENTITY(1,1) NOT NULL,
	[�������� ��������] [nvarchar](50) NOT NULL,
	[���������������] nvarchar(50) not null
) 


CREATE TABLE ����(
	ID_����� int PRIMARY KEY IDENTITY(1,1) NOT NULL,
	Flight_Number int not null,
	[������ ��������] nvarchar(50) not null,
	[���� �����] nvarchar(50) not null,
	[���� ������] date not null,
	[���� �����������] date not null,
	[�������� ��������] [nvarchar](50) NOT NULL,
	[ID_���������] [int] NOT NULL,
	FOREIGN KEY (ID_���������) REFERENCES dbo.Aviapark(ID_���������)
)


CREATE TABLE �������������(
	ID_����� int  not null,
	ID_��������� int not null,
	FOREIGN KEY (ID_�����) REFERENCES dbo.����(ID_�����),
	FOREIGN KEY (ID_���������) REFERENCES dbo.��������(ID_���������)
	)


CREATE TABLE ��������(
	[ID_���������] [int] PRIMARY KEY IDENTITY(1,1) NOT NULL,
	[���] [nvarchar](50) NOT NULL,
	[�������] [nvarchar](50) NOT NULL,
	[��������] [nvarchar](50) NULL,
	PasportNumber int 
)
 ALTER TABLE �������� ADD  Price int 









SELECT Flight_Number AS �����_�����, [���], [�������], CASE WHEN [��������] IS NULL THEN '��� ��������' ELSE �������� END [��������], PasportNumber FROM �������� JOIN ������������� ON �������������.ID_��������� = ��������.ID_��������� JOIN ���� ON ����.ID_����� = �������������.ID_����� WHERE Flight_Number = 322;


SELECT ����.Flight_Number as �����_�����, avg(��������.Price) as �������_���� FROM �������� JOIN ������������� ON ��������.ID_��������� = �������������.ID_��������� JOIN ���� ON ����.ID_����� = �������������.ID_����� GROUP BY Flight_Number HAVING  AVG(Price) > 20000

SELECT  ���, �������, ��������, Price FROM �������� WHERE ID_��������� = ALL(SELECT ID_��������� FROM ������������� WHERE ID_����� = ALL(SELECT ID_����� FROM ����))

--------------------------/ View /-------------------------

CREATE VIEW Passenger AS SELECT ID_���������, [���], [�������], CASE WHEN [��������] IS NULL THEN '��� ��������' ELSE [��������] END [��������], PasportNumber, Price FROM �������� 

CREATE VIEW Flight AS SELECT * FROM ����





CREATE PROCEDURE insert_Aviapark (@[�������� ��������] nvarchar , @[���������������] nvarchar)
AS
BEGIN 
INSERT INTO Aviapark([�������� ��������], [���������������]) VALUES (@[�������� ��������], @[���������������]) END;






CREATE PROCEDURE Insert_Aviapark (@Name nvarchar(50), @Place [nvarchar](50))
AS
BEGIN 
INSERT INTO Aviapark ([�������� ��������], [���������������]) VALUES (@Name, @Place) END;

EXEC Insert_Aviapark @Name = '������', @Place = '���������'


---------------------/ ������� /------------------
create index pass on ��������(ID_���������, �������)
create index Flight on ����(ID_�����, Flight_Number)
create index Avia on Aviapark(ID_���������)
create index rav on �������������(ID_�����, ID_���������)




----------------/ ����� /-------------------
CREATE PROCEDURE Trans(@id int, @Name INT, @Place nvarchar(50))
AS
BEGIN
BEGIN TRANSACTION
INSERT INTO Aviapark([�������� ��������], [���������������] VALUES (@Name, @Place);
IF @Name = @Place
ROLLBACK
COMMIT TRANSACTION
END


 



 -----------------/ ������ /------------------
 CREATE PROCEDURE Cur_Update_Aviapark(@update_id INT, @update_name nvarchar(50), @update_place nvarchar (50)) AS
 BEGIN
 declare cur CURSOR
 FOR SELECT ID_��������� FROM Aviapark;
 OPEN cur
 DECLARE @id int;
 FETCH NEXT FROM cur INTO @id;
 WHILE @@FETCH_STATUS = 0
 BEGIN 
 IF @update_id = @id
 UPDATE Aviapark 
 SET [�������� ��������] = '', ��������������� = ''
 WHERE ID_��������� = @update_id
 FETCH NEXT FROM cur INTO @id
 END
 CLOSE cur
 DEALLOCATE cur;
 END;



 
 ---------------------/ ��������� �� ���������� /-------------------------------------------------------

 CREATE PROCEDURE Select_Flight (@FlightNumber int)
AS
SELECT * FROM ����


CREATE PROCEDURE Select_Passenger (@Last_Name nvarchar(50))
AS
SELECT Flight_Number AS �����_�����, [���], [�������], CASE WHEN [��������] IS NULL THEN '��� ��������' ELSE �������� END [��������], PasportNumber, Price FROM �������� JOIN ������������� ON �������������.ID_��������� = ��������.ID_��������� JOIN ���� ON ����.ID_����� = �������������.ID_����� WHERE ������� = @Last_Name;



 CREATE FUNCTION Select_from_Fligt(@FlightNumber int)
 RETURNS
 TABLE
 AS
 RETURN
 SELECT Flight_Number AS �����_�����, [���], [�������], CASE WHEN [��������] IS NULL THEN '��� ��������' ELSE �������� END [��������], PasportNumber FROM �������� JOIN ������������� ON �������������.ID_��������� = ��������.ID_��������� JOIN ���� ON ����.ID_����� = �������������.ID_����� WHERE Flight_Number = @FlightNumber;


 CREATE PROCEDURE Select_from_Flight(@Last_Name1 nvarchar (50))
 AS
 BEGIN
 EXEC Select_Passenger @Last_Name1
 END


 -----------------/ ��������� �� ���������� /-----------
 CREATE PROCEDURE Update_Aviapark (@id int, @Name nvarchar(50), @Place nvarchar(50))
AS
BEGIN
UPDATE Aviapark SET [�������� ��������] = @Name, [���������������] = @Place WHERE ID_��������� = @id
END;


-------------------/ ��������� �� �������� /-----------------

CREATE PROCEDURE Delete_Aviapark (@id int)
AS
BEGIN
DELETE FROM Aviapark WHERE ID_��������� = @id END;


 -----------------------/ �������� /------------------------

 CREATE TRIGGER delete_passenger ON �������� INSTEAD OF DELETE AS
    BEGIN
        DELETE FROM ������������� WHERE ID_���������=(
            SELECT ID_��������� FROM deleted)
		DELETE FROM �������� WHERE ID_��������� = (
			SELECT ID_��������� FROM deleted)
    END;

CREATE TRIGGER delete_flight ON ���� INSTEAD OF DELETE AS
    BEGIN
		DELETE FROM ������������� WHERE ID_����� = (
			SELECT ID_����� FROM deleted)
		DELETE FROM ���� WHERE ID_����� = (
			SELECT ID_����� FROM deleted)
	END;





---------------------/ ������������� ���� /--------------------
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
(SELECT ID FROM Book WHERE Book.Name = ��������� No1�));

SELECT ID_����� FROM ���� WHERE Flight_Number < (SELECT Flight_Number FROM ���� WHERE  ID_��������� = (SELECT ID_��������� FROM Aviapark WHERE [���������������] = '�����������'))



SELECT * FROM (SELECT ID_��������� FROM �������� WHERE Price >= 20000) AS Pas JOIN �������� ON Pas.ID_��������� =
��������.ID_���������;

SELECT * FROM (SELECT �������, Price AS Pr1 FROM ��������) AS Pr2 WHERE Pr1 > 15000;


SELECT Av.*, (SELECT Flight_Number FROM ���� AS R WHERE R.ID_��������� = Av.ID_���������) AS '����� �����' FROM Aviapark AS
Av;
SELECT R.Flight_Number, (SELECT Count(*) FROM Aviapark WHERE ID_��������� = R.ID_���������) AS '����������' FROM ���� AS R;


