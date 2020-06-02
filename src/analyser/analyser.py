from .units_plot import build_basic_units_plot, build_win_lose_units_plot
from .helper import split_units_df_by_cost
import pandas as pd
from bokeh.io import save, output_file
from bokeh.models.widgets import Panel, Tabs
from bokeh.layouts import gridplot
from bokeh.models import Row

class TFTDataAnalyser:
    def __init__(self, db, region='na'):
        self.db = db

    def basic_units_plot(self, units_df):
        output_file(f"experiments/plot/unit_plot/units_plot.html")

        # Plot with all units
        panels = []
        fig, background_image = build_basic_units_plot(units_df) 
        panels += [Panel(child=Row(fig, background_image), title='All Champions')]
        
        # Plot by cost of units
        units_df_by_cost = split_units_df_by_cost(set_name='set3', units_df=units_df)
        for key, df_data in units_df_by_cost.items():
            cost_unit_df = pd.DataFrame(df_data, columns = units_df.columns)
            fig, background_image = build_basic_units_plot(cost_unit_df) 
            panels += [Panel(child=Row(fig, background_image), title=key)]

        tabs = Tabs(tabs=panels)
        save(tabs)

    
    def win_lose_units_plot(self, win_units_df, lose_units_df):
        output_file(f"experiments/plot/unit_plot/win_lose_units_plot.html")
        # Plot with all units
        win_fig, lose_fig, background_image = build_win_lose_units_plot(win_units_df, lose_units_df)
        

        # Winner plot  by cost of units
        win_panels = []
        win_panels += [Panel(child=Row(win_fig, background_image), title='All Champions')]
        win_units_df_by_cost = split_units_df_by_cost(set_name='set3', units_df=win_units_df)
        
        for key, df_data in win_units_df_by_cost.items():
            cost_unit_df = pd.DataFrame(df_data, columns = win_units_df.columns)
            fig, background_image = build_basic_units_plot(cost_unit_df) 
            win_panels += [Panel(child=Row(fig, background_image), title=key)]
        
        win_tabs = Tabs(tabs=win_panels)

        # Loser plot  by cost of units
        lose_panels = []
        lose_panels += [Panel(child=Row(lose_fig, background_image), title='All Champions')]
        lose_units_df_by_cost = split_units_df_by_cost(set_name='set3', units_df=lose_units_df)
        
        for key, df_data in lose_units_df_by_cost.items():
            cost_unit_df = pd.DataFrame(df_data, columns = lose_units_df.columns)
            fig, background_image = build_basic_units_plot(cost_unit_df) 
            lose_panels += [Panel(child=Row(fig, background_image), title=key)]
        
        los_tabs = Tabs(tabs=lose_panels)
        
        res = gridplot([[win_tabs, los_tabs]])
        save(res)


        



        save(res)

