# -*- coding: utf-8 -*-
"""
Created on Tue May 14 2018

@author: Gebruiker
"""

import pandas as pd
from bokeh.plotting import figure
from bokeh.io import curdoc
from bokeh.models import ColumnDataSource
from bokeh.models import HoverTool, RangeSlider, Select, TapTool, LassoSelectTool, Slider
from bokeh.models.callbacks import CustomJS
from bokeh.layouts import widgetbox, row, column
from bokeh.models.widgets import DataTable, TableColumn, Button
from bokeh.tile_providers import CARTODBPOSITRON
from bokeh.models import LogColorMapper, ColorBar, FixedTicker, NumeralTickFormatter, Div

# Create the color mapper
color_mapper = LogColorMapper(palette="Viridis256", low=0, high=15000000)

df1 = pd.read_csv('data.csv', low_memory=False, sep=';')

# set column data source within range of 1700 untill 1805, using only origins of goods
source= ColumnDataSource(data= {
         'LongitudeO' : df1.loc[(df1['jaar'] >= 1700) & (df1['jaar'] <= 1710)][df1['products'] == 'Rye'][(df1['totalmin'] >= 0) & (df1['totalmin'] <=1000000 )].newLongO,
         'LatitudeO' : df1.loc[(df1['jaar'] >= 1700) & (df1['jaar'] <= 1710)][df1['products'] == 'Rye'][(df1['totalmin'] >= 0) & (df1['totalmin'] <=1000000 )].newLatO,
         'LongitudeD' : df1.loc[(df1['jaar'] >= 1700) & (df1['jaar'] <= 1710)][df1['products'] == 'Rye'][(df1['totalmin'] >= 0) & (df1['totalmin'] <=1000000 )].newLongD,
         'LatitudeD' : df1.loc[(df1['jaar'] >= 1700) & (df1['jaar'] <= 1710)][df1['products'] == 'Rye'][(df1['totalmin'] >= 0) & (df1['totalmin'] <=1000000 )].newLatD,
         'products' : df1.loc[(df1['jaar'] >= 1700) & (df1['jaar'] <= 1710)][df1['products'] == 'Rye'][(df1['totalmin'] >= 0) & (df1['totalmin'] <=1000000 )].products,
         'CitiesO' : df1.loc[(df1['jaar'] >= 1700) & (df1['jaar'] <= 1710)][df1['products'] == 'Rye'][(df1['totalmin'] >= 0) & (df1['totalmin'] <=1000000 )].CitiesO,
         'CitiesD' : df1.loc[(df1['jaar'] >= 1700) & (df1['jaar'] <= 1710)][df1['products'] == 'Rye'][(df1['totalmin'] >= 0) & (df1['totalmin'] <=1000000 )].CitiesD,
         'totalmin' : df1.loc[(df1['jaar'] >= 1700) & (df1['jaar'] <= 1710)][df1['products'] == 'Rye'][(df1['totalmin'] >= 0) & (df1['totalmin'] <=1000000 )].totalmin,
         'totalmax' : df1.loc[(df1['jaar'] >= 1700) & (df1['jaar'] <= 1710)][df1['products'] == 'Rye'][(df1['totalmin'] >= 0) & (df1['totalmin'] <=1000000 )].totalmax,
         'Year' : df1.loc[(df1['jaar'] >= 1700) & (df1['jaar'] <= 1710)][df1['products'] == 'Rye'][(df1['totalmin'] >= 0) & (df1['totalmin'] <=1000000 )].jaar,
         'passage' : df1.loc[(df1['jaar'] >= 1700) & (df1['jaar'] <= 1710)][df1['products'] == 'Rye'][(df1['totalmin'] >= 0) & (df1['totalmin'] <=1000000 )].passage
         })

#creating downloadable table

sourcetable= ColumnDataSource(data= {
         'products' : df1.loc[(df1['jaar'] >= 1700) & (df1['jaar'] <= 1710)][df1['products'] == 'Rye'][(df1['totalmin'] >= 0) & (df1['totalmin'] <=1000000 )].products,
         'CitiesO' : df1.loc[(df1['jaar'] >= 1700) & (df1['jaar'] <= 1710)][df1['products'] == 'Rye'][(df1['totalmin'] >= 0) & (df1['totalmin'] <=1000000 )].CitiesO,
         'CitiesD' : df1.loc[(df1['jaar'] >= 1700) & (df1['jaar'] <= 1710)][df1['products'] == 'Rye'][(df1['totalmin'] >= 0) & (df1['totalmin'] <=1000000 )].CitiesD,
         'Year' : df1.loc[(df1['jaar'] >= 1700) & (df1['jaar'] <= 1710)][df1['products'] == 'Rye'][(df1['totalmin'] >= 0) & (df1['totalmin'] <=1000000 )].jaar,
         'totalmin' : df1.loc[(df1['jaar'] >= 1700) & (df1['jaar'] <= 1710)][df1['products'] == 'Rye'][(df1['totalmin'] >= 0) & (df1['totalmin'] <=1000000 )].totalmin,
         'totalmax' : df1.loc[(df1['jaar'] >= 1700) & (df1['jaar'] <= 1710)][df1['products'] == 'Rye'][(df1['totalmin'] >= 0) & (df1['totalmin'] <=1000000 )].totalmax,
         'passage' : df1.loc[(df1['jaar'] >= 1700) & (df1['jaar'] <= 1710)][df1['products'] == 'Rye'][(df1['totalmin'] >= 0) & (df1['totalmin'] <=1000000 )].passage
         })


# updates year of sliders
def update_plot (attr, old, new):
    mask1=(df1['jaar'] >= slider1.value[0]) & (df1['jaar'] <= slider1.value[1])
    mask2=df1['products'] == x_select.value
    mask3=(df1['totalmin'] >= slider2.value[0]) & (df1['totalmin'] <= slider2.value[1])
    
    yr = df1.loc[mask1][mask2][mask3]
 # Swithces between origins or destination based on users selection
    if y_select.value == 'Origins': 
        longitude1 = 'newLongO'
        latitude1 = 'newLatO' 
        cities1= 'CitiesO'
        longitude2 = 'newLongD'
        latitude2 = 'newLatD' 
        cities2= 'CitiesD'
    elif y_select.value == 'Destination':
        longitude1 = 'newLongD' 
        latitude1 = 'newLatD' 
        cities1= 'CitiesO'
        longitude2 = 'newLongO'
        latitude2 = 'newLatO' 
        cities2= 'CitiesD'
  #adjust data based on yr
    new_data= {
         'LongitudeO' : yr[longitude1],
         'LatitudeO' : yr[latitude1],
         'products' : yr.products,
         'CitiesO' : yr[cities1],
         'totalmin' : yr.totalmin,
         'totalmax' : yr.totalmax,
         'LongitudeD' : yr[longitude2],
         'LatitudeD' : yr[latitude2],
         'CitiesD' : yr[cities2],
         'Year' : yr.jaar,
         'passage' : yr.passage
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
         'totalmax' : yr.totalmax,
         'passage' : yr.passage
         }
    sourcetable.data=new_data
     
slider1=RangeSlider(start=1700, end=1805, step=1, value=(1700, 1710), title='Year Range')
slider1.on_change('value', update_plot)
slider1.on_change('value', update_table)

slider2=RangeSlider(start=0, end=15000000, step=5000, value=(0, 1000000), title='Volume of trade, per year in kg (min)')
slider2.on_change('value', update_plot)
slider2.on_change('value', update_table)

# updates year of sliders
def update_plot2 (attr, old, new):
    mask1=df1['jaar'] == slider3.value
    mask2=df1['products'] == x_select.value
    mask3=(df1['totalmin'] >= slider2.value[0]) & (df1['totalmin'] <= slider2.value[1])
    
    yr = df1.loc[mask1][mask2][mask3]
 # Swithces between origins or destination based on users selection
    if y_select.value == 'Origins': 
        longitude1 = 'newLongO'
        latitude1 = 'newLatO' 
        cities1= 'CitiesO'
        longitude2 = 'newLongD'
        latitude2 = 'newLatD' 
        cities2= 'CitiesD'
    elif y_select.value == 'Destination':
        longitude1 = 'newLongD' 
        latitude1 = 'newLatD' 
        cities1= 'CitiesO'
        longitude2 = 'newLongO'
        latitude2 = 'newLatO' 
        cities2= 'CitiesD'
  #adjust data based on yr
    new_data= {
         'LongitudeO' : yr[longitude1],
         'LatitudeO' : yr[latitude1],
         'products' : yr.products,
         'CitiesO' : yr[cities1],
         'totalmin' : yr.totalmin,
         'totalmax' : yr.totalmax,
         'LongitudeD' : yr[longitude2],
         'LatitudeD' : yr[latitude2],
         'CitiesD' : yr[cities2],
         'Year' : yr.jaar,
         'passage' : yr.passage
         }
    source.data=new_data

def update_table2 (attr, old, new):
    yr = df1[df1['jaar'] == slider3.value][df1['products'] == x_select.value][(df1['totalmin'] >= slider2.value[0]) & (df1['totalmin'] <= slider2.value[1])]
  #adjust data based on yr
    new_data= {
         'products' : yr.products,
         'CitiesO' : yr.CitiesO,
         'CitiesD' : yr.CitiesD,
         'Year' : yr.jaar,
         'totalmin' : yr.totalmin,
         'totalmax' : yr.totalmax,
         'passage' : yr.passage
         }
    sourcetable.data=new_data

slider3=Slider(start=1700, end=1805, step=1, value=1700, title='Select a Single Year')
slider3.on_change('value', update_plot2)
slider3.on_change('value', update_table2)

#Select options for type of goods
x_select = Select(options= ['Barley', 'Cacao', 'Coffee', 'Oats', 'Pepper', 'Rye', 'Sugar', 'Tea', 'Wheat'], title = 'Type of goods', value='Rye')
x_select.on_change('value', update_plot)
x_select.on_change('value', update_table)

# Select polygons for either origins or destiantion
y_select = Select(options= ['Origins', 'Destination'], title = 'Origins or Destination', value = 'Origins' ) 

y_select.on_change('value', update_plot)
                          
#Mapping
    
p= figure(x_range=(-3000000, 3000000), y_range=(1000000, 9000000),
           x_axis_type="mercator", y_axis_type="mercator", tools=['pan, wheel_zoom, reset, save'], toolbar_location='below', title='Sound Toll Trade Flow Map')
p.add_tile(CARTODBPOSITRON)

#Glyps

cr = p.segment(x0='LongitudeO', y0='LatitudeO', x1='LongitudeD', y1='LatitudeD', color={'field': 'totalmin', 'transform': color_mapper}, alpha=1, line_width=2, source=source, selection_alpha=1, nonselection_alpha=0, selection_color={'field': 'totalmin', 'transform': color_mapper})
p.circle(x='LongitudeD', y='LatitudeD', size=5, color='blue', source=source, selection_color='blue', selection_alpha=1, nonselection_alpha=0)
p.circle(x='LongitudeO', y='LatitudeO', size=5, color='red', source=source, selection_color='red', nonselection_alpha=0, name='foo')

# map options and hover tools, including colorbar legend 
hover=HoverTool(tooltips=[('Year','@Year'), ('Origins','@CitiesO'), ('Destination', '@CitiesD'), ('Amount in kg','@totalmin' ), ('Type', '@products')], names=['foo'])

tap = TapTool(names=['foo'])
lasso = LassoSelectTool(names=['foo'])
p.add_tools(tap, lasso, hover)
p.plot_width=1000

ticker=FixedTicker(ticks=[1, 1000, 10000, 100000, 250000, 500000, 750000, 1000000, 10000000, 15000000])
color_bar = ColorBar(color_mapper=color_mapper, ticker=ticker,
                     label_standoff=12, border_line_color=None, location=(0,0), formatter= NumeralTickFormatter())

p.add_layout(color_bar, 'right')

# adds a callback that show the selected glyphs in p in the table

source.callback = CustomJS(args=dict(s2=sourcetable), code="""
        var inds = cb_obj.selected.indices;
        var d1 = cb_obj.data;
        var d2 = s2.data;
        d2['CitiesO'] = []
        d2['CitiesD'] = []
        d2['Year'] = []
        d2['totalmin'] = []
        d2['totalmax'] = []
        d2['passage'] = []
        for (var i = 0; i < inds.length; i++) {
            d2['CitiesO'].push(d1['CitiesO'][inds[i]])
            d2['CitiesD'].push(d1['CitiesD'][inds[i]])
            d2['Year'].push(d1['Year'][inds[i]])
            d2['totalmin'].push(d1['totalmin'][inds[i]])
            d2['totalmax'].push(d1['totalmax'][inds[i]])
            d2['passage'].push(d1['passage'][inds[i]])
        }
        s2.change.emit();
    """)

# create a data table based on sourcetable df.

columns = [
        TableColumn(field='CitiesO', title='Place of Origin'),
        TableColumn(field='CitiesD', title='Destination'),
        TableColumn(field='Year', title='Year'),
        TableColumn(field='passage', title='Nr of passages'),
        TableColumn(field='totalmin', title='Amount (min)'),
        TableColumn(field='totalmax', title='Amount (max)')
        ]
datatable = DataTable(source=sourcetable, columns=columns, width=800)

#Code for the creation of a download  button to download the table

downloadcallback = CustomJS(args=dict(source=sourcetable), code="""
var data = source.data;
var filetext = 'Year,Origin,Destination,passage,totalmin, totalmax\\n';

for (i=0; i < data['CitiesO'].length; i++) {
	var currRow = [data['Year'][i].toString(), data['CitiesO'][i].toString(), data['CitiesD'][i].toString(), data['passage'][i].toString(), data['totalmin'][i].toString(), data['totalmax'][i].toString().concat('\\n')];
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

# Add all text here

div= Div(text=""" <h3>The SoundToll Registers Imagined</h3> <p>This application was developed to visually analyze the Sound Toll Registers based on the information from the <a href="http://www.soundtoll.nl/index.php/en/">Sound Toll Registers Online</a>. Use the sliders to select a data, product and a volume of trade (in kg). 
         On the bottom right side of the map there's a tool box to active specific tools for selecting, panning and zooming on the map. By default only panning and selecting on click are active. The vertical bar on the right side of the map indicates the volume of a product on a logarithmic scale shown on the map as a connection between two places. 
         Currently, selecting and hover only work on <b>red</b> nodes, this might change in the future. Nodes that are selected on the map will also be shown in the table below the map. Using the sliders after a selection will display the visualization to display incorrectly, either reselect or unslect nodes after shifting sliders. </p>
         <p> Because measurement could often vary between time and location a estimated minimum value is shown on the map. An estimated maximum value is shown in the table for each corresponding year for additional accuracy. Occasianly a measurement could not be identified, the volume of trade was set at 0, and is shown on the map in purple. </p>""", width=1000, height=180)
div2= Div(text="""<p>Picking either origins or destination changes what can be selected on the map. If origins is selected, are the red nodes are origins of trade. If destination is selected the red nodes are the destinations.<b>Note that only red nodes on the map can currenlty be selected.</b></p>
          """, width=300, height=100)
#Combnes all aspects, sliders, map and table, into a layout 
layouttext=row(widgetbox(div))
layouttop = column(widgetbox(slider1, slider3, slider2, width=500), row(widgetbox(x_select), widgetbox(y_select), widgetbox(div2, width=300)), p)
layoutbot = row(widgetbox(button), datatable)
layout = column(layouttext, layouttop, layoutbot)
curdoc().add_root(layout)
curdoc().title='Sound'