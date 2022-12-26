# Solace
Solace is an application that was created for a school assignment where we had to digitalise a pre-existing business by creating an application for it.

## Background Information
Solace is a Thriftstore web application designed to reduce climate emissions and fast fashion trends through digitialisation of the
current business processes and needs for better efficiency and use of resources.

# Thriftstore Database Class Usage Documentation

## Database Methods
- All the below methods are function delcarations.

### Create Connection

```python
create_connection(self, db_name: str)
```

#### Description
Utitlised by the database class instance to ensure a successful connection before any queries / operations are performed via the class instance.

##### **Note**
This method is **NOT INTENDED** to be used **DIRECTLY OUTSIDE** of the database class.

#### Parameters
- db_name : String value of database name

#### Return / Output 
1. returns a sqlite3 connection to the specified db_name
2. returns None during exceptions.

### Close Connection

```python
close_connection(self)
```

#### Description
Used at the end of a session after all query operations have been completed, to close the database cursor and connection properly.

#### Parameters
- none

#### Return / Output 
- success / error message in console

### Create Table

```python
create_table(self, table_name: str, table_str: str)
```

#### Description
Creates a table in the database.

#### Parameters
- table_name: String name of the table
- table_str: an sql create table query surrounded by "" or """
    - should contain:
        1. The column headers in order
        2. Specifications of data types for headers
        3. Maximum value count of certain types (if applicable)
        4. **Specifcation of Primary and Foreign keys**

#### Resources:
- [Guide to foreign keys](https://www.youtube.com/watch?v=FrTQSPSbVC0)

#### Return / Output 
- success / error message in console

### Drop Table

```python
drop_table(self, table_name: str)
```

#### Description
Drops an existing specified table in the database.

#### Parameters
- table_name: String value of table name to drop

#### Return / Output 
- success / error message in console

### Insert Into Table

```python
insert_into_table(self, insert_query: str, class_object: object)
```

#### Description
Inserts a class instance as a tuple into a table in the database via an sql insert query.

#### Parameters
- insert_query: an sql insert query surrounded by "" or """
    - should contain:
        1. The table to insert into
        2. The column headers to insert into by order
- class_object: a class instance 

#### Return / Output 
- success / error message in console

### Update Table Item

```python
update_table_item(self, update_query: str)
```

#### Description
Updates an item in the table in the database.

#### Parameters
- update_query: an sql update query surrounded by "" or """
    - should contain:
        1. The name of table to update
        2. The specified header to change
        3. The new value to set for that header
        4. The condition to set the new value

#### Return / Output 
- success / error message in console

### Delete By Id From Table

```python
delete_by_id_from_table(self, table_name: str, id_name: str, id: int)
```

#### Description
Deletes an item from a specified table in the database based on a given unique id

#### Parameters
- table_name: String value of table name to delete item
- id_name: String value of named id header in table
- id: Integer value of unique id of item

#### Return / Output 
- success / error message in console

### Delete All From Table

```python
delete_all_from_table(self, table_name: str)
```

#### Description
Deletes all items from a specified table in the database.

#### Parameters
- table_name: String value of table name to delete all items

#### Return / Output 
- success / error message in console

### Get Item By Id

```python
get_item_by_id(self, table_name: str, id_name: str, id: int)
```

#### Description
Retrieves an item from a specified table in the database by using the unique id of the item.

#### Parameters
- table_name: String value of table name to retrieve item
- id_name: String value of named id header in table
- id: Integer value of unique id of item

#### Return / Output 
- returns the tuple item in a list
- returns None during exceptions

### Get Item By Custom Value

```python
get_item_by_custom_value(self, custom_query: str, value: any)
```

#### Description
Retrieves an item based on a custom value and sql get query. 

#### Parameters
- custom_query: an sql custom get query surrounded by "" or """
    - should contain:
        1. The name of table to retrieve from
        2. The condition to retrieve the item
        3. The value used to retrieve the item eg. id

- value: The value specified within the condition of the query to retrieve the item

#### Return / Output 
- returns the tuple item in a list
- returns None during exceptions

### Get All Items

```python
get_all_items(self, table_name: str)
```

#### Description
Retrieves all items from a specified table in the database.

#### Parameters
- table_name: String value of table name to retrieve items

#### Return / Output 
- returns a list of tuple items 
- returns None during exceptions

### Get Cursor / Get Connection

```python
get_cursor(self)
get_connection(self)

# Usage Outside Of Class:
db = Thriftstore()

db_cur = db.get_cursor()
db_con = db.get_connection()
```

#### Description
Only used when an additional method needs to be created from outside the database class for methods not defined in the class.

#### Parameters
- none

#### Return / Output
- returns cursor / connection of database

### Get Ordered By Custom Value

```python
get_ordered_by_custom_value(self, table_name: str, custom_value: str, order_type: str)
```

#### Description
Retrieves all items from a specified table in a specified order

#### Parameters
- table_name: String value of table name to retrieve items
- custom_value: String value of custom value to sort in order
- order_type: **ASC** for ascending and **DESC** for descending order

#### Return / Output 
- returns a list of tuple items in order
- returns None during exceptions

### Foreign Key Query

```python
def foreign_key_query(self, t_name_one: str, t_name_two: str, fk_name: str, pk_name: str, select_values: list, type_of_join: str, specifc_query: str)
```

#### Description
Retrieves all items depending on foreign key query between two relational tables

#### Parameters
- t_name_one: One of the tables in relation to the other table
- t_name_two: The other specified table in the relation
- fk_name: String name of foreign key of table with primary key
- pk_name: String name of primary key of table without foreign key
- select_values: A list of values to be selected in the query
- type_of_join: Can be **JOIN**, **LEFT JOIN**, **RIGHT JOIN**, **INNER JOIN**, etc. depending on desired results of query
- specific_query: Specifications such as GROUP BY, WHERE, etc.

#### Return / Output 
- returns a specified list of tuple items dependent on query
- returns None during exceptions

## Simple Example Case of Usage (Primary Key Only)

### Book Class
```python
class Book:
    def __init__(self, id, title, author, pages) -> None:
        self.__id = id
        self.__title = title
        self.__author = author
        self.__pages = pages
```

### Book Instances
```python
b1 = Book(1, "SpyxFamily", "Tatsuya Endo", 125)
b2 = Book(2, "Travelling Cat Chronicles", "Hiro Arikawa", 235)
b3 = Book(3, "Le Petit Prince", "Antoine de Saint-Exupéry", 96)
```

### Book Sql Queries

#### Creating
```python
bookTable = """ 
    Id INT PRIMARY KEY,
    Title CHAR(25) NOT NULL,
    Author CHAR(25) NOT NULL,
    Pages INT
    """
```
#### Inserting
```python
book_insert_query = """ INSERT INTO Books(
    Id, 
    Title, 
    Author, 
    Pages)
    VALUES (?, ?, ?, ?);
    """
```
#### Updating
```python
book_update_query = """ UPDATE Books
    SET Pages = 100 
    WHERE Id = 1;
    """
```

#### Custom Retrieval 
```python
get_custom_query = """ SELECT * FROM Books 
    WHERE Pages=?
    """
```

### Implementation With Database Methods

##### **Note**
After Creating a Table, create_table method SHOULD NOT be called again unless necessary to reinstantiate table.
The above also applies to Dropping a Table for drop_table, where there is no need to call it again after the table has
already been dropped.

The following is an implementation of the most common usage methods used at once.

```python
# In Your Main Compiling File:
db = Thriftstore()
db.create_table("Books", bookTable)
db.insert_into_table(book_insert_query, b1)
db.insert_into_table(book_insert_query, b2)
db.insert_into_table(book_insert_query, b3)
db.update_table_item(book_update_query)

# returns a list of tuples matching the custom query
# print to view return value in console.
print(db.get_item_by_custom_value(get_custom_query, 125))

'''
A MUST USE at the end of every user session after all db operations are completed:
'''
db.close_connection()
```
## Simple Example Case of Usage (Primary And Foreign Key)

### Student Class
```python
class Student:
    def __init__(self, stud_id, name, admin_no, grp_id) -> None:
        self.__student_id = stud_id
        self.__name = name
        self.__admin_no = admin_no
        self.__group_id = grp_id
```

### Group Class
```python
class Group:
    def __init__(self, grp_id, name, topic_chosen) -> None:
        self.__group_id = grp_id
        self.__name = name
        self.__topic_chosen = topic_chosen
```

### Instances 
```python
# Creating Students
s1 = Student(1, "Tom", "202212E", 1)
s2 = Student(2, "Alice", "202276B", 1)
s3 = Student(3, "David", "202182Z", 2)
s4 = Student(4, "Sam", "202232A", 2)

# Creating Groups
g1 = Group(1, "Team 1", "Python")
g2 = Group(2, "Team 2", "Java")
```

### Queries

#### Creating
```python
studentTableAttributes = """
    student_id INT PRIMARY KEY,
    name CHAR(25) NOT NULL,
    admin_no CHAR(7) NOT NULL,
    group_id INT REFERENCES Groups(group_id)
"""

groupTableAttributes = """
    group_id INT PRIMARY KEY,
    name CHAR(25) NOT NULL,
    topic_chosen CHAR(25) NOT NULL
"""
```


#### Inserting
```python
insert_query_student = """INSERT INTO Students(
    student_id,
    name,
    admin_no,
    group_id)
    VALUES(?, ?, ?, ?);
"""

insert_query_group = """INSERT INTO Groups(
    group_id,
    name,
    topic_chosen)
    VALUES(?, ?, ?);
"""
```

### Implementation With Database Methods
```python
# In Your Main Compiling File
db = Thriftstore()

# Creating Tables
db.create_table("Students", studentTableAttributes)
db.create_table("Groups", groupTableAttributes)

# Adding Students 
db.insert_into_table(insert_query_student, s1)
db.insert_into_table(insert_query_student, s2)
db.insert_into_table(insert_query_student, s3)
db.insert_into_table(insert_query_student, s4)

# Adding Groups
db.insert_into_table(insert_query_group, g1)
db.insert_into_table(insert_query_group, g2)

# Foreign Key Queries Examples

# Returns the number of students in each group
print(db.foreign_key_query(
    t_name_one="Groups",
    t_name_two="Students",
    fk_name= "group_id",
    pk_name= "group_id",
    select_values= ["Groups.name", "COUNT(Students.student_id)"],
    type_of_join= "LEFT JOIN",
    specifc_query= "GROUP BY Groups.group_id"
))

# Returns: [('Team 1', 2), ('Team 2', 2)]

# Returns all admin numbers who are under the topic of "Java"
print(db.foreign_key_query(
    t_name_one="Students",
    t_name_two="Groups",
    fk_name= "group_id",
    pk_name= "group_id",
    select_values= ["Students.admin_no"],
    type_of_join= "JOIN",
    specifc_query= "WHERE Groups.topic_chosen = 'Java'"
))

# Returns : [('202182Z',), ('202232A',)]

db.close_connection()
```

## Additional Tips

### Viewing Changes In Database
- (Applicable to Visual Studio Code)
    - There is an sqlite viewer extension which allows you to read .db files in the VSC IDE:
    - [VSC SQLite Viewer Extension](https://marketplace.visualstudio.com/items?itemName=qwtel.sqlite-viewer)

- (Alternatives)
    - SQLite Viewer Web can also be used: 
    - [SQLite Viewer Web](https://sqliteviewer.app/?ref=vscode)
