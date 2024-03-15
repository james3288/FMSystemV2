from sqlcon import SQLcon
import pyodbc
import random
import string
from datetime import datetime

class RepairOrder:
    def insert(self,**kwargs):
        data = kwargs['datas']
        repair_order_no = self.generate_repair_order_no()
        #print(data)
       
        SQL = SQLcon()
        conn = SQL.connection2()
        cursor = conn.cursor()

        sql = f'''INSERT INTO tbl_wh_repair_order (
                        custodian_id, 
                        item_code_id, 
                        item_name_desc_id, 
                        problem_encountered, 
                        delivered_by, 
                        delivered_date,
                        repair_order_no,
                        userLogDate,
                        userLog_id,
                        received_by,
                        cellphone_no) VALUES 
                    (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'''
        
        userLog_id          = data.get('user_id')  
        userLogDate         = datetime.now()
        repair_order_no     = repair_order_no
        item_code_id        = data.get('item_code_id')
        problem_encountered = data.get('problem_encountered')
        # recepients          = data.get('recepients')
        delivered_by        = data.get('delivered_by')
        repair_date         = data.get('repair_date')
        custodian_id        = data.get('custodian_id')
        item_name_desc_id   = data.get('item_name_desc_id')
        received_by         = data.get('received_by')
        contact_number      = data.get('contact_number')

        values = (custodian_id,
                  item_code_id,
                  item_name_desc_id, 
                  problem_encountered.replace("'","`"), 
                  delivered_by.replace("'","`"), 
                  repair_date,
                  repair_order_no.replace("'","`"),
                  userLogDate,
                  userLog_id,
                  received_by.replace("'","`"),
                  contact_number
                  )
        
         
        try:
            with conn.cursor() as cursor:
                cursor.execute(sql, values)
                conn.commit()
        except pyodbc.Error as e:
            print(f"An error occurred: {e}")
        finally:
            conn.close()

        # cursor.execute(sql, values)

        # conn.commit()
        # cursor.close()
        # conn.close()

    def update(self,**kwargs):
        data = kwargs['datas']

        SQL = SQLcon()
        conn = SQL.connection2()
        cursor = conn.cursor()

        sql = f'''UPDATE tbl_wh_repair_order 
            SET
                problem_encountered = '{data.get('problem_encountered').replace("'","`")}',
                delivered_by = '{data.get('delivered_by').replace("'","`")}',
                delivered_date = '{data.get('repair_date')}',
                received_by = '{data.get('received_by')}',
                cellphone_no = '{data.get('contact_number')}'
            WHERE repair_order_id = {data.get('id')}'''
        
        cursor.execute(sql)

        conn.commit()
        cursor.close()
        conn.close()

    def generate_repair_order_no(self)->0:
        SQL = SQLcon()
        conn = SQL.connection2()
        cursor = conn.cursor()

        gro = 0

        cursor.execute('select top 1 a.repair_order_id from tbl_wh_repair_order a order by a.repair_order_id desc')
        rows = cursor.fetchall()

        for row in rows:
            gro = row.repair_order_id

        cursor.close()
        conn.close()
        
        result = f'{self.generate_random_letters(5)}-{gro}'
        return result
            
    def generate_random_letters(self,length):
        letters = string.ascii_letters  # Contains all uppercase and lowercase letters
        random_letters = ''.join(random.choice(letters) for _ in range(length))
        return random_letters

