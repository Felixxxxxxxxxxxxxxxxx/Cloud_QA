
import pymysql
import datetime


class Database(object):

    dbhost=your_server_ip
    dbuser=your_database_uname
    dbpassword=your_database_passwd


    def create_time():                                          

        # generate date
        now_time = datetime.datetime.now()
        date="{2}_{1}_{0}".format(now_time.day,now_time.month,now_time.year)
        return date


    def create_table(table_name,db_name='cancer'):                                                   
        # create table
        db = pymysql.connect(host=Database.dbhost,
                            user=Database.dbuser,
                            password=Database.dbpassword,
                            database=db_name)     
        cursor = db.cursor()

        if table_name == 'Question' :
            #创建新表
            sql = """CREATE TABLE IF NOT EXISTS  %s(
                    Id INT UNSIGNED NOT NULL PRIMARY KEY AUTO_INCREMENT,
                    Question CHAR(255),
                    Answer CHAR(255),
                    Date CHAR(255))AUTO_INCREMENT=1,DEFAULT CHARSET=utf8;"""%(table_name)
        
        elif table_name == 'Fixed_collocation' :
            #创建新表
            sql = """CREATE TABLE IF NOT EXISTS  %s(
                    Id INT UNSIGNED NOT NULL PRIMARY KEY AUTO_INCREMENT,
                    Fixed_collocation CHAR(255),
                    Translation CHAR(255),
                    Example CHAR(255),
                    Date CHAR(255))AUTO_INCREMENT=1,DEFAULT CHARSET=utf8;"""%(table_name)
                
        try:
            cursor.execute(sql)
            db.commit()
        except:
            print('Create table error')
            db.rollback()

        cursor.close()
        db.close()
    

    def insert_value(table_name,db_name='cancer',a='',b='',c=''):
        db = pymysql.connect(host=Database.dbhost,
                            user=Database.dbuser,
                            password=Database.dbpassword,
                            database=db_name
                            )
        cursor = db.cursor()

        #生成日期时间
        now_time = datetime.datetime.now()
        date="{2}_{1}_{0}".format(now_time.day,now_time.month,now_time.year)
        

        if table_name == "Question":

            sql =  'INSERT INTO {}(\
                    Question,\
                    Answer,\
                    Date)\
                    VALUES (%s,%s,%s)'\
                    .format(table_name)
            value=(a,b,date)

        elif table_name == "Fixed_collocation":

            #插入表单
            sql =  'INSERT INTO {}(\
                    Fixed_collocation,\
                    Translation,\
                    Example,\
                    Date)\
                    VALUES (%s,%s,%s,%s)'\
                    .format(table_name)
            value=(a,b,c,date)
        try:
            cursor.execute(sql,value)
            db.commit()
        except:
            print("Insert value error")
            db.rollback()
            
        cursor.close()
        db.close()

    def display_value(n,table_name,db_name='cancer'):
        # 打开数据库连接
        db = pymysql.connect(host=Database.dbhost,
                            user=Database.dbuser,
                            password=Database.dbpassword,
                            database=db_name
                            )
        cursor = db.cursor()

        sql =  'SELECT * FROM {} order by Id desc limit 0,{}'.format(table_name,n)

        try:
            cursor.execute(sql)
            get_row = cursor.fetchall()
            db.commit()

            
        except:
            print("Accquire value error.")
            db.rollback()
            
        cursor.close()
        db.close()
        if table_name == 'Question':
            for i in range(0,int(n)):
                    print("\n"+str(get_row[i][0])+".\nQuestion:\n "+str(get_row[i][1])+"\nAnswer:\n"+str(get_row[i][2]))
        elif table_name == 'Fixed_collocation':
            for i in range(0,int(n)):
                    print("\n"+str(get_row[i][0])+".\n"+str(get_row[i][1])+"\n"+str(get_row[i][2])+"\n"+str(get_row[i][3]))


    def delete_value(n,table_name,db_name='cancer'):
        # 打开数据库连接
        db = pymysql.connect(host=Database.dbhost,
                            user=Database.dbuser,
                            password=Database.dbpassword,
                            database=db_name
                            )
        cursor = db.cursor()



        #插入表单
        sql =  'DELETE FROM {} WHERE ID = {}'.format(table_name,n)

        try:
            cursor.execute(sql)   
            db.commit()
        except:
            print("Delete value error")
            db.rollback()
        
        cursor.close()
        db.close()

    def reload_value(table_name,db_name='cancer'):
        # 打开数据库连接
        db = pymysql.connect(host=Database.dbhost,
                            user=Database.dbuser,
                            password=Database.dbpassword,
                            database=db_name
                            )
        cursor = db.cursor()

        #生成日期时间
        now_time = datetime.datetime.now()
        date="{2}_{1}_{0}".format(now_time.day,now_time.month,now_time.year)


        sql =  'SET @auto_id = 0'

        try:
            cursor.execute(sql)     
        except:
            print("Reload value error")
            db.rollback()
        
        sql =  'UPDATE {} SET {} = (@auto_id := @auto_id + 1)'.format(table_name,"Id")

        try:
            cursor.execute(sql)     
        except:
            print("Reload ID error")
            db.rollback()

        sql = 'ALTER TABLE {} AUTO_INCREMENT = 1'.format(table_name)

        try:
            cursor.execute(sql)     
            db.commit()
        except:
            print("Reload ID error.")
            db.rollback()

        cursor.close()
        db.close()


class do_cmd(object):
    def input(table_name):
        if table_name == 'Question':
            stopword=":q"
            content=""

            print("Please enter the question:(Enter :q to finish entry)")
            for line in iter(input,stopword):
                content=content+line+"\n"
            Question = content
            print("Please enter the answer:(Enter :q to finish entry)")
            content=""
            for line in iter(input,stopword):
                content=content+line+"\n"
            Answer = content
            
            Database.create_table("Question")
            Database.insert_value(a = Question,b = Answer,table_name = 'Question')

        elif table_name == 'Fixed_collocation':
            stopword=":q"
            content=""

            print("Please enter the Fixed collocation:(Enter :q to finish entry)")
            for line in iter(input,stopword):
                content=content+line+"\n"
            Fixed_collocation = content
            print("Please enter the Translation:(Enter :q to finish entry)")
            content=""
            for line in iter(input,stopword):
                content=content+line+"\n"
            Translation = content
            print("Please enter the Example:(Enter :q to finish entry)")
            content=""
            for line in iter(input,stopword):
                content=content+line+"\n"
            Example = content
            
            Database.create_table("Question")
            Database.insert_value(a = Fixed_collocation,b = Translation, c = Example, table_name = 'Fixed_collocation')
    
    def delete_the_last_n_record(table_name):
        n = input("Please enter the record you want to delete:\n ")
        Database.delete_value(n,table_name)
        Database.reload_value(table_name)
    
    def show(table_name):
        n = input("Please enter how many rows you want to see from buttom:\n")
        Database.display_value(n,table_name)



table_number = input("\nChoose a table:\n1. Question.\n2. Fixed_collocation:\nPlease enter the number:\n")
table_state = 0 
while True :

    if table_state == 1:
        table_number = input("\nChoose a table:\n1. Question.\n2. Fixed_collocation:\nPlease enter the number:\n")
        table_state = 0 

    if table_number == '1':
        table_name = 'Question'
        cmd = input("\nYou are now in table Question\nChoose a command:\n1. Insert.\n2. Delete.\n3. Display.\n4. Change a table.\nPlease enter the command:\n")
        if cmd == "1":
            do_cmd.input(table_name)
        elif cmd == "2":
            do_cmd.delete_the_last_n_record(table_name)
        elif cmd == "3":
            do_cmd.show(table_name)
        elif cmd == "4":
            table_state = 1
            
    elif table_number == '2':
        table_name = 'Fixed_collocation'
        cmd = input("\nYou are now in table Fixed_collocation\nChoose a command\n1. Insert.\n2. Delete.\n3. Display.\n4. Change a table.\nPlease enter the command:\n")
        if cmd == "1":
            do_cmd.input(table_name)
        elif cmd == "2":
            do_cmd.delete_the_last_n_record(table_name)
        elif cmd == "3":
            do_cmd.show(table_name)
        elif cmd == "4":
            table_state = 1
    
