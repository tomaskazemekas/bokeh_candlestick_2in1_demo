# -*- coding: utf-8 -*-
# Python environment: Anaconda3

# by Tomas Kazemekas, 
# tomaskazemekas@gmail.com

# Version: 2.0

"""
2 in 1 graph.

This is a script that extracts the data on the qoutes and the positions 
of the futures instuments from the Postgres database. It produces pandas 
dataframes from the data. One can select an instrument by its adjusted id
and the graph will be outputed in a new browser tab. The integrated graph
 will show a candlestick plot of the quotes and the bar graph for the
 postions on the date of the selected insrument. 
 """
 
# Bokeh version 0.9.0 is required!

import psycopg2
import pandas as pd
from bokeh.io import output_file, show
from bokeh.plotting import figure


# Connecting to the database. 
# Set the database name and you user name (password, if required) below
# in the brackets.
conn = psycopg2.connect(" dbname='paris_dev' user='tomas' password=None ")


# Geting the data form the database in a form of pandas dataframes.
# This part of the script can be done only once and is not necesary
# to execute it if you just want to change adjusted instrument id.
with conn:
    q1 = "SELECT * FROM oxl.adjusted_quotes"
    q2 = "SELECT * FROM oxl.da_position"
    df1 = pd.read_sql(q1, conn)
    df2 = pd.read_sql(q2, conn)
    print (df1.shape)
    print (df2.shape)
    
    
print(df1.head(30))
print(df2.head(30))  


# Set wanted ajdusted instrument id, e.g. 41, 38, 27, 48, 21...
ADJ_INSTR_ID = 41

# Renaming the date column to the sam ename in both dataframes.
df2.rename(columns={'last_data_date':'timestamp'}, inplace=True)


# Extracting the data for the selected instument.
df1_ai1 = df1.loc[df1['adjusted_instrument_id'] == ADJ_INSTR_ID]

df2_ai1 = df2.loc[df2['adjusted_instrument_id'] == ADJ_INSTR_ID]


# Merging both dataframes on the timestamp field. It is an inner join.
df_j = pd.merge(df1_ai1, df2_ai1, on="timestamp", sort=False)


# Starting the visualisation.

# Seting the name ogf the output file ant the title.
output_file("candlestick_bar2in1.html", title="Candlestick and Bar Graph 2 in 1")

TOOLS = "pan, wheel_zoom, box_zoom, reset, save"


# Calculations for the candlestick graph.
mids = (df_j.open + df_j.close)/2
spans = abs(df_j.close - df_j.open)

# Consturcting logical series.
inc = df_j.close > df_j.open
dec = df_j.open > df_j.close

# Seting width of the bars.
w = 12*60*60*1000 # half day in ms

# Seting the params for the first figure.
s1 = figure(x_axis_type="datetime", tools=TOOLS, plot_width=1000,
           plot_height=600)

# Setting the segment glyph params.
s1.segment(df_j.timestamp, df_j.high, df_j.timestamp, df_j.low,
          color="black", toolbar_location="left")

# Setting the rect glyph params.          
s1.rect(df_j.timestamp[inc], mids[inc], w, spans[inc],
        fill_color="#D5E1DD", line_color="black")          

s1.rect(df_j.timestamp[dec], mids[dec], w, spans[dec],
        fill_color="#F2583E", color="red")
        
# Seting the title of the first graph.
s1.title = "Price (candlestick) and Position (bar) \
 for Adj. Instrument Id {value}".format(value=ADJ_INSTR_ID)


# Calculations for the bar graph.

# Consturcting logical series.
long = df_j.position > 0
short = df_j.position < 0

# Adjusting the cetral coordinate of the bars for display on the 0 line.
ad_bar_coord = df_j.position / 2

bar_span = abs(df_j.position)


# Setting the bar graph.
             
# Setting the params for the rect glyph used as for bars.             
s1.rect(df_j.timestamp[long], ad_bar_coord[long], w, bar_span[long],
         fill_color="#D5E1DD", color="green")
s1.rect(df_j.timestamp[short], ad_bar_coord[short], w, bar_span[short],
         fill_color="#F2583E", color="red")

# Show the 2 in 1 graph.
show(s1)

