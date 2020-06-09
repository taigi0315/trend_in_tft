import math

from bokeh.io import curdoc, output_file, save, show
from bokeh.models import (ColorBar, ColumnDataSource, CustomJS, Div,
                          FixedTicker, LinearAxis, Range1d, Row, LabelSet)
from bokeh.models.tools import HoverTool
from bokeh.plotting import figure
from bokeh.transform import linear_cmap

from .helper import get_count_axis_ticker
from .theme import unit_stacked_bar_color_palette, unit_tier_stacked_bar_color_palette

def hover_tool():
        """
        Return custom HoverTool with <div>
        <div>
                - champion image
                - champion usage count
                - champion average tier
                - champion average placement
                - champion average number of item
        </div>
        """

        hover = HoverTool()
        hover.tooltips = """
        <div style="background-color:rgba(0,0,0,0.1);">
                <div style="border-radius: 1px; background-color:rgba(0,0,0,0.1);">
                        <img src=@image alt="" width="125" height="125">
                </div>
                <div style="text-align:center; font-size:16px;"><strong>@champion_name</strong></div>
                <div><strong>Count: @count (@count_percen%)</strong></div>
                <div><strong>Avg_Tier: @average_tier</strong></div>
                <div><strong>Avg_Placement: @average_placement</strong></div>
                <div><strong>Avg_#_Item: @average_number_item</strong></div>
        </div>
        """

        return hover

def build_plot(champion_count_tier_df, title=None, theme=None):
        """
        Build units_count_tier_plot for winner and loser group
            tabs: 6 tabs, cost of champion
            x_axis: champion name
            y_axis: champion usage count in stack of placement
            scatter: average placement of champion
        """
        source = ColumnDataSource(data=champion_count_tier_df)
              
        fig = figure(
                x_range=champion_count_tier_df['champion_name'].tolist(),
                y_range=(0, max(champion_count_tier_df['count'])+int(max(champion_count_tier_df['count'])*0.1)),
                toolbar_location=None,
                tools="",
        )

        # Set Theme
        if theme:
                curdoc().theme = theme
        if title:
                fig.title.text = title

        y_stack_names = ["tier_1", "tier_2", "tier_3"]
        fig.vbar_stack(
            y_stack_names,
            x='champion_name',
            width=0.52,
            color=unit_tier_stacked_bar_color_palette,
            alpha=0.64,
            source=source,
            legend_label=y_stack_names
        )
        fig.legend.location = 'top_left'
        fig.legend.background_fill_color = "#1C1A10"
        fig.legend.background_fill_alpha = 0.3
        fig.legend.label_text_color = "#C4913B"
        fig.legend.border_line_width = 3
        fig.legend.border_line_color = "#1C1A10"
        fig.legend.border_line_alpha = 0.3
        fig.legend.title = 'Tier'
        fig.legend.title_text_color = '#F7E64B'
        fig.legend.label_text_color = '#F7E64B'
        fig.legend.title_text_font_size = '12px'

        
        # Adding second axis for Scatter Plot(champion_name | average_tier)
        fig.add_layout(
                LinearAxis(
                        y_range_name="Average_Tier_Axis",
                        ticker=[0, 1, 2, 3]
                ), "right")
        # Add second y-axis for average tier
        fig.extra_y_ranges = {"Average_Tier_Axis": Range1d(start=0, end=3)}
        
        fig.hex(
                x="champion_name",
                y="average_tier",
                y_range_name="Average_Tier_Axis", 
                color="#F7E64B",
                size=17,
                line_color='#F7E64B',
                line_width=2.5,
                fill_alpha=0.45,
                line_alpha=0.85,
                source=source
        )

        # Add hover tool div
        fig.add_tools(hover_tool())

        # Axis design setting
        fig.xaxis.major_label_orientation = math.pi/3
        fig.xaxis.major_label_text_font_style = 'bold'
        
        # Plot grid setting
        fig.xgrid.visible = False
        fig.ygrid.visible = True
        fig.ygrid.grid_line_color = "#EABB74"
        fig.ygrid.grid_line_width = 3
        fig.ygrid.grid_line_alpha = 0.2
        
        # Adding background image to plot
        logo_image_path = "../../../assets/image/tft_logo.png"
        plot_width = fig.plot_width
        plot_height= fig.plot_height
        logo_image_width = plot_width*0.2
        logo_image_height = plot_height*0.2
        background_image = Div(
            text = f'<div style="position: relative; left:{-(1.0*plot_width)}px; top:{plot_height*0.025}px; z-index:100;">\
            <img src={logo_image_path} style="width:{logo_image_width}; height:{logo_image_height}px; opacity: 0.70">\
            </div>')

        return fig, background_image
