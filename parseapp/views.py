from django.shortcuts import render
from django.views import View
import os
from django.conf import settings
from django.http import HttpResponse
import json
import re
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import pandas as pd
import matplotlib.pyplot as plt
from parseapp.utils import senti, wordcount
import plotly.offline as opy
import plotly.graph_objs as go
import plotly.express as px

# Create your views here.

class Index(View):

    def get(self,request):
        with open(os.path.join(settings.BASE_DIR, 'model/keyphrase.txt')) as f:
            lines = f.readlines()
        words = lines[0:30]
        context = {"keywords" : words}
        return render(request,'index.html', context)

    def post(self,request):
        search_keyword = request.POST.get("search")
        df = pd.read_csv(os.path.join(settings.BASE_DIR, 'model/newfeed1.csv'),index_col=None, sep=',', error_bad_lines=False, dtype='unicode')
        header_list = ["year","month","day", "title", "link","description"]
        df[["year", "month","day"]] = df[["year", "month","day"]].apply(pd.to_numeric)
        title=[]
        des=[]
        data=[]
        mon=[]
        sen=[]
        context = {}
        for j in range(2005,2022):
            title=[]
            data=[]
            des=[]
            #extracting data from csv file
            for i in df.index:
                if int(df["year"][i])==j:
                    title.append(df["title"][i])
                    des.append(df["description"][i])
            data=data+title+des
            mon.append(wordcount(data, search_keyword))
            sen.append(senti(data, search_keyword)*1000)
        tick_label = [2005, 2006, 2007, 2008, 2009,2010,2011,2012,2013,2014,2015,2016,2017,2018,2019,2020,2021]

        x = tick_label
        y = mon
        trace1 = go.Scatter(x=x, y=y, 
                            mode="lines",  name='1st Trace')

        data=go.Data([trace1])
        layout=go.Layout(title=search_keyword, xaxis={'title':'YEAR'}, yaxis={'title':'COUNT'})
        figure=go.Figure(data=data,layout=layout)
        div = opy.plot(figure, auto_open=False, output_type='div')
        context['graph1'] = div

        x = tick_label
        y = sen
        trace1 = go.Scatter(x=x, y=y, 
                            mode="lines",  name='1st Trace')

        data=go.Data([trace1])
        layout=go.Layout(title=search_keyword, xaxis={'title':'YEAR'}, yaxis={'title':'POPULARITY'})
        figure=go.Figure(data=data,layout=layout)
        div2 = opy.plot(figure, auto_open=False, output_type='div')
        context['graph2'] = div2

        sen=[]
        mon=[]
        for j in range(1,13):
            title=[]
            data=[]
            des=[]
            for i in df.index:
                if int(df["year"][i])==2021 and int(df["month"][i])==j:
                    title.append(df["title"][i])
                    des.append(df["description"][i])
            data=data+title+des
            mon.append(wordcount(data, search_keyword))
            sen.append(senti(data, search_keyword)*1000)
        
        a=[1,2,3,4,5,6,7,8,9,10,11,12]
  
        # labels for bars
        tick_label = ['jan', 'feb', 'mar', 'apr', 'may','jun','jul','aug','sep','oct','nov','dec']

        data = [go.Bar(
            x = tick_label,
            y = mon,
            name = 'COUNT'
        )]
        fig = go.Figure(data=data)
        div3 = opy.plot(fig, auto_open=False, output_type='div')
        context['graph3'] = div3

        data = [go.Bar(
            x = tick_label,
            y = sen,
            name = 'COUNT'
        )]
        fig = go.Figure(data=data)
        div4 = opy.plot(fig, auto_open=False, output_type='div')
        context['graph4'] = div4
        
        return render(request,'index.html', context)


def get_keywords(request, *args, **kwargs):

    if request.is_ajax() and request.method == "POST":

        texteditor = request.POST['TextEntered']
        with open(os.path.join(settings.BASE_DIR, 'model/keyphrase.txt')) as f:
            lines = f.readlines()
            
        r = re.compile(texteditor)
        keywords = list(filter(r.match, lines)) # Read Note below
        keywords = keywords[0:30]
            
        return HttpResponse(json.dumps({'keywords': keywords}), content_type="application/json")
    else:
        
        return render(request,'index.html')

def keyWord(request, keyword):
    search_keyword = keyword.replace("_", " ")
    df = pd.read_csv(os.path.join(settings.BASE_DIR, 'model/newfeed1.csv'),index_col=None, sep=',', error_bad_lines=False, dtype='unicode')
    header_list = ["year","month","day", "title", "link","description"]
    df[["year", "month","day"]] = df[["year", "month","day"]].apply(pd.to_numeric)
    title=[]
    des=[]
    data=[]
    mon=[]
    sen=[]
    context = {}
    for j in range(2005,2022):
        title=[]
        data=[]
        des=[]
        #extracting data from csv file
        for i in df.index:
            if int(df["year"][i])==j:
                title.append(df["title"][i])
                des.append(df["description"][i])
        data=data+title+des
        mon.append(wordcount(data, search_keyword))
        sen.append(senti(data, search_keyword)*1000)
    tick_label = [2005, 2006, 2007, 2008, 2009,2010,2011,2012,2013,2014,2015,2016,2017,2018,2019,2020,2021]

    x = tick_label
    y = mon
    trace1 = go.Scatter(x=x, y=y, 
                mode="lines",  name='1st Trace')

    data=go.Data([trace1])
    layout=go.Layout(title=search_keyword, xaxis={'title':'YEAR'}, yaxis={'title':'COUNT'})
    figure=go.Figure(data=data,layout=layout)
    div = opy.plot(figure, auto_open=False, output_type='div')
    context['graph1'] = div

    x = tick_label
    y = sen
    trace1 = go.Scatter(x=x, y=y, 
                mode="lines",  name='1st Trace')

    data=go.Data([trace1])
    layout=go.Layout(title=search_keyword, xaxis={'title':'YEAR'}, yaxis={'title':'POPULARITY'})
    figure=go.Figure(data=data,layout=layout)
    div2 = opy.plot(figure, auto_open=False, output_type='div')
    context['graph2'] = div2

    sen=[]
    mon=[]
    for j in range(1,13):
        title=[]
        data=[]
        des=[]
        for i in df.index:
            if int(df["year"][i])==2021 and int(df["month"][i])==j:
                title.append(df["title"][i])
                des.append(df["description"][i])
        data=data+title+des
        mon.append(wordcount(data, search_keyword))
        sen.append(senti(data, search_keyword)*1000)
    
    a=[1,2,3,4,5,6,7,8,9,10,11,12]
  
    # labels for bars
    tick_label = ['jan', 'feb', 'mar', 'apr', 'may','jun','jul','aug','sep','oct','nov','dec']

    data = [go.Bar(
        x = tick_label,
        y = mon,
        name = 'COUNT'
    )]
    fig = go.Figure(data=data)
    div3 = opy.plot(fig, auto_open=False, output_type='div')
    context['graph3'] = div3

    data = [go.Bar(
        x = tick_label,
        y = sen,
        name = 'COUNT'
    )]
    fig = go.Figure(data=data)
    div4 = opy.plot(fig, auto_open=False, output_type='div')
    context['graph4'] = div4
    
    return render(request,'index.html', context)
