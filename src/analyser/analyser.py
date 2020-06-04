import pandas as pd
from bokeh.io import output_file, save
from bokeh.layouts import gridplot
from bokeh.models import Row
from bokeh.models.widgets import Panel, Tabs

from .helper import split_units_df_by_cost
from .item_usage_plot import build_all_player_items_plot, build_winner_loser_item_usage_plot
from .theme import (all_unit_usage_plot_theme,
                    winner_loser_unit_usage_plot_theme)
from .unit_usage_plot import (build_all_player_unit_usage_plot,
                              build_winner_loser_unit_usage_plot)


class TFTDataAnalyser:
    def __init__(self, db, region='na'):
        self.db = db

    def units_plot(self, units_df):
        """
        Build units_plot for winner and loser group
            tabs: 6 tabs, cost of champion
            x_axis: champion name
            y_axis: champion usage count
            scatter: average tier of champion
            vbar_color : average placement map
        """
        output_file(f"experiments/plot/unit_plot/units_plot.html")

        # Plot with all units
        panels = []
        fig, background_image = build_all_player_unit_usage_plot(units_df, theme=all_unit_usage_plot_theme) 
        panels += [Panel(child=Row(fig, background_image), title='All Champions')]
        
        # Plot by cost of units
        units_df_by_cost = split_units_df_by_cost(set_name='set3', units_df=units_df)
        for index, df_data in enumerate(units_df_by_cost.values()):
            cost_unit_df = pd.DataFrame(df_data, columns = units_df.columns)
            fig, background_image = build_all_player_unit_usage_plot(cost_unit_df, theme=all_unit_usage_plot_theme) 
            panels += [Panel(child=Row(fig, background_image), title=f'{index+1} Cost Champions')]

        tabs = Tabs(tabs=panels)
        save(tabs)

    
    def winner_loser_units_plot(self, winner_units_df, loser_units_df):
        """
        Build units_plot for winner and loser group
            tabs: 6 tabs, cost of champion
            x_axis: champion name
            y_axis: champion usage count
            scatter: average tier of champion
            vbar_color : average placement map
        """
        output_file(f"experiments/plot/unit_plot/win_lose_units_plot.html")
        # Plot with all units
        win_fig, lose_fig, background_image = build_winner_loser_unit_usage_plot(winner_units_df, loser_units_df, theme=all_unit_usage_plot_theme)
        

        # Winner plot  by cost of units
        win_plots = []
        win_plots += [Row(win_fig, background_image)]
        win_units_df_by_cost = split_units_df_by_cost(set_name='set3', units_df=winner_units_df)
        
        for df_data in win_units_df_by_cost.values():
            cost_unit_df = pd.DataFrame(df_data, columns = winner_units_df.columns)
            fig, background_image = build_all_player_unit_usage_plot(cost_unit_df, theme=winner_loser_unit_usage_plot_theme) 
            win_plots += [Row(fig, background_image)]

        # Loser plot  by cost of units
        lose_plots = []
        lose_plots += [Row(lose_fig, background_image)]
        lose_units_df_by_cost = split_units_df_by_cost(set_name='set3', units_df=loser_units_df)
        
        for df_data in lose_units_df_by_cost.values():
            cost_unit_df = pd.DataFrame(df_data, columns = loser_units_df.columns)
            fig, background_image = build_all_player_unit_usage_plot(cost_unit_df, theme=winner_loser_unit_usage_plot_theme) 
            lose_plots += [Row(fig, background_image)]
        
        win_lose_tabs = []
        for index in range(len(win_plots)):
            if index == 0:
                tab_title = 'All Champions'
            else:
                tab_title = f'{index} Cost Champions'
            win_lose_tabs += [Panel(child=gridplot([[win_plots[index], lose_plots[index] ]]), title=tab_title)]

        res = Tabs(tabs=win_lose_tabs)
        save(res)


    def items_plot(self, items_df):
        """
        Build items_plot
            x_axis: item name
            y_axis: item usage count
            vbar_color : average placement map
        """
        output_file(f"experiments/plot/item_plot/items_plot.html")

        fig, background_image = build_all_player_items_plot(items_df)
        
        save(Row(fig, background_image))



    def winner_loser_items_plot(self, winner_items_df, loser_items_df):
        """
        Build items_plot for winner and loser group
            x_axis: item name
            y_axis: item usage count
            vbar_color : average placement map
        """
        output_file(f"experiments/plot/item_plot/winner_loser_items_plot.html")
        # Plot with all units
        winner_fig, loser_fig, background_image = build_winner_loser_item_usage_plot(winner_items_df, loser_items_df)
        winner_plot = Row(winner_fig, background_image)
        loser_plot = Row(loser_fig, background_image)
        
        res = gridplot([[winner_plot, loser_plot ]])
        save(res)

