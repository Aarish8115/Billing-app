from flask import Flask,render_template,request,redirect,url_for
from products import productsLists
from receipts import receiptsList
from users import userList
from db_connect import connect
from measure_unit import unit_id,measure_list

# creating a flask app
app=Flask(__name__,template_folder="../templates",static_folder="../static")

connection=connect()
product_list=productsLists(connection)
receipts_list=receiptsList(connect())
user_list=userList(connect())


# home page
@app.route("/")
def home():
    return render_template("index.html")
# products page
@app.route("/products")
def products():
    global connection
    product_list=productsLists(connection)
    unit_list=measure_list(connection)
    return render_template("products.html",product_list=product_list,unit_list=unit_list)

@app.route("/products/add",methods=['POST'])
def addProduct():
    global connection
    cursor=connection.cursor()
    product={}
    product["name"]=request.form.get("name")
    product["unit"]=request.form.get("unit")
    product["price"]=request.form.get("price")
    query="insert into products (name,unit,price) values (%s,%s,%s)"
    values=(product["name"],product["unit"],product["price"])

    cursor.execute(query,values)
    connection.commit()
    return redirect("/products")
    
@app.route(f"/delete-product/<productId>")
def deleteProduct(productId):
    global connection
    cursor=connection.cursor()
    query="delete from products where p_id="+productId
    cursor.execute(query)
    connection.commit()
    return redirect("/products")

@app.route(f"/update-product/<productId>",methods=['POST'])
def updateProduct(productId):
    global connection
    cursor=connection.cursor()
 
    product={}
    product["name"]=request.form.get("name")
    product["unit"]=request.form.get("unit")

    product["price"]=request.form.get("price")
    query="update products set name=%s,unit=%s,price=%s where p_id=%s"
    values=(product["name"],product["unit"],product["price"],productId)

    cursor.execute(query,values)
    connection.commit()
    return redirect("/products")


# receipts page
@app.route("/receipts")
def receipts():
    global connection
    receipts_list=receiptsList(connection)
    return render_template("receipts.html",receipts_list=receipts_list)

@app.route("/receipts/search")
def searchReceipt():
    global connection
    cursor=connection.cursor()
    listId=request.args.get("search")
    if listId:
        query=f"select l_id,u_id,date,amount from lists where l_id like '%{listId}%'"
        cursor.execute(query)
        receipts_list=[]
        for (l_id,u_id,date,amount) in cursor:
            receipts_list.append({
                "bill_id":l_id,
                "user_id":u_id,
                "billing_date":date,
                "bill_amount":amount
            })
    else:
        receipts_list=receiptsList(connection)

    return render_template("receipts.html",receipts_list=receipts_list)

@app.route("/new-receipt")
def new_receipt():
    return render_template("newreceipt.html")

@app.route("/receipts/<listId>")
def receiptDetails(listId):
    global connection
    cursor=connection.cursor()
    query=f"SELECT p_id,quantity,subtotal FROM grocery_app.list_items where l_id={listId}"
    cursor.execute(query)
    listItems=[]
    for p_id,quantity,subtotal in cursor:
        listItems.append({
            "product_id":p_id,
            "quantity":quantity,
            "subtotal":subtotal
        })
    return render_template("list_details.html",listItems=listItems)

#users page
@app.route("/users")
def users():
    global connection
    user_list=userList(connection)
    return render_template("users.html",user_list=user_list)

@app.route("/users/add",methods=['POST'])
def addUser():
    global connection
    cursor=connection.cursor()

    user={}
    user["name"]=request.form.get("name")
    user["mail"]=request.form.get("mail")
    query="insert into users (name,mail) values (%s,%s)"
    values=(user["name"],user["mail"])
    cursor.execute(query,values)
    connection.commit()
    return redirect("/users")

@app.route("/users/search")
def searchUser():
    global connection
    userId=request.args.get("search")
    if userId:
        cursor=connection.cursor()
        query=f"SELECT * FROM grocery_app.users where u_id like '%{userId}%'"
        user_list=[]
        cursor.execute(query)
        for (id,name,mail) in cursor:
            user_list.append({
                "user_id":id,
                "user_name":name.title(),
                "user_mail":mail
            })
        return render_template("users.html",user_list=user_list)
    else:
        return redirect("/users")
    
@app.route("/users/lists")
def userLists():
    global connection
    userId=request.args.get("user_id")
    cursor=connection.cursor()
    query=f"SELECT l_id,date,amount FROM grocery_app.lists where u_id={userId}"
    cursor.execute(query)
    ulist=[]
    for l_id,date,amount in cursor:
        ulist.append({
            "list_id":l_id,
            "date":date,
            "amount":amount
        })

    return render_template("user_receipts.html",ulist=ulist)

if __name__=="__main__":
    app.run()
