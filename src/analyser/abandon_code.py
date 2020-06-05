# Temp Trash Can

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





all_unit_usage_plot_theme = Theme(
    json={
        "attrs" : {
            "Figure" : {
                "background_fill_color": "#AEB6C1",
                "background_fill_alpha": 0.2,
                "plot_height": 1000,
                "plot_width": 1610
            },
            "Axis": {
                "major_label_text_font_size": "10pt",
                "axis_label_text_font_size" : "30pt",
                "axis_label_text_color": "#EDBE74",
                "axis_line_color": "#3A3042",
                "axis_line_width": 3.3,
                "axis_line_alpha": 0.7
            },
            "Grid": {
            },
            "Title": {
                "text_color": "#feffe1",
                "text_font": "times",
                "text_font_style": "italic"
            }
        }
    }   
)

winner_loser_unit_usage_plot_theme = Theme(
    json={
        "attrs" : {
            "Figure" : {
                "background_fill_color": "#AEB6C1",
                "background_fill_alpha": 0.2,
                "plot_height": 600,
                "plot_width": 966
            },
            "Axis": {
                "major_label_text_font_size": "10pt",
                "axis_label_text_font_size" : "30pt",
                "axis_label_text_color": "#EDBE74",
                "axis_line_color": "#3A3042",
                "axis_line_width": 3.3,
                "axis_line_alpha": 0.7
            },
            "Grid": {
            },
            "Title": {
                "text_color": "#feffe1",
                "text_font": "times",
                "text_font_style": "italic"
            }
        }
    }   
)

bar_color_palette = ['#FE3D3D', "#F59537", "#FCD89F", "#998c8c", "#302E2E"]
