# -*- coding: utf-8 -*-
"""
Created on Tue May 14 2018

@author: Gebruiker
"""

import pandas as pd
from bokeh.plotting import figure, save, gmap, output_file
from bokeh.io import show, curdoc
from bokeh.models import ColumnDataSource, GMapOptions
from bokeh.models import HoverTool, Slider, RangeSlider, Select, Dropdown
from bokeh.models.callbacks import CustomJS
from bokeh.layouts import widgetbox, row, column
from bokeh.models.widgets import DataTable, TableColumn, Button

df = pd.read_csv('dfall.csv', low_memory=False, sep=';')
df2 = df[['products', 'CitiesO', 'CoordinatesO', 'LatitudeO',	'LongitudeO', 'jaar', 'CitiesD', 'LatitudeD',	'LongitudeD', 'totalmin', 'totalmax']]
df1= df2.groupby(['products', 'CitiesO', 'CoordinatesO', 'LatitudeO',	'LongitudeO', 'jaar', 'CitiesD', 'LatitudeD',	'LongitudeD']).sum().reset_index()

# set column data source within range of 1700 untill 1805, using only origins of goods
source= ColumnDataSource(data= {
         'LongitudeO' : df1.loc[(df1['jaar'] >= 1700) & (df1['jaar'] <= 1805)][df1['products'] == 'Rye'][(df1['totalmin'] >= 0) & (df1['totalmin'] <=1000000 )].LongitudeO,
         'LatitudeO' : df1.loc[(df1['jaar'] >= 1700) & (df1['jaar'] <= 1805)][df1['products'] == 'Rye'][(df1['totalmin'] >= 0) & (df1['totalmin'] <=1000000 )].LatitudeO,
         'LongitudeD' : df1.loc[(df1['jaar'] >= 1700) & (df1['jaar'] <= 1805)][df1['products'] == 'Rye'][(df1['totalmin'] >= 0) & (df1['totalmin'] <=1000000 )].LongitudeD,
         'LatitudeD' : df1.loc[(df1['jaar'] >= 1700) & (df1['jaar'] <= 1805)][df1['products'] == 'Rye'][(df1['totalmin'] >= 0) & (df1['totalmin'] <=1000000 )].LatitudeD,
         'products' : df1.loc[(df1['jaar'] >= 1700) & (df1['jaar'] <= 1805)][df1['products'] == 'Rye'][(df1['totalmin'] >= 0) & (df1['totalmin'] <=1000000 )].products,
         'CitiesO' : df1.loc[(df1['jaar'] >= 1700) & (df1['jaar'] <= 1805)][df1['products'] == 'Rye'][(df1['totalmin'] >= 0) & (df1['totalmin'] <=1000000 )].CitiesO,
         'CitiesD' : df1.loc[(df1['jaar'] >= 1700) & (df1['jaar'] <= 1805)][df1['products'] == 'Rye'][(df1['totalmin'] >= 0) & (df1['totalmin'] <=1000000 )].CitiesD,
         'totalmin' : df1.loc[(df1['jaar'] >= 1700) & (df1['jaar'] <= 1805)][df1['products'] == 'Rye'][(df1['totalmin'] >= 0) & (df1['totalmin'] <=1000000 )].totalmin,
         'totalmax' : df1.loc[(df1['jaar'] >= 1700) & (df1['jaar'] <= 1805)][df1['products'] == 'Rye'][(df1['totalmin'] >= 0) & (df1['totalmin'] <=1000000 )].totalmax 
         })

#creating downloadable table

sourcetable= ColumnDataSource(data= {
         'products' : df1.loc[(df1['jaar'] >= 1700) & (df1['jaar'] <= 1805)][df1['products'] == 'Rye'][(df1['totalmin'] >= 0) & (df1['totalmin'] <=1000000 )].products,
         'CitiesO' : df1.loc[(df1['jaar'] >= 1700) & (df1['jaar'] <= 1805)][df1['products'] == 'Rye'][(df1['totalmin'] >= 0) & (df1['totalmin'] <=1000000 )].CitiesO,
         'CitiesD' : df1.loc[(df1['jaar'] >= 1700) & (df1['jaar'] <= 1805)][df1['products'] == 'Rye'][(df1['totalmin'] >= 0) & (df1['totalmin'] <=1000000 )].CitiesD,
         'Year' : df1.loc[(df1['jaar'] >= 1700) & (df1['jaar'] <= 1805)][df1['products'] == 'Rye'][(df1['totalmin'] >= 0) & (df1['totalmin'] <=1000000 )].jaar,
         'totalmin' : df1.loc[(df1['jaar'] >= 1700) & (df1['jaar'] <= 1805)][df1['products'] == 'Rye'][(df1['totalmin'] >= 0) & (df1['totalmin'] <=1000000 )].totalmin,
         'totalmax' : df1.loc[(df1['jaar'] >= 1700) & (df1['jaar'] <= 1805)][df1['products'] == 'Rye'][(df1['totalmin'] >= 0) & (df1['totalmin'] <=1000000 )].totalmax 
         })


# updates year of sliders
def update_plot (attr, old, new):
    yr = df1[(df1['jaar'] >= slider1.value[0]) & (df1['jaar'] <= slider1.value[1])][df1['products'] == x_select.value][(df1['totalmin'] >= slider2.value[0]) & (df1['totalmin'] <= slider2.value[1])]
 # Swithces between origins or destination based on users selection
    if y_select.value == 'Origins': 
        longitude1 = 'LongitudeO'
        latitude1 = 'LatitudeO' 
        cities= 'CitiesO'
    elif y_select.value == 'Destination':
        longitude1 = 'LongitudeD' 
        latitude1 = 'LatitudeD' 
        cities= 'CitiesD'
  #adjust data based on yr
    new_data= {
         'LongitudeO' : yr[longitude1],
         'LatitudeO' : yr[latitude1],
         'products' : yr.products,
         'CitiesO' : yr[cities],
         'totalmin' : yr.totalmin,
         'totalmax' : yr.totalmax
         }
    source.data=new_data

def update_table (attr, old, new):
    yr = df1[(df1['jaar'] >= slider1.value[0]) & (df1['jaar'] <= slider1.value[1])][df1['products'] == x_select.value][(df1['totalmin'] >= slider2.value[0]) & (df1['totalmin'] <= slider2.value[1])]
  #adjust data based on yr
    new_data= {
         'products' : yr.products,
         'CitiesO' : yr.CitiesO,
         'CitiesD' : yr.CitiesD,
         'Year' : yr.jaar,
         'totalmin' : yr.totalmin,
         'totalmax' : yr.totalmax
         }
    sourcetable.data=new_data
     
slider1=RangeSlider(start=1700, end=1805, step=1, value=(1700, 1805), title='Year')
slider1.on_change('value', update_plot)
slider1.on_change('value', update_table)

slider2=RangeSlider(start=0, end=1000000, step=1000, value=(0, 1000000), title='Amount (min)')
slider2.on_change('value', update_plot)
slider2.on_change('value', update_table)

#Select options for type of goods
x_select = Select(options= ['Barley', 'Cacao', 'Coffee', 'Oats', 'Pepper', 'Rye', 'Sugar', 'Tea', 'Wheat'], title = 'Type of goods', value='Rye')
x_select.on_change('value', update_plot)
x_select.on_change('value', update_table)

# Select polygons for either origins or destiantion
y_select = Select(options= ['Origins', 'Destination'], title = 'Origins or Destination', value = 'Origins' ) 
y_select.on_change('value', update_plot)
                          
#Mapping
# map options and hover tools
map_options = GMapOptions(lat=50, lng=0, zoom=5)
hover=HoverTool(tooltips=[('Location','@CitiesO'), ('Type', '@products')])
p= gmap('AIzaSyDmZPFmiPy6FqGxEv88X-wamwbReyvY_Og', map_options, title='Sound Toll Trade', tools=[hover, "pan,wheel_zoom,lasso_select,reset, poly_draw"])
p.circle(x='LongitudeO', y='LatitudeO', size=5, color='red', alpha=0.5, source=source)
p.add_tools()
p.plot_width=800

columns = [
        TableColumn(field='CitiesO', title='Place of Origin'),
        TableColumn(field='CitiesD', title='Destination'),
        TableColumn(field='Year', title='Year'),
        TableColumn(field='totalmin', title='Amount (min)'),
        TableColumn(field='totalmax', title='Amount (max)')
        ]
datatable = DataTable(source=sourcetable, columns=columns, width=800)

def update(attr, new, old):
    inds = source.selected['1d']['indices']
    results= df1.iloc[inds]

source.on_change('selected', update)

downloadcallback = CustomJS(args=dict(source=sourcetable), code="""
var data = source.data;
var filetext = 'Origin,Destination,Year\\n';

for (i=0; i < data['CitiesO'].length; i++) {
	var currRow = [data['CitiesO'][i].toString(), data['CitiesD'][i].toString(), data['Year'][i].toString().concat('\\n')];
	var joined = currRow.join();
	filetext = filetext.concat(joined);
}	

var filename = 'data.csv';
var blob = new Blob([filetext], { type: 'text/csv;charset=utf-8;' });

//addresses IE
if (navigator.msSaveBlob) {
	navigator.msSaveBlob(blob, filename);
}

else {
	var link = document.createElement("a");
	link = document.createElement('a')
	link.href = URL.createObjectURL(blob);
	link.download = filename
	link.target = "_blank";
	link.style.visibility = 'hidden';
	link.dispatchEvent(new MouseEvent('click'))
}
""")

button = Button(label='Download', button_type='success', callback=downloadcallback)

layouttop = row(widgetbox(slider1, slider2, x_select, y_select), p)
layoutbot = row(widgetbox(button), datatable)
layout = column(layouttop, layoutbot)
curdoc().add_root(layout)