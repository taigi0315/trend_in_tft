from bokeh.plotting import figure
from bokeh.io import output_file, show
from bokeh.models import ColumnDataSource, LinearAxis, Range1d, CustomJS, Div, Row, ColorBar
from bokeh.transform import linear_cmap
from bokeh.models.tools import HoverTool
import math

class TFTDataAnalyser:
    def __init__(self, db, region='na'):
        self.db = db

    def get_match_data_from_db(self, region='na1'):
        regx = "^" + region.upper()
        match_data = list(self.db.collection.find( {'_id': {'$regex':regx} }))
        # match_data = match_data[:10]
        # test_data_ids = ["NA1_3436887139", "NA1_3436855922"]
        # match_data = list(self.db.collection.find({'_id': {'$in': test_data_ids }}))
        self.match_data = match_data

    def get_count_axis_ticker(self, max_count):
        max_num = int(math.ceil(max_count / 50.0)) * 50
        interval = int(max_num / 5)
        return list(range(0, max_num+interval, interval))

    def plot_units_df(self, units_df, title='Unit Usage'):
        output_file("test_plot.html")
        sorted_units_df = units_df.sort_values(by=['Count'], ascending=False)

        champions = sorted_units_df['Champion'].tolist()
        counts = sorted_units_df['Count'].tolist()
        tiers = sorted_units_df['Average_Tier']
        placements = sorted_units_df['Average_Placement']
        images = sorted_units_df['Image']
        
        source = ColumnDataSource(data=dict(champions=champions, counts=counts, tiers=tiers, placements=placements, images=images))
        plot_height = 500
        plot_width = int(plot_height * 1.61)
        
        
        p = figure(x_range=champions, y_range=(0, max(counts)+10), plot_height=plot_height,
                plot_width=plot_width, title=title, toolbar_location=None, tools="",
                background_fill_color="#FAFCFC", y_axis_label='Count')
        p.background_fill_alpha = 0.35
        #p.legend.orientation = "horizontal"
        #p.legend.location = "top_right"

        # Remove the grid
        p.xgrid.visible = False
        p.ygrid.visible = False

        # Adding background image to plot
        logo_image_path = "assets/image/tft_logo_2.png"
        logo_image_height = plot_height * 0.3
        logo_image_width = plot_width * 0.35
        background_image = Div(
            text = f'<div style="position: relative; right:{plot_width*0.5}px; top:{plot_height*0.06}px">\
            <img src={logo_image_path} style="width:{logo_image_width}; height:{logo_image_height}px; opacity: 0.5">\
            </div>')

        # Adding bar chart to plot
        color_palette = ["#b2200c","#e0461f","#f18350","#f4bc8e","#52b2d5","#0a7197","#085776","#04364e"]
        bar_color_mapper = linear_cmap("placements", color_palette, low=min(placements), high=max(placements))
        p.vbar(x='champions', top='counts', color=bar_color_mapper, width=0.6, source=source)
        
        
        # Calculate Count ticker
        p.yaxis.ticker = self.get_count_axis_ticker(max(counts))
        # Rotate x-axis label
        p.xaxis.major_label_orientation = math.pi/3
        p.xaxis.axis_label_text_font_size = "200pt"
        # Adding second y-axis for average tier
        p.extra_y_ranges = {"Tier": Range1d(start=1, end=3)}
        # Adding second axis for Scatter Plot(average tier)
        p.add_layout(LinearAxis(y_range_name="Tier", axis_label="Tier", ticker=[1, 1.5, 2, 2.5, 3]), "right")
        p.scatter(champions, tiers, y_range_name="Tier", marker="hex",
                color='#9e6c36', size=15, line_color='#ff5a00', line_width=2.5, fill_alpha=0.45, line_alpha=0.7)

        # Adding average placement Color Bar(average placement)
        tier_mapper = linear_cmap(field_name='Average_Placement', palette=color_palette ,low=1 ,high=8)
        color_bar = ColorBar(color_mapper=tier_mapper['transform'], width=8,  location=(0,0))
        p.add_layout(color_bar, 'right')
        
        # Set Title
        p.title.text_color = '#feffe1'
        p.title.text_font = "times"
        p.title.text_font_style = "italic"
        
        
        # Add Tooltips
        hover = HoverTool()
        hover.tooltips = """
        <div>
            <div><img src=@images alt="" width="100" /></div>
            <h3>@champions</h3>
            <div><strong>Count: </strong>@counts</div>
            <div><strong>Avg_Tier: </strong>@tiers</div>
            <div><strong>Avg_Placement: </strong>@placements</div>
        </div>
        """
        p.add_tools(hover)
        
        show(Row(p, background_image))
