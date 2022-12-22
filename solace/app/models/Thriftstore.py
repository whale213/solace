import sqlite3

class Thriftstore:
    def __init__(self) -> None:
        # initialise connection to thriftstore db
        self.__con = self.create_connection("Thriftstore.db")
        if self.__con is None:
            print("Error in connecting to database!")
        else:
            # initialise the db cursor to perform sql queries 
            self.__cur = self.__con.cursor()
            # enable foreign key support for any queries with foreign keys
            self.__cur.execute("PRAGMA foreign_keys = ON")
        
    # method to create and ensure db connection
    def create_connection(self, db_name: str) -> any:
        con = None
        try:
            con = sqlite3.connect(db_name)
            return con
        except Exception as exc:
            print(exc)
        return con

    # method to close and end connection after all operations done at end of user session
    def close_connection(self) -> None:
        if self.__con:
            self.__cur.close()
            self.__con.close()
            print("Cursor and Connection to database has been closed.")
        else:
            print("There is no database cursor and connection to close!")
    
    
    # Methods (1): CRUD Methods

    def create_table(self, table: str) -> None:
        try:
            self.__cur.execute(table)
            print("Table successfully created.")
        except sqlite3.Error as e:
            print("Failed to create table: ", "".join(e.args))
        except Exception as exc:
            print(exc)

        
    def drop_table(self, table_name: str) -> None:
        try:
            self.__cur.execute(f"DROP TABLE IF EXISTS {table_name}")
            print(f"{table_name} table was successfully dropped.")
        except sqlite3.Error as e:
            print("Failed to drop table: ", "".join(e.args))
        except Exception as exc:
            print(exc)


    def insert_into_table(self, insert_query: str, class_object: object) -> None:
        try:
            # Part 1: convert class object arguement into tuple
            obj_list_attr = []
            obj_tuple = ()
            try:
                # appends value of dict represented version of class obj into obj list attributes
                for keys in class_object.__dict__:
                    obj_list_attr.append(class_object.__dict__[keys])
                
                # assign obj tuple to tuple converted obj list attribute
                obj_tuple = tuple(obj_list_attr)
            except Exception as exc:
                print("Error occured during class object conversion: ", exc)

            # Part 2: inserted converted object into queried table
            self.__cur.execute(insert_query, obj_tuple)
            self.__con.commit()
            print(f"Successfully inserted {class_object.__dict__} into table.")
        except sqlite3.Error as e:
            print(f"Failed to insert into table: ", "".join(e.args))
        except Exception as exc:
            print(exc)

    
    def update_table_item(self, update_query: str) -> None:
        try:
            self.__cur.execute(update_query)
            self.__con.commit()
            print("Successfully updated table item.")
        except sqlite3.Error as e:
            print("Failed to update item: ", "".join(e.args))
        except Exception as exc:
            print(exc)

        
    def delete_by_id_from_table(self, table_name: str, id: int) -> None:
        try:
            delete_id_query = f"DELETE FROM {table_name} WHERE id=?"
            self.__cur.execute(delete_id_query, (id,))
            self.__con.commit()
            print(f"Successfully deleted item id of: {id} from {table_name} table.")
        except sqlite3.Error as e:
            print("Failed to delete item: ", "".join(e.args))
        except Exception as exc:
            print(exc)


    def delete_all_from_table(self, table_name: str) -> None:
        try:
            delete_query = f"DELETE FROM {table_name}"
            self.__cur.execute(delete_query)
            self.__con.commit()
            print(f"Successfully deleted all items from {table_name} table.")
        except sqlite3.Error as e:
            print("Failed to delete all items: ", "".join(e.args))
        except Exception as exc:
            print(exc)
    
    # Methods (2): Getters

    def get_item_by_id(self, table_name: str, id_name: str, id: int) -> list:
        try:
            get_id_query = f"SELECT * FROM {table_name} WHERE {id_name}=?"
            self.__cur.execute(get_id_query, (id,))
            item = self.__cur.fetchall()
            print(f"Successfully retrieved {id_name} of {id} from {table_name}")
            return item
        except sqlite3.Error as e:
            print("Failed to retrieve item: ", "".join(e.args))
            return None
        except Exception as exc:
            print(exc)
            return None

    def get_item_by_custom_value(self, custom_query: str, value: any) -> list:
        try:
            self.__cur.execute(custom_query, (value,))
            item = self.__cur.fetchall()
            print("Item successfully retrieved.")
            return item
        except sqlite3.Error as e:
            print("Failed to retrieve item: ", "".join(e.args))
            return None
        except Exception as exc:
            print(exc)
            return None
        

    def get_all_items(self, table_name: str) -> list:
        try:
            allData = self.__cur.execute(f"SELECT * FROM {table_name}")
            print("All items successfully retrieved.")
            return allData.fetchall()
        except sqlite3.Error as e:
            print("Failed to retrieve all items: ", "".join(e.args))
            return None
        except Exception as exc:
            print(exc)
            return None

    '''
    Getters for connection and cursor to 
    perform or make custom query methods not defined
    in the Thriftstore database model class
    '''
    def get_cursor(self):
        return self.__cur
    
    def get_connection(self):
        return self.__con

    # Methods (3): Additional Methods

    def get_ordered_by_custom_value(self, table_name: str, custom_value: str, order_type: str) -> list:
        try:
            order_id_query = f"SELECT * FROM {table_name} ORDER BY {custom_value} {order_type}"
            allData = self.__cur.execute(order_id_query)
            print(f"All items successfully retrieved in {order_type} order.")
            return allData.fetchall()
        except sqlite3.Error as e:
            print("Failed to retrieve all items: ", "".join(e.args))
            return None
        except Exception as exc:
            print(exc)
            return None
    