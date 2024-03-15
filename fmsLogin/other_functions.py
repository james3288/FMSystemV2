from datetime import datetime

def ConvertToDate(data):
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
        
def ConvertToDateOnly(data):
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
            datetime_str = date_obj.strftime('%m-%d-%Y')
            return datetime_str
        
def Time_Ago(timestamp):
    now = datetime.now()
    diff = now - timestamp

    if diff.total_seconds() < 60:
        return f"{int(diff.total_seconds())} sec/s"
    elif diff.total_seconds() < 3600:
        minutes = int(diff.total_seconds() / 60)
        return f"{minutes} min{'s' if minutes > 1 else ''}"
    elif diff.total_seconds() < 86400:
        hours = int(diff.total_seconds() / 3600)
        return f"{hours} hr{'s' if hours > 1 else ''}"
    elif diff.total_seconds() < 604800:
        days = int(diff.total_seconds() / 86400)
        return f"{days} day{'s' if days > 1 else ''}"
    elif diff.total_seconds() < 2419200:
        weeks = int(diff.total_seconds() / 604800)
        return f"{weeks} week{'s' if weeks > 1 else ''}"
    elif diff.total_seconds() < 29030400:
        months = int(diff.total_seconds() / 2419200)
        return f"{months} month{'s' if months > 1 else ''}"
    else:
        years = int(diff.total_seconds() / 29030400)
        return f"{years} year{'s' if years > 1 else ''}"
    
def kwargs_exist(kwargs):
    print(kwargs)