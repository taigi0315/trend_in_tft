import math

from bokeh.io import curdoc, output_file, save, show
from bokeh.models import (ColorBar, ColumnDataSource, CustomJS, Div,
                          FixedTicker, LinearAxis, Range1d, Row)
from bokeh.models.tools import HoverTool
from bokeh.plotting import figure
from bokeh.transform import linear_cmap

from .helper import get_count_axis_ticker
from .theme import unit_stacked_bar_color_palette

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


def build_item_count_placement_plot(items_df, title=None, theme=None):
        """
        Build a figure of item usage plot
        Arguments:
                items_df(DataFrame): result from TFTDataBuilder.build_units_dataframe
                columns : ['Id', 'Count', Sum_Placement', 'Placement_List',
                        'Placement', 'Name', 'Average_Placement', 'Count(%)', 'Image']) 
        Returns:
                fig(Figure)
                background_image: logo image file
        """       
        items_df  = items_df.sort_values(by=['Count'])
        Item_Name = items_df['Name'].tolist()
        Plot_Data = {
            "1": [],
            "2": [],
            "3": [],
            "4": [],
            "5": [],
            "6": [],
            "7": [],
            "8": []
        }
        for placements in items_df['Placements']:
            for placement, count in placements.items():
                Plot_Data[str(placement)].append(count)
        
        Plot_Data['Image'] = items_df['Image']
        Plot_Data['Item_Name'] = items_df['Name']
        Plot_Data['Average_Placement'] = items_df['Average_Placement']
        Plot_Data['Count'] = items_df['Count']
        Plot_Data['Count_Pct'] = items_df['Count(%)']

        source = ColumnDataSource(data=Plot_Data)
              
        fig = figure(
                x_range=Item_Name,
                y_range=(0, max(items_df['Count'])+int(max(items_df['Count'])*0.05)),
                toolbar_location=None,
                tools="",
        )

        # Set Theme
        if theme:
                curdoc().theme = theme
        if title:
                fig.title.text = title

        # Adding second axis for Scatter Plot(Champion_Name | Average_Tier)
        fig.add_layout(
                LinearAxis(
                        y_range_name="Average_Placement",
                        ticker=[1, 2, 3, 4, 5, 6, 7, 8]
                ), "right"
        )

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

        # Add second y-axis for average placement
        fig.extra_y_ranges = {"Average_Placement": Range1d(start=1, end=8)}
        fig.hex(
                x="Item_Name",
                y="Average_Placement",
                y_range_name="Average_Placement", 
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
        
        # Adding background image to plot
        logo_image_path = "../../../assets/image/tft_logo.png"
        plot_width = fig.plot_width
        plot_height= fig.plot_height
        logo_image_width = plot_width*0.15
        logo_image_height = plot_height*0.15
        background_image = Div(
            text = f'<div style="position: relative; left:{-(1.65*plot_width)}px; top:{plot_height*0.05}px; z-index:100;">\
            <img src={logo_image_path} style="width:{logo_image_width}; height:{logo_image_height}px; opacity: 0.70">\
            </div>')

        return fig, background_image
