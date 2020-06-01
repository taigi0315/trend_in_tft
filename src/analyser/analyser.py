from .units_plot import build_units_plot
from .helper import split_units_df_by_cost
import pandas as pd
from bokeh.io import save, output_file
from bokeh.models.widgets import Panel, Tabs

class TFTDataAnalyser:
    def __init__(self, db, region='na'):
        self.db = db

    def plot_all_units(self, units_df):
        output_file(f"experiments/plot/unit_plot/units_plot.html")
        panels = []
        # Plot units_df
        panels += [Panel(child=build_units_plot(units_df), title='All Champions')]
        # Plot units_df by cost of units
        units_df_by_cost = split_units_df_by_cost(set_name='set3', units_df=units_df)
        for key, df_data in units_df_by_cost.items():
            cost_unit_df = pd.DataFrame(df_data, columns = units_df.columns)
            panels += [Panel(child=build_units_plot(cost_unit_df), title=key)]

        tabs = Tabs(tabs=panels)
        save(tabs)


