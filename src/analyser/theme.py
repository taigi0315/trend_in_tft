from bokeh.themes.theme import Theme

unit_stacked_bar_color_palette = ["#F53315","#F86B32","#F4A564","#F0D5A8","#6EAA9F","#038996","#036C8E","#011E50"]
unit_tier_stacked_bar_color_palette = ["#036C8E","#F4A564","#F53315"]
unit_stacked_bar_theme = Theme(
    json={
        "attrs" : {
            "Figure" : {
                "background_fill_color": "#1C1A10",
                "background_fill_alpha": 0.85,
                "plot_height": 1000,
                "plot_width": 1610
            },
            "Axis": {
                "major_label_text_font_size": "10pt",
                "axis_label_text_font_size" : "30pt",
                "axis_label_text_font_style": 'bold',
                "axis_label_text_color": "#F8BE00",
                "axis_line_color": "#46433D",
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
