from sqlcon import SQLcon
import pyodbc
import random
import string
from datetime import datetime
import json 

class RepairOrderTurnover():
    def insert(self,**kwargs):
        
        data = kwargs['datas']

        print(data)
       
        SQL = SQLcon()
        conn = SQL.connection2()
        cursor = conn.cursor()

        sql = f'''INSERT INTO tbl_wh_repair_released (
                        repair_order_id,
                        repair_by,
                        details_work_done,
                        released_to,
                        released_date,
                        date_repaired,
                        userLogDate,
                        userLog,
                        status
                       ) 
                       VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)'''
        
        rep_id                  = data.get('id')  
        repaired_by             = data.get('repaired_by').replace("'","`")
        details_work_done       = data.get('details_work_done').replace("'","`")
        released_to             = data.get('released_to').replace("'","`")
        released_date           = data.get('turnover_date')
        date_repaired           = data.get('repaired_date')
        userLogDate             = datetime.now()
        userLog                 = data.get('user_id')
        status                  = data.get('status').replace("'","`")

        
        values = (rep_id, 
                  repaired_by, 
                  details_work_done, 
                  released_to, 
                  released_date, 
                  date_repaired, 
                  userLogDate, 
                  userLog,
                  status)
        
        cursor.execute(sql, values)

        conn.commit()
        cursor.close()
        conn.close()

    def update(self,**kwargs):
        data = kwargs['datas']

        SQL = SQLcon()
        conn = SQL.connection2()
        cursor = conn.cursor()


        rep_released_id = data.get('id')

        sql = f'''UPDATE tbl_wh_repair_released 
                    SET repair_by = '{data.get('repaired_by').replace("'","`")}',
                        details_work_done = '{data.get('details_work_done').replace("'","`")}',
                        released_to = '{data.get('released_to').replace("'","`")}',
                        released_date = '{data.get('turnover_date')}',
                        date_repaired = '{data.get('repaired_date')}',
                        status = '{data.get('status')}'
                    WHERE rep_released_id = {rep_released_id}'''
   
        
        cursor.execute(sql)

        conn.commit()
        cursor.close()
        conn.close()

    def delete_repairorder_turnover(self,**kwargs):
        SQL = SQLcon()
        conn = SQL.connection2()
        cursor = conn.cursor()

        rep_released_id = kwargs.get('id')

        sql = f'''delete from tbl_wh_repair_released where rep_released_id = {rep_released_id}''' 
        cursor.execute(sql)

        conn.commit()
        cursor.close()
        conn.close()

    def delete_repairorder(self,**kwargs):
        # DELETE repairorder
        repair_order_id = kwargs.get('id')

        SQL = SQLcon()
        conn = SQL.connection2()
        cursor = conn.cursor()


        sql = f'''delete from tbl_wh_repair_order where repair_order_id = {repair_order_id}''' 
        cursor.execute(sql)

        conn.commit()
        cursor.close()
        conn.close()

    #DELETE repairorder Turnover
# -----------------------------------------------------
        SQL2 = SQLcon()
        conn2 = SQL2.connection2()
        cursor2 = conn2.cursor()

        id = self.get_rep_release_id(id = repair_order_id)

        sql2 = f'''delete from tbl_wh_repair_released where rep_released_id = {id}''' 
        cursor2.execute(sql2)

        conn2.commit()
        cursor2.close()
        conn2.close()

        


    def get_rep_release_id(self,**kwargs) -> int:
        SQLCON = SQLcon()

        if SQLCON.has_connection() == True:
            cursor = SQLCON.connection()
            
            id = kwargs.get('id')
    
            cursor.execute(f'''select top 1 a.rep_released_id from tbl_wh_repair_released a where a.repair_order_id = {id}
                           ''')
                
            datas = cursor.fetchall()

            rep_released_id = 0
            for data in datas:
                rep_released_id = data.rep_released_id

            return rep_released_id
        