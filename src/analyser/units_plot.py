import math

from bokeh.io import curdoc, output_file, save, show
from bokeh.models import (ColorBar, ColumnDataSource, CustomJS, Div,
                          FixedTicker, LinearAxis, Range1d, Row)
from bokeh.models.tools import HoverTool
from bokeh.plotting import figure
from bokeh.transform import linear_cmap

from .helper import get_count_axis_ticker
from .theme import choi_theme


def build_hover_tool():
         # Add Tooltips
        hover = HoverTool()
        hover.tooltips = """
        <div style="background-color:rgba(0,0,0,0.1);">
                <div style="border-radius: 1px; background-color:rgba(0,0,0,0.1);">
                        <img src=@images alt="" width="125" height="125">
                </div>
                <div><strong>Count: @counts</strong></div>
                <div><strong>Avg_Tier: @tiers</strong></div>
                <div><strong>Avg_Placement: @placements %</strong></div>
        </div>
        """

        return hover

def plot_units_df(units_df, title='Unit Usage'):
        output_file(f"experiments/plot/unit_plot/{title}_plot.html")
        # Set Theme
        curdoc().theme = choi_theme
        
        sorted_units_df = units_df.sort_values(by=['Count'], ascending=False)
        champions = sorted_units_df['Champion_Name'].tolist()
        counts = sorted_units_df['Count'].tolist()
        tiers = sorted_units_df['Average_Tier']
        placements = sorted_units_df['Average_Placement']
        images = sorted_units_df['Image']
        
        source = ColumnDataSource(data=dict(
                champions=champions,
                counts=counts,
                tiers=tiers,
                placements=placements,
                images=images)
        )
        
        plot_height = 750
        plot_width = int(plot_height * 1.61)   
        
        p = figure(x_range=champions, y_range=(0, max(counts)+10), plot_height=plot_height,
                plot_width=plot_width, title=title, toolbar_location=None, 
                tools="", y_axis_label='Count')

        # Adding background image to plot
        logo_image_path = "../../../assets/image/tft_logo_2.png"
        logo_image_height = plot_height * 0.18
        logo_image_width = plot_width * 0.18
        background_image = Div(
            text = f'<div style="position: relative; right:{plot_width*0.5 + logo_image_width}px; top:{plot_height*0.06}px">\
            <img src={logo_image_path} style="width:{logo_image_width}; height:{logo_image_height}px; opacity: 0.7">\
            </div>')

        # Set color palette on bar color
        color_palette = ["#bf3440","#e69978","#f7c67d","#998c8c","#5c5151"]
        bar_color_mapper = linear_cmap("placements", color_palette, low=min(placements), high=max(placements))
        p.vbar(x='champions', top='counts', color=bar_color_mapper, width=0.6, source=source)
        
        # Calculate Count ticker * ticker seems not good
        #p.yaxis.ticker = get_count_axis_ticker(max(counts))
        
        # Adding second y-axis for average tier
        p.extra_y_ranges = {"Tier": Range1d(start=1, end=3)}
        
        # Adding second axis for Scatter Plot(average tier)
        p.add_layout(
                LinearAxis(
                        y_range_name="Tier",
                        axis_label="Tier",
                        ticker=[0, 1, 2, 3],
                        axis_label_text_color="#EDBE74",
                        axis_label_text_font_size="18pt",
                        major_label_text_font_size="8pt"
                ), "right"
        )
        p.scatter(champions, tiers, y_range_name="Tier", marker="hex",
                color='#9e6c36', size=12, line_color='#ff5a00', line_width=2.5, fill_alpha=0.5, line_alpha=0.7)

        # Adding ColorBar(average placement)
        tier_mapper = linear_cmap(field_name='Average_Placement', palette=color_palette ,low=0 ,high=5)
        ticker = FixedTicker(ticks=[0,1,2,3,4,5])
        color_bar = ColorBar(color_mapper=tier_mapper['transform'], width=15,  location=(0,0), ticker=ticker)
        p.add_layout(color_bar, 'right')
        
        # Add hover tool div
        p.add_tools(build_hover_tool())
        
        # Axis design setting
        p.xaxis.major_label_orientation = math.pi/3
        
        # Plot grid setting
        p.xgrid.visible = False
        p.ygrid.visible = True
        p.ygrid.grid_line_color = "#EABB74"
        p.ygrid.grid_line_width = 3
        p.ygrid.grid_line_alpha = 0.2

        # Save plot
        save(Row(p, background_image))
