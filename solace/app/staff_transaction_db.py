from asyncio import sleep
from models.Thriftstore import Thriftstore

class Config():
    # Add on here with your table names
    tables = ["Products", "Static_Inputs", "Donations", "Donation_Details"]

    inputs1 = [ ("Adidas", "Dress","Unisex","Not All Donations Approved"), ("Asos", "Shirt","Men","Delivery Timing Too Late"), 
    ("Baliza","Skirt", "Women", "Delivery Timing Too Early") ]

    inputs2 = [ ("Levi's", "Shorts",), ("Love Bonito", "Sweater",), ("Nike", "Jacket",), ("Esse", "Jumper",), ("Puma", "Pants",), ("New Balance", "Shoes",) ]

    inputs3 = [("H&M",), ("Zara",), ("Uniqlo",), ("Gucci",), ("Tommy Hilfiger",), ("Cotton On",), ("No Brand",)]

    # Just here for reference
    dummyDonations = [
            (1, 1, 2, "Some Used", "Pending", "None", "Drop Off", "14:30:00PM", "11/3/2023", "None", "None", "None", 0, "None"),
            (2, 2, 3, "Most Are Used", "Pending", "None", "Delivery", "11:00:00AM", "17/8/2023", "None", "None", "None", 0, "None")
    ]

    static_inputs_insert_queries = [
        '''INSERT INTO Static_Inputs(
        brand,
        apparel_type,
        category,
        req_stat_reason)
        VALUES (?, ?, ?, ?);
        ''',
        '''INSERT INTO Static_Inputs(
        brand,
        apparel_type)
        VALUES (?, ?);
        ''',
        '''INSERT INTO Static_Inputs(
        brand)
        VALUES (?);
        '''
    ]

    donation_query = '''INSERT INTO Donations(
    donation_id, 
    user_id, 
    num_of_donations,
    general_condition,
    donation_approval,
    donation_remarks,
    donation_method,
    drp_off_or_donate_collect_time,
    drp_off_or_donate_collect_date,
    drp_off_or_donate_req_stat,
    req_stat_reason,
    total_delivery_amt,
    total_possible_comm,
    eligible_bid_items)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
    '''

    fk_table = "Donation_Details"

    Donation_Details_Table = '''
    donated_item_id INTEGER PRIMARY KEY AUTOINCREMENT,
    donation_id INT REFERENCES Donations(donation_id),
    donation_item_name CHAR(50) NOT NULL,
    donation_image_filename TEXT NOT NULL,
    quantity INT NOT NULL,
    condition CHAR(25) NOT NULL,
    brand CHAR(25) NOT NULL,
    size CHAR(3) NOT NULL
    '''

    donation_details_query = '''INSERT INTO Donation_Details(
    donated_item_id,
    donation_id,
    donation_item_name,
    donation_image_filename,
    quantity,
    condition,
    brand,
    size)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?);
    '''
    
    # Just here for reference
    dummyDonationDetails = [
        (1, 1, "Cropped Shirt", "H&M_Shirt.jpg", 1, "Well Used", "H&M", "M"),
        (2, 1, "Light Joggers", "Puma_Joggers.jpg", 2, "Hardly Used", "Puma", "L"),
        (3, 2, "Puffed Jacket", "Uniqlo_Jacket.jpg", 1, "Well Used", "Uniqlo", "M"),
        (4, 2, "Ruffle Dress", "Playdress_ruffle_dress.jpg", 1, "Hardly Used", "Playdress", "M"),
        (5, 2, "Tank Top", "Zara_tank_top.jpg", 3, "Used", "Zara", "S")
    ]

    create_table_queries = [
        """
           product_id INTEGER PRIMARY KEY AUTOINCREMENT,
           name CHAR(50) NOT NULL,
           brand CHAR(25) NOT NULL,
           apparel_type CHAR(25) NOT NULL,
           stock INT NOT NULL,
           price CHAR(6) NOT NULL,
           discount INT NOT NULL,
           source CHAR(25) NOT NULL, 
           category CHAR(15) NOT NULL,
           sizes TEXT NOT NULL,
           colours TEXT NOT NULL,
           image_filename TEXT NOT NULL,
           description TEXT NOT NULL
         """,
         """
            input_id INTEGER PRIMARY KEY AUTOINCREMENT,
            brand CHAR(25),
            apparel_type CHAR(25),
            category CHAR(15),
            req_stat_reason CHAR(50)
         """,
         """
            donation_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INT REFERENCES Users(user_id),
            num_of_donations INT NOT NULL,
            general_condition CHAR(25) NOT NULL,
            donation_approval CHAR(25) NOT NULL,
            donation_remarks TEXT NOT NULL,
            donation_method CHAR(15) NOT NULL,
            drp_off_or_donate_collect_time CHAR(10) NOT NULL,
            drp_off_or_donate_collect_date CHAR(10) NOT NULL,
            drp_off_or_donate_req_stat CHAR(25) NOT NULL,
            req_stat_reason CHAR(50) NOT NULL,
            total_delivery_amt CHAR(25) NOT NULL,
            total_possible_comm CHAR(6) NOT NULL
         """,
         """
            donated_item_id INTEGER PRIMARY KEY AUTOINCREMENT,
            donation_id INT REFERENCES Donations(donation_id),
            donation_item_name CHAR(50) NOT NULL,
            donation_image_filename TEXT NOT NULL,
            quantity INT NOT NULL,
            condition CHAR(25) NOT NULL,
            brand CHAR(25) NOT NULL,
            size CHAR(3) NOT NULL
        """
    ]

    def resetTablesInDB(self):
        db = Thriftstore()
        conn = db.get_connection()
        cur = db.get_cursor()

        for table_names, table_queries in zip(
            self.__class__.tables, self.__class__.create_table_queries
        ):
            db.drop_table(table_name=table_names)
            db.create_table(table_name=table_names, table_str=table_queries)
        
        for i in self.__class__.inputs1:
            cur.execute(self.__class__.static_inputs_insert_queries[0], i)
        for i in self.__class__.inputs2:
            cur.execute(self.__class__.static_inputs_insert_queries[1], i)
        for i in self.__class__.inputs3:
            cur.execute(self.__class__.static_inputs_insert_queries[2], i)

        # for details in self.__class__.dummyDonationDetails:
        #     cur.execute(self.__class__.donation_details_query, details)

        conn.commit()
        db.close_connection()
