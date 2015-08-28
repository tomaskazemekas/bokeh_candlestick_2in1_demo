# bokeh_candlestic_2in1_demo

2 in 1 graph.

This is a script that extracts the data on the qoutes and the positions 
of the futures instuments from the Postgres database. It produces pandas 
dataframes from the data. One can select an instrument by its adjusted id
and the graph will be outputed in a new browser tab. The integrated graph
will show a candlestick plot of the quotes and the bar graph for the
postions on the date of the selected insrument. 
