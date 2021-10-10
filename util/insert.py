from discord import user
from util.connection import cur,conn

def insert_new_temp(host,usr1,usr2,usr3):

    sql = "insert into temp_user(user1_id,user2_id,user3_id,host) values ('{user1}','{user2}','{user3}','{host}');".format(user1=usr1,user2=usr2,user3=usr3,host=host)
    try:
        cur.execute(sql)
        conn.commit()
        return True
    except Exception as e:
        print(e)
        print('12')
        return False

def pick_chit(usr,host):
    sql_user_pending =  f"select count(*) from accepted_pending_game where user_id = '{usr}';"
    sql_user_current = f"select count(*) from current_players where user_id = '{usr}';"
    sql_host_temp = f"select user1_id,user2_id,user3_id,host from temp_user where host = '{host}';"
    sql_host_temp_count = f"select count(*) from temp_user where host = '{host}';"

    try:
        cur.execute(sql_user_pending)
        result = cur.fetchone()
        print(result[0])
        if(result[0] != 0):
            return False
        cur.execute(sql_user_current)
        result = cur.fetchone()
        print(result[0])
        if(result[0] != 0):
            return False
        cur.execute(sql_host_temp)
        results = cur.fetchone()
        cur.execute(sql_host_temp_count)
        resu = cur.fetchone()
        if(resu[0] != 1):
            return host
        if str(usr) not in set(results):
            print(set(results))
            print('not in game')
            return 'no game'
    except Exception as e:
        print(e)
        print('13')
        return None
    us_in = results.index(str(usr))+1
    updt_sql = f"update temp_user SET user{us_in}_status = {True} where host = '{host}';"
    updt = f"insert into accepted_pending_game (user_id) values('{usr}');"
    try:
        cur.execute(updt_sql)
        conn.commit()
        cur.execute(updt)
        conn.commit()
    except Exception as e:
        print(e)
        print(11)
        return None
    
    sql_user_temp = f"select user1_status,user2_status,user3_status from temp_user where host = '{host}';"

    try:
        cur.execute(sql_user_temp)
        result = cur.fetchone()
        if((result[0] == True) and (result[1] == True) and (result[2] == True)):
            updt = f"delete from accepted_pending_game where user_id= '{results[0]}' or user_id = '{results[1]}' or user_id = '{results[2]}';"
            
            try:
                cur.execute(updt)
                conn.commit()
                return True
            except:
                return None
        else:
            return 'accpted'

    except:
        return None

def start_game(character,host):
    sql = f"select user1_id,user2_id,user3_id,host from temp_user where host = '{host}';"
    try:
        cur.execute(sql)
        users = cur.fetchone()
    except:
        print(15)
        return None
    
    sql = f"insert into game (user1,user2,user3,user4,user1_character,user2_character,user3_character,user4_character) values ('{users[0]}','{users[1]}','{users[2]}','{users[3]}','{character[0]}','{character[1]}','{character[2]}','{character[3]}');"
    
    try:
        cur.execute(sql)
        conn.commit()
        sql = f"delete from temp_user where host = '{host}'"
        cur.execute(sql)
        conn.commit()
        resp = [{'usr':users[0],'chr':character[0]},{'usr':users[1],'chr':character[1]},{'usr':users[2],'chr':character[2]},{'usr':users[3],'chr':character[3]}]
        sql = f"insert into current_players (user_id) values ('{users[0]}'),('{users[1]}'),('{users[2]}'),('{users[3]}');"
        cur.execute(sql)
        conn.commit()
        return resp
    except:
        print(14)
        return None

    

def ans_mantri(mantri,thief):
    sql_verify = f"select count(*) from game where user1 = '{mantri}' OR user2 = '{mantri}' OR user3 = '{mantri}' OR user4 = '{mantri}';"
    sql_user = f"select user1,user2,user3,user4 from game where user1 = '{mantri}' OR user2 = '{mantri}' OR user3 = '{mantri}' OR user4 = '{mantri}';"
    sql_char = f"select user1_character,user2_character,user3_character,user4_character from game where user1 = '{mantri}' OR user2 = '{mantri}' OR user3 = '{mantri}' OR user4 = '{mantri}';"
    try:
        cur.execute(sql_verify)
        resu_verify = cur.fetchone()
        if(resu_verify[0] != 1):
            return False
        cur.execute(sql_user)
        users = cur.fetchone()
        cur.execute(sql_char)
        char= cur.fetchone()
    except:
        print(17)
        return None
    thief_index = char.index('CHOR')
    mantri_index = char.index('MANTRI')
    if str(mantri) != str(users[mantri_index]):
        return False
    if str(thief) in str(users[thief_index]):
        sql_del_curr_play = f"delete from current_players where user_id = '{users[0]}' OR user_id = '{users[1]}' OR user_id = '{users[2]}' OR user_id = '{users[3]}';"
        sql_del__game = f"delete from game where user1 = '{mantri}' OR user2 = '{mantri}' OR user3 = '{mantri}' OR user4 = '{mantri}';"
        try:
            cur.execute(sql_del_curr_play)
            conn.commit()
            cur.execute(sql_del__game)
            conn.commit()
        except Exception as e:
            print(e)
            print(19)
            return None
        
        raja_index = char.index('RAJA')
        sipahi_index = char.index('SIPAHI')
        char_point = [1,2,3,4]
        char_point[raja_index] = 1000
        char_point[sipahi_index] = 500

        if str(thief) == str(users[thief_index]):
            char_point[mantri_index] = 800
            char_point[thief_index] =0
            resp = [True,{'usr':users[0],'chr':char[0]},{'usr':users[1],'chr':char[1]},{'usr':users[2],'chr':char[2]},{'usr':users[3],'chr':char[3]},users[thief_index]]
            return resp
        else:
            char_point[mantri_index] = 0
            char_point[thief_index] =800
            resp = [False,{'usr':users[0],'chr':char[0]},{'usr':users[1],'chr':char[1]},{'usr':users[2],'chr':char[2]},{'usr':users[3],'chr':char[3]},users[thief_index]]
            return resp