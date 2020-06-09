import pandas as pd
from bokeh.io import output_file, save
from bokeh.layouts import gridplot
from bokeh.models import Row
from bokeh.models.widgets import Panel, Tabs

from . import champion_count_placement, champion_count_tier,champion_item_placement
from .helper import split_df_by_champion_cost
from .item_count_placement_plot import build_item_count_placement_plot
from .theme import unit_stacked_bar_theme


class TFTDataAnalyser:
    def __init__(self, DataBuilder, region='na'):
        self.DataBuilder = DataBuilder

    def champion_count_tier(self, champion_count_tier_df):
        """
        Build units_count_tier_plot for winner and loser group
            tabs: 6 tabs, cost of champion
            x_axis: champion name
            y_axis: champion usage count in stack of tier
            scatter: average tier of champion
        """
        output_file(f"experiments/plot/unit_plot/units_count_tier_plot.html")

        champion_count_tier_df  = champion_count_tier_df.sort_values(by=['count'])

        # Plot with all units
        panels = []
        fig, background_image = champion_count_tier.build_plot(champion_count_tier_df, theme=unit_stacked_bar_theme) 
        panels += [Panel(child=Row(fig, background_image), title='All Champions')]
        
        # Plot by cost of units
        units_df_by_cost = split_df_by_champion_cost(set_name='set3', df=champion_count_tier_df)
        for index, df_data in enumerate(units_df_by_cost.values()):
            cost_unit_df = pd.DataFrame(df_data, columns = champion_count_tier_df.columns)
            fig, background_image = champion_count_tier.build_plot(cost_unit_df, theme=unit_stacked_bar_theme) 
            panels += [Panel(child=Row(fig, background_image), title=f'{index+1} Cost Champions')]

        tabs = Tabs(tabs=panels)
        save(tabs)

    def champion_count_placement(self, champion_count_placement_df):
        output_file(f"experiments/plot/unit_plot/unit_count_placement_plot.html")
        # Sort dataframe by cost
        champion_count_placement_df = champion_count_placement_df.sort_values(by=['count'])

        # Plot with all units
        panels = []
        fig, background_image = champion_count_placement.build_plot(champion_count_placement_df, theme=unit_stacked_bar_theme) 
        panels += [Panel(child=Row(fig, background_image), title='All Champions')]
        
        # Plot by cost of units
        units_df_by_cost = split_df_by_champion_cost(set_name='set3', df=champion_count_placement_df)
        for index, df_data in enumerate(units_df_by_cost.values()):
            cost_unit_df = pd.DataFrame(df_data, columns = champion_count_placement_df.columns)
            fig, background_image = champion_count_placement.build_plot(cost_unit_df, theme=unit_stacked_bar_theme) 
            panels += [Panel(child=Row(fig, background_image), title=f'{index+1} Cost Champions')]

        tabs = Tabs(tabs=panels)
        save(tabs) 


    def champion_item_placement(self, champion_item_placement_df):
        champion_item_placement.build_plot(champion_item_placement_df)
        
    def items_plot(self, items_df):
        """
        Build items_plot
            x_axis: item name
            y_axis: item usage count
            vbar_color : average placement map
        """
        output_file(f"experiments/plot/item_plot/item_count_placement_plot.html")

        fig, background_image = build_item_count_placement_plot(items_df)
        
        save(Row(fig, background_image))


    def units_item_placement(self):
        output_file(f'test_unit_item_placement.html')
        fig = build_units_item_placement_plot(self.DataBuilder.units_item_placement_df, title='Champion Item & Placement', theme=unit_stacked_bar_theme)
        save(fig)
