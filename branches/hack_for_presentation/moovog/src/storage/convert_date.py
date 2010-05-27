
# a function that convert date from letters to ????-??-??

def convert_date(date):
    if (date==None):
        return None
    day = ''
    i = 0
    #print date
    while(date[i] != ' '):
        day = day + date[i]
        i = i + 1   
    i = i + 1
    month = ''
    
    while(date[i] != ' '):
        month = month + date[i]
        i = i + 1
    i= i + 1

    #print date[i:]

    if (month == 'January'):
        month = '01'
    elif (month == 'February'):
        month = '02'
    elif (month == 'March'):
        month = '03'
    elif (month == 'April'):
        month = '04'
    elif (month =='May'):
        month = '05'
    elif (month == 'June'):
        month = '06'
    elif (month == 'July'):
        month = '07'
    elif (month == 'August'):
        month = '08'
    elif (month == 'September'):
        month = '09'
    elif (month == 'October'):
        month = '10'
    elif (month == 'November'):
        month = '11'
    elif (month == 'December'):
        month = '12'
    
    year = date[i:]
    return year+'-'+month+'-'+day
