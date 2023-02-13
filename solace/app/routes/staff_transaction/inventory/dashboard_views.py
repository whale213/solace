from flask import render_template, request, redirect, Blueprint, flash
from models.Thriftstore import Thriftstore
from models.InventoryChart import InventoryChart
from flask import Response
import pandas as pd
import io

get_excel_downloadable = Blueprint("productDownloadExcelData", __name__)
view_invent_dashboard = Blueprint("inventoryDashboard", __name__)
view_bar_chart = Blueprint("barchart_png", __name__)
view_pie_chart = Blueprint("piechart_png", __name__)

@get_excel_downloadable.route("/ProductsRawData")
def productDownloadExcelData():
    db = Thriftstore()
    sorted_products = db.get_ordered_by_custom_value(
        "Products", "stock", "DESC"
    )

    # Create a dataframe empty structure
    dataDict = {
        "product_name": [],
        "brand": [],
        "apparel_type": [],
        "category": [],
        "source": [],
        "stock": [],
        "price": []
    }

    # Populate the structure
    for product in range(len(sorted_products)):
        dataDict["product_name"].append(sorted_products[product][1])
        dataDict["brand"].append(sorted_products[product][2])
        dataDict["apparel_type"].append(sorted_products[product][3])
        dataDict["category"].append(sorted_products[product][8])
        dataDict["source"].append(sorted_products[product][7])
        dataDict["stock"].append(sorted_products[product][4])
        dataDict["price"].append(sorted_products[product][5])

    # Pass into the data frame method to make a dataframe
    dataFrame = pd.DataFrame(dataDict)
    try:
        # Saves the excel data to memory instead of local disk
        bufferData = io.BytesIO()
        dataFrame.to_excel(bufferData, index=True, sheet_name="Products Sorted Data")
        # Sets it such that it is an absolute file positioning
        # Essentially tells the buffer data to start from the first byte or read the start of the file
        bufferData.seek(0)
        # Just returning the bufferData in format of xlsx as response obj so not saved onto local server
        # mimetype is the one for "xlsx" files so that it can return this type of file
        return Response(bufferData, mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
        # Add products data to sheet
    except:
        flash("Error! Unable to download Excel Data")
    
    db.close_connection()
    return redirect("/viewInventoryDashboard")

@view_invent_dashboard.route("/viewInventoryDashboard")
def inventoryDashboard():
    db = Thriftstore()
    # Set all variables
    product_stock, brands = [], []
    supplier_count, distinct_brand_count = 0, 0
    recommendation = False
    targeted_products = []

    # Get all mini panel values to display in dashboard
    products = db.get_all_items("Products")
    for product in range(len(products)):
        product_stock.append(products[product][4])
        if products[product][4] <= 20:
            recommendation = True
            targeted_products.append(products[product][1])
        if products[product][7] == "Suppliers":
            supplier_count += 1
        if products[product][2] not in brands:
            brands.append(products[product][2])
            distinct_brand_count += 1
    
    db.close_connection()
    return render_template("staff_transaction/viewDashboard.html", products_length=len(products), flagged_products=str(targeted_products)[1:-1]
                    ,stock_total=sum(product_stock), supplier_total=supplier_count, brand_total=distinct_brand_count, recommendation=recommendation)

@view_bar_chart.route("/barchart.png")
def barchart_png():
    db = Thriftstore()
    # Use db method to get products in descending order to populate x and y in a presort way
    sorted_products = db.get_ordered_by_custom_value(
        "Products", "stock", "DESC"
    )
    product_names, product_stocks, colours = [], [], []
    supplier_colour = "#212420"
    donation_colour = "#E8A165"
    danger_colour = "#F04D43"
    identifier = ""

    # Assign stock and name and colour appropriately for axises x and y
    for products in range(len(sorted_products)):
        product_stocks.append(sorted_products[products][4])
        if sorted_products[products][7] == "Suppliers":
            identifier = "(S)"
        else:
            identifier = "(D)"
        product_names.append(identifier + " " + sorted_products[products][1])
        colour = ""
        if sorted_products[products][4] > 20:
            if sorted_products[products][7] == "Suppliers":
                colour = supplier_colour
            else:
                colour = donation_colour
        else:
            colour = danger_colour
        colours.append(colour)
    
    # call inventory chart class to create a chart as img
    chart = InventoryChart()
    chart_img = chart.create_bar_chart(
        chart_title="Total Individual Product Stock Count", x=product_names, y=product_stocks,
        xlabel="Total Stock", ylabel= "", direction="horizontal", colours=colours
    )
    # Pass the response as an img to load in html for src img
    db.close_connection()
    return Response(chart_img, mimetype="image/png")

@view_pie_chart.route("/piechart.png")
def piechart_png():
    db = Thriftstore()
    products = db.get_all_items("Products")
    # Assign suppliers and donators ratio for pie chart
    suppliers, donations = 0, 0
    for product in range(len(products)):
        if products[product][7] == "Suppliers":
            suppliers += 1
        else:
            donations +=1

    chart = InventoryChart()
    chart_img = chart.create_pie_chart(
        "Distribution Of Product Source", [suppliers, donations], 
        ["Suppliers", "Donated"], "Source", ["#212420", "#E8A165"]
    )
    db.close_connection()
    return Response(chart_img, mimetype="image/png")