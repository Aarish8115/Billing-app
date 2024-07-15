from db_connect import connect 

def measure_list(connection):
    cursor=connection.cursor()
    query="select * from measure_unit"
    measure_list=[]
    cursor.execute(query)
    for (id,name) in cursor:
        measure_list.append({
            "unit_id":id,
            "unit_name":name.title(),
        })
    return measure_list

def unit_id(connection,unit):
    cursor=connection.cursor()
    query="select * from measure_unit"
    cursor.execute(query)
    unitList=cursor.fetchall()
    for row in unitList:
        if unit==row[1]:
            uid=row[0]
        else: uid=1
    return uid

def id_unit(connection,uid):
    cursor=connection.cursor()
    query="select * from measure_unit"
    cursor.execute(query)
    unitList=cursor.fetchall()
    for row in unitList:
        if uid==row[0]:
            unit=row[0]
    return unit
