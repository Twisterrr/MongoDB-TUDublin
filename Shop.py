from pymongo import MongoClient
import pymongo
import json
import datetime

## To display the program Help menu
def client_menu():
    print('You have different options or commands :\n\
        - To view product : /products\n\
        - To view your order : /order\n\
        - To add a new product : /add_product\n\
        - To see the menu : menu\n\
        - To exit : leave\n\
        ')

## Retrieves orders from the DB
def get_order(db, username):
    for doc in db.Orders.find():
        if (doc['shipping']['name'] == username):
            print('\nShipping information : ')
            print('     Name            : ', doc['shipping']['name'])
            print('     Address         : ', doc['shipping']['address'])
            print('\nPayment information :')
            print('     Method          : ', doc['payment']['method'])
            print('     Transaction id  : ', doc['payment']['transaction_id'])
            for prod in doc['products']:
                print('\nProducts in your order : ')
                print('     Quantity        : ', prod['quantity'])
                print('     Name            : ', prod['name'])
                print('     Price           : ', prod['price'])

## Inserting a product in the DB
def insert_product(db, username):
    print_products(db)
    for itm in db.Orders.find():
        if (itm['shipping']['name'] == username):
            print(itm.get('_id'))
            id = itm.get('_id')
    product = input('Please enter the product : ')
    while True:
        try :
            json_product = db.Products.find_one({'name': product})
            if (json_product['qty'] != 0):
                print(json_product)
                break
            else:
                print('We do not have enough stock for this product')
                product = input('Please enter the product : ')
        except:
            print('We do not have this product')
            product = input('Please enter the product : ')
    filter = {'_id': id}
    print(json_product)
    final_json = {
            "quantity": json_product['qty'],
            "name": json_product['name'],
            "price": json_product['price']
              }
    new_value = {"$push": {'products': final_json}}
    db.Orders.update_one(filter, new_value)
    get_order(db, username)

## Print a product from the DB
def print_products(db):
    products = []
    for doc in db.Products.find():
        print(doc['name'])
        products.append(doc['name'])
    for product in products:
        print(product)

## Adding a product in the DB
def add_product(db):
    colors = []
    categories = []
    release_date = str(datetime.date.today())
    print(release_date)
    sku = input('Enter a sku : ')
    name = input('Enter a name : ')
    description = input('Enter a description : ')
    qty = input('Enter a quantity : ')
    price = input('Enter a price : ')
    while True:
        print('Write next to go to next step :')
        color = input(' Enter a color : ')
        if (color == 'next'):
            break
        colors.append(color)
    model_number = input('Enter a model number : ')
    
    weight = input('Enter a weight : ')
    width = input('Enter a width : ')
    height = input('Enter a height : ')
    depth = input('Enter a depth : ')
    while True:
        print('Write next to go to next step :')
        category = input(' Enter a category : ')
        if (category == 'next'):
            break
        categories.append(category)
    json_file = {
        "sku": sku,
        "name": name,
        "description": description,
        "color" : colors,
        "manufacturing_details": {
            "depth": depth,
            "height": height,
            "width": width,
            "weight": weight
        },
        "shipping_details" : {
            "model_number": model_number,
            "release_date": release_date
        },
        "qty": qty,
        "price": price,
        "category": categories
    }
    db.Products.insert_one(json_file)

## Parsing commands for the customer
def parser_command_client(input, db, username):
    if(input == '/menu'):
        client_menu()
    if (input == '/products'):
        print_products(db)
    if (input == '/order'):
        get_order(db, username)
    if (input == '/add_product'):
        insert_product(db, username)

## Parsing commands for the admin
def parser_command_admin(input, db):
    if(input == '/menu'):
        client_menu()
    if (input == '/products'):
        print_products(db)
    if (input == '/add_product'):
        add_product(db)

## Loop
def loop(username, db):
    quit = True
    type_user = True if username != 'Admin' else False
    client_menu()
    while quit:
        input_ = input('Write a command : ')
        if (input_ == 'leave'):
            break
        parser_command_client(input_, db, username) if type_user == True else parser_command_admin(input_,db)
        
## Main Function
def main_terminal():
    username = input('Username : ')
    password = input('Password : ')
    while True:
        try:
            client = MongoClient('mongodb://localhost:27017',
                     username=username,
                     password=password,
                     authSource='shop',
                     authMechanism='SCRAM-SHA-1')
            client.shop.Products.find_one()
            print('You are login as ', username)
            break
        except:
            print('Login or password false')
            username = input('Username : ')
            password = input('Password : ')
    loop(username, client.shop)

if __name__ == "__main__":
    main_terminal()