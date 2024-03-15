

from django.db import models
from sqlcon import SQLcon
# Create your models here.

class Items():
  def Facilities_Item(self,**kwargs):

        print(kwargs['category'].upper())

        SQLCON = SQLcon()
        if SQLCON.has_connection() == True:
            cursor = SQLCON.connection()
         
            cursor.execute('''select 
                                    a.item_code_id,
                                    b.item_code,
                                    d.cat_type_id,
                                    d.cat_name as category,
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
                                    a.borrowed_to,
                                    a.borrowed_for,
                                    a.location,
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
                                            then 'Repaired'
                                        when c.item_name_desc_id not in (select x.item_name_desc_id from tbl_wh_repair_order x) 
                                            then null
                                        else 'On-going Repair'
                                    end as repair_status,
                                    
                                    k.sys_specs_id,
                                    c.acqui_date as acquisition_date,
                                    c.serial_no	  
                                                                                 
                                from tbl_wh_location_details a
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

            fac_item = cursor.fetchall()

        return fac_item
   