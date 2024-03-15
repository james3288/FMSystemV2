from django.db import models
from sqlcon import SQLcon
# Create your models here.
from .other_functions import ConvertToDate,ConvertToDateOnly, Time_Ago
import os


class Thumbnail_Images(models.Model):
    category = models.CharField('Category', max_length=200)
    thumbnail = models.ImageField(null=True,blank=True)

    def __str__(self):
        return self.category
    
class Items():
    def Facilities(self):
        SQLCON = SQLcon()
        
        if SQLCON.has_connection() == True:
            cursor = SQLCON.connection()
            #cursor.execute(f"select cat_name from tbl_wh_category_type order by cat_name asc")
            cursor.execute('''select distinct
                                a.cat_name
                                from tbl_wh_category_type a order by a.cat_name asc
                            ''')
            
            f = cursor.fetchall()

            items = []

            for facility in f:
                items.append(facility.cat_name)
            return items

        #items = ['Computer Desktop','Computer Laptop','Cellphone','Aircon']
        #return items
    
    def Borrowed(self):

        # fac_items = self.Facilities_Item(category='')
        # no_of_borrowed_items = 0
        
        # for items in fac_items:
        #     if items.status_served_name == 'Serve':
        #         no_of_borrowed_items += 1

        no_of_borrowed_items = self.get_no_of_all_items()
        no = 0

        for x in no_of_borrowed_items:
            no = x.no_of_borrowed

        return no
    
    def Repaired(self):
        no_of_repaired_items = []
        SQLCON = SQLcon()
        if SQLCON.has_connection() == True:
            cursor = SQLCON.connection()
            cursor.execute(f'''select
                                    a.repair_order_id,
                                    a.repair_order_no,
                                    b.custodian_name,
                                    a.problem_encountered,
                                    a.delivered_date,
                                    a.delivered_by,
                                    a.received_by,
                                    c.item_code,
                                    case when d.rep_released_id is null then 'False' else 'True' end as turnovered
                                from tbl_wh_repair_order a
                                left join tbl_wh_location_details b
                                on b.custodian_id = a.custodian_id 
                                left join tbl_wh_item_code c
                                on c.item_code_id = a.item_code_id    
                                left join tbl_wh_repair_released d
                                on d.repair_order_id = a.repair_order_id   
                                where (case when d.rep_released_id is null then 'False' else 'True' end) = 'False'
                                order by delivered_date desc''')
            no_of_repaired_items = cursor.fetchall()

        return no_of_repaired_items
    
    def Vacant(self):
        
        fac_items = self.Facilities_Item(category='')
        no_of_vacant_items = 0
        
        for items in fac_items:
            if items.status_served_name == 'Vacant':
                no_of_vacant_items += 1
    
        return no_of_vacant_items

    def Defective(self):
        # fac_items = self.Facilities_Item(category='')
        # no_of_defective = 0
        
        # for items in fac_items:
        #     if items.status_served_name == 'Disposed' or items.status_served_name == 'For Disposal':
        #         no_of_defective += 1
        no_of_defective = []
        SQLCON = SQLcon()
        if SQLCON.has_connection() == True:
            cursor = SQLCON.connection()
            cursor.execute(f'''             
            select count(*) as defective
			from tbl_wh_custodian_info a
			left join tbl_wh_item_code b                 on a.item_code_id      = b.item_code_id
			left join tbl_wh_item_name_desc c            on a.item_name_desc_id = c.item_name_desc_id
			left join tbl_wh_category_type d             on c.cat_type_id       = d.cat_type_id
			left join tbl_wh_status_served e             on a.status_served_id  = e.status_served_id
			left join tbl_wh_borrower_slip f             on f.custodian_id      = a.custodian_id
			left join tbl_wh_sched_maint g               on g.sm_id             = a.sm_id
			left join tbl_wh_update_status_sched_maint h on g.sm_id             = h.sm_id
			left join tbl_wh_ontime_fac_maint j          on a.fac_maint_id      = j.fac_maint_id
			left join tbl_wh_system_specs k              on c.item_name_desc_id = k.item_name_desc_id			
			where (a.status_served_id <> 1 and c.cat_sub_main = 'main')
            AND e.status_served_name = 'For Disposal'
                                        OR 
                                        case 
                                            when (select top 1 aa.repair_order_id from tbl_wh_repair_order aa where aa.item_name_desc_id = c.item_name_desc_id order by aa.repair_order_id desc) in (select repair_order_id from tbl_wh_repair_released) 
                                                then 
                                                    case
                                                        when (select top 1 aaa.[status] from tbl_wh_repair_released aaa 
                                                        left join tbl_wh_repair_order bbb
                                                        on bbb.repair_order_id = aaa.repair_order_id
                                                        where bbb.item_code_id = b.item_code_id
                                                        order by aaa.date_repaired,aaa.rep_released_id desc) = 'Repaired' then
                                                            'Repaired'
                                                        else
                                                            'Defective'
                                                    end
                                            when c.item_name_desc_id not in (select x.item_name_desc_id from tbl_wh_repair_order x) 
                                                then null
                                            else 'On-going Repair'
                                        end = 'Defective'
            ''')
            no_of_defective = cursor.fetchall()

        xx = 0
        for x in no_of_defective:
            xx = x[0]
        
        return xx

    def get_no_of_all_items(self):
        SQLCON = SQLcon()
        no_of_all_items = []
        if SQLCON.has_connection() == True:

            # cursor = SQLCON.connection()
            # cursor.execute('''select count(*) as no_of_borrowed                             
            #                     from tbl_wh_location_details a
            #                     left join tbl_wh_item_code b                 on a.item_code_id      = b.item_code_id
            #                     left join tbl_wh_item_name_desc c            on a.item_name_desc_id = c.item_name_desc_id
            #                     left join tbl_wh_category_type d             on c.cat_type_id       = d.cat_type_id
            #                     left join tbl_wh_status_served e             on a.status_served_id  = e.status_served_id
            #                     left join tbl_wh_borrower_slip f             on f.custodian_id      = a.custodian_id
            #                     left join tbl_wh_sched_maint g               on g.sm_id             = a.sm_id
            #                     left join tbl_wh_update_status_sched_maint h on g.sm_id             = h.sm_id
            #                     left join tbl_wh_ontime_fac_maint j          on a.fac_maint_id      = j.fac_maint_id
            #                     left join tbl_wh_system_specs k              on c.item_name_desc_id = k.item_name_desc_id                         
            #                     where (a.status_served_id <> 1 and c.cat_sub_main = 'main')
            #                 ''')
            
            cursor = SQLCON.connection()
            cursor.execute('''  select 
                                    COUNT(*) as	no_of_borrowed
                                    from tbl_wh_custodian_info a
                                    left join tbl_wh_item_code b                 on a.item_code_id      = b.item_code_id
                                    left join tbl_wh_item_name_desc c            on a.item_name_desc_id = c.item_name_desc_id
                                    left join tbl_wh_category_type d             on c.cat_type_id       = d.cat_type_id
                                    left join tbl_wh_status_served e             on a.status_served_id  = e.status_served_id
                                    left join tbl_wh_borrower_slip f             on f.custodian_id      = a.custodian_id
                                    left join tbl_wh_sched_maint g               on g.sm_id             = a.sm_id
                                    left join tbl_wh_update_status_sched_maint h on g.sm_id             = h.sm_id
                                    left join tbl_wh_ontime_fac_maint j          on a.fac_maint_id      = j.fac_maint_id
                                    left join tbl_wh_system_specs k              on c.item_name_desc_id = k.item_name_desc_id                                    
                                where (a.status_served_id <> 1 and c.cat_sub_main = 'main')
                            ''')

            no_of_all_items = cursor.fetchall()
        return no_of_all_items
    
    def Recent_Activities(self):
        # activities = [
        #         {'id': 1,'category': 'Desktop', 'item_name': 'Computer Desktop - coreI9', 'rs_no': '0992','status': 'Borrowed','borrowed_by': 'King'},
        #         {'id': 2,'category': 'Desktop', 'item_name': 'Computer Desktop - coreI5', 'rs_no': '0133','status': 'Borrowed','borrowed_by': 'Jophet'},
        #         {'id': 3,'category': 'Laptop', 'item_name': 'Computer Laptop - coreI3', 'rs_no': '22333','status': 'Repaired','borrowed_by': 'Jeoseph'},
        #         {'id': 4,'category': 'Cellphone', 'item_name': 'Cellphone - Iphone 12 Pro', 'rs_no': '11134','status': 'Turnover','borrowed_by': 'Kelvin'},
        # ]


        # return activities
        recent_activities = []
        SQLCON = SQLcon()
        if SQLCON.has_connection() == True:
            cursor = SQLCON.connection()
            # cursor.execute(f'''
            #                     select * from (
            #                         select 
            #                             a.received_by as custodian_name,
            #                             a.delivered_date as dDate,
            #                             a.userLogDate datelog,
            #                             f.item_name,
            #                             f.brand,
            #                             'Under-Repair' as stat,
            #                             c.item_code,
            #                             a.problem_encountered,
            #                             a.received_by,
            #                             '' as details_work_done,
            #                             '' as repaired_by,
            #                             '' as location
            #                         from tbl_wh_repair_order a
            #                         left join tbl_wh_location_details b
            #                         on b.custodian_id = a.custodian_id 
            #                         left join tbl_wh_item_code c
            #                         on c.item_code_id = a.item_code_id    
            #                         left join tbl_wh_repair_released d
            #                         on d.repair_order_id = a.repair_order_id   
            #                         left join tbl_wh_item_code e
            #                         on e.item_code_id = a.item_code_id
            #                         left join tbl_wh_item_name_desc f
            #                         on f.item_name_desc_id = a.item_name_desc_id 


            #                         UNION ALL

            #                         select 
            #                             a.repair_by as repaired_by, 
            #                             a.released_date as dDate,
            #                             a.userLogDate as datelog,
            #                             c.item_name as item_name,
            #                             c.brand as brand,
            #                             a.status as stat,
            #                             d.item_code,
            #                             '' as problem_encountered,
            #                             '' as received_by,
            #                             a.details_work_done,
            #                             a.repair_by as repaired_by,
            #                             '' as location
            #                         from tbl_wh_repair_released a
            #                         left join tbl_wh_repair_order b
            #                         on b.repair_order_id = a.repair_order_id 
            #                         left join tbl_wh_item_name_desc c
            #                         on c.item_name_desc_id = b.item_name_desc_id 
            #                         left join tbl_wh_item_code d
            #                         on d.item_code_id = b.item_code_id 
                           
            #                         UNION ALL
                                    
            #                         select
            #                             a.custodian_name,
            #                             a.date_borrowed as dDate,
            #                             d.log_date as datelog,
            #                             c.item_name as item_name,
            #                             c.brand as brand,
            #                             e.status_served_name as stat,
            #                             b.item_code,
            #                             '' as problem_encountered,
            #                             '' as received_by,
            #                             '' as details_work_done,
            #                             '' as repaired_by,
            #                             a.borrowed_for as location
            #                         from tbl_wh_location_details a 
            #                         left join tbl_wh_item_code b
            #                         on b.item_code_id = a.item_code_id 
            #                         left join tbl_wh_item_name_desc c
            #                         on c.item_name_desc_id = a.item_name_desc_id 
            #                         left join tbl_wh_item_code_history d
            #                         on d.item_name_desc_id = a.item_name_desc_id 
            #                         left join tbl_wh_status_served e
            #                         on e.status_served_id = a.status_served_id  
            #                     ) AA
            #                     ORDER BY AA.datelog desc''')
            cursor.execute(f'''
                select * from (
                                    select 
                                        a.received_by as custodian_name,
                                        a.delivered_date as dDate,
                                        a.userLogDate datelog,
                                        f.item_name,
                                        f.brand,
                                        'Under-Repair' as stat,
                                        c.item_code,
                                        a.problem_encountered,
                                        a.received_by,
                                        '' as details_work_done,
                                        '' as repaired_by,
                                        '' as location
                                    from tbl_wh_repair_order a
                                    left join tbl_wh_location_details b
                                    on b.custodian_id = a.custodian_id 
                                    left join tbl_wh_item_code c
                                    on c.item_code_id = a.item_code_id    
                                    left join tbl_wh_repair_released d
                                    on d.repair_order_id = a.repair_order_id   
                                    left join tbl_wh_item_code e
                                    on e.item_code_id = a.item_code_id
                                    left join tbl_wh_item_name_desc f
                                    on f.item_name_desc_id = a.item_name_desc_id 


                                    UNION ALL

                                    select 
                                        a.repair_by as repaired_by, 
                                        a.released_date as dDate,
                                        a.userLogDate as datelog,
                                        c.item_name as item_name,
                                        c.brand as brand,
                                        a.status as stat,
                                        d.item_code,
                                        '' as problem_encountered,
                                        '' as received_by,
                                        a.details_work_done,
                                        a.repair_by as repaired_by,
                                        '' as location
                                    from tbl_wh_repair_released a
                                    left join tbl_wh_repair_order b
                                    on b.repair_order_id = a.repair_order_id 
                                    left join tbl_wh_item_name_desc c
                                    on c.item_name_desc_id = b.item_name_desc_id 
                                    left join tbl_wh_item_code d
                                    on d.item_code_id = b.item_code_id 
                           
                                    UNION ALL
                                    
                                    select
                                        a.custodian_name,
                                        a.date_borrowed as dDate,
                                        d.log_date as datelog,
                                        c.item_name as item_name,
                                        c.brand as brand,
                                        e.status_served_name as stat,
                                        b.item_code,
                                        '' as problem_encountered,
                                        '' as received_by,
                                        '' as details_work_done,
                                        '' as repaired_by,
										dbo.funct_get_multiple_charges_custodian_id(a.custodian_id,1) as location
                                    from tbl_wh_custodian_info a 
                                    left join tbl_wh_item_code b
                                    on b.item_code_id = a.item_code_id 
                                    left join tbl_wh_item_name_desc c
                                    on c.item_name_desc_id = a.item_name_desc_id 
                                    left join tbl_wh_item_code_history d
                                    on d.item_name_desc_id = a.item_name_desc_id 
                                    left join tbl_wh_status_served e
                                    on e.status_served_id = a.status_served_id  
                                ) AA
                                ORDER BY AA.datelog desc
            ''')
            activities = cursor.fetchall()

            recent_activities = []

            for x in activities:
                recent_activities.append({
                    'custodian_name': x.custodian_name,
                    'my_date': ConvertToDate(x.dDate),
                    'date_log': Time_Ago(x.datelog),
                    'item_code': x.item_code,
                    'item_name': x.item_name,
                    'brand': x.brand,
                    'status': x.stat,
                    'problem_encountered': x.problem_encountered,
                    'received_by': x.received_by,
                    'details_work_done': x.details_work_done,
                    'repaired_by': x.repaired_by,
                    'location': x.location,
                })

        return recent_activities

    def Supplier_Price_Update(self):
        price_update = []
        price_update = [
                {'id':1, 'items': 'Computer Desktop - coreI9', 'supplier': 'FasTech', 'price':'P50,000', 'date': '06/01/2023','img_path': 'assets/img/computer.png'},
                {'id':2, 'items': 'Computer Desktop - coreI3', 'supplier': 'Columbia', 'price':'P34,000', 'date': '05/29/2023','img_path': 'assets/img/computer.png'},
                {'id':3, 'items': 'Computer Laptop - coreI9', 'supplier': 'Datalan', 'price':'P70,000', 'date': '05/28/2023','img_path': 'assets/img/laptop.png'},
                {'id':4, 'items': 'Cellphone - Iphone Max Pro', 'supplier': 'King Tech', 'price':'P68,000', 'date': '05/28/2023','img_path': 'assets/img/chat.png'},
                {'id':5, 'items': 'Cellphone - vivo Y36 - 8BG', 'supplier': 'King Tech', 'price':'P32,000', 'date': '05/25/2023','img_path': 'assets/img/chat.png'}
        ]
        return price_update
    
        # SQLCON = SQLcon()
        # if SQLCON.has_connection() == True:
        #     cursor = SQLCON.connection()
        #     cursor.execute(f'''select
        #                         a.rr_item_id,
        #                         b.rs_no, 
        #                         f.Supplier_Name, 
        #                         h.item_code,
        #                         i.cat_name,
        #                         d.whItemDesc,
        #                         g.item_name,
        #                         g.brand,
        #                         c.amount,
        #                         e.date_received
        #                     from dbreceiving_items a
        #                     left join dbrequisition_slip b
        #                     on b.rs_id = a.rs_id 
        #                     left join dbreceiving_items_sub c
        #                     on c.rr_item_id = a.rr_item_id 
        #                     left join dbwarehouse_items d
        #                     on d.wh_id = b.wh_id 
        #                     left join dbreceiving_info e
        #                     on e.rr_info_id = a.rr_info_id 
        #                     left join dbSupplier f
        #                     on f.Supplier_Id = e.supplier_id
        #                     left join tbl_wh_item_name_desc g
        #                     on g.rs_no = b.rs_no 
        #                     left join tbl_wh_item_code h
        #                     on h.item_code_id = g.item_code_id 
        #                     left join tbl_wh_category_type i
        #                     on i.cat_type_id = g.cat_type_id where i.cat_name = 'Desktop'
        #                    ''')
            
        #     data = cursor.fetchall()

        #     price_update = []

        #     for x in data:
        #         price_update.append({
        #                 'id': x.rr_item_id,
        #                 'items': x.brand,
        #                 'supplier': x.Supplier_Name,
        #                 'price': x.amount,
        #                 'date': x.date_received,
        #                 'img_path':'assets/img/computer.png',
        #             })
        
        # return price_update
       
    def Receiving_History(self, **kwargs):
        
        SQLCON = SQLcon()
        if SQLCON.has_connection() == True:
            cursor = SQLCON.connection()
            cursor.execute(f'''select 
                                    a.rr_item_id,
                                    b.rs_no, 
                                    f.Supplier_Name, 
                                    d.whItem,
                                    d.whItemDesc,
                                    b.item_desc,
                                    c.amount,
                                    e.date_received,
                                    b.type_of_purchasing,
                                    h.item_code 
                                from dbreceiving_items a
                                left join dbrequisition_slip b
                                on b.rs_id = a.rs_id 
                                left join dbreceiving_items_sub c
                                on c.rr_item_id = a.rr_item_id 
                                left join dbwarehouse_items d   
                                on d.wh_id = b.wh_id 
                                left join dbreceiving_info e
                                on e.rr_info_id = a.rr_info_id 
                                left join dbSupplier f
                                on f.Supplier_Id = e.supplier_id 
								left join tbl_wh_item_name_desc g
								on g.rs_no = b.rs_no 
								left join tbl_wh_item_code h
								on h.item_code_id = g.item_code_id 
                                where 
                                b.rs_no = '{kwargs['rs_no']}'
                                order by e.date_received desc
                           ''')
            
            data = cursor.fetchall()

            receiving = []

            for x in data:           
                receiving.append({
                        'id': x.rr_item_id,
                        'supplier': "" if x.Supplier_Name == None else x.Supplier_Name,
                        'item_name': "" if x.whItem == None else x.whItem,
                        'items': ('' if x.item_desc == None else x.item_desc) if x.whItemDesc == None else x.whItemDesc,
                        'price': "P{:,.2f}".format(0 if x.amount is None else x.amount),
                        'date': ConvertToDateOnly(x.date_received),
                        'rs_no': "" if x.rs_no == None else x.rs_no,
                        'type_of_purchasing': "" if x.type_of_purchasing == None else x.type_of_purchasing,
                        'item_code': "" if x.item_code == None else x.item_code,
                    })
                
        return receiving

    def Facilities_Item(self,**kwargs):
        fac_item = []
        SQLCON = SQLcon()
        if SQLCON.has_connection() == True:
            # no_to_display = kwargs['no_to_display']
            
            cursor = SQLCON.connection()
          
            sql_query = '''
                select
				a.item_code_id,
				b.item_code,
				d.cat_type_id,
				d.cat_name as category,
				c.item_name,
				c.item_name_desc_id,
				c.type_maint,
				c.brand,
				c.rs_no,
				c.acqui_date,
				CAST(c.qty as varchar(50)) +' '+ c.unit as qty_unit,
				a.date_borrowed,
				f.bs_id,
				f.bs_no,
				a.custodian_id,
				a.custodian_name,
				(select top 1 borrowed_to from tbl_wh_multi_location where custodian_id = a.custodian_id) as borrowed_to,
				dbo.funct_get_multiple_charges_custodian_id(a.custodian_id,1) as borrowed_for,
				dbo.funct_get_multiple_charges_custodian_id(a.custodian_id,2) as location,
				a.status_item,
				e.status_served_name,
				c.cat_sub_main,
				g.date_schedule,
				g.sm_id,
				j.fac_maint_id,
				h.ussm_id,
				CASE
					WHEN h.ussm_id is null Or h.ussm_id = '' THEN CONVERT(varchar, g.date_schedule, 101) 
					ELSE 'Waiting for the next sched...'
				END as date_schedule_final,
				--CASE 
				--	WHEN j.date_maint is null THEN CONVERT(varchar, j.date_maint, 101)
				--	ELSE j.date_maint
				--END as last_date_maint, 
				j.date_maint as last_date_maint,
				j.performed_by,
				j.verified_by,
				
				case 
					when (select top 1 aa.repair_order_id from tbl_wh_repair_order aa where aa.item_name_desc_id = c.item_name_desc_id order by aa.repair_order_id desc) in (select repair_order_id from tbl_wh_repair_released) 
                        then 
                            case
                                when (select top 1 aaa.[status] from tbl_wh_repair_released aaa 
                                left join tbl_wh_repair_order bbb
                                on bbb.repair_order_id = aaa.repair_order_id
                                where bbb.item_code_id = b.item_code_id
                                order by aaa.date_repaired,aaa.rep_released_id desc) = 'Repaired' then
                                    'Repaired'
                                else
                                    'Defective'
                            end
					when c.item_name_desc_id not in (select x.item_name_desc_id from tbl_wh_repair_order x) 
						then null
					else 'On-going Repair'
				end as repair_status,
				k.sys_specs_id,
                c.acqui_date as acquisition_date,
				c.serial_no,
				(
                    SELECT COUNT(*)
                    FROM tbl_wh_repair_order aa
                    WHERE aa.item_code_id = b.item_code_id
                ) as no_of_repair_history 	

			from tbl_wh_custodian_info a
			left join tbl_wh_item_code b                 on a.item_code_id      = b.item_code_id
			left join tbl_wh_item_name_desc c            on a.item_name_desc_id = c.item_name_desc_id
			left join tbl_wh_category_type d             on c.cat_type_id       = d.cat_type_id
			left join tbl_wh_status_served e             on a.status_served_id  = e.status_served_id
			left join tbl_wh_borrower_slip f             on f.custodian_id      = a.custodian_id
			left join tbl_wh_sched_maint g               on g.sm_id             = a.sm_id
			left join tbl_wh_update_status_sched_maint h on g.sm_id             = h.sm_id
			left join tbl_wh_ontime_fac_maint j          on a.fac_maint_id      = j.fac_maint_id
			left join tbl_wh_system_specs k              on c.item_name_desc_id = k.item_name_desc_id			
			where (a.status_served_id <> 1 and c.cat_sub_main = 'main')'''

            # search by borrowed-items
            if kwargs['category'] == 'borrowed-items':          
                sql_query = sql_query + ''' AND b.item_code LIKE ?
                                            order by a.date_borrowed desc
                                        '''
                
                value = '' if kwargs['search'] == 'undefined' else kwargs['search']
                # value = '' if value == None else value
                cursor.execute(sql_query, ('%' + value + '%',))
                fac_item = cursor.fetchall()

            elif kwargs['category'] == 'all':
                columns = '''
                    b.item_code + ' ' + d.cat_name + ' ' + c.item_name + ' ' + c.brand + ' ' + a.custodian_name'''
                
                search      = '' if kwargs['search'] == 'undefined' else kwargs['search']

                sql_query = sql_query + f'''
                                            AND 
                                            {columns} LIKE ?
                                            order by a.date_borrowed desc
                                        '''
  
                cursor.execute(sql_query,('%' + search + '%',))
                fac_item = cursor.fetchall()

            elif kwargs['category'] == 'defective':
                sql_query = sql_query + '''
                                        AND e.status_served_name = 'For Disposal'
                                        OR 
                                        case 
                                            when (select top 1 aa.repair_order_id from tbl_wh_repair_order aa where aa.item_name_desc_id = c.item_name_desc_id order by aa.repair_order_id desc) in (select repair_order_id from tbl_wh_repair_released) 
                                                then 
                                                    case
                                                        when (select top 1 aaa.[status] from tbl_wh_repair_released aaa 
                                                        left join tbl_wh_repair_order bbb
                                                        on bbb.repair_order_id = aaa.repair_order_id
                                                        where bbb.item_code_id = b.item_code_id
                                                        order by aaa.date_repaired,aaa.rep_released_id desc) = 'Repaired' then
                                                            'Repaired'
                                                        else
                                                            'Defective'
                                                    end
                                            when c.item_name_desc_id not in (select x.item_name_desc_id from tbl_wh_repair_order x) 
                                                then null
                                            else 'On-going Repair'
                                        end = 'Defective'
                                        '''

                cursor.execute(sql_query)
                fac_item = cursor.fetchall()

            else:
             
                # search by categories and search by all      
                columns = '''
                    b.item_code + ' ' + d.cat_name + ' ' + c.item_name + ' ' + c.brand + ' ' + a.custodian_name
                '''

                if 'search' in kwargs:
                    sql_query   = sql_query + f''' AND d.cat_name LIKE ? AND 
                        {columns} LIKE ?
                        order by a.date_borrowed desc
                        '''
                    
                    search      = '' if kwargs['search'] == 'undefined' else kwargs['search']
                    value       = kwargs['category'].replace('-',' ')

                    cursor.execute(sql_query, ('%' + value + '%', '%' + search + '%',))
                    fac_item = cursor.fetchall()

                # search by categories
                else:
             
                    sql_query = sql_query + ''' AND d.cat_name LIKE ?
                        order by a.date_borrowed desc
                        '''
                                
                    value = kwargs['category'].replace('-',' ')
                    cursor.execute(sql_query, ('%' + value + '%',))
                    fac_item = cursor.fetchall()

            # Execute the SQL query with a parameterized query
            # cursor.execute(sql_query, ('%' + value + '%',))
            

        return fac_item

    def Fac_Packages(self, **kwargs):
        SQLCON = SQLcon()
        fac_packages = []
        if SQLCON.has_connection() == True:
            cursor = SQLCON.connection()
            cursor.execute(f'''select 
                                a.item_code_id,
                                b.item_code,
                                d.cat_type_id,
                                d.cat_name,
                                c.item_name,
                                c.item_name_desc_id,
                                c.type_maint,
                                c.brand,
                                c.rs_no,
                                CAST(c.qty as varchar(50)) +' '+ c.unit as qty_unit,
                                a.date_borrowed,
                                f.bs_id,
                                f.bs_no,
                                a.custodian_id,
                                a.custodian_name,
                                (select top 1 borrowed_to from tbl_wh_multi_location where custodian_id = a.custodian_id) as borrowed_to,
                                dbo.funct_get_multiple_charges_custodian_id(a.custodian_id,1) as borrowed_for,
                                '' as location,
                                a.status_item,
                                e.status_served_name,
                                c.cat_sub_main
                            from tbl_wh_custodian_info a
                            left join tbl_wh_item_code b       on a.item_code_id      = b.item_code_id
                            left join tbl_wh_item_name_desc c  on a.item_name_desc_id = c.item_name_desc_id
                            left join tbl_wh_category_type d   on c.cat_type_id       = d.cat_type_id
                            left join tbl_wh_status_served e   on a.status_served_id  = e.status_served_id
                            left join tbl_wh_borrower_slip f   on f.custodian_id      = a.custodian_id
                            where  (a.status_served_id <> 1 and (d.cat_type_id = 1 or d.cat_type_id = 2) and a.status_item <> 'Defective')
                            order by c.item_name asc''')
            fac_packages = cursor.fetchall()

        return fac_packages
    
    def Repair_Order_History(self,**kwargs):

        search = kwargs['item_code'].upper()
        roh = []
        SQLCON = SQLcon()
        if SQLCON.has_connection() == True:
            cursor = SQLCON.connection()


            if search == 'ALL':
                cursor.execute(f'''select
                                        a.repair_order_id,
                                        a.repair_order_no,
                                        b.custodian_name,
                                        a.problem_encountered,
                                        a.delivered_date,
                                        a.delivered_by,
                                        a.received_by,
                                        c.item_code,
                                        c.item_code_id,
                                        isnull(d.rep_released_id,0) as rep_released_id,
                                        case when d.rep_released_id is null then 'False' else 'True' end as turnovered,
                                        a.cellphone_no
                                    from tbl_wh_repair_order a
                                    left join tbl_wh_custodian_info b
                                    on b.custodian_id = a.custodian_id 
                                    left join tbl_wh_item_code c
                                    on c.item_code_id = a.item_code_id    
                                    left join tbl_wh_repair_released d
                                    on d.repair_order_id = a.repair_order_id   
                                    order by delivered_date,a.repair_order_id desc''')
            else:
                cursor.execute(f'''select
                                        a.repair_order_id,
                                        a.repair_order_no,
                                        b.custodian_name,
                                        a.problem_encountered,
                                        a.delivered_date,
                                        a.delivered_by,
                                        a.received_by,
                                        c.item_code,
                                        c.item_code_id,
                                        isnull(d.rep_released_id,0) as rep_released_id,
                                        case when d.rep_released_id is null then 'False' else 'True' end as turnovered,
                                        a.cellphone_no
                                    from tbl_wh_repair_order a
                                    left join tbl_wh_custodian_info b
                                    on b.custodian_id = a.custodian_id 
                                    left join tbl_wh_item_code c
                                    on c.item_code_id = a.item_code_id    
                                    left join tbl_wh_repair_released d
                                    on d.repair_order_id = a.repair_order_id   
                                    where UPPER(c.item_code) = '{search}'
                                    order by delivered_date,a.repair_order_id desc''')
                
            roh = cursor.fetchall()

        return roh
    
    def Repair_Order_Turnover(self,**kwargs):
        search = kwargs['item_code'].upper()
        rot = []
        SQLCON = SQLcon()
        if SQLCON.has_connection() == True:
            cursor = SQLCON.connection()
            cursor.execute(f''' select 
                                    a.rep_released_id,
                                    b.repair_order_id,
                                    a.details_work_done,
                                    a.released_to,
                                    a.repair_by as repaired_by,
                                    a.released_date,
                                    a.date_repaired,
                                    a.status
                                from tbl_wh_repair_released a
                                left join tbl_wh_repair_order b
                                on b.repair_order_id = a.repair_order_id''')
            
            rot = cursor.fetchall()

        return rot
    
    def Borrower_History(self,**kwargs):
        # borrower = [
        #         {'custodian_name': 'Geoseph', 'location': 'DUBAI', 'item_code': 'DT-01', 'bs_no': 'n/a','status': 'Returned','new_custodian': 'King'}, 
        # ]

        search = kwargs['item_code'].upper()
        info = kwargs['info'] 
        
        borrower = []

        SQLCON = SQLcon()
        if SQLCON.has_connection() == True:
            cursor = SQLCON.connection()

            cursor.execute(f'''select
				 a.mto_no,
				 a.from_borrowed_to,
				 a.from_borrowed_for,
				 a.from_Proj_location,
				 a.from_borrowed_by,
				 a.from_date_borrowed,
				 e.cat_name,
                 c.brand,
				 CAST(c.qty as varchar(50)) +' '+ c.unit as qty_unit,
				 c.item_name,
				 b.item_code as from_item_code,
				 d.status_item,
				 d.borrowed_for,
				 d.date_borrowed,
				 d.custodian_name,
				 CASE
					WHEN (select item_code from tbl_wh_item_code where item_code_id = d.item_code_id) =  b.item_code then 'N/A'
					ELSE (select item_code from tbl_wh_item_code where item_code_id = d.item_code_id)
				 END as to_item_code,
				 a.remarks,
				 a.submitted_by,
				 a.submitted_date,
				 a.noted_by,
				 a.noted_date,
				 d.borrowed_to,
				 a.date_log,
				 a.proj_status,
				 f.status_served_name,
				 a.item_code_id,
				 a.custodian_id,
				 a.turn_over_id,
				 (g.fname +' '+ g.lname) as complete_name,
				 (select fname + ' '+ lname from dbregistrationform where user_id = a.userLog_update) as userlog_update,
				 CONVERT(varchar,a.userLog_update_date, 101) as userLog_update_date
			 from tbl_wh_mat_turn_over_report a
			 left join tbl_wh_item_code b        on a.item_code_id      = b.item_code_id
			 left join tbl_wh_item_name_desc c   on a.item_name_desc_id = c.item_name_desc_id
			 left join tbl_wh_location_details d on a.custodian_id      = d.custodian_id
			 left join tbl_wh_category_type e    on c.cat_type_id       = e.cat_type_id
			 left join tbl_wh_status_served f    on d.status_served_id  = f.status_served_id
			 left join dbregistrationform g      on a.userLog_save      = g.user_id
			 where UPPER(b.item_code) = '{ search }'
            ''')
                
            borrower = cursor.fetchall()

        return borrower
    
    def MTO(self,**kwargs):
        search = kwargs['item_code'].upper()
        mto = []
        SQLCON = SQLcon()
        if SQLCON.has_connection() == True:
            cursor = SQLCON.connection()

            cursor.execute(f'''select distinct 
                                    a.mto_no from tbl_wh_mat_turn_over_report a
                                left join tbl_wh_item_code b
                                on b.item_code_id = a.item_code_id 
                                where b.item_code = '{ search }' 
                                order by a.mto_no desc
                           ''')
                
            mto = cursor.fetchall()
        return mto
    
    def SubItemHistory(self,**kwargs):

        id = kwargs['id']

        SQLCON = SQLcon()
        sih = []
        if SQLCON.has_connection() == True:
            cursor = SQLCON.connection()
            cursor.execute(f'''select 
                                c.item_name_desc_id,
                                b.item_code,
                                d.cat_name,
                                c.item_name,
                                a.date_borrowed,
                                a.custodian_name,                        
                                a.custodian_id,
                                c.brand,
                                dbo.funct_get_multiple_charges_custodian_id(a.custodian_id,1) as borrowed_for,
                                (select top 1 borrowed_to from tbl_wh_multi_location where custodian_id = a.custodian_id) as borrowed_to
                            from tbl_wh_custodian_info a
                            left join tbl_wh_item_code b      on a.item_code_id      = b.item_code_id
                            left join tbl_wh_item_name_desc c on a.item_name_desc_id = c.item_name_desc_id
                            left join tbl_wh_category_type d  on c.cat_type_id       = d.cat_type_id
                            where c.item_name_desc_id = {id}
                            order by a.date_borrowed desc
                           ''')
            
            sih = cursor.fetchall()

        return sih
        
    def maintenance_checklist(self):

        SQLCON = SQLcon()
        mc = []
        if SQLCON.has_connection() == True:
            cursor = SQLCON.connection()
            cursor.execute(f'''select distinct
                                h.cat_name
                                ,f.item_code
                                ,g.item_name
                                ,b.performed_by
                                ,b.verified_by
                                ,d.date_schedule
                                ,b.date_maint
                                ,c.date_log
                                ,e.custodian_name
                                ,(select top 1 borrowed_to from tbl_wh_multi_location where custodian_id = e.custodian_id) as borrowed_to
                                ,dbo.funct_get_multiple_charges_custodian_id(e.custodian_id,1) as borrowed_for
                                ,a.fac_maint_id
                            from tbl_wh_fac_maint_checklist a 
                            left join tbl_wh_ontime_fac_maint b           on a.fac_maint_id      = b.fac_maint_id 
                            inner join tbl_wh_update_status_sched_maint c on b.ussm_id           = c.ussm_id
                            inner join tbl_wh_sched_maint d               on c.sm_id             = d.sm_id
                            inner join tbl_wh_custodian_info e			  on d.custodian_id      = e.custodian_id
                            inner join tbl_wh_item_code f                 on d.item_code_id      = f.item_code_id
                            inner join tbl_wh_item_name_desc g            on d.item_code_desc_id = g.item_name_desc_id
                            inner join tbl_wh_category_type h             on g.cat_type_id       = h.cat_type_id
                            order by b.date_maint desc
                           ''')
            
            mc = cursor.fetchall()

        return mc
    
    def maintenance_checklist_details(self):
        SQLCON = SQLcon()
        mcd = []
        if SQLCON.has_connection() == True:
            cursor = SQLCON.connection()
            cursor.execute(f'''select 
                                    a.col_no,
                                    b.Activity,
                                    b.Notes,
                                    a.status_col_no,
                                    a.fac_maint_id from tbl_wh_fac_maint_checklist a
                                left join (select 
                                                'col_'+convert(varchar,aa.[no]) as col_no2,
                                                aa.Activity,
                                                aa.Notes
                                            from tbl_wh_fac_maint_details aa) b
                                on b.col_no2 = a.col_no 
                           ''')
            
            mcd = cursor.fetchall()

        return mcd
    
    def get_rs_no_for_price_update(self,**kwargs):

        SQLCON = SQLcon()
        fac_item = []
        if SQLCON.has_connection() == True:
            # no_to_display = kwargs['no_to_display']
            
            cursor = SQLCON.connection()
            sql_query = '''
                select * from (
                    select distinct
                            c.rs_no,
                            b.item_code,
                            a.date_borrowed
                    from tbl_wh_custodian_info a
                    left join tbl_wh_item_code b                 on a.item_code_id      = b.item_code_id
                    left join tbl_wh_item_name_desc c            on a.item_name_desc_id = c.item_name_desc_id
                    left join tbl_wh_category_type d             on c.cat_type_id       = d.cat_type_id
                    left join tbl_wh_status_served e             on a.status_served_id  = e.status_served_id
                    left join tbl_wh_borrower_slip f             on f.custodian_id      = a.custodian_id
                    left join tbl_wh_sched_maint g               on g.sm_id             = a.sm_id
                    left join tbl_wh_update_status_sched_maint h on g.sm_id             = h.sm_id
                    left join tbl_wh_ontime_fac_maint j          on a.fac_maint_id      = j.fac_maint_id
                    left join tbl_wh_system_specs k              on c.item_name_desc_id = k.item_name_desc_id			
                    where (a.status_served_id <> 1 and c.cat_sub_main = 'main')'''

            if kwargs['category'] == 'borrowed-items':          
                sql_query = sql_query + ''' AND b.item_code LIKE ?''' #order by a.date_borrowed,b.item_code desc
                
                value = kwargs['item_code']
            else:
                sql_query = sql_query + ''' AND d.cat_name LIKE ? or b.item_code LIKE ?''' #order by a.date_borrowed,b.item_code desc
                
                #value = kwargs['category'].replace('-',' ')
                value = kwargs['category']
            sql_query = sql_query + ''') AA order by AA.date_borrowed,AA.item_code desc'''

            # Execute the SQL query with a parameterized query
            cursor.execute(sql_query, ('%' + value + '%','%' + value + '%'))
            fac_item = cursor.fetchall()
   
        return fac_item
        
    def get_all_defective_items(self,**kwargs):
        SQLCON = SQLcon()
        fac_items = []

        if SQLCON.has_connection() == True:
            cursor = SQLCON.connection()
 
            n = 333333
            lof_search = 'Defective'
            search = '' if kwargs.get('search') == 'undefined' else kwargs.get('search')

            print('search',search)
            cursor.execute("EXEC crud_wh_Facility_Maintenance @n=?, @lof_search=?, @search_3=?", (n, lof_search,search))
            
            f = cursor.fetchall()
                
        return f

class NewItems():
    pass