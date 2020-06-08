import pandas as pd
from bokeh.io import output_file, save
from bokeh.layouts import gridplot
from bokeh.models import Row
from bokeh.models.widgets import Panel, Tabs

from .helper import split_units_df_by_cost
from .item_count_placement_plot import build_item_count_placement_plot
from .theme import unit_stacked_bar_theme
from .unit_count_placement_plot import build_unit_count_placement_plot
from .unit_count_tier_plot import build_unit_count_tier_plot
from .unit_item_placement_plot import build_units_item_placement_plot

class TFTDataAnalyser:
    def __init__(self, db, DataBuilder, region='na', units_df=None):
        self.db = db
        self.units_df = units_df
        self.DataBuilder = DataBuilder

    def units_count_tier_plot(self):
        """
        Build units_count_tier_plot for winner and loser group
            tabs: 6 tabs, cost of champion
            x_axis: champion name
            y_axis: champion usage count in stack of tier
            scatter: average tier of champion
        """
        output_file(f"experiments/plot/unit_plot/units_count_tier_plot.html")

        # Plot with all units
        panels = []
        fig, background_image = build_unit_count_tier_plot(self.units_df, theme=unit_stacked_bar_theme) 
        panels += [Panel(child=Row(fig, background_image), title='All Champions')]
        
        # Plot by cost of units
        units_df_by_cost = split_units_df_by_cost(set_name='set3', units_df=self.units_df)
        for index, df_data in enumerate(units_df_by_cost.values()):
            cost_unit_df = pd.DataFrame(df_data, columns = self.units_df.columns)
            fig, background_image = build_unit_count_tier_plot(cost_unit_df, theme=unit_stacked_bar_theme) 
            panels += [Panel(child=Row(fig, background_image), title=f'{index+1} Cost Champions')]

        tabs = Tabs(tabs=panels)
        save(tabs)

    def units_count_placement_plot(self):
        output_file(f"experiments/plot/unit_plot/unit_count_placement_plot.html")
        
        # Plot with all units
        panels = []
        fig, background_image = build_unit_count_placement_plot(self.units_df, theme=unit_stacked_bar_theme) 
        panels += [Panel(child=Row(fig, background_image), title='All Champions')]
        
        # Plot by cost of units
        units_df_by_cost = split_units_df_by_cost(set_name='set3', units_df=self.units_df)
        for index, df_data in enumerate(units_df_by_cost.values()):
            cost_unit_df = pd.DataFrame(df_data, columns = self.units_df.columns)
            fig, background_image = build_unit_count_placement_plot(cost_unit_df, theme=unit_stacked_bar_theme) 
            panels += [Panel(child=Row(fig, background_image), title=f'{index+1} Cost Champions')]

        tabs = Tabs(tabs=panels)
        save(tabs) 

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
