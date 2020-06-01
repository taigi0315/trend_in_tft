import math

from bokeh.io import curdoc, output_file, save, show
from bokeh.models import (ColorBar, ColumnDataSource, CustomJS, Div,
                          FixedTicker, LinearAxis, Range1d, Row)
from bokeh.models.tools import HoverTool
from bokeh.plotting import figure
from bokeh.transform import linear_cmap

from .helper import get_count_axis_ticker
from .theme import choi_theme


def hover_tool():
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
        
        fig = figure(x_range=champions, y_range=(0, max(counts)+10), title=title, toolbar_location=None, 
                tools="", y_axis_label='Count')
        
        # Adding second axis for Scatter Plot(Champion_Name | Average_Tier)
        fig.add_layout(
                LinearAxis(
                        y_range_name="Tier",
                        axis_label="Tier",
                        ticker=[0, 1, 2, 3],
                ), "right"
        )

        # Set color palette on bar color
        # bar_color_palette = ["#bf3440","#e69978","#f7c67d","#998c8c","#5c5151"]
        bar_color_palette = ['#FE3D3D', "#f7c67d", "#998c8c"]
        # Adding ColorBar(Champion_Name | Average_Placement)
        tier_mapper = linear_cmap(field_name='Average_Placement', palette=bar_color_palette ,low=0 ,high=5)
        fig.add_layout(
                ColorBar(
                        color_mapper=tier_mapper['transform'],
                        width=10,
                        location=(0,0),
                        ticker=FixedTicker(ticks=[0,1,2,3])
                ), 'right')
        
        # Plot bar chart(Champion_Name | Count)
        bar_color_mapper = linear_cmap("placements", bar_color_palette, low=min(placements), high=max(placements))
        fig.vbar(x='champions', top='counts', color=bar_color_mapper, width=0.77, source=source)

        # # Adding second y-axis for average tier
        fig.extra_y_ranges = {"Tier": Range1d(start=0.5, end=3.5)}
        fig.hex(champions, tiers, y_range_name="Tier", color='#FE3D3D', size=((tiers*3)**1.5).tolist(),
                line_color="#F9C35C", line_width=3, fill_alpha=0.85, line_alpha=0.85)
       
        # Add hover tool div
        fig.add_tools(hover_tool())
        
        # Axis design setting
        fig.xaxis.major_label_orientation = math.pi/3
        
        # Plot grid setting
        fig.xgrid.visible = False
        fig.ygrid.visible = True
        fig.ygrid.grid_line_color = "#EABB74"
        fig.ygrid.grid_line_width = 3
        fig.ygrid.grid_line_alpha = 0.2
        
        # Adding background image to plot
        logo_image_path = "../../../assets/image/tft_logo.png"
        logo_image_height = plot_height * 0.18
        logo_image_width = plot_width * 0.18
        background_image = Div(
            text = f'<div style="position: relative; right:{plot_width*0.5 + logo_image_width}px; top:{plot_height*0.06}px; z-index:100;">\
            <img src={logo_image_path} style="width:{logo_image_width}; height:{logo_image_height}px; opacity: 0.6">\
            </div>')
        
        # Save plot
        save(Row(fig, background_image))
