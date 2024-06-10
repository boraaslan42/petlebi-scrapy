import mysql.connector
import json


def insert_product(product):
    connection = mysql.connector.connect(
        host="localhost", user="root", password="boraaslan", database="take2"
    )

    cursor = connection.cursor()

    sql = "INSERT INTO petlebi (ProductURL, ProductName, ProductBarcode, ProductPrice, ProductStock, ProductImages, Description, SKU, Category, ProductID, Brand) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"

    val = (
        product["Product URL"],
        product["Product Name"],
        product["Product Barcode"],
        product["Product Price"],
        product["Product Stock"],
        ", ".join(product["Product Images"]), # Converting the list to string to store in mySQL
        product["Description"],
        product["SKU"],
        product["Category"],
        product["Product ID"],
        product["Brand"],
    )

    try:

        cursor.execute(sql, val)

        connection.commit()

        print('Product "{}" inserted successfully.'.format(
            product["Product Name"]))

    except mysql.connector.Error as error:
        print("Error inserting product {}:".format(product["Product Name"]), error)

    finally:

        cursor.close()
        connection.close()


index = 1
with open("petlebi_products.json", "r") as file:
    products = json.load(file)
    products = products[:-1]
    len = len(products)

    for product in products:
        print(index, "/", len,end=" ")
        index += 1
        insert_product(product)
