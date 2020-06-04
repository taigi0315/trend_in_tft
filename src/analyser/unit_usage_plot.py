import math

from bokeh.io import curdoc, output_file, save, show
from bokeh.models import (ColorBar, ColumnDataSource, CustomJS, Div,
                          FixedTicker, LinearAxis, Range1d, Row)
from bokeh.models.tools import HoverTool
from bokeh.plotting import figure
from bokeh.transform import linear_cmap

from .helper import get_count_axis_ticker
from .theme import bar_color_palette


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
                <div style="text-align:center; font-size:16px;"><strong>@Champion_Name</strong></div>
                <div><strong>Count: @Count (@Count_Pct%)</strong></div>
                <div><strong>Avg_Tier: @Average_Tier</strong></div>
                <div><strong>Avg_Placement: @Average_Placement</strong></div>
                <div><strong>Avg_Item: @Average_Item</strong></div>
        </div>
        """

        return hover

def build_all_player_unit_usage_plot(units_df, title=None, theme=None):
        """
        Build a figure of unit usage plot
        Arguments:
                units_df(DataFrame): result from TFTDataBuilder.build_units_dataframe
                columns : ['Champion_Id', 'Champion_Name', 'Count', 'Tier', 'Traits',
                        'Item', 'Average_#_Item', 'Placement_List', 'Average_Placement',
                        'Average_Tier', 'Count(%)', 'Image']) 
        Returns:
                fig(Figure)
                background_image: logo image file
        """       
        sorted_units_df = units_df.sort_values(by=['Count'], ascending=False)
        Champion_Name = sorted_units_df['Champion_Name'].tolist()
        Count = sorted_units_df['Count'].tolist()
        Average_Tier = sorted_units_df['Average_Tier'].tolist()
        Average_Placement = sorted_units_df['Average_Placement'].tolist()
        Image = sorted_units_df['Image'].tolist()
        
        source = ColumnDataSource(data=dict(
                Champion_Name=Champion_Name,
                Count=Count,
                Count_Pct=sorted_units_df['Count(%)'],
                Average_Tier=Average_Tier,
                Average_Placement=Average_Placement,
                Average_Item=sorted_units_df['Average_#_Item'],
                Image=Image)
        )
              
        fig = figure(
                x_range=Champion_Name,
                y_range=(0, max(Count)+int(max(Count)*0.05)),
                toolbar_location=None,
                tools="",
                y_axis_label='Count'
        )

        # Set Theme
        if theme:
                curdoc().theme = theme
        if title:
                fig.title.text = title

        # Adding second axis for Scatter Plot(Champion_Name | Average_Tier)
        fig.add_layout(
                LinearAxis(
                        y_range_name="Average_Tier",
                        axis_label="Tier",
                        ticker=[0, 1, 2, 3, 4, 5]
                ), "right"
        )
        
        # Add ColorBar(Champion_Name | Average_Placement)
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
                        location=(0,0),
                        ticker=FixedTicker(ticks=[1, 2, 3, 4, 5])
                ), 'right')
        
        # Plot bar chart(Champion_Name | Count)
        bar_color_mapper = linear_cmap(
                "Average_Placement",
                bar_color_palette,
                low=min(Average_Placement),
                high=max(Average_Placement)
        )
        fig.vbar(
                x='Champion_Name',
                top='Count',
                color=bar_color_mapper,
                width=0.77,
                source=source
        )

        # Add second y-axis for average tier
        fig.extra_y_ranges = {"Average_Tier": Range1d(start=0.5, end=3.5)}
        fig.hex(
                x="Champion_Name",
                y="Average_Tier",
                y_range_name="Average_Tier", 
                color='#A517E1',
                size=11,
                line_color="#9B0DAC",
                line_width=2,
                fill_alpha=0.55,
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
            text = f'<div style="position: relative; right:{plot_width*0.6 + logo_image_width}px; top:{plot_height*0.05}px; z-index:100;">\
            <img src={logo_image_path} style="width:{logo_image_width}; height:{logo_image_height}px; opacity: 0.70">\
            </div>')

        return fig, background_image


def build_winner_loser_unit_usage_plot(winner_units_df, loser_units_df, theme=None):
        """
        Build a figure of unit usage plot spliting units_df in winner(placement:1~4) and loser(placement:5~8)
        Arguments:
                units_df(DataFrame): result from TFTDataBuilder.build_units_dataframe
                columns : ['Champion_Id', 'Champion_Name', 'Count', 'Tier', 'Traits',
                        'Item', 'Average_#_Item', 'Placement_List', 'Average_Placement',
                        'Average_Tier', 'Count(%)', 'Image']) 
        Returns:
                fig(Figure)
                background_image: logo image file
        """       
        win_fig, background_image = build_all_player_unit_usage_plot(
                units_df=winner_units_df,
                title="Winner",
                theme=theme
        )
        lose_fig, background_image = build_all_player_unit_usage_plot(
                units_df=loser_units_df,
                title="Loser",
                theme=theme
        )

        return [win_fig, lose_fig, background_image]
