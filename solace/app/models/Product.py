class Product:
    # Product Constructor
    # Product ID is not an attribute because sqlite handles the id as the primary key already
    def __init__(self, name, brand, apparel_type, stock, price, discount,
                source, category, sizes, colours, image_filename, description) -> None:
        self.__name = name
        self.__brand = brand
        self.__apparel_type = apparel_type
        self.__stock = stock
        self.__price = price
        self.__discount = discount
        self.__source = source
        self.__category = category
        self.__sizes = sizes
        self.__colours = colours
        self.__image_filename = image_filename
        self.__description = description