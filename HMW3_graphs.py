
# coding: utf-8

# In[122]:


from plotly.offline import plot, iplot
import plotly.graph_objs as go
import plotly.figure_factory as ff
from plotly.offline import init_notebook_mode
init_notebook_mode(connected=True)


# In[123]:


xv1 = [-35,-5,-50,-15]
xv2 = [20,15,50,15]
yv1 = ['x1','x2','x3','x4']
yv2 = ['x5','x6','x7','x8']
tr1 = go.Bar(x = xv1, y = yv1, 
               orientation='h', name = '<b>Negative</b>'
             )
tr2 = go.Bar(x = xv2, y = yv2, 
               orientation='h', name = 'Positive'
            )


layout = go.Layout(
    title = '<b>Correlations with employees probability of churn</b>',
    yaxis = dict(autorange='reversed', title ='Variable' )
)
data = [tr1,tr2]
figure = dict(data=data, layout = layout)
iplot(figure)


# In[124]:


import quandl
quandl.ApiConfig.api_key = "WLod4FCtLHjeK8fdx3qR"
df0 = quandl.get("FRED/GDP")
type(df0)
df0.shape
df0.head()
df0.tail()
df1 = df0.reset_index()
df1.shape


# In[125]:


x_values1 = df1['Date']
y_values1 = df1['Value']

trace1 = go.Scatter(x = x_values1, y = y_values1, mode = 'lines', fill = 'tozeroy')
data1 = [trace1]
layout1 = go.Layout(title = '<b>US GDP over time</b>')
figure1 = dict(data=data1, layout = layout1)
iplot(figure1)


# In[126]:


df2_1 = quandl.get("WIKI/GOOGL")
df2_2 = quandl.get("BCHARTS/ABUCOINSUSD")
df2_1.head()
df2_2.head()


# In[127]:


x_values2_1 = df2_1.Open.pct_change()
x_values2_2 = df2_2.Open.pct_change()
trace2_1 = go.Box(x=x_values2_1, name = 'Google')
trace2_2 = go.Box(x=x_values2_2, name = 'Bitcoin')
layout2 = go.Layout(title = '<i>Distribution of Price changes</i>')
data2 = [trace2_2, trace2_1]
figure2 = dict(data=data2, layout = layout2)

iplot(figure2)


# In[128]:


header = dict(values=['Google','Bitcoin'],
              fill = dict(color='#119DFF')
             )
cells = dict(values=[round(df2_1.Open.pct_change()[1:5,],3),
                    round(df2_2.Open.pct_change()[1:5,],3)],
             fill = dict(color=["yellow","white"])
            )
trace3 = go.Table(header=header, cells=cells)

data3 = [trace3]
layout3 = dict(width=500, height=300)
figure3 = dict(data=data3, layout=layout3)
iplot(figure3)


# In[135]:



df4 = [dict(Task="Task1", Start='2018-01-1', Finish='2018-01-30', Resource='Idea Validation'),
      dict(Task="Task2", Start='2018-03-1', Finish='2018-04-15', Resource = 'Prototyping'),
      dict(Task="Task3", Start='2018-04-15', Finish='2018-09-30', Resource='Team formation')]

figure4 = ff.create_gantt(df4,index_col='Resource',show_colorbar=True ,title = 'Startup Roadmap')
iplot(figure4, filename='gantt-simple-gantt-chart')

