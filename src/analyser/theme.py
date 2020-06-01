from bokeh.themes.theme import Theme
choi_theme = Theme(
    json={
        "attrs" : {
            "Figure" : {
                "background_fill_color": "#AEB6C1",
                "background_fill_alpha": 0.2,
                "plot_height": 750,
                "plot_width": 1230
            },
            "Axis": {
                "major_label_text_font_size": "8pt",
                "axis_label_text_font_size" : "20pt",
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
