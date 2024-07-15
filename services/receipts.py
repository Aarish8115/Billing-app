from db_connect import connect
import datetime

def receiptsList(connection):
    cursor=connection.cursor()
    query="select l_id,u_id,date,amount from lists"
    cursor.execute(query)
    receipts_list=[]
    for (l_id,u_id,date,amount) in cursor:
        receipts_list.append({
            "bill_id":l_id,
            "user_id":u_id,
            "billing_date":date,
            "bill_amount":amount
        })
    return receipts_list

def receipt_items(connection,listId):
    cursor=connection.cursor()
    query="select p_id,quantity,subtotal from list_items where l_id="+str(listId)
    cursor.execute(query)
    list_items_list=[]
    for (p_id,quantity,subtotoal) in cursor:
        list_items_list.append({
            "product_id":p_id,
            "quantity":quantity,
            "subtotal":subtotoal
        })
    query="select sum(subtotal) from list_items where l_id="+str(listId)
    cursor.execute(query)
    total=cursor.fetchone()[0]
    return list_items_list,total

