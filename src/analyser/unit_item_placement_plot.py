import pandas as pd
import math
from os.path import dirname, join

from bokeh.io import curdoc, output_file, save, show
from bokeh.models import (ColorBar, ColumnDataSource, CrosshairTool, CustomJS,
                          Div, FixedTicker, LinearAxis, Range1d, Row)
from bokeh.models.tools import HoverTool
from bokeh.plotting import figure
from bokeh.transform import linear_cmap

from .helper import get_count_axis_ticker, find_item_name
from .theme import unit_stacked_bar_color_palette
DATA_DIR = join(dirname(__file__), '../experiment')

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
	            <img src=@Image alt="" width="125" height="125">
	    </div>
	    <div style="text-align:center; font-size:16px;"><strong>@Item_Name</strong></div>
	    <div><strong>Count: @Count (@Count_Pct%)</strong></div>
	    <div><strong>Avg_Placement: @Average_Placement</strong></div>
    </div>
    """

    return hover


def build_units_item_placement_plot(units_item_placement_df, title=None, theme=None):
    """
    
    """
    test_data = units_item_placement_df['TFT3_Kayle']
    sorted_data = test_data.reindex(test_data.sum().sort_values().index, axis=1)

    Plot_Data = {
        "1": list(sorted_data.loc[1][:]),
        "2": list(sorted_data.loc[1][:]),
        "3": list(sorted_data.loc[1][:]),
        "4": list(sorted_data.loc[1][:]),
        "5": list(sorted_data.loc[1][:]),
        "6": list(sorted_data.loc[1][:]),
        "7": list(sorted_data.loc[1][:]),
        "8": list(sorted_data.loc[1][:])
    }
    source = ColumnDataSource(data=Plot_Data)
    
    print()
    fig = figure(
        x_range=sorted_data['Item_Name'],
        y_range=(0, int(max_count_value + (max_count_value*0.1))),
        toolbar_location=None,
        tools="",
    )
    
    # Set Theme
    if theme:
            curdoc().theme = theme
    if title:
       fig.title.text = title

    y_stack_names = ["1", "2", "3", "4", "5", "6", "7", "8"]
    fig.vbar_stack(
        y_stack_names,
        x='Item_Name',
        width=0.52,
        color=unit_stacked_bar_color_palette,
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
    fig.legend.title = 'Placement'
    fig.legend.title_text_color = '#F7E64B'
    fig.legend.label_text_color = '#F7E64B'
    fig.legend.title_text_font_size = '12px'
    fig.xaxis.major_label_orientation = math.pi/3
    fig.xaxis.major_label_text_font_style = 'bold'
    
    # Plot grid setting
    fig.xgrid.visible = False
    fig.ygrid.visible = True
    fig.ygrid.grid_line_color = "#EABB74"
    fig.ygrid.grid_line_width = 3
    fig.ygrid.grid_line_alpha = 0.2


    fig.add_layout(
        LinearAxis(
                y_range_name="Average_Placement",
                ticker=[1, 2, 3, 4, 5, 6, 7, 8]
        ), "right"
    )
    fig.extra_y_ranges = {"Average_Placement": Range1d(start=1, end=8)}

    # # Add second y-axis for average placement
    # fig.extra_y_ranges = {"Average_Placement": Range1d(start=1, end=8)}
    # fig.hex(
    #         x="Name",
    #         y="Average_Placement",
    #         y_range_name="Average_Placement", 
    #         color="#F7E64B",
    #         size=17,
    #         line_color='#F7E64B',
    #         line_width=2.5,
    #         fill_alpha=0.25,
    #         line_alpha=0.85,
    #         source=source
    # )

    # Add hover tool div
    fig.add_tools(hover_tool())

    
    # # Add hover tool div
    # fig.add_tools(hover_tool())

    # # Set color palette on bar color
    # bar_color_palette = ['#FE3D3D', "#F59537", "#FCD89F", "#998c8c", "#302E2E"]

    # # Add ColorBar(Item_Name | Average_Placement)
    # tier_mapper = linear_cmap(
    #     field_name='Average_Placement',
    #     palette=bar_color_palette,
    #     low=0,
    #     high=5
    # )

    # fig.add_layout(
    #     ColorBar(
    #         color_mapper=tier_mapper['transform'],
    #         width=10,
    #         location=(0, 0),
    #         ticker=FixedTicker(ticks=[1, 2, 3, 4, 5])
    #     ), 'right')

    # # Plot bar chart(Item_Name | Count)
    # bar_color_mapper = linear_cmap(
    #     "Average_Placement",
    #     bar_color_palette,
    #     low=min(Average_Placement),
    #     high=max(Average_Placement)
    # )
    # fig.vbar(
    #     x='Item_Name',
    #     top='Count',
    #     color=bar_color_mapper,
    #     width=0.77,
    #     source=source
    # )

    # # Axis design setting
    # fig.xaxis.major_label_orientation = math.pi/3
    # fig.xaxis.major_label_text_font_style = 'bold'

    # # Plot grid setting
    # fig.xgrid.visible = False
    # fig.ygrid.visible = True
    # fig.ygrid.grid_line_color = "#EABB74"
    # fig.ygrid.grid_line_width = 3
    # fig.ygrid.grid_line_alpha = 0.2

    # # Adding background image to plot
    # logo_image_path = "../../../assets/image/tft_logo.png"
    # plot_width = fig.plot_width
    # plot_height = plot_width * 1.61
    # logo_image_height = plot_width*0.16
    # logo_image_width = plot_height*0.16
    # background_image = Div(
    #     text=f'<div style="position: relative; right:{plot_width*0.5 + logo_image_width}px; top:{plot_height*0.02}px; z-index:100;">\
    #         <img src={logo_image_path} style="width:{logo_image_width}; height:{logo_image_height}px; opacity: 0.70">\
    #         </div>')

    # return fig, background_image

    return fig