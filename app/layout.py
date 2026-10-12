from dash import html
from carte import carte_layout, points
from visualisation import visu_layout

index_string = '''
<!DOCTYPE html>
<html>
<head>
    {%metas%}
    <title>Vélos — Rouen</title>
    {%favicon%}
    {%css%}
    <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: 'Outfit', sans-serif; background: #f4f6fb; color: #1a2035; min-height: 100vh; }

        .app-header {
            background: #fff; border-bottom: 1px solid #e8eaf0;
            height: 60px; padding: 0 20px;
            display: flex; align-items: center; justify-content: space-between;
            position: sticky; top: 0; z-index: 200;
            box-shadow: 0 1px 6px rgba(0,0,0,0.05);
        }
        .header-left { display: flex; align-items: center; gap: 10px; }
        .header-icon {
            width: 34px; height: 34px;
            background: linear-gradient(135deg, #7c3aed, #a855f7);
            border-radius: 10px;
            display: flex; align-items: center; justify-content: center;
            font-size: 17px;
        }
        .header-title { font-size: 15px; font-weight: 700; color: #1a2035; letter-spacing: -0.02em; }
        .header-sub   { font-size: 11px; color: #8892a4; }
        .header-badge {
            background: #f3e8ff; color: #7c3aed;
            border: 1px solid #e9d5ff;
            padding: 4px 12px; border-radius: 20px;
            font-size: 12px; font-weight: 600;
        }
        .btn-toggle-sidebar {
            width: 36px; height: 36px;
            background: #f3e8ff; border: 1px solid #e9d5ff;
            border-radius: 10px; cursor: pointer;
            display: flex; align-items: center; justify-content: center;
            font-size: 16px; color: #7c3aed;
            transition: all 0.2s; margin-right: 8px;
        }
        .btn-toggle-sidebar:hover { background: #7c3aed; color: white; }

        .main-layout { display: flex; height: calc(100vh - 60px); overflow: hidden; }

        .sidebar {
            width: 700px; min-width: 700px;
            background: #fff;
            border-right: 1px solid #e8eaf0;
            display: flex; flex-direction: column;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            overflow: hidden;
            box-shadow: 2px 0 12px rgba(0,0,0,0.04);
            z-index: 10;
        }
        .sidebar.collapsed { width: 0; min-width: 0; border-right: none; box-shadow: none; }
        .sidebar-inner {
            width: 700px; padding: 16px;
            overflow-y: auto; flex: 1;
            display: flex; flex-direction: column; gap: 14px;
        }

        .card {
            background: #fff; border-radius: 14px;
            border: 1px solid #e8eaf0;
            box-shadow: 0 2px 8px rgba(0,0,0,0.04);
            overflow: visible;
        }
        .card-header {
            padding: 12px 16px; border-bottom: 1px solid #f0f2f7;
            display: flex; align-items: center; justify-content: space-between;
        }
        .card-title { font-size: 11px; font-weight: 700; color: #8892a4; text-transform: uppercase; letter-spacing: 0.08em; }
        .card-body { padding: 14px 16px; overflow: visible; }

        .Select-control { background: #f8f9fc !important; border: 1px solid #e8eaf0 !important; border-radius: 10px !important; box-shadow: none !important; }
        .Select-control:hover { border-color: #a855f7 !important; }
        .is-focused .Select-control { border-color: #7c3aed !important; box-shadow: 0 0 0 3px rgba(124,58,237,0.1) !important; }
        .Select-placeholder { color: #b0b8c8 !important; font-size: 13px !important; font-family: 'Outfit', sans-serif !important; }
        .Select-value-label { color: #1a2035 !important; font-size: 13px !important; font-family: 'Outfit', sans-serif !important; }
        .Select-menu-outer { background: #fff !important; border: 1px solid #e8eaf0 !important; border-radius: 12px !important; box-shadow: 0 8px 24px rgba(0,0,0,0.12) !important; margin-top: 4px !important; z-index: 9999 !important; position: absolute !important; }
        .Select-option { font-size: 13px !important; font-family: 'Outfit', sans-serif !important; color: #1a2035 !important; padding: 9px 13px !important; }
        .Select-option:hover, .Select-option.is-focused { background: #f3e8ff !important; color: #7c3aed !important; }
        .Select-option.is-selected { background: #7c3aed !important; color: white !important; }
        .Select-arrow { border-top-color: #8892a4 !important; }

        .btn-reset {
            width: 100%; margin-top: 10px; padding: 9px 14px;
            background: #f8f9fc; border: 1px solid #e8eaf0;
            border-radius: 10px; color: #8892a4;
            font-size: 12px; font-family: 'Outfit', sans-serif;
            cursor: pointer; transition: all 0.2s;
        }
        .btn-reset:hover { background: #f3e8ff; color: #7c3aed; border-color: #e9d5ff; }

        .mini-map-wrapper { border-radius: 0 0 14px 14px; overflow: hidden; height: 360px; }

        .photo-nom { font-size: 13px; font-weight: 600; color: #1a2035; margin-bottom: 10px; line-height: 1.3; }
        .stat-row { display: flex; gap: 6px; margin-top: 10px; }
        .stat-chip { flex: 1; background: #f8f9fc; border: 1px solid #f0f2f7; border-radius: 10px; padding: 7px; text-align: center; }
        .stat-value { font-size: 12px; font-weight: 700; color: #7c3aed; }
        .stat-label { font-size: 9px; color: #8892a4; text-transform: uppercase; letter-spacing: 0.06em; margin-top: 2px; }

        .right-zone { flex: 1; overflow-y: auto; padding: 20px; display: flex; flex-direction: column; gap: 16px; }

        /* ── Raccourcis ── */
        .raccourci-btn {
            flex: 1; padding: 14px 10px;
            border-radius: 14px; border: 1.5px solid #e9d5ff;
            background: white; color: #7c3aed;
            cursor: pointer; font-family: 'Outfit', sans-serif;
            text-align: center; transition: all 0.2s;
            box-shadow: 0 2px 8px rgba(124,58,237,0.08);
            min-width: 80px;
        }
        .raccourci-btn:hover {
            background: linear-gradient(135deg, #7c3aed, #a855f7);
            color: white; border-color: transparent;
            box-shadow: 0 4px 16px rgba(124,58,237,0.3);
            transform: translateY(-2px);
        }

        /* ── Date fields ── */
        .date-field {
            background: white; border-radius: 12px;
            padding: 14px 18px; border: 1.5px solid #e9d5ff;
            transition: all 0.2s;
        }
        .date-field:hover {
            border-color: #a855f7;
            box-shadow: 0 0 0 3px rgba(168,85,247,0.1);
        }

        /* ── DatePicker ── */
        .date-picker-custom .DateInput_input {
            font-family: 'Outfit', sans-serif !important;
            font-size: 15px !important; font-weight: 700 !important;
            color: #1a2035 !important; background: transparent !important;
            border: none !important; padding: 0 !important;
            cursor: pointer; width: 140px !important;
        }
        .date-picker-custom .DateInput { background: transparent !important; }
        .date-picker-custom .SingleDatePickerInput { background: transparent !important; border: none !important; }
        .DayPickerKeyboardShortcuts_show__bottomRight { display: none; }
        .CalendarDay__selected { background: #7c3aed !important; border-color: #7c3aed !important; }
        .CalendarDay__selected:hover { background: #6d28d9 !important; border-color: #6d28d9 !important; }
        .CalendarDay__hovered_span, .CalendarDay__selected_span { background: #f3e8ff !important; border-color: #e9d5ff !important; color: #7c3aed !important; }
        .DayPicker_weekHeader { color: #8892a4 !important; }
        .CalendarMonth_caption { color: #1a2035 !important; font-family: 'Outfit', sans-serif !important; }

        /* ── Leaflet ── */
        .leaflet-tooltip {
            font-family: 'Outfit', sans-serif !important; font-size: 12px !important;
            font-weight: 500 !important; border-radius: 8px !important;
            border: 1px solid #e8eaf0 !important;
            box-shadow: 0 4px 12px rgba(0,0,0,0.1) !important;
            padding: 5px 10px !important;
        }
    </style>
</head>
<body>
    {%app_entry%}
    <footer>
        {%config%}
        {%scripts%}
        {%renderer%}
    </footer>
</body>
</html>
'''


def create_layout():
    return html.Div([

        html.Div([
            html.Div([
                html.Button("☰", id="btn-toggle-sidebar", className="btn-toggle-sidebar", n_clicks=0),
                html.Div("🚲", className="header-icon"),
                html.Div([
                    html.Div("Capteurs Vélos", className="header-title"),
                    html.Div("Rouen Métropole", className="header-sub"),
                ])
            ], className="header-left"),
            html.Span(f"{len(points)} capteurs actifs", className="header-badge"),
        ], className="app-header"),

        html.Div([

            html.Div(
                id="sidebar",
                className="sidebar",
                children=[carte_layout()]
            ),

            html.Div([
                visu_layout()
            ], className="right-zone"),

        ], className="main-layout"),

    ])