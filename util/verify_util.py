from util.connection import cur 

def verify_start_game(host,usr1,usr2,usr3):
    sql = "select count(*) from temp_user where host = '{host}'".format(host= host)
    try:
        cur.execute(sql)
    except Exception as e:
        print(e)
        print(2)
        return False
    
    result = cur.fetchone()

    if(result[0]>=1):
        return host
    
    sql = "select count(*) from current_players where user_id = '{}'".format(host)
    try:
        cur.execute(sql)
    except Exception as e:
        print(e)
        print(3)
        return False
     
    result = cur.fetchone()

    if(result[0]>=1):
        return host
    
    sql1 = "select count(*) from current_players where user_id= '{}'".format(usr1)
    sql2 = "select count(*) from current_players where user_id= '{}'".format(usr2)
    sql3 = "select count(*) from current_players where user_id= '{}'".format(usr3)

    
    
    
    try:
        cur.execute(sql1)
        result1 = cur.fetchone()
        cur.execute(sql2)
        result2 = cur.fetchone()
        cur.execute(sql3)
        result3 = cur.fetchone()

    except Exception as e:
        print(e)
        print(4)
        return False

    if(result1[0]>=1):
        return usr1
    
    if(result2[0]>=1):
        return usr2
    
    if(result3[0]>=1):
        return usr3

    sql1 = "select count(*) from accepted_pending_game where user_id= '{}'".format(usr1)
    sql2 = "select count(*) from accepted_pending_game where user_id= '{}'".format(usr2)
    sql3 = "select count(*) from accepted_pending_game where user_id= '{}'".format(usr3)

    try:
        cur.execute(sql1)
        result1 = cur.fetchone()
        cur.execute(sql2)
        result2 = cur.fetchone()
        cur.execute(sql3)
        result3 = cur.fetchone()

    except Exception as e:
        print(e)
        print(4)
        return False
    
    if(result1[0]>=1):
        return usr1
    
    if(result2[0]>=1):
        return usr2
    
    if(result3[0]>=1):
        return usr3

    return True
