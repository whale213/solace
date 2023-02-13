from werkzeug.utils import secure_filename
from flask import render_template, request, redirect, Blueprint, flash
from models.Thriftstore import Thriftstore
from forms.staff_transaction_forms import ProductForm, SearchProductForm, InputSettingForm
from models.Product import Product
from datetime import date
import os
# Function to populate the drop down choices with db inputs
def populateDropDownLists(db_drop_down_data, htmlList):

    for drp_down_data in range(len(db_drop_down_data)):
        drp_down_data_tuple = []
        drp_down_data_item = db_drop_down_data[drp_down_data][0]
        for value_and_label in range(2):
            # Assign the value and label to the same value in the db tuple's first data item
            drp_down_data_tuple.append(drp_down_data_item)
        # Add the tuple with value and label into html list to populate into form
        htmlList.append(tuple(drp_down_data_tuple))


# Set the blueprints for the app
view_settings = Blueprint("productFormSettings", __name__)
view_inventory = Blueprint("inventory", __name__)
add_Product = Blueprint("addProduct", __name__)
delete_Product = Blueprint("deleteProduct", __name__)
edit_Product = Blueprint("editProduct", __name__)

# Set upload folder file path for product images
upload_folder = "static/product_images"
# Set Accepted Extensions for images
ACCEPETED_EXTENSIONS = ["jpeg","JPEG", "jpg", "JPG", "png", "PNG"]

# Populate drop down selections db queries
get_brands_query = '''SELECT brand FROM Static_Inputs WHERE brand IS NOT NULL'''
get_apparel_types_query = '''SELECT apparel_type FROM Static_Inputs WHERE apparel_type IS NOT NULL'''
get_categories_query = '''SELECT category FROM Static_Inputs WHERE category IS NOT NULL'''

# Settings routes

@view_settings.route("/viewProductFormSettings", methods=["GET", "POST"])
def productFormSettings():
    db = Thriftstore()
    all_inputs = db.get_all_items("Static_Inputs")
    brands, apparels, categories = [], [], []

    def populateArray(db_data, array, db_col_num):
        for input in range(len(db_data)):
            if db_data[input][db_col_num] != None:
                array.append(db_data[input][db_col_num])

    populateArray(all_inputs, brands, 1)
    populateArray(all_inputs, apparels, 2)
    populateArray(all_inputs, categories, 3)
    addInputForm = InputSettingForm(request.form) 
    cur = db.get_cursor()
    con = db.get_connection()

    def checkDbForInput(new_input):
        for inputs in range(len(all_inputs)):
            for input in all_inputs[inputs]:
                if input == new_input:
                    return True

    if request.method == "POST" and addInputForm.validate():
        if request.form['submit_input'] == "Add Input":
            selected_dropdown = addInputForm.selected_input.data
            newInput = addInputForm.new_input.data

            # Get the last row
            result = cur.execute(
                f"SELECT {selected_dropdown} FROM Static_Inputs ORDER BY input_id DESC LIMIT 1"
            ).fetchone()

            # Get the lowest row id where the slot is null
            highest_null_row = cur.execute(
                f"""SELECT MIN(rowid) FROM Static_Inputs WHERE {selected_dropdown} IS NULL"""
            ).fetchone()[0]

            # Update that specific lowest row id where it is null with the new input value
            updateInput = f"""UPDATE Static_Inputs
            SET {selected_dropdown} = ?
            WHERE {selected_dropdown} IS NULL AND rowid = {highest_null_row}"""

            updateInputNull = f"""UPDATE Static_Inputs
            SET {selected_dropdown} = ? WHERE {selected_dropdown} IS NULL"""
            inputExists = checkDbForInput(newInput)
            # If the input slot is null
            if result[0] is None:
                if not inputExists:
                    db.update_table_item(updateInput, (newInput,))
                else:
                    flash(f"{newInput} already exists in database!")
            # Else make a new null row and update the new null value slot with input
            else:
                if not inputExists:
                    insert_null_query = """INSERT into Static_Inputs(
                    brand,
                    apparel_type,
                    category,
                    req_stat_reason
                    )VALUES(?, ?, ?, ?);
                    """
                    # Null tuple
                    input_tuple = (None, None, None, None)

                    cur.execute(insert_null_query, input_tuple)
                    db.update_table_item(updateInputNull, (newInput,))
                    flash(f"Successfully Updated {selected_dropdown} with '{newInput}''.")
                else:
                    flash(f"{newInput} already exists in database!")
            # Perform queries
            return redirect(request.url)
        else:
            selected_dropdown = addInputForm.selected_input.data
            newInput = addInputForm.new_input.data
            all_products = db.get_all_items("Products")
            for product in range(len(all_products)):
                checkInputs = [all_products[product][2], all_products[product][3], all_products[product][8]]
                if newInput in checkInputs:
                    flash(f"Delete failed: {all_products[product][1]} is currently using {newInput} for {selected_dropdown}!")
                    db.close_connection()
                    return redirect(request.url)

            # Check if the input exists in the database
            if newInput not in brands and newInput not in apparels and newInput not in categories:
                flash(f"'{newInput}' not found in database.")
                return redirect(request.url)

            # "Removing" input query by setting to null instead of deleting entirely
            # due to the format of correlating rows in sqlite
            update_setToNull = f"""UPDATE Static_Inputs
            SET {selected_dropdown} = NULL
            WHERE {selected_dropdown} = "{newInput}";"""
            cur.execute(update_setToNull)
            con.commit()

            flash(f"Successfully Deleted '{newInput}' from {selected_dropdown}.")
            db.close_connection()
            return redirect(request.url)

    db.close_connection()
    return render_template("staff_transaction/productFormSettings.html", brands=brands,
                    apparels=apparels, categories=categories, form=addInputForm)


# Products CRUD Routes:

@view_inventory.route("/viewInventory", methods=["GET", "POST"])
def inventory():
    db = Thriftstore()
    products = db.get_all_items("Products")
    flagged = False
    for product in range(len(products)):
        if products[product][4] <= 20:
            flagged = True
    
    searchForm = SearchProductForm(request.form)
    search = False

    def searchProducts(query):
        search_qeury = f'''SELECT * FROM Products WHERE 
        product_id LIKE "%{query}%" 
        or name LIKE "%{query}%" 
        or brand LIKE "%{query}%"
        or source LIKE "%{query}%"
        '''
        cur = db.get_cursor()
        search_result = cur.execute(search_qeury).fetchall()
        return search_result
    
    # Get Today's Date
    today = date.today()
    date_formatted = today.strftime("%B %d, %Y")

    if request.method == "POST" and searchForm.validate():
        search = True
        query_item = searchForm.search.data
        result = searchProducts(query_item)
        db.close_connection()
        return render_template("staff_transaction/viewInventory.html", products=products, 
                            flagged=flagged, form=searchForm, result=result, searchState=search, today=date_formatted)
    
    db.close_connection()
    return render_template("staff_transaction/viewInventory.html", 
                            products=products, flagged=flagged, form=searchForm, today=date_formatted)


@add_Product.route("/addProduct", methods=["GET", "POST"])
def addProduct():
    addProductForm = ProductForm(request.form)
    db = Thriftstore()
    products = db.get_all_items("Products")
    cur = db.get_cursor()

    db_brands = cur.execute(get_brands_query).fetchall()
    db_apparel_types = cur.execute(get_apparel_types_query).fetchall()
    db_categories = cur.execute(get_categories_query).fetchall()

    brand_choices = [("", "Select Brand")]
    apparel_type_choices = [("", "Select Clothing Type")]
    category_choices = [("", "Select Category")]

    populateDropDownLists(db_brands, brand_choices)
    populateDropDownLists(db_apparel_types, apparel_type_choices)
    populateDropDownLists(db_categories, category_choices)

    # Set default variables such as image, preview var, and product details
    productCoverImage = "images/blank_shirt_template.png"

    addProductForm.brand.choices = brand_choices
    addProductForm.apparel_type.choices = apparel_type_choices
    addProductForm.category.choices = category_choices
    # Set this preview variable to check if staff had previewed item before confirmation to add product to db
    preview = False
    name, stock, price, discount, source, brand, apparel_type, category, sizes, colours, description\
        = None, None, None, None, None, None, None, None, None, None, None
    
    if request.method == 'POST' and addProductForm.validate():
        # If the submission is just to preview the product before adding to db
        if request.form['submit_btn'] == "Preview":
            preview = True
            p_name = addProductForm.name.data
            p_brand = addProductForm.brand.data
            p_apparel_type = addProductForm.apparel_type.data
            p_stock = addProductForm.stock.data
            p_price = str(addProductForm.price.data)
            p_discount = int(addProductForm.discount.data)
            p_source = addProductForm.source.data
            p_category = addProductForm.category.data
            p_sizes = str(addProductForm.sizes.data)[1:-1]
            p_colours = str(addProductForm.colours.data)[1:-1]
            p_image_data = request.files["image"]
            p_description = addProductForm.description.data

            if p_image_data.filename.split(".")[1] not in ACCEPETED_EXTENSIONS:
                flash(f"Invalid Image File! Previously Submitted: {p_image_data.filename.split('.')[1]}. Only jpg, jpeg, png allowed.")
            else:
                p_image_data.save(os.path.join(upload_folder, secure_filename(p_image_data.filename)))
            
            return render_template("staff_transaction/addProduct.html", 
                                    form=addProductForm, preview=preview, img=p_image_data.filename, 
                                    name=p_name, stock=p_stock, price=p_price, discount=p_discount, 
                                    brand=p_brand, source=p_source, apparel_type=p_apparel_type, 
                                    category=p_category, sizes=p_sizes, colours=p_colours, description=p_description)

        # Else the submission is to add the product to db
        elif request.form['submit_btn'] == "Confirm Details":
            productExists = False
            db = Thriftstore()
            products = db.get_all_items("Products")
            # Check if the name, brand and source type matches any existing product in db
            for product in range(len(products)):
                if products[product][1] == addProductForm.name.data and \
                products[product][2] ==  addProductForm.brand.data and \
                products[product][7] == addProductForm.source.data:
                    productExists = True
                    flash(f"{products[product][7]} : {products[product][2]} {products[product][1]} Already Exists In Database!")
            
            if productExists is False:
                p_name = addProductForm.name.data
                p_brand = addProductForm.brand.data
                p_apparel_type = addProductForm.apparel_type.data
                p_stock = addProductForm.stock.data
                p_price = str(addProductForm.price.data)
                p_discount = int(addProductForm.discount.data)
                p_source = addProductForm.source.data
                p_category = addProductForm.category.data
                p_sizes = str(addProductForm.sizes.data)[1:-1]
                p_colours = str(addProductForm.colours.data)[1:-1]
                p_image_data = request.files["image"]
                p_image_data.save(os.path.join(upload_folder, secure_filename(p_image_data.filename)))
                p_description = addProductForm.description.data
                # Insert Product Sqlite Query
                product_insert_query = """ INSERT INTO Products(
                name, 
                brand, 
                apparel_type,
                stock,
                price,
                discount,
                source,
                category,
                sizes,
                colours,
                image_filename,
                description)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
                """

                product = Product(p_name, p_brand, p_apparel_type, p_stock, p_price,
                p_discount, p_source, p_category, p_sizes, p_colours, p_image_data.filename, p_description)

                db.insert_into_table(product_insert_query, product)
                db.close_connection()
                return redirect("/viewInventory")
            else:
                return redirect(request.url)
    else:
        db.close_connection()
        return render_template("staff_transaction/addProduct.html", 
                                form=addProductForm, preview=preview, img=productCoverImage, 
                                name=name, stock=stock, price=price, discount=discount, 
                                brand=brand, source=source, apparel_type=apparel_type, 
                                category=category, sizes=sizes, colours=colours, description=description)


@delete_Product.route("/deleteProduct/<int:id>", methods=["GET", "POST"])
def deleteProduct(id):
    db = Thriftstore()
    image_filename = db.get_item_by_id("Products", "product_id", id)[0][11]
    # Ensure the image is also removed from the folder to ensure:
    # the folder does not keep storing product images which the product does not exist in the db anymore
    os.remove(os.path.join(upload_folder, image_filename))
    # Delete the product from Products Table in db
    db.delete_by_id_from_table("Products", "product_id", id)
    db.close_connection()
    return redirect("/viewInventory")

@edit_Product.route("/editProduct/<int:id>", methods=["GET", "POST"])
def editProduct(id):
    editProductForm = ProductForm(request.form)
    db = Thriftstore()
    cur = db.get_cursor()

    db_brands = cur.execute(get_brands_query).fetchall()
    db_apparel_types = cur.execute(get_apparel_types_query).fetchall()
    db_categories = cur.execute(get_categories_query).fetchall()

    brand_choices = [("", "Select Brand")]
    apparel_type_choices = [("", "Select Clothing Type")]
    category_choices = [("", "Select Category")]

    populateDropDownLists(db_brands, brand_choices)
    populateDropDownLists(db_apparel_types, apparel_type_choices)
    populateDropDownLists(db_categories, category_choices)

    editProductForm.brand.choices = brand_choices
    editProductForm.apparel_type.choices = apparel_type_choices
    editProductForm.category.choices = category_choices

    new_image = False
    # Retrieving all details pertaining to the specified product id
    current_editing_product = db.get_item_by_id("Products", "product_id", id)[0]
    # Retrieving the image and assigning to a var for ease of access to pass into
    # jinja template for product image viewing, etc.
    current_editing_image = db.get_item_by_id("Products", "product_id", id)[0][11]

    if request.method == "POST" and editProductForm.validate():
        p_name = editProductForm.name.data
        p_brand = editProductForm.brand.data
        p_apparel_type = editProductForm.apparel_type.data
        p_stock = editProductForm.stock.data
        # Reformatted to fit Sqlite parameter type
        p_price = str(editProductForm.price.data)
        p_discount = int(editProductForm.discount.data)
        p_source = editProductForm.source.data
        p_category = editProductForm.category.data
        # Reformatted to fit Sqlite parameter type
        p_sizes = str(editProductForm.sizes.data)
        p_colours = str(editProductForm.colours.data)
        p_image_data = request.files["image"]
        p_image = p_image_data.filename
        p_description = editProductForm.description.data

        # Work around for filefield issue  
        if p_image != "":
            if p_image.split(".")[1] not in ACCEPETED_EXTENSIONS:
                p_image = current_editing_image
                flash(f"Invalid Image File! Previously Submitted: {p_image.split('.')[1]}. Only jpg, jpeg, png allowed.")
            else:
                p_image_data.save(os.path.join(upload_folder, secure_filename(p_image_data.filename)))   
            new_image = True
        else:
            p_image = current_editing_image

        #Update Product Query
        product_update_query = """ UPDATE Products 
        SET name = ?, 
        brand = ?, 
        apparel_type = ?,
        stock = ?,
        price = ?,
        discount = ?,
        source = ?,
        category = ?,
        sizes = ?,
        colours = ?,
        image_filename = ?,
        description = ?
        WHERE product_id = ?
        """

        # New Product Tuple not the Product class instance because the 
        # added product instance was converted into tuple to store into db
        new_product_tuple = (p_name, p_brand, p_apparel_type, p_stock, p_price,
        p_discount, p_source, p_category, p_sizes, p_colours, p_image, p_description, id)

        db = Thriftstore()
        db.update_table_item(product_update_query, new_product_tuple)
        db.close_connection()
        if new_image is True:
            return redirect(request.url)
        else:
            return redirect("/viewInventory")
    # Else statement here so that if no form submitted, 
    # Original data can be passed into the form and be overriden if necessary by submission of form
    else:
        # data here just equals to whatever original uneditted product details were
        editProductForm.name.data = current_editing_product[1]
        editProductForm.brand.data = current_editing_product[2]
        editProductForm.apparel_type.data = current_editing_product[3]
        editProductForm.stock.data = current_editing_product[4]
        editProductForm.price.data = float(current_editing_product[5])
        editProductForm.discount.data = str(current_editing_product[6])
        editProductForm.source.data = current_editing_product[7]
        editProductForm.category.data = current_editing_product[8]
        editProductForm.description.data = current_editing_product[12]

        # Sizes and Colours need to be reformatted back in such a way that:
        # - it is a proper array of values in python first and not a string due to parameter type by sqlite
        # - Then after when submitted it gets reconverted back to a string to become TEXT type in sqlite
        # Note: sqlite is not meant to store array / dict values hence string was used.
        editProductForm.sizes.data = list(str(current_editing_product[9])[1:-1].replace(",", "").replace("'","").split())
        editProductForm.colours.data = list(str(current_editing_product[10])[1:-1].replace(",", "").replace("'","").split())
        # If no changes made, end the connection from retreival request and render the template
        db.close_connection()
        return render_template("staff_transaction/editProduct.html", form=editProductForm, 
                                current_editing_product=current_editing_product, 
                                img = current_editing_image)

