from django.shortcuts import render
import requests
from .models import Location
import datetime
import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot as plt
import numpy as np

# Create your views here.
def home(request):
    location = Location.objects.all()
    if request.method == 'GET':
        return render(request, 'html/home.html',{'location':location})
    if request.method == 'POST':
        scode = request.POST.get("source")
        dcode = request.POST.get('destination')
        start_date = request.POST.get('tdate')
        start_date = datetime.datetime.strptime(start_date, "%Y-%m-%d")
        end_date = (start_date + datetime.timedelta(days=7))
        delta = end_date - start_date
        all_dates = []
        for i in range(delta.days + 1):
            day = start_date + datetime.timedelta(days=i)
            all_dates.append(datetime.datetime.strptime(str(day), "%Y-%m-%d %H:%M:%S").date())
        # print(" >>> Dates >>>",all_dates)
        final_data = []
        from_station = ''
        to_station = ''
        # return False
        for d in all_dates:
            url = f'https://www.rajeshtransports.in/search/search-list?fromStationCode={scode}&toStationCode={dcode}&onwardDate={d}&returnDate=&searchType=&reschedule=0'
            print(" URL",url)
            response = requests.post(url)
            print("Status Code",response.status_code)
            if response.status_code == 200:
                trip_data = dict(response.json()).get('data')
                print(" response length ", len(trip_data) if trip_data is not None else None)
                if trip_data is not None:
                    first_trip = {}
                    start_trip = ''
                    for trip in trip_data:
                        tripDateTime = trip['fromStation']['dateTime']
                        if start_trip == '' or (start_trip > tripDateTime):
                            print(" start_trip",start_trip)
                            start_trip = tripDateTime
                            first_trip = trip
                        if from_station == '' and to_station == '':
                            from_station = trip['fromStation']['name']
                            to_station = trip['toStation']['name']
                    final_data.append(first_trip)
        # print(" final_data",final_data)
        price = []
        dates = []
        for item in final_data:
            if item.keys():
                dates.append(item['travelDate'])
                if len(item['stageFare']) > 0:
                    price.append(item['stageFare'][0]['fare'])
        print("   Price",price,"==== dates",dates)
        if len(price) == 0 and len(dates) == 0:
            return render(request, 'html/home.html',{'success':False,'location':location,'from_station':from_station,'to_station':to_station,'start_date':start_date})
        y_pos = np.arange(len(dates))
        # qty = [10,20,25]
        fig = plt.figure(figsize =(10, 7))
        plt.bar(y_pos, price, align='center', alpha=0.5,width = 0.4)
        plt.xticks(y_pos, dates,fontsize=10)
        plt.ylabel('Price')
        plt.xlabel('Date')
        plt.title(f'{from_station} To {to_station}')
        plt.savefig('media/barchart.png')
        loadImage(request)
        return render(request, 'html/home.html',{'success':True,'location':location,'from_station':from_station,'to_station':to_station,'start_date':start_date})
        

def loadImage(request):
    return render(request, 'html/home.html')
