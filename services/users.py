from db_connect import connect 

def userList(connection):
    cursor=connection.cursor()
    query="select * from users"
    user_list=[]
    cursor.execute(query)
    for (id,name,mail) in cursor:
        user_list.append({
            "user_id":id,
            "user_name":name.title(),
            "user_mail":mail
        })
    return user_list


def addUser(connection,user):
    cursor=connection.cursor()
    query="insert into users (name,mail) values (%s,%s)"
    values=(user["name"],user["mail"])
    cursor.execute(query,values)
    connection.commit()
    return None
