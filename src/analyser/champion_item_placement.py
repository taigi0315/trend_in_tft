import math
import os

import pandas as pd
from bokeh.io import curdoc, output_file, save, show
from bokeh.models import (ColorBar, ColumnDataSource, CustomJS, Div,
                          FixedTicker, Legend, LinearAxis, Range1d, Row, Select, PreText)
from bokeh.models.tools import HoverTool
from bokeh.plotting import figure
from bokeh.transform import linear_cmap
from bokeh.layouts import column, row
from .helper import get_count_axis_ticker, CHAMPION_NAMES
from .theme import unit_stacked_bar_color_palette

FILE_PATH = None

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
                <div style="text-align:center; font-size:16px;"><strong>@item_name</strong></div>
                <div><strong>Count: @count (@count_percent%)</strong></div>
                <div><strong>Avg_Placement: @average_placement</strong></div>
        </div>
        """

        return hover


def build_plot(file_name_prefix, title=None, theme=None):
        """
        """
        for champion_name in CHAMPION_NAMES:
                stats = PreText(text=champion_name, width=1200)
                FILE_PATH = f'assets/data/{file_name_prefix}/champion_item_placement'
                # def champ_ticker_change(attrname, old, new):
                        
                #         data = pd.read_csv(f"{FILE_PATH}/{champ_name}_item_placement.csv")
                #         data = data.sort_values(by=['count'])
                #         data = data[data['count'] > 0]

                #         selected_champ_name = champ_select_ticker.value
                #         data = get_data(selected_champ_name)
                #         source.data = data
                
                if not os.path.exists(f"assets/plot/{file_name_prefix}/champion_item_placement/"):
                        os.makedirs(f"assets/plot/{file_name_prefix}/champion_item_placement/")

                output_file(f"assets/plot/{file_name_prefix}/champion_item_placement/{champion_name}_item_placement_plot.html")
                
                champion_item_placemet_data_list = os.listdir(FILE_PATH)
                data = pd.read_csv(f"{FILE_PATH}/{champion_name}_item_placement.csv")
                data = data.sort_values(by=['count'])
                data = data[data['count'] > 0]

                source = ColumnDataSource(data=data)

                
                try:
                        y_range_max = max(data['count'])+int(max(data['count'])*0.1)
                except ValueError:
                        y_range_max = 1

                fig = figure(
                        x_range=data['item_name'].tolist(),
                        y_range=(0, y_range_max),
                        tools="undo, box_zoom, reset",
                        toolbar_location="right"
                )

                # Set Theme
                if theme:
                        curdoc().theme = theme
                if title:
                        fig.title.text = title

                y_stack_names = ["1", "2", "3", "4", "5", "6", "7", "8"]
                fig.vbar_stack(
                y_stack_names,
                x='item_name',
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

                # Adding second axis for Scatter Plot(Champion_Name | Average_Tier)
                fig.add_layout(
                        LinearAxis(
                                y_range_name="Average_Placement_Axis",
                                ticker=[1, 2, 3, 4, 5, 6, 7, 8]
                        ), "right"
                )
                # Set extra axis range
                fig.extra_y_ranges = {"Average_Placement_Axis": Range1d(start=0.5, end=8.5)}
                # Add scatter of average placement of champion on the plot
                fig.hex(
                        x="item_name",
                        y="average_placement",
                        y_range_name="Average_Placement_Axis", 
                        color="#F7E64B",
                        size=17,
                        line_color='#F7E64B',
                        line_width=2.5,
                        fill_alpha=0.25,
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
                
                # Add dropdown for champion 
                # champ_select_ticker = Select(value=selected_champion_name, options=CHAMPION_NAMES)
                # champ_select_ticker.on_change('value', champ_ticker_change)
                # widgets = column(champ_select_ticker)

                # Adding background image to plot
                logo_image_path = "../../../../statics/tft_logo.png"
                plot_width = fig.plot_width
                plot_height= fig.plot_height
                logo_image_width = plot_width*0.2
                logo_image_height = plot_height*0.2
                background_image = Div(
                text = f'<div style="position: relative; left:{-(1*plot_width)}px; top:{plot_height*0.025}px; z-index:100;">\
                <img src={logo_image_path} style="width:{logo_image_width}; height:{logo_image_height}px; opacity: 0.70">\
                </div>')

                #return fig, widgets, background_image
                save(column(stats, Row(fig, background_image)))

