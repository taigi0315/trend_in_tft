from bokeh.models import CustomJS, CrosshairTool
import math

from bokeh.io import curdoc, output_file, save, show
from bokeh.models import (ColorBar, ColumnDataSource, CustomJS, Div,
                          FixedTicker, LinearAxis, Range1d, Row)
from bokeh.models.tools import HoverTool
from bokeh.plotting import figure
from bokeh.transform import linear_cmap

from .helper import get_count_axis_ticker


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


def build_all_player_items_plot(items_df, title=None, theme=None):
    """
    Plot default items figure
    """
    # Set Theme
    if theme:
        curdoc().theme = theme

    sorted_items_df = items_df.sort_values(by=['Count'], ascending=False)
    Item_Name = sorted_items_df['Name'].tolist()
    Count = sorted_items_df['Count'].tolist()
    Average_Placement = sorted_items_df['Average_Placement'].tolist()
    Image = sorted_items_df['Image'].tolist()

    source = ColumnDataSource(data=dict(
        Item_Name=Item_Name,
        Count=Count,
        Count_Pct=sorted_items_df['Count(%)'],
        Average_Placement=Average_Placement,
        Image=Image)
    )

    fig = figure(
        x_range=Item_Name,
        y_range=(0, max(Count) + int(max(Count)*0.05)),
        toolbar_location=None,
        tools="",
        y_axis_label='Count'
    )
    if title:
        fig.title.text = title

    # Add hover tool div
    fig.add_tools(hover_tool())

    # Set color palette on bar color
    bar_color_palette = ['#FE3D3D', "#F59537", "#FCD89F", "#998c8c", "#302E2E"]

    # Add ColorBar(Item_Name | Average_Placement)
    tier_mapper = linear_cmap(
        field_name='Average_Placement',
        palette=bar_color_palette,
        low=0,
        high=5
    )

    fig.add_layout(
        ColorBar(
            color_mapper=tier_mapper['transform'],
            width=10,
            location=(0, 0),
            ticker=FixedTicker(ticks=[1, 2, 3, 4, 5])
        ), 'right')

    # Plot bar chart(Item_Name | Count)
    bar_color_mapper = linear_cmap(
        "Average_Placement",
        bar_color_palette,
        low=min(Average_Placement),
        high=max(Average_Placement)
    )
    fig.vbar(
        x='Item_Name',
        top='Count',
        color=bar_color_mapper,
        width=0.77,
        source=source
    )

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
    plot_height = plot_width * 1.61
    logo_image_height = plot_width*0.16
    logo_image_width = plot_height*0.16
    background_image = Div(
        text=f'<div style="position: relative; right:{plot_width*0.5 + logo_image_width}px; top:{plot_height*0.02}px; z-index:100;">\
            <img src={logo_image_path} style="width:{logo_image_width}; height:{logo_image_height}px; opacity: 0.70">\
            </div>')

    return fig, background_image


def build_winner_loser_item_usage_plot(winner_items_df, loser_items_df, theme=None):
    win_fig, background_image = build_all_player_items_plot(
        items_df=winner_items_df,
        title="Winner",
        theme=theme
    )
    win_fig.add_tools(hover_tool())
    
    lose_fig, background_image = build_all_player_items_plot(
        items_df=loser_items_df,
        title="Loser",
        theme=theme
    )

    return [win_fig, lose_fig, background_image]
