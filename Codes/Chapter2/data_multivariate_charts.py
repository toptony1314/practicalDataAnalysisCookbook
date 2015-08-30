import bokeh.plotting as b
import sqlalchemy as sa
import pandas as pd

# colors for different bed count
colormap = {
    2: 'red',
    3: 'green',
    4: 'blue'
}

# database credentials
usr  = 'drabast'
pswd = 'pAck7!B0ok'

# create the connection to the database
engine = sa.create_engine(
    'postgresql://{0}:{1}@localhost:5432/{0}' \
    .format(usr, pswd)
)

# print the top 10 rows from the database
query = 'SELECT beds, sq__ft, price / 1000 AS price \
    FROM real_estate \
    WHERE sq__ft > 0 \
    AND beds BETWEEN 2 AND 4'

# extract the data
data = pd.read_sql_query(query, engine)

# attach the color based on the bed count
data['color'] = data['beds'].map(lambda x: colormap[x])

# specify the output HTML file
b.output_file(
    '../../Data/Chapter2/Figures/price_bed_area.html',
    title='Price vs floor area for different bed count'
)

# create the figure and specify label for axes
fig = b.figure(title='Price vs floor area and bed count')
fig.xaxis.axis_label = 'Feet sq'
fig.yaxis.axis_label = 'Price ($ \'000)'

# and plot the data
for i in range(2,5):
    d = data[data.beds == i]

    fig.circle(d['sq__ft'],d['price'], color=d['color'],
        fill_alpha=.1, size=8, legend='{0} beds'.format(i))

# then show the plot in the browser
b.show(fig)