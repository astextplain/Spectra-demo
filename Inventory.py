import pandas as pd
# import os
def order():
    file = r"D:\Dwonloads\inventory.csv"
    data = pd.read_csv(file)
    data1 = pd.DataFrame(data)
    print()
    df = data1[["Item Name", "Price/unit"]]
    print(df)
    print("Select item from above:")

    your_order_input = {}
    n = int(input("number of input:-  ").strip())
    for i in range(n):
        item = input("enter item").strip()
        number_of_item = int(input("enter number of items :-  ").strip())
        your_order_input[item] = number_of_item
    your_order(your_order_input)


def add_item_inventory():
    file = r"D:\Dwonloads\inventory.csv"
    data = pd.read_csv(file)
    data1 = pd.DataFrame(data)
    print(data1)
    x = int(input("How many items to add: "))
    item_name_add_list = []
    item_units_add_list = []
    item_price_add_list = []

    for i in range(x):
        Item_Name = input("Enter Item to add: ")
        item_name_add_list.append(Item_Name)
        Units_Available = int(input("Enter Units Available for the item: "))
        item_units_add_list.append(Units_Available)
        Price_unit = float(input("Enter price for Item_Name: "))
        item_price_add_list.append(Price_unit)
    df = {
        "Item Name": item_name_add_list,
        "Units Available": item_units_add_list,
        "Price/unit": item_price_add_list,
    }
    dataframe = pd.DataFrame(df)
    dataframe.to_csv(file, mode="a", header=False, index=False)
    print("Data appended successfully")


def Authenticate(username, password):
    file = r"D:\Dwonloads\inventory.xlsx"
    user_data = pd.read_excel(file)
    rows = user_data[
        (user_data["username"] == username) & (user_data["password"] == password)
    ]

    if username == "mru":
        print("Successfully Logged in as admin")
        choice = int(input("Want to update item in inventory? Press 1: "))
        if choice == 1:
            print("Updating inventory...")
            add_item_inventory()

    if not rows.empty:
        return True
    else:
        return False


def create_user(username, password):
    file_path = r"D:\Dwonloads\inventory.csv"

    try:
        existing_data = pd.read_excel(file_path)
    except FileNotFoundError:
        existing_data = pd.DataFrame()

    user_data = {"username": [username], "password": [password]}
    new_data = pd.DataFrame(user_data)
    updated_data = pd.concat([existing_data, new_data], ignore_index=True)
    with pd.ExcelWriter(file_path, engine="xlsxwriter") as writer:
        updated_data.to_excel(writer, index=False, sheet_name="Sheet1")

    print("Create successful")


def your_order(your_order_input):
    file = r"D:\Dwonloads\inventory.csv"
    data = pd.read_csv(file)
    data1 = pd.DataFrame(data)
    price = 0
    remaining_item = 0
    stock = []

    print("\n{:<30} | {:<10}".format("Item", "Price"))
    print("-" * 45)

    for item_name, item_quantity in your_order_input.items():
        lower_item_name = item_name.lower()

        if any(data["Item Name"].str.lower() == lower_item_name):

            item_price = data1[data1["Item Name"].str.lower() == lower_item_name][
                "Price/unit"
            ].values[0]
            item_stock = data1[data1["Item Name"].str.lower() == lower_item_name][
                "Units Available"
            ].values[0]

            if item_stock >= item_quantity:
                remaining_item = item_stock - item_quantity
                item_total_price = item_price * item_quantity
                price += item_total_price
                print("{:<30} | RS{:<10.2f}".format(item_name, item_total_price))

                stock.append(remaining_item)
                item_stock -= item_quantity
                data1.loc[
                    data1["Item Name"].str.lower() == lower_item_name, "Units Available"
                ] = remaining_item
                data1.to_csv(file, index=False)

            else:
                print("Not enough stock for {:<30}".format(item_name))

        else:
            print("Oops!! '{}' does not exist in the inventory".format(item_name))

    print("-" * 45)
    print("Total | Rs{:<10.2f}".format(price))
    print("*" * 45)

    print("Remaining stock:", stock)
    a = int(input("Enter [4] to Exit or [1] to proceed to your order: "))
    print()
    if a == 4:
        Exit(a)
    else:
        order()


def Exit(a):
    user_name = input("Enter your username").strip()
    user_password = input("Enter your password").strip()
    result = Authenticate(user_name, user_password)

    if result == True:
        print("Sucessfully log In")
        order()

    else:
        print("Wrong credentilas")


def password_changed(new_password):
    file_path = r"D:\Dwonloads\user_name_password.xls"

    existing_data = pd.read_excel(file_path)

    existing_data = pd.DataFrame()
    existing_data.loc[0, "password"] = new_password
    existing_data.to_excel(file_path, index=False, sheet_name="Sheet1")

    print("Password updated successfully!!")


print()
print("Enter 1 to LogIn")
print()
print("Create Account Enter 2")
a = int(input(""))
if a == 1:

    user_name = input("Enter your username").strip()
    user_password = input("Enter your password").strip()

    if Authenticate(user_name, user_password):
        print("Sucessfully log In")
        password_change = int(
            input("Enter 5 to change your password or anyother key to procedd")
        )
        if password_change == 5:
            new_password = input("Enter your new password")
            password_changed(new_password)
        a = int(input("Enter [4] to Exit or anyother to proceed"))
        print()
        if a == 4:
            Exit(a)
        else:
            order()
    else:
        print("Wrong credentilas")

elif a == 2:
    username = input("Enter your username:   ").strip()
    password = input("Enter your password:   ").strip()
    create_user(username, password)
else:
    print("Invalid_input")






