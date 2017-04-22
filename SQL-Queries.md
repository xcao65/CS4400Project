# Admin
## 1. Select all pending data point	
```sql
SELECT LocName, DataType, DataValue, DateTime, Status FROM Data_Point WHERE Status = 'Pending'
```
## 2. Selcet all pending CoA
```sql
SELECT UserName, B.EmailAddress, City, State, Title FROM User AS A, City_Official AS B WHERE Status = 'Pending' AND A.EmailAddress = B.EmailAddress
```
## 3. Update one data point	
```sql
UPDATE Data_Point SET Status = (status) WHERE LocName = (location) AND DateTime = (date_time)
```
## 4. Update many data point
```python
sql = "UPDATE Data_Point SET Status = \'{0}\' WHERE (LocName = \'{1}\' AND DateTime = \'{2}\')" +
for i in range(1,len(keys)):
	sql = sql + "OR (LocName = \'{3}\'".format(status, keys[i][0], keys[i][1])"



## 5. Change a CoA
```sql
UPDATE City_Official SET Status = (status) WHERE EmailAddress = (email)
```


***
# City & State
## 1. Import cities and states into frontend
```sql
SELECT * FROM City_State
```
## 2. Import locations into frontend
```sql 
SELECT DISTINCT LocationName FROM POI
```
## 3. Import datatypes into frontend
```sql
SELECT DISTINCT Type FROM Data_Type
```
***
# City Scientist
## 1. Add a new location
```sql
INSERT INTO POI (Flag, LocationName, ZipCode, City, State) VALUES (0, locationname, zipcode, city, state)
```
## 2. Add a new data point
```sql
INSERT INTO Data_Point (DateTime, LocName, DataType, DataValue) VALUES (Formalized_DateTime, locationname, datatype, value)
```
***
# City Official
## 1. Show POI detail
```sql
SELECT DataType, DataValue, DateTime FROM Data_Point WHERE LocName = (locname) AND DataType = (dataType) AND DataValue BETWEEN (dataValue[0]) AND (dataValue[1]) AND DateTime BETWEEN (Formalized_DateTime[0]) AND (Formalized_DateTime[1])
```
## 2. Filter
```python
"SELECT * FROM POI WHERE LocationName = \'{0}\' AND State = \'{1}\' AND ZipCode = \'{2}\' AND Flag = {3} AND DateFlagged BETWEEN \'{4}\' AND \'{5}\'".format(name, city, state, zipCode, flag, Formalized_Date[0], Formalized_Date[1])
```
***
# POI Report
##1. Get location name
```sql
SELECT LocationName,Flag,City,State FROM POI
```
##2. Funtions to fetch columns for the report
```sql
SELECT MIN(DataValue) FROM Data_Point WHERE LocName = (locationname) AND DataType = (datatype)
SELECT MAX(DataValue) FROM Data_Point WHERE LocName = (locationname) AND DataType = (datatype)
SELECT AVG(DataValue) FROM Data_Point SELECT COUNT(LocName) FROM Data_Point WHERE LocName = (locationname)
```
***
# All Users
## 1. Log in
```sql
SELECT Username, Password, Type FROM User WHERE Username = (username)
```
## 2. Register
### (1) New user
```sql
INSERT INTO User (EmailAddress, UserName, Password, Type) VALUES (email, name, pwd, utype)
```
### (2) Check whether the username exists
```sql
SELECT username FROM User WHERE Username = (name)
```
### (3) Check whether the email exists
```sql
SELECT EmailAddress FROM User WHERE EmailAddress = (email)
```
### (4) Delete a user
```sql
DELETE FROM User WHERE Username = (name)
```
