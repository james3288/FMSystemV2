from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import Items
import math
import json
from .serializers import ItemSerializer
import datetime 
import pyodbc 
from sqlcon import SQLcon
from .repair_order_insert import RepairOrder
from .repair_order_turnover import RepairOrderTurnover
from django.http import JsonResponse
from .encrypt_decrypt import encrypt_number,decrypt_number,generate_random_letters
import base64
import random
import os
from .models import Thumbnail_Images
from django.db.models.fields.files import ImageFieldFile
from django.core import serializers
from django.core.serializers import serialize
from .other_functions import kwargs_exist,Time_Ago


# Create your views here.
def LoginPage(request):
    context = my_context()
    item_category = {'category': 'Dashboard','pages': 'Dashboard'}   
    context.update(item_category)

    if request.method == 'POST':
        
        username = request.POST["username"].replace("'","`")
        password = request.POST["password"].replace("'","`")

        #user = authenticate(request, username=username, password=password)

        SQLCON = SQLcon()
        if SQLCON.has_connection() == True:
            cursor = SQLCON.connection()
            cursor.execute(f"select * from dbregistrationform where username = '{username}' and password = '{password}'")
            users = cursor.fetchall()

            if len(users) > 0:             
                if 'user_id' not in request.session:   
                    for user in users:

                        request.session['user_id'] = user.user_id
                        request.session['username'] = user.username
                        request.session['fname'] = user.fname.title()
                        request.session['lname'] = user.lname.title()
                        request.session['restriction'] = user.restriction.title()
                        request.session['position'] = 'Web Developer' if user.user_id == 91 else 'Guest'
                        request.session['gender'] = user.gender.title()

                    return render(request, 'fmsLogin/index.html', context)
                    #return redirect('/menu/')
            
            else:             
                new_context = {'message': 'Invalid username or password'}      
                return render(request, 'fmsLogin/pages-login.html',new_context)
            
                #return redirect('login/')
            
        #     login(request, user) 
        #     context = {}
        #     #context = {'user_data': user}
        #     # Redirect to a success page.
        #     return render(request, 'fmsLogin/index.html',context)
        # else:
        #     # Return an 'invalid login' error message.
        #     return render(request, 'fmsLogin/pages-login.html',{})
    
    else: 
        #request.session.flush()
        if 'user_id' in request.session:      
            return render(request, 'fmsLogin/index.html',context)
            #return redirect('/menu/')     
        else:
            return render(request, 'fmsLogin/pages-login.html',{})
           
def LogoutPage(request,log_out='False'):
    
    if log_out == 'True':
        request.session.flush()
        return redirect('/login/')
    else:
        #return redirect('/menu/')
        items = Items()    
        
        context = {
                    'facilities': items.Facilities(),
                    'borrowed': items.Borrowed(),
                    'repaired': items.Repaired(),
                    }   
         
        return render(request, 'fmsLogin/index.html',context)
    
        #return render(request, 'fmsLogin/pages-login.html',{})
   
def DashboardPage(request):
    context = my_context()

    items = Items()
    price_update  = items.get_rs_no_for_price_update(category='',no_to_display=0)
    price_update_filter = [item[0] for item in price_update if item[0].lower() != 'n/a']
    
    receiving = []
    
    for x in price_update_filter[0:5]:
        receiving.append(items.Receiving_History(rs_no = x))

    # activities = Items.Recent_Activities()
    # print(activities)
    # print(receiving)

    return JsonResponse({"dashboard_data": context, "updated_price": receiving})

#DASHBOARD PAGE
def IndexPage(request):
    context = my_context()
    item_category = {'category': 'Dashboard','pages': 'Dashboard'}   
    context.update(item_category)

    if 'user_id' in request.session:  

        return render(request, 'fmsLogin/index.html',context)
        #return redirect('/menu/')     
    else:
        return redirect('/login/')
        #return render(request, 'fmsLogin/pages-login.html',{})

def MenuPage(request):
    if 'user_id' in request.session:      
        return render(request, 'fmsLogin/index.html',my_context())  
    else:
        return redirect('/login/')
        #return render(request, 'fmsLogin/pages-login.html',{})

def MainMenuPage(request):
    return render(request, 'fmsLogin/menu.html',{})

def FacilitiesPage(request,**kwargs):
    false_slugify = {'doublesingle-burner-stove': 'double/single-burner-stove'}

    # this code is for false slugify like / and other characters
    if 'category' in kwargs and kwargs['category'] in false_slugify:
        kwargs['category'] = false_slugify[kwargs['category']]
    
    if 'user_id' in request.session:   
  
        context     = my_context()
        items       = Items()

        item_code=kwargs['item_code'] if 'item_code' in kwargs else None
   
        # if 'item_code' in kwargs:
        #     item_code = kwargs['item_code']
        # else:
        #     item_code = 'None'

        facilities  = items.Facilities_Item(category=kwargs['category'].replace("'","`"),item_code=item_code)

        packages    = items.Fac_Packages(category=None)

        request.session['current_page'] = kwargs['page'] 
        request.session['page_range']   = int(kwargs['page']) * 10 

        count_pages                     = range(int(math.ceil(len(facilities)/10))+1)
        count_from                      = request.session['page_range'] - 9
        count_all_items                 = len(facilities)
        last_page                       = list(count_pages)[-1]
        request.session['next_page']    = request.session['current_page'] + 1
        request.session['prev_page']    = request.session['current_page'] - 1
        image_path                      = "assets/img/laptop.png"
             
        dic = {}
        dic2 = {}

        l = []
        p = []

        serializer = ItemSerializer(facilities, many=True)
        serialized_data = serializer.data
        
        myImages = Thumbnail_Images.objects.all()

        #Loop for Item Facilities
        for x in facilities:
            random_number = f'{x.item_code_id}{generate_random_letters(5)}'

            rs_no = None 
            if x.rs_no == None:
                rs_no = "None"
            elif x.rs_no.upper() == 'N/A':
                rs_no = "None"
            else:
                rs_no = x.rs_no

            receiving = items.Receiving_History(rs_no = rs_no)

            thumbnails = None
            for img in myImages:
                if img.category == x.category:
                    thumbnails = str(img.thumbnail.url)
        
            l.append({
                'random_item_code_id': 0 if x.item_code_id == None else x.item_code_id,
                'item_code_id': 0 if x.item_code_id == None else x.item_code_id,
                'custodian_id': 0 if x.custodian_id == None else x.custodian_id,
                'item_code': "" if x.item_code == None else x.item_code,
                'item_name': "" if x.item_name == None else x.item_name,
                'item_name_desc_id': 0 if x.item_name_desc_id == None else x.item_name_desc_id,
                'category': "" if x.category == None else x.category,
                'brand': "" if x.brand == None else x.brand,
                'custodian_name': "" if x.custodian_name == None else x.custodian_name,
                'borrowed_for': "" if x.borrowed_for == None else x.borrowed_for,
                'status_served_name': "" if x.status_served_name == None else x.status_served_name,
                'date_schedule_final': "" if x.date_schedule_final == None else convertToDate(x.date_schedule_final),
                'last_date_maint': "" if x.last_date_maint == None else convertToDate(x.last_date_maint),
                'location': "" if x.location == None else x.location,
                'date_borrowed': "" if x.date_borrowed == None else convertToDate(x.date_borrowed),
                'acquisition_date': "" if x.acquisition_date == None else convertToDate(x.acquisition_date),
                'rs_no': "" if x.rs_no == None else x.rs_no,
                'bs_no': "" if x.bs_no == None else x.bs_no,
                'serial_no': "" if x.serial_no == None else x.serial_no,
                'search': f'{"" if x.item_name == None else x.item_name} {x.brand} {x.item_code} {x.category} {x.custodian_name} {x.location} {x.rs_no} {x.bs_no} {x.borrowed_for}',
                'no_of_repair_history' : 0 if x.no_of_repair_history == None else x.no_of_repair_history,
                'repair_status':"" if x.repair_status == None else x.repair_status,
                'receiving_data': receiving,
                'no_of_borrowed': len(items.MTO(item_code=x.item_code)), 
                'img': 'default.jpg' if thumbnails == None else thumbnails,
                #Time_Ago(convertToDate(x.date_borrowed)),
            })


        # Loop for SubItems
        for x in packages:
            p.append({
                'subitems_id': "" if x.item_name_desc_id == None else x.item_name_desc_id,
                'item_code': "" if x.item_code == None else x.item_code,
                'item_name': "" if x.item_name == None else x.item_name,
                'brand': "" if x.brand == None else x.brand,
                'status_served_name': "" if x.status_served_name == None else x.status_served_name,
                'borrowed_for': "" if x.borrowed_for == None else x.borrowed_for,
                'status_item': "" if x.status_item == None else x.status_item,
            })

        # dict_list = []
        # for item in serialized_data.items:
        #     dict_list.append(dict(item))
        #     #print(dict_list.value)

        dict_list = [dict(item) if not isinstance(item, datetime.date) else item.strftime('%Y-%m-%d') for item in serialized_data]
        
        dic['qs_json'] = list(l)
        dic2['qs_json2'] = list(p)

        # print(list(l))
        # print('')       
        # print(dict_list)

        item_category   = {
                         'category':kwargs['category'].replace('-',' ').title(),
                         'pages': 'Item Facilities',
                         'fac_items':facilities,
                         'count_pages': count_pages,
                         'count_from': count_from,
                         'count_all_items': count_all_items,
                         'packages': packages,
                         'last_page': last_page,         
                         'image_path': image_path,
                         'qs_json' : dic,
                         'qs_json2': dic2,
                         'item_code': item_code,
                         
                         }
        
        context.update(item_category)
  
        return render(request, 'fmsLogin/facilities.html',context)  
    else:
        return redirect('/login/')

def ListofFacilitiesPage(request):
    
    return render(request, 'fmsLogin/list_of_facilities.html',{})

def RepairPage(request):

    if request.method == 'POST':
        form_data = request.POST  # Access the form data
        # Process the form data or perform any necessary operations
        # ...

        #print(form_data)


        decrypt = form_data.get('item_code_id')
        myItemCode = form_data.get('item_code')

        if 'id' in form_data: # UPDATE
            data = {
                        'id'                  : form_data.get('id'),
                        'item_code_id'        : form_data.get('item_code_id'),
                        'item_code'           : form_data.get('item_code'),
                        'item_name_desc_id'   : form_data.get('item_name_desc_id'),
                        'brand'               : form_data.get('brand'),
                        'problem_encountered' : form_data.get('problem_encountered'),
                        # 'recepients'          : form_data.get('recepient'),
                        'contact_number'      : form_data.get('contact_number'), 
                        'delivered_by'        : form_data.get('delivered_by') ,
                        'repair_date'         : form_data.get('repair_date'),
                        'custodian_id'        : form_data.get('custodian_id'),
                        'user_id'             : request.session.get('user_id'),
                        'received_by'         : form_data.get('received_by'),
                    }
            
            RO = RepairOrder()

            RO.update(datas=data)

        else: # SAVE
            data = {
                        'item_code_id'        : form_data.get('item_code_id'),
                        'item_code'           : form_data.get('item_code'),
                        'item_name_desc_id'   : form_data.get('item_name_desc_id'),
                        'brand'               : form_data.get('brand'),
                        'problem_encountered' : form_data.get('problem_encountered'),
                        # 'recepients'          : form_data.get('recepient'),
                        'contact_number'      : form_data.get('contact_number'), 
                        'delivered_by'        : form_data.get('delivered_by') ,
                        'repair_date'         : form_data.get('repair_date'),
                        'custodian_id'        : form_data.get('custodian_id'),
                        'user_id'             : request.session.get('user_id'),
                        'received_by'         : form_data.get('received_by'),
                    }
            
            RO = RepairOrder()

            RO.insert(datas=data)

        # Return a JSON response indicating the success or any other relevant data
        response_data = {'success': True,
                         'item_code': myItemCode}
        
        return JsonResponse(response_data)
        
    else:
        # Handle GET requests or other HTTP methods if needed
        # ...
        pass

def Repair_Order_Create(request):
    if request.method == 'POST':
        item_code_id    = request.POST.get('item_code_id', '')
        custodianid     = request.POST.get('custodianid', '')
        item_code       = request.POST.get('item_code', '')
        recepient       = request.POST.get('recepient', '')
        repair_date     = request.POST.get('repair_date', '')
        #print(custodianid)

         # Check if any required field is empty or blank
        if not all([item_code_id, custodianid, item_code, recepient, repair_date]):
            # If any required field is empty or blank, you can display an error message
            return HttpResponse('Please fill in all the required fields.')

        # Continue with your other processing logic here if all required fields are filled

        # If everything is fine, you can redirect to a success page or another view
        return render(request,'fmsLogin/facilities.html',{})  # Replace 'success_view' with the name of the view you want to redirect to

def RepairOrderHistoryPage(request,**kwargs):
    context     =  my_context()
    items       = Items()
    item_code   = kwargs['item_code']

    raw_roh_data = items.Repair_Order_History(item_code=kwargs['item_code'])
    raw_rth_data = items.Repair_Order_Turnover(item_code=kwargs['item_code'])

    repair_order_history = []
    repair_order_history_dict = {}

    for x in raw_roh_data:
        random_number = f'{x.repair_order_id}{generate_random_letters(5)}'
        
        encrypted = encrypt_number(x.repair_order_id)

        # print(encrypted)

        # decrypted = str(decrypt_number(encrypted,x.repair_order_id))
        # print(decrypted)                

        repair_order_history.append({
            #'encrypted': encrypted,
            'item_code': x.item_code,
            'random_repair_order_id': x.repair_order_id,
            'repair_order_id': x.repair_order_id,
            'rep_released_id': x.rep_released_id,
            'repair_order_no': x.repair_order_no,
            'custodian_name': x.custodian_name,
            'problem_encountered': x.problem_encountered,
            'delivered_date': convertToDateOnly(x.delivered_date),
            'delivered_by': '' if x.delivered_by == None else x.delivered_by,
            'received_by': '' if x.received_by == None else x.received_by, #received_by
            'turnovered' : x.turnovered
        })

    repair_order_turnover =[]
    repair_order_turnover_dict = {}


    for x in raw_rth_data:
        
        repair_order_turnover.append({
            'rep_released_id'   : x.rep_released_id,
            'repair_order_id'   : x.repair_order_id,
            'details_work_done' : x.details_work_done,
            'released_to'       : x.released_to,
            'repaired_by'       : x.repaired_by,
            'released_date'     : convertToDateOnly(x.released_date),
            'date_repaired'     : convertToDateOnly(x.date_repaired),
            'status'            : x.status,
        })
       
    #print(repair_order_turnover)

    repair_order_history_dict['roh_json'] = list(repair_order_history) 
    repair_order_turnover_dict['rot_json'] = list(repair_order_turnover)

    #extend datas from context
    datas = {
        'category': kwargs['category'].replace('-',' ').title(),
        'item_code': item_code,
        'repair_order_history': repair_order_history,
        'repair_order_turnover': repair_order_turnover,
        'repair_order_history_json': repair_order_history_dict,
        'repair_order_turnover_json': repair_order_turnover_dict,
    }

    

    context.update(datas)
    return render(request,'fmsLogin/repairorder_history.html',context)
    # return render(request, 'fmsLogin/repair_order_history_new.html',context)

def RepairTurnoverPage(request):
    if request.method == 'POST':
        form_data = request.POST  # Access the form data
        # Process the form data or perform any necessary operations
        # ...
        
        #decrypt = form_data.get('repair_order_id')

        option = form_data.get('option')
      
        if option == 'save':
            data =  {
                        'id'                        : form_data.get('id'),
                        'details_work_done'         : form_data.get('details_work_done'),
                        'released_to'               : form_data.get('released_to'),
                        'repaired_by'               : form_data.get('repaired_by'),
                        'turnover_date'             : form_data.get('turnover_date'),
                        'repaired_date'             : form_data.get('repaired_date'),
                        'status'                    : form_data.get('status'),
                        'user_id'                   : request.session.get('user_id'),
                    }

            ROT = RepairOrderTurnover()

            ROT.insert(datas=data)

            response_data = {'success': True}
            return JsonResponse(response_data)
        
        elif option == 'update':
            data =  {
                        # 'id'                        : form_data.get('repair_order_id'),
                        'details_work_done'         : form_data.get('details_work_done'),
                        'released_to'               : form_data.get('released_to'),
                        'repaired_by'               : form_data.get('repaired_by'),
                        'turnover_date'             : form_data.get('turnover_date'),
                        'repaired_date'             : form_data.get('repaired_date'),
                        'status'                    : form_data.get('status'),
                        'user_id'                   : request.session.get('user_id'),
                        'id'                        : form_data.get('id'),
                    }
            
            print(data,option)

            ROT = RepairOrderTurnover()

            ROT.update(datas=data)

            response_data = {'success': True}
            return JsonResponse(response_data)

def RepairTurnoverRemove(request,**kwargs):
    if request.method == 'POST':

        ROT_REMOVE = RepairOrderTurnover()
        ROT_REMOVE.delete_repairorder_turnover(id=kwargs.get('id'))

        response_data = {'success': True}
    return JsonResponse(response_data)

def RepairOrderRemove(request,**kwargs):
    if request.method == 'POST':

        RO_REMOVE = RepairOrderTurnover()
        RO_REMOVE.delete_repairorder(id=kwargs.get('id'))

        response_data = {'success': True}
    return JsonResponse(response_data)


def RepairTurnoverUpdatePage(request):
    if request.method == 'POST':
        form_data = request.POST  # Access the form data

        data =  {
                    'repair_order_id'           : form_data.get('repair_order_id'),
                    'details_work_done'         : form_data.get('details_work_done'),
                    'released_to'               : form_data.get('released_to'),
                    'repaired_by'               : form_data.get('repaired_by'),
                    'turnover_date'             : form_data.get('turnover_date'),
                    'status'                    : form_data.get('status'),
                    'user_id'                   : request.session.get('user_id'),
                }
        
def convertToDate(data):
   
    if isinstance(data, str):
        if data == 'Waiting for the next sched...':
            return data    
        else:
            # date_obj = datetime.datetime(1990, 1, 1)
            # datetime_str = date_obj.strftime('%Y-%m-%d %H:%M:%S')

            # return datetime_str
            return 'None'
   
    else:
        if data == None:
            #date_obj = datetime.datetime(1990, 1, 1)
            return 'None'
        else:
            date_obj = data

            #datetime_str = date_obj.strftime('%Y-%m-%d %H:%M:%S')
            datetime_str = date_obj.strftime('%m-%d-%Y %H:%M:%S')
            return datetime_str
    
def convertToDateOnly(data):
    if isinstance(data, str):
       
        return 'Waiting...'
   
    else:
        if data == None:
            #date_obj = datetime.datetime(1990, 1, 1)
            return 'Waiting...'
        else:
            date_obj = data

            #datetime_str = date_obj.strftime('%Y-%m-%d %H:%M:%S')
            datetime_str = date_obj.strftime('%m-%d-%Y')
            return datetime_str
    
def my_context():
    items = Items()    
    context = {
                'facilities': items.Facilities(),
                'borrowed': items.Borrowed(),
                'repaired': len(items.Repaired()),
                'vacant': items.Vacant(),
                #'activities': items.Recent_Activities(),
                'supplier_price_update': items.Supplier_Price_Update(),         
                'selected': '',
                'defective': items.Defective(),
                }    
    
    return context

def active_pages(request):
    pass

def RecentActivityPage(request):
    item = Items()
    activities = list(item.Recent_Activities())[0:10]

    return JsonResponse({"recent_activities": activities})

def BorrowerPage(request,**kwargs):
    item            = Items()
    borrower        = item.Borrower_History(item_code=kwargs['item_code'],info=False)
    # borrower_info   = item.Borrower_History(item_code=kwargs['item_code'],info=True)
    context         = my_context()
    mto             = item.MTO(item_code=kwargs['item_code'])

    borrower_info = [] 

    for mtono in mto:
        for borrowed in borrower:
            if mtono.mto_no == borrowed.mto_no:
                borrower_info.append({
                    'mto_no': mtono.mto_no,
                    'custodian': borrowed.from_borrowed_by,
                    'location': borrowed.from_Proj_location,
                    'department': borrowed.from_borrowed_for,
                    'turnover_to': borrowed.custodian_name,
                    'turnover_location': borrowed.borrowed_for,
                    'date_turnover': convertToDateOnly(borrowed.date_borrowed),
                    'noted_date': convertToDateOnly(borrowed.noted_date),
                    'noted_by': borrowed.noted_by,
                    'date_borrowed': convertToDateOnly(borrowed.from_date_borrowed),
                    'submitted_date': convertToDateOnly(borrowed.submitted_date),

                })
                break
  
    # print(borrower_info)

    borrower_history = {
        'borrower_history': borrower,
        'mto': mto,
        'no_of_borrowed': len(mto),
        'borrower_history_length': len(borrower),
        'borrower_info': borrower_info,
        'item_code': kwargs['item_code'],
        }
    
    context.update(borrower_history)

    return render(request, 'fmsLogin/borrower.html',context)

def UserProfilePage(request):
    
    uploaded = False
    category_uploaded = None 

    if request.method == 'POST':
        data = request.POST
        image = request.FILES.get('image')

        # myThumbnail = Thumbnail_Images.objects.create(
        #     category=data['category'],
        #     thumbnail=image,
        # )

        # Get an existing object or create a new one
        thumbnail_obj, created = Thumbnail_Images.objects.get_or_create(
            category=data['category'],
            defaults={'thumbnail': image}  # Set the default attributes
        )

        # If the object was not created, update its attributes
        if not created:
            thumbnail_obj.thumbnail = image
            thumbnail_obj.save()

        uploaded = True
        category_uploaded = data['category']

    context = my_context()
    images = Thumbnail_Images.objects.all()

    items = Items()  

    newItems = []

    for x in items.Facilities():
        thumbnails = None
    
        for img in images:
            if img.category == x:
                thumbnails = img.thumbnail

        newItems.append({
            'category': x,
            'thumbnail':thumbnails,
        })

    context.update({'thumbnail': newItems,
                    'uploaded': uploaded,
                    'category_uploaded': category_uploaded,
                    'pages': 'User Profile',
                    })
    

    return render(request, 'fmsLogin/user_profile.html',context)

def handling_404(request,exception):
    return render(request, 'fmsLogin/pages-error-404.html', {})

def UploadFacilitiesPic(request):
    
    if request.method == 'POST':
        data = request.POST
        image = request.FILES.get('image')

        print('data:', data)
        print('image:', image)

    context = my_context()

    images = Thumbnail_Images.objects.all()

    items = Items()  
    newItems = []

    for x in items.Facilities():
        thumbnails = None
        for img in images:
            if img.category == x:
                thumbnails = img.thumbnail

        newItems.append({
            'category': x,
            'thumbnail':thumbnails,
        })

    context.update({'thumbnail': newItems})

    return render(request, 'fmsLogin/user_profile.html',context)    

def SubItemHistory(request,**kwargs):

        items = Items() 
        subitemhistory = items.SubItemHistory(id=kwargs.get('id'))

        subhistory = []

        for x in subitemhistory:
            subhistory.append({'item_code': '' if x.item_code == None else x.item_code,
                               'category': '' if x.cat_name == None else x.cat_name,
                               'item_name': '' if x.item_name == None else x.item_name,
                               'brand': '' if x.brand == None else x.brand,
                               'custodian': '' if x.custodian_name == None else x.custodian_name,
                               'date_borrowed': '' if x.date_borrowed == None else x.date_borrowed,
                               'borrowed_for': '' if x.borrowed_for == None else x.borrowed_for,
                               'borrowed_to': '' if x.borrowed_to == None else x.borrowed_to,
                               })

        response_data = {'success': True,
                         'data': 'hello world',   
                         'subitemhistory': subhistory,             
                        }
        
        return JsonResponse(response_data)

def RecentActivityHistory(request):
    context = my_context()
    return render(request, 'fmsLogin/recent_activity_history.html',context)

def LoadRecentActivityHistory(request,**kwargs):
    upper = kwargs.get('visible')
    lower = upper - 3

    item = Items()
    activities = list(item.Recent_Activities()[lower:upper])
    
    activity_size = len(item.Recent_Activities())

    size = True if upper >= activity_size else False

    return JsonResponse({"recent_activities": activities,'max': size})

def ComputerMaintenanceHistory(request):
    items = Items()
    context = {
        'maintenance_checklist': items.maintenance_checklist(),
        'maintenance_checklist_details': items.maintenance_checklist_details(),
    }
    return render(request, 'fmsLogin/computer_maintenance.html',context)

def Practice(request):
    return render(request, 'fmsLogin/practice.html',{})

def SupplierPriceUpdate(request):
    context = my_context()
    return render(request, 'fmsLogin/supplier_price_update.html', context)

def LoadSupplierPriceUpdate(request,**kwargs):
    search = kwargs.get('search')
    upper = kwargs.get('visible')
    lower = upper - 3


    if kwargs.get('search') == 'undefined':
        search = ''
    else:
        search = kwargs.get('search')

    # item = Items()
    # activities = list(item.Recent_Activities()[lower:upper])
    
    # activity_size = len(item.Recent_Activities())

    items = Items()
    price_update  = items.get_rs_no_for_price_update(category=search,no_to_display=0)
    price_update_filter = [item[0] for item in price_update if item[0].lower() != 'n/a']
    

    price_update_size = len(price_update_filter)
    price_update_filter = price_update_filter[lower:upper]
    receiving = []
    
    for x in price_update_filter:
        xx = items.Receiving_History(rs_no = x)

        if xx != []: # check if empty ky pag abot sa javascript mag error
            receiving.append(xx)
            
    # return JsonResponse({"updated_price": receiving})
    size = True if upper >= price_update_size else False

    return JsonResponse({"updated_price": receiving,'max': size})

def FacilitiesPage_new(request,**kwargs):

    item_code = kwargs.get('item_code') if 'item_code' in kwargs else 'undefined'
    
    # facilities_type = request.GET.get('q',None)
    # print(facilities_type)

    item_category = {
        'category': kwargs['category'].replace('-',' ').title(),
        'item_code': item_code,
        # 'facilities_type': facilities_type,
        }
     
    context = my_context()
    context.update(item_category)

    return render(request, 'fmsLogin/facilities_new.html',context)

def Facilities_json(request,**kwargs):
    # search = kwargs.get('search')
    false_slugify = {'doublesingle-burner-stove': 'double/single-burner-stove'}

    search = kwargs.get('search')
    upper = kwargs.get('visible')
    lower = upper - 5


    if 'category' in kwargs:
        # get items class
        items = Items()

        category = false_slugify[kwargs['category']] if kwargs['category']  in false_slugify else kwargs['category']

        item_code = kwargs.get('item_code') if 'item_code' in kwargs else None


        facilities  = items.Facilities_Item(category=kwargs['category'].replace("'","`"),item_code=item_code,search=search)
        packages = items.Fac_Packages(category=None)
        fac_size = len(facilities)
        
        myImages = Thumbnail_Images.objects.all()
        
        #Loop for Item Facilities
        facList = []
        packagesList = []  

        # manual serialization for facilities data
        for x in list(facilities)[lower:upper]:
            # random_number = f'{x.item_code_id}{generate_random_letters(5)}'
    
            rs_no = "None" if x.rs_no is None or x.rs_no.upper() == 'N/A' else x.rs_no

            receiving = items.Receiving_History(rs_no = rs_no)

            thumbnails = str(next((img.thumbnail.url for img in myImages if img.category == x.category), None))
                        
                # rs_no = None 
                # if x.rs_no == None:
                #     rs_no = "None"
                # elif x.rs_no.upper() == 'N/A':
                #     rs_no = "None"
                # else:
                #     rs_no = x.rs_no


                # thumbnails = None
                # for img in myImages:
                #     if img.category == x.category:
                #         thumbnails = str(img.thumbnail.url)


            facList.append({
                'random_item_code_id': 0 if x.item_code_id == None else x.item_code_id,
                'item_code_id': 0 if x.item_code_id == None else x.item_code_id,
                'custodian_id': 0 if x.custodian_id == None else x.custodian_id,
                'item_code': "" if x.item_code == None else x.item_code,
                'item_name': "" if x.item_name == None else x.item_name,
                'item_name_desc_id': 0 if x.item_name_desc_id == None else x.item_name_desc_id,
                'category': "" if x.category == None else x.category,
                'brand': "" if x.brand == None else x.brand,
                'custodian_name': "" if x.custodian_name == None else x.custodian_name,
                'borrowed_for': "" if x.borrowed_for == None else x.borrowed_for,
                'status_served_name': "" if x.status_served_name == None else x.status_served_name,
                'date_schedule_final': "" if x.date_schedule_final == None else convertToDate(x.date_schedule_final),
                'last_date_maint': "" if x.last_date_maint == None else convertToDate(x.last_date_maint),
                'location': "" if x.location == None else x.location,
                'date_borrowed': "" if x.date_borrowed == None else convertToDate(x.date_borrowed),
                'acquisition_date': "" if x.acquisition_date == None else convertToDate(x.acquisition_date),
                'rs_no': "" if x.rs_no == None else x.rs_no,
                'bs_no': "" if x.bs_no == None else x.bs_no,
                'serial_no': "" if x.serial_no == None else x.serial_no,
                'search': f'{"" if x.item_name == None else x.item_name} {x.brand} {x.item_code} {x.category} {x.custodian_name} {x.location} {x.rs_no} {x.bs_no} {x.borrowed_for}',
                'no_of_repair_history' : 0 if x.no_of_repair_history == None else x.no_of_repair_history,
                'repair_status':"" if x.repair_status == None else x.repair_status,
                'receiving_data': receiving,
                'no_of_borrowed': len(items.MTO(item_code=x.item_code)), 
                'img': 'default.jpg' if thumbnails == None else thumbnails,
                'time_ago': Time_Ago('-' if x.date_borrowed == None else x.date_borrowed),
            })

         
        # manual serialization for packages data
        for x in packages:
            packagesList.append({
                    'subitems_id': "" if x.item_name_desc_id == None else x.item_name_desc_id,
                    'item_code': "" if x.item_code == None else x.item_code,
                    'item_name': "" if x.item_name == None else x.item_name,
                    'brand': "" if x.brand == None else x.brand,
                    'status_served_name': "" if x.status_served_name == None else x.status_served_name,
                    'borrowed_for': "" if x.borrowed_for == None else x.borrowed_for,
                    'status_item': "" if x.status_item == None else x.status_item,
                })      

        size = True if upper >= fac_size else False
        context = { 
                    'category': category,
                    'fac_data': list(facList),
                    'packages':list(packagesList),
                    'max': size,
                    'no_of_items':fac_size,
                   }

        
    return JsonResponse(context)

def RepairOrderHistoryNew(request,**kwargs):
    myContext     =  my_context()
    if request.method == 'POST':
        print(request)

    context = {
        'category':  kwargs.get('category'),
        'item_code': kwargs.get('item_code'),
    }

    myContext.update(context)

    return render(request,'fmsLogin/repair_order_history_new.html',myContext)

def RepairOrderHistory_json(request,**kwargs):

    category    = kwargs.get('category')
    item_code   = kwargs.get('item_code')
    visible     = kwargs.get('visible')
    search      = kwargs.get('search')

    # print(item_code)

    # context = {
    #     'category': category,
    #     'item_code': item_code,
    #     'visible': visible,
    #     'search': search,
    # }

     # search = kwargs.get('search')

    search = kwargs.get('search')
    upper = kwargs.get('visible')
    lower = upper - 5

    if 'category' in kwargs:
        # get items class
        items = Items()
        repairOrderHistory = items.Repair_Order_History(item_code=item_code,)
        turnOverRepairHistory = items.Repair_Order_Turnover(item_code=item_code)
        serializeRepairData = []
        serializeTurnoverData = []
        

        for x in repairOrderHistory:
            serializeRepairData.append({
                'repair_order_id': x.repair_order_id,
                'item_code': x.item_code,
                'random_repair_order_id': x.repair_order_id,
                'repair_order_id': x.repair_order_id,
                'rep_released_id': x.rep_released_id,
                'repair_order_no': x.repair_order_no,
                'custodian_name': x.custodian_name,
                'problem_encountered': x.problem_encountered,
                'delivered_date': convertToDateOnly(x.delivered_date),
                'delivered_by': '' if x.delivered_by == None else x.delivered_by,
                'received_by': '' if x.received_by == None else x.received_by, #received_by
                'turnovered' : x.turnovered,
                'contact_no': x.cellphone_no,
            })


        for x in turnOverRepairHistory:
            serializeTurnoverData.append({
                'rep_released_id'   : x.rep_released_id,
                'repair_order_id'   : x.repair_order_id,
                'details_work_done' : x.details_work_done,
                'released_to'       : x.released_to,
                'repaired_by'       : x.repaired_by,
                'released_date'     : convertToDateOnly(x.released_date),
                'date_repaired'     : convertToDateOnly(x.date_repaired),
                'status'            : x.status,
        })

        context = {
                    'category': category,
                    'item_code': item_code,
                    'repair_order_data': serializeRepairData,
                    'turnover_data': serializeTurnoverData,
                   }

    return JsonResponse(context)