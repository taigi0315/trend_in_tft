from .units import build_default_units_plot, build_win_lose_units_plot
from .items import build_default_items_plot
from .helper import split_units_df_by_cost
import pandas as pd
from bokeh.io import save, output_file
from bokeh.models.widgets import Panel, Tabs
from bokeh.layouts import gridplot
from bokeh.models import Row
from .theme import units_fig_theme, win_lose_units_fig_theme

class TFTDataAnalyser:
    def __init__(self, db, region='na'):
        self.db = db

    def default_units_plot(self, units_df):
        output_file(f"experiments/plot/unit_plot/units_plot.html")

        # Plot with all units
        panels = []
        fig, background_image = build_default_units_plot(units_df) 
        panels += [Panel(child=Row(fig, background_image), title='All Champions')]
        
        # Plot by cost of units
        units_df_by_cost = split_units_df_by_cost(set_name='set3', units_df=units_df)
        for index, df_data in enumerate(units_df_by_cost.values()):
            cost_unit_df = pd.DataFrame(df_data, columns = units_df.columns)
            fig, background_image = build_default_units_plot(cost_unit_df, theme=units_fig_theme) 
            panels += [Panel(child=Row(fig, background_image), title=f'{index+1} Cost Champions')]

        tabs = Tabs(tabs=panels)
        save(tabs)

    
    def win_lose_units_plot(self, win_units_df, lose_units_df):
        output_file(f"experiments/plot/unit_plot/win_lose_units_plot.html")
        # Plot with all units
        win_fig, lose_fig, background_image = build_win_lose_units_plot(win_units_df, lose_units_df)
        

        # Winner plot  by cost of units
        win_plots = []
        win_plots += [Row(win_fig, background_image)]
        win_units_df_by_cost = split_units_df_by_cost(set_name='set3', units_df=win_units_df)
        
        for df_data in win_units_df_by_cost.values():
            cost_unit_df = pd.DataFrame(df_data, columns = win_units_df.columns)
            fig, background_image = build_default_units_plot(cost_unit_df, theme=win_lose_units_fig_theme) 
            win_plots += [Row(fig, background_image)]

        # Loser plot  by cost of units
        lose_plots = []
        lose_plots += [Row(lose_fig, background_image)]
        lose_units_df_by_cost = split_units_df_by_cost(set_name='set3', units_df=lose_units_df)
        
        for df_data in lose_units_df_by_cost.values():
            cost_unit_df = pd.DataFrame(df_data, columns = lose_units_df.columns)
            fig, background_image = build_default_units_plot(cost_unit_df, theme=win_lose_units_fig_theme) 
            lose_plots += [Row(fig, background_image)]
        
        win_lose_tabs = []
        for index in range(len(win_plots)):
            if index == 0:
                tab_title = 'All Champions'
            else:
                tab_title = f'{index+1} Cost Champions'
            win_lose_tabs += [Panel(child=gridplot([[win_plots[index], lose_plots[index] ]]), title=tab_title)]
        
        res = Tabs(tabs=win_lose_tabs)
        save(res)

    def default_items_plot(self, items_df):
        output_file(f"experiments/plot/item_plot/items_plot.html")

        fig, background_image = build_default_items_plot(items_df)
        
        save(Row(fig, background_image))