from django.shortcuts import render, HttpResponse
from datetime import datetime
from home.models import skuId
import requests
import json
import pandas as pd
from django.contrib import messages

# Create your views here.

apiUrl = "https://script.google.com/macros/s/AKfycbwdJHP8jl9eH8quYXBAnpDZjr72RWbVrPqwN4rL37esPmwCgMnQnxG0l8u8CAfw78Xg/exec"


response_API = requests.get(apiUrl).text
data = json.loads(response_API)
df = pd.DataFrame(data)
# Pandas Convert Row to Column Header in DataFrame
df = pd.DataFrame(df.values[1:], columns=df.iloc[0])

def index(request):

    if request.method == "POST":
        searchID = request.POST.get('name')
        date = datetime.now().strftime("%c")
        search = skuId(searchID=searchID, date=date)
        # search.save()
        # print(skuId._meta.get_fields())
        print(searchID)
        print(date)

        index = searchID
        
        if searchID!="":
            try:
                for i in range(df.shape[0]):
                    if df['SKU Code'][i] == index or index in df['SKU Code'][i]:
                        print("Row no. :",i+1)
                        index = i
                        break

                column_id = list(df)
                row_list = df.loc[index, :].values.flatten().tolist()

                required_columns = [0,1,2,10,11,12,13]

                id = {
                    'search': searchID,
                }

                rw = ['row_0','row_1','row_2','row_3','row_4','row_5','row_6','row_7','row_8','row_9','row_10','row_11','row_12','row_13','row_14',]
                col = ['col_0','col_1','col_2','col_3','col_4','col_5','col_6','col_7','col_8','col_9','col_10','col_11','col_12','col_13','col_14',]
                
                for i in required_columns:
                    id.update({col[i] : column_id[i]})
                    id.update({rw[i] : row_list[i]})

                print(id)
                return render(request, 'search.html', id)
            
            except:
                return render(request, 'home.html')

    return render(request, 'home.html')
    # return HttpResponse("This is our dashboard")