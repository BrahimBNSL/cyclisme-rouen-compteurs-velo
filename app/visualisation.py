import pandas as pd
from dash import html, dcc, Input, Output
import plotly.graph_objects as go


from pathlib import Path

DATA_PATH = Path(__file__).resolve().parent.parent / "data" / "data-set-clean.csv"
df = pd.read_csv(DATA_PATH)
df["jour"] = pd.to_datetime(df["jour"])

dates_uniques = sorted(df["jour"].dt.date.unique())
n_dates = len(dates_uniques)
date_min = dates_uniques[0]
date_max = dates_uniques[-1]


def visu_layout():
    return html.Div([

        # Card sélecteur de dates
        html.Div([
            html.Div([
                html.Span("Période d'analyse", className="card-title"),
            ], className="card-header"),
            html.Div([

                # Raccourcis
                html.Div([
                    html.Button([
                        html.Span("7J", style={"fontSize": "16px", "fontWeight": "800", "display": "block"}),
                        html.Span("Cette semaine", style={"fontSize": "9px", "opacity": "0.8", "display": "block", "marginTop": "2px"}),
                    ], id="btn-semaine", n_clicks=0, className="raccourci-btn"),
                    html.Button([
                        html.Span("1M", style={"fontSize": "16px", "fontWeight": "800", "display": "block"}),
                        html.Span("Ce mois", style={"fontSize": "9px", "opacity": "0.8", "display": "block", "marginTop": "2px"}),
                    ], id="btn-mois", n_clicks=0, className="raccourci-btn"),
                    html.Button([
                        html.Span("1A", style={"fontSize": "16px", "fontWeight": "800", "display": "block"}),
                        html.Span("Cette année", style={"fontSize": "9px", "opacity": "0.8", "display": "block", "marginTop": "2px"}),
                    ], id="btn-annee", n_clicks=0, className="raccourci-btn"),
                    html.Button([
                        html.Span("∞", style={"fontSize": "20px", "fontWeight": "800", "display": "block"}),
                        html.Span("Tout", style={"fontSize": "9px", "opacity": "0.8", "display": "block", "marginTop": "2px"}),
                    ], id="btn-tout", n_clicks=0, className="raccourci-btn"),
                ], style={"display": "flex", "gap": "10px", "marginBottom": "24px"}),

                # Date inputs
                html.Div([
                    html.Div([
                        html.Div([
                            html.Span("🗓", style={"fontSize": "18px"}),
                            html.Div([
                                html.Span("DATE DE DÉBUT", style={
                                    "fontSize": "9px", "fontWeight": "800", "color": "#7c3aed",
                                    "letterSpacing": "0.12em", "display": "block", "marginBottom": "4px"
                                }),
                                dcc.DatePickerSingle(
                                    id="date-input-start",
                                    min_date_allowed=date_min,
                                    max_date_allowed=date_max,
                                    date=date_min,
                                    display_format="DD MMM YYYY",
                                    className="date-picker-custom"
                                ),
                            ]),
                        ], style={"display": "flex", "alignItems": "center", "gap": "12px"}),
                    ], className="date-field"),

                    html.Div([
                        html.Div(style={"width": "2px", "height": "30px", "background": "linear-gradient(180deg, #7c3aed, #a855f7)", "borderRadius": "2px", "margin": "0 auto"}),
                        html.Div("⇅", style={"color": "#a855f7", "fontSize": "16px", "textAlign": "center", "lineHeight": "1"}),
                        html.Div(style={"width": "2px", "height": "30px", "background": "linear-gradient(180deg, #a855f7, #c084fc)", "borderRadius": "2px", "margin": "0 auto"}),
                    ], style={"display": "flex", "flexDirection": "column", "alignItems": "center", "padding": "4px 16px"}),

                    html.Div([
                        html.Div([
                            html.Span("🗓", style={"fontSize": "18px"}),
                            html.Div([
                                html.Span("DATE DE FIN", style={
                                    "fontSize": "9px", "fontWeight": "800", "color": "#a855f7",
                                    "letterSpacing": "0.12em", "display": "block", "marginBottom": "4px"
                                }),
                                dcc.DatePickerSingle(
                                    id="date-input-end",
                                    min_date_allowed=date_min,
                                    max_date_allowed=date_max,
                                    date=date_max,
                                    display_format="DD MMM YYYY",
                                    className="date-picker-custom"
                                ),
                            ]),
                        ], style={"display": "flex", "alignItems": "center", "gap": "12px"}),
                    ], className="date-field"),

                ], style={
                    "display": "flex", "flexDirection": "column", "gap": "0",
                    "background": "linear-gradient(135deg, #faf5ff, #f3e8ff)",
                    "borderRadius": "16px", "padding": "20px 24px",
                    "border": "1px solid #e9d5ff", "marginBottom": "16px",
                }),

                # Résumé
                html.Div([
                    html.Span("📊 ", style={"fontSize": "13px"}),
                    html.Span("Période : ", style={"fontSize": "12px", "color": "#8892a4", "fontWeight": "500"}),
                    html.Span(id="label-date-start", style={"fontSize": "12px", "fontWeight": "700", "color": "#7c3aed"}),
                    html.Span(" → ", style={"color": "#8892a4", "fontSize": "12px"}),
                    html.Span(id="label-date-end", style={"fontSize": "12px", "fontWeight": "700", "color": "#a855f7"}),
                    html.Span(id="label-nb-jours", style={"fontSize": "11px", "color": "#b0b8c8", "marginLeft": "8px"}),
                ], style={
                    "padding": "10px 16px", "background": "white",
                    "borderRadius": "10px", "border": "1px solid #f0f2f7",
                    "display": "flex", "alignItems": "center", "gap": "4px", "flexWrap": "wrap"
                }),

            ], className="card-body", style={"paddingBottom": "24px"}),
        ], className="card"),

        # Card top 5 stations
        html.Div([
            html.Div([
                html.Span("Top 5 des stations", style={
                    "fontSize": "13px", "fontWeight": "700", "color": "#1a2035",
                    "textTransform": "uppercase", "letterSpacing": "0.1em"
                }),
            ], className="card-header"),
            html.Div([
                html.Div(id="photos-top5", style={
                    "display": "flex", "gap": "12px",
                    "overflowX": "auto", "paddingBottom": "8px",
                }),
            ], className="card-body"),
        ], className="card"),

        # Card histogramme tous capteurs
        html.Div([
            html.Div([
                html.Span("Tous les capteurs", className="card-title"),
                html.Span("Moyenne de passages par jour", style={"fontSize": "11px", "color": "#8892a4"})
            ], className="card-header"),
            html.Div([
                dcc.Graph(id="graph-all", config={"displayModeBar": False}, style={"height": "400px"})
            ], className="card-body"),
        ], className="card"),

        # Card top 10 journées
        html.Div([
            html.Div([
                html.Span("Top 10 des journées", style={
                    "fontSize": "13px", "fontWeight": "700", "color": "#1a2035",
                    "textTransform": "uppercase", "letterSpacing": "0.1em"
                }),
                html.Span("Total de passages sur une journée", style={
                    "fontSize": "11px", "color": "#8892a4"
                })
            ], className="card-header"),
            html.Div([
                dcc.Graph(id="graph-top10-jours", config={"displayModeBar": False}, style={"height": "400px"})
            ], className="card-body"),
        ], className="card"),

    ], style={"display": "flex", "flexDirection": "column", "gap": "14px"})


def register_visu_callbacks(app):

    # ── Raccourcis → date inputs ───────────────────────────
    @app.callback(
        Output("date-input-start", "date"),
        Output("date-input-end", "date"),
        Input("btn-semaine", "n_clicks"),
        Input("btn-mois", "n_clicks"),
        Input("btn-annee", "n_clicks"),
        Input("btn-tout", "n_clicks"),
        prevent_initial_call=True
    )
    def raccourcis(s, m, a, t):
        from dash import callback_context
        triggered = callback_context.triggered[0]["prop_id"]
        if "btn-semaine" in triggered:
            start = date_max - pd.Timedelta(days=date_max.weekday())
            end   = date_max
        elif "btn-mois" in triggered:
            start = date_max.replace(day=1)
            end   = date_max
        elif "btn-annee" in triggered:
            start = date_max.replace(month=1, day=1)
            end   = date_max
        else:
            start = date_min
            end   = date_max
        return start, end

    # ── Update top 5 ────────────────────────────────────────
    @app.callback(
        Output("photos-top5", "children"),
        Output("label-date-start", "children"),
        Output("label-date-end", "children"),
        Output("label-nb-jours", "children"),
        Input("date-input-start", "date"),
        Input("date-input-end", "date"),
    )
    def update_top5(d_start, d_end):
        if not d_start or not d_end:
            return [], "", "", ""
        d_start = pd.to_datetime(d_start).date()
        d_end   = pd.to_datetime(d_end).date()
        if d_start > d_end:
            d_start, d_end = d_end, d_start
        mask = (df["jour"].dt.date >= d_start) & (df["jour"].dt.date <= d_end)
        df_filtre = df[mask]
        label_start = d_start.strftime("%d %b %Y")
        label_end   = d_end.strftime("%d %b %Y")
        n_jours     = (d_end - d_start).days + 1
        label_jours = f"({n_jours} jour{'s' if n_jours > 1 else ''})"
        if df_filtre.empty:
            return [], label_start, label_end, label_jours
        top5 = (
            df_filtre.groupby(["Nom", "Photo"])["Counts"]
            .sum()
            .div(n_jours)
            .round(1)
            .nlargest(5)
            .reset_index()
        )
        top5.columns = ["Nom", "Photo", "Moyenne"]
        couleurs = ["#7c3aed", "#a855f7", "#c084fc", "#d8b4fe", "#ede9fe"]
        photos = []
        for i, row in top5.iterrows():
            photo_src = row["Photo"] if row["Photo"] and row["Photo"] != "nan" else ""
            rang = i
            carte = html.Div([
                html.Div([
                    html.Div(str(rang + 1), style={
                        "position": "absolute", "top": "10px", "left": "10px",
                        "width": "24px", "height": "24px",
                        "background": "white", "borderRadius": "50%",
                        "display": "flex", "alignItems": "center", "justifyContent": "center",
                        "fontSize": "11px", "fontWeight": "700", "color": "#1a2035",
                        "boxShadow": "0 2px 6px rgba(0,0,0,0.2)", "zIndex": "2"
                    }),
                    html.Img(src=photo_src, style={
                        "width": "100%", "height": "220px", "objectFit": "cover", "display": "block",
                    }) if photo_src else html.Div("📷", style={
                        "width": "100%", "height": "220px", "background": "#f3e8ff",
                        "display": "flex", "alignItems": "center", "justifyContent": "center", "fontSize": "40px"
                    }),
                ], style={"position": "relative", "borderRadius": "12px 12px 0 0", "overflow": "hidden"}),
                html.Div([
                    html.Div(row["Nom"], style={
                        "fontSize": "12px", "fontWeight": "700", "color": "#1a2035",
                        "marginBottom": "6px", "lineHeight": "1.3"
                    }),
                    html.Div([
                        html.Span(f"{row['Moyenne']:.0f}", style={
                            "fontSize": "22px", "fontWeight": "700", "color": couleurs[rang]
                        }),
                        html.Span(" vélos en moyenne par jour", style={
                            "fontSize": "10px", "color": "#8892a4", "marginLeft": "4px"
                        }),
                    ]),
                    html.Div(f"du {label_start} au {label_end}",
                             style={"fontSize": "10px", "color": "#b0b8c8", "marginTop": "6px"}),
                ], style={"padding": "12px 14px", "borderTop": f"3px solid {couleurs[rang]}"}),
            ], style={
                "minWidth": "220px", "flex": "1", "background": "white",
                "borderRadius": "14px", "border": "1px solid #e8eaf0",
                "boxShadow": "0 4px 16px rgba(0,0,0,0.07)", "overflow": "hidden",
            })
            photos.append(carte)
        return photos, label_start, label_end, label_jours

    # ── Update histogramme tous capteurs ────────────────────
    @app.callback(
        Output("graph-all", "figure"),
        Input("date-input-start", "date"),
        Input("date-input-end", "date"),
    )
    def update_all(d_start, d_end):
        if not d_start or not d_end:
            return go.Figure()
        d_start = pd.to_datetime(d_start).date()
        d_end   = pd.to_datetime(d_end).date()
        if d_start > d_end:
            d_start, d_end = d_end, d_start
        mask = (df["jour"].dt.date >= d_start) & (df["jour"].dt.date <= d_end)
        df_filtre = df[mask]
        if df_filtre.empty:
            return go.Figure()
        n_jours = (d_end - d_start).days + 1
        tous = (
            df_filtre.groupby("Nom")["Counts"]
            .sum()
            .div(n_jours)
            .round(1)
            .sort_values(ascending=False)
            .reset_index()
        )
        tous.columns = ["Nom", "Moyenne"]
        tous["Nom_court"] = tous["Nom"].apply(lambda x: x[:22] + "..." if len(x) > 22 else x)
        couleurs_bar = ["#7c3aed" if i < 5 else "#e2e8f0" for i in range(len(tous))]
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=tous["Nom_court"], y=tous["Moyenne"],
            marker=dict(color=couleurs_bar, line=dict(width=0)),
            text=[f"{v:.0f}" for v in tous["Moyenne"]],
            textposition="outside",
            textfont=dict(size=9, color="#8892a4", family="Outfit, sans-serif"),
            hovertemplate="<b>%{x}</b><br>%{y:.0f} vélos/jour<extra></extra>",
        ))
        fig.update_layout(
            margin=dict(l=10, r=10, t=20, b=100),
            paper_bgcolor="white", plot_bgcolor="white",
            xaxis=dict(showgrid=False, showline=False,
                       tickfont=dict(size=9, color="#8892a4", family="Outfit, sans-serif"), tickangle=-40),
            yaxis=dict(showgrid=True, gridcolor="#f0f2f7", showline=False, zeroline=False,
                       tickfont=dict(size=10, color="#8892a4"),
                       title=dict(text="vélos/jour", font=dict(size=10, color="#8892a4"))),
            font=dict(family="Outfit, sans-serif"),
            hoverlabel=dict(bgcolor="white", bordercolor="#e8eaf0",
                            font=dict(size=12, family="Outfit, sans-serif")),
        )
        return fig

    # ── Update top 10 journées ──────────────────────────────
    @app.callback(
        Output("graph-top10-jours", "figure"),
        Input("date-input-start", "date"),
        Input("date-input-end", "date"),
    )
    def update_top10_jours(d_start, d_end):
        if not d_start or not d_end:
            return go.Figure()
        d_start = pd.to_datetime(d_start).date()
        d_end   = pd.to_datetime(d_end).date()
        if d_start > d_end:
            d_start, d_end = d_end, d_start
        mask = (df["jour"].dt.date >= d_start) & (df["jour"].dt.date <= d_end)
        df_filtre = df[mask]
        if df_filtre.empty:
            return go.Figure()
        top10 = (
            df_filtre.groupby("jour")["Counts"]
            .sum()
            .nlargest(10)
            .sort_values(ascending=True)
            .reset_index()
        )
        top10.columns = ["Jour", "Total"]
        top10["Jour_str"] = top10["Jour"].dt.strftime("%d %b %Y")
        couleurs_bar = [
            "#ede9fe", "#e5d0fe", "#d8b4fe", "#c984fa",
            "#c07bf9", "#b366f8", "#a855f7", "#9b52f0",
            "#8b46f0", "#7c3aed"
        ]
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=top10["Total"],
            y=top10["Jour_str"],
            orientation="h",
            marker=dict(color=couleurs_bar[:len(top10)], line=dict(width=0)),
            text=[f"{v:,.0f} passages" for v in top10["Total"]],
            textposition="outside",
            textfont=dict(size=11, color="#1a2035", family="Outfit, sans-serif"),
            hovertemplate="<b>%{y}</b><br>%{x:,.0f} passages<extra></extra>",
        ))
        fig.update_layout(
            margin=dict(l=10, r=120, t=10, b=10),
            paper_bgcolor="white", plot_bgcolor="white",
            xaxis=dict(
                showgrid=True, gridcolor="#f0f2f7",
                showline=False, zeroline=False,
                tickfont=dict(size=10, color="#8892a4"),
            ),
            yaxis=dict(
                showgrid=False, showline=False,
                tickfont=dict(size=11, color="#1a2035", family="Outfit, sans-serif"),
            ),
            font=dict(family="Outfit, sans-serif"),
            hoverlabel=dict(bgcolor="white", bordercolor="#e8eaf0",
                            font=dict(size=12, family="Outfit, sans-serif")),
        )
        return fig