from bokeh.themes.theme import Theme
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
        