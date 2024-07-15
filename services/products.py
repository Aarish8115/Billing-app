from db_connect import connect 



def productsLists(connection):
    cursor=connection.cursor()
    query="select products.p_id, products.name, measure_unit.unit_name, products.price from products inner join measure_unit on products.unit=measure_unit.p_unit;"
    product_list=[]
    cursor.execute(query)
    for (id,name,unit,price) in cursor:
        product_list.append({
            "product_id":id,
            "product_name":name.title(),
            "product_unit":unit,
            "product_price":price
        })
    return product_list

def addProduct(connection,product):
    cursor=connection.cursor()
    query="insert into products (name,unit,price) values (%s,%s,%s)"
    values=(product["name"],product["unit"],product["price"])

    cursor.execute(query,values)
    connection.commit()
    return None
    

def deleteProduct(connection,productId):
    cursor=connection.cursor()
    query="delete from products where p_id="+productId
    cursor.execute(query)
    connection.commit()
    return None
    

def updateProduct(connection,productId,product):
    cursor=connection.cursor()
    query="update products set name=%s,unit=%s,price=%s where p_id=%i"
    values=(product["name"],product["unit"],product["price"],productId)
    cursor.execute(query,values)
    connection.commit()
    return None
    
