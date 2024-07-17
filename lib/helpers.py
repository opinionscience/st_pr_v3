import streamlit as st
from opsci_toolbox.helpers.dataviz import generate_random_hexadecimal_color, general_kwargs, wrap_text
import plotly.graph_objects as go
import pandas as pd
from plotly.subplots import make_subplots

# def fig_horizontal_bar_trend(df: pd.DataFrame, col_x: str, col_bar: str, col_trend: str, **kwargs) -> go.Figure:
#     """
#     Display a graph that combines bar and trend chart to compare 2 metrics.

#     Args:
#         df (pd.DataFrame): DataFrame containing all data.
#         col_x (str): Name of the column containing X values.
#         col_bar (str): Name of the column containing Y values. Data represented as bar diagram.
#         col_trend (str): Name of the column containing Z values. Data represented as trend line.
#         **kwargs: Additional keyword arguments to update default plotting parameters.

#     Returns:
#         go.Figure: Plotly figure object.
#     """
    
#     params = general_kwargs()
#     params.update(kwargs)


#     xaxis_title = params["xaxis_title"]
#     xaxis_range = params["xaxis_range"]
#     yaxis_title = params["yaxis_title"]
#     yaxis_range = params["yaxis_range"]
#     zaxis_title = params["zaxis_title"]
#     zaxis_range = params["xaxis_range"]
#     col_hover = params['col_hover']

#     fig = make_subplots(rows=1, cols=1, specs=[[{ "shared_xaxis": False}]])
#     # fig=go.Figure()
#     hovertemplate="<br><b>"+xaxis_title+"</b> :"+df[col_x].astype(str)+"<br><b>"+yaxis_title+"</b> - "+df[col_bar].astype(str)+"<br><b>"+zaxis_title+"</b> : "+df[col_trend].astype(str)+"<extra></extra>"

#     for c in col_hover:
#         hovertemplate+="<br><b>"+c+"</b> :"+df[c].apply(wrap_text).astype(str)

#     fig.add_trace(
#         go.Scatter(
#             y=df[col_x].apply(wrap_text), 
#             x=df[col_trend], 
#             name=params["zaxis_title"],
#             mode=params["mode"], 
           
#             line_color=params["marker_line_color"], 
#             line_width=params["marker_line_width"],
#             textfont=dict(size=params["font_size"]),
#             hovertemplate = hovertemplate,
#         ),
#         1, 1
#         # secondary_y=True,
#     )
#     # Add traces
#     fig.add_trace(
#         go.Bar(
#             y=df[col_x].apply(wrap_text), 
#             x = df[col_bar], 
#             orientation='h',
#             name = params["yaxis_title"], 
#             marker_color=params["marker_color"], 
#             opacity = params["marker_opacity"],
#             hovertemplate=hovertemplate
#         ),
#         1, 1
#         # secondary_y=False,

#     )

#     if yaxis_range is None:
#         try:
#             yaxis_range=[-0.5,df[col_bar].max()*1.01]
#         except Exception as e:
#             pass
#             print(e)
#             yaxis_range is None
#     if xaxis_range is None:
#         try:
#             xaxis_range = [df[col_x].min() - 0.1, df[col_x].max() + 0.1]
#         except Exception as e:
#             pass
#             print(e)
#             xaxis_range=None
#     if zaxis_range is None:
#         try:
#             zaxis_range = [-0.5,df[col_trend].max()*1.01]
#         except Exception as e:
#             pass
#             print(e)
#             zaxis_range=None

#     if yaxis_range == "auto":
#         yaxis_range = None
#     if xaxis_range == "auto":
#         xaxis_range = None
#     if zaxis_range == "auto":
#         zaxis_range = None


#     # secondary_axis_range=[-0.5,df[col_trend].max()*1.01]

#     fig.update_layout(
#         title_text=params["title_text"],  # graph title
#         width=params["width"],  # plot size
#         height=params["height"],  # plot size
#         showlegend = params["showlegend"],
#         template=params["template"],
#         plot_bgcolor=params["plot_bgcolor"],  # background color (plot)
#         paper_bgcolor=params["paper_bgcolor"],  # background color (around plot)
#         font_family=params["font_family"],  # font
#         font_size=params["font_size"],
#         xaxis_title=params["xaxis_title"],
#         xaxis_title_font_size=params["xaxis_title_font_size"],
#         xaxis_tickangle=params["xaxis_tickangle"],
#         xaxis_tickfont_size=params["xaxis_tickfont_size"],
#         xaxis_range=xaxis_range,
#         xaxis_showgrid=params["xaxis_showgrid"],
#         xaxis_showline=params["xaxis_showline"],
#         xaxis_zeroline=params["xaxis_zeroline"],
#         xaxis_gridwidth=params["xaxis_gridwidth"],
#         xaxis_gridcolor=params["xaxis_gridcolor"],
#         xaxis_linewidth=params["xaxis_linewidth"],
#         xaxis_linecolor=params["xaxis_linecolor"],
#         xaxis_mirror=params["xaxis_mirror"],
#         yaxis_title=params["yaxis_title"],
#         yaxis_title_font_size=params["yaxis_title_font_size"],
#         yaxis_tickangle=params["yaxis_tickangle"],
#         yaxis_tickfont_size=params["yaxis_tickfont_size"],
#         yaxis_range=yaxis_range,
#         yaxis_showgrid=params["yaxis_showgrid"],
#         yaxis_showline=params["yaxis_showline"],
#         yaxis_zeroline=params["yaxis_zeroline"],
#         yaxis_gridwidth=params["yaxis_gridwidth"],
#         yaxis_gridcolor=params["yaxis_gridcolor"],
#         yaxis_linewidth=params["yaxis_linewidth"],
#         yaxis_linecolor=params["yaxis_linecolor"],
#         yaxis_mirror=params["yaxis_mirror"],
#     )

#     # # Set y-axes titles
#     # fig.update_yaxes(title_text=yaxis_title, range = yaxis_range, secondary_y=False)
#     # fig.update_yaxes(title_text=zaxis_title, range = zaxis_range, secondary_y=True)  
#     # fig.update_xaxes(layer="below traces")  # Ensure x-axis grid is below the data
#     # fig.update_yaxes(layer="below traces")  # Ensure y-axis grid is below the data
    
#     return fig
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

def fig_horizontal_bar_trend(df: pd.DataFrame, col_x: str, col_bar: str, col_trend: str, **kwargs) -> go.Figure:
    """
    Display a graph that combines bar and trend chart to compare 2 metrics.

    Args:
        df (pd.DataFrame): DataFrame containing all data.
        col_x (str): Name of the column containing X values.
        col_bar (str): Name of the column containing Y values. Data represented as bar diagram.
        col_trend (str): Name of the column containing Z values. Data represented as trend line.
        **kwargs: Additional keyword arguments to update default plotting parameters.

    Returns:
        go.Figure: Plotly figure object.
    """
    
    params = general_kwargs()
    params.update(kwargs)

    xaxis_title = params["xaxis_title"]
    xaxis_range = params["xaxis_range"]
    yaxis_title = params["yaxis_title"]
    yaxis_range = params["yaxis_range"]
    zaxis_title = params["zaxis_title"]
    zaxis_range = params["zaxis_range"]
    col_hover = params['col_hover']

    fig = make_subplots(rows=1, cols=1, specs=[[{"secondary_y": True}]])
    
    hovertemplate = ("<br><b>" + xaxis_title + "</b>: " + df[col_x].astype(str) + 
                     "<br><b>" + yaxis_title + "</b>: " + df[col_bar].astype(str) + 
                     "<br><b>" + zaxis_title + "</b>: " + df[col_trend].astype(str) + "<extra></extra>")

    for c in col_hover:
        hovertemplate += "<br><b>" + c + "</b>: " + df[c].apply(wrap_text).astype(str)

    fig.add_trace(
        go.Scatter(
            x=df[col_trend], 
            y=df[col_x].apply(wrap_text), 
            name=params["zaxis_title"],
            mode=params["mode"], 
            line_color=params["marker_line_color"], 
            line_width=params["marker_line_width"],
            textfont=dict(size=params["font_size"]),
            hovertemplate=hovertemplate,
        ),
        secondary_y=True,
    )
    
    fig.add_trace(
        go.Bar(
            x=df[col_bar], 
            y=df[col_x].apply(wrap_text), 
            orientation='h',
            name=params["yaxis_title"], 
            marker_color=params["marker_color"], 
            opacity=params["marker_opacity"],
            hovertemplate=hovertemplate
        ),
        secondary_y=False,
    )

    if yaxis_range is None:
        try:
            yaxis_range = [-0.5, df[col_x].max() + 0.1]
        except Exception as e:
            print(e)
            yaxis_range = None

    if xaxis_range is None:
        try:
            xaxis_range = [df[col_bar].min() - 0.1, df[col_bar].max() + 0.1]
        except Exception as e:
            print(e)
            xaxis_range = None

    if zaxis_range is None:
        try:
            zaxis_range = [-0.5, df[col_trend].max() * 1.01]
        except Exception as e:
            print(e)
            zaxis_range = None

    fig.update_layout(
        title_text=params["title_text"],  # graph title
        width=params["width"],  # plot size
        height=params["height"],  # plot size
        showlegend=params["showlegend"],
        template=params["template"],
        plot_bgcolor=params["plot_bgcolor"],  # background color (plot)
        paper_bgcolor=params["paper_bgcolor"],  # background color (around plot)
        font_family=params["font_family"],  # font
        font_size=params["font_size"],
        xaxis=dict(
            title=params["xaxis_title"],
            title_font_size=params["xaxis_title_font_size"],
            tickangle=params["xaxis_tickangle"],
            tickfont_size=params["xaxis_tickfont_size"],
            range=xaxis_range,
            showgrid=params["xaxis_showgrid"],
            showline=params["xaxis_showline"],
            zeroline=params["xaxis_zeroline"],
            gridwidth=params["xaxis_gridwidth"],
            gridcolor=params["xaxis_gridcolor"],
            linewidth=params["xaxis_linewidth"],
            linecolor=params["xaxis_linecolor"],
            mirror=params["xaxis_mirror"],
        ),
        yaxis=dict(
            title=params["yaxis_title"],
            title_font_size=params["yaxis_title_font_size"],
            tickangle=params["yaxis_tickangle"],
            tickfont_size=params["yaxis_tickfont_size"],
            range=yaxis_range,
            showgrid=params["yaxis_showgrid"],
            showline=params["yaxis_showline"],
            zeroline=params["yaxis_zeroline"],
            gridwidth=params["yaxis_gridwidth"],
            gridcolor=params["yaxis_gridcolor"],
            linewidth=params["yaxis_linewidth"],
            linecolor=params["yaxis_linecolor"],
            mirror=params["yaxis_mirror"],
        ),
        xaxis2=dict(
            title=params["zaxis_title"],
            title_font_size=params["xaxis_title_font_size"],
            tickangle=params["xaxis_tickangle"],
            tickfont_size=params["xaxis_tickfont_size"],
            range=zaxis_range,
            showgrid=params["xaxis_showgrid"],
            showline=params["xaxis_showline"],
            zeroline=params["xaxis_zeroline"],
            gridwidth=params["xaxis_gridwidth"],
            gridcolor=params["xaxis_gridcolor"],
            linewidth=params["xaxis_linewidth"],
            linecolor=params["xaxis_linecolor"],
            mirror=params["xaxis_mirror"],
            overlaying='x',
            side='top',
        ),
    )
    
    return fig


def format_number(number: float, digits=1) -> str:
    """
    Format a number into a human-readable string with K, M, or B suffixes.

    Args:
        number (float): The number to format.

    Returns:
        str: The formatted number as a string with an appropriate suffix.
    """

    if number < 1000:
        return str(number)
    elif number < 1000000:
        return f"{number / 1000:.{digits}f}K"
    elif number < 1000000000:
        return f"{number / 1000000:.{digits}f}M"
    else:
        return f"{number / 1000000000:.{digits}f}B"
    
def update_session_state(states : dict):
    for key, value in states.items():
        st.session_state[key] = value


def line_per_cat(df, col_x, col_y, col_cat, color_palette, **kwargs):
    params = general_kwargs()
    params.update(kwargs)
    col_hover = params["col_hover"]
    fig = go.Figure()
    for cat in df[col_cat].unique():
        df_cat = df[df[col_cat]==cat]
        if color_palette:
            marker_line_color = color_palette.get(cat, generate_random_hexadecimal_color())
        else :
            marker_line_color = generate_random_hexadecimal_color()
        hovertemplate = '<b>'+col_cat+'</b> : '+cat+'<br><b>'+col_x+'</b> : '+df_cat[col_x].astype(str)+'<br><b>'+col_y+'</b> : '+df_cat[col_y].astype(str)
        for c in col_hover:
            hovertemplate += '<br><b>'+c+'</b> : '+df_cat[c].astype(str)

        fig.add_trace(
            go.Line(
                x=df_cat[col_x], 
                y=df_cat[col_y], 
                line_color=marker_line_color, 
                name=cat,
                hovertemplate = hovertemplate+'<extra></extra>',                    
                )
                )
    fig.update_layout(
        title_text=params['title_text'],
        barmode='overlay',
        bargap=params["bargap"],
        width=params["width"],
        height=params["height"],
        font_family=params["font_family"],
        font_size=params["font_size"],
        template=params["template"],
        plot_bgcolor=params["plot_bgcolor"],  # background color (plot)
        paper_bgcolor=params["paper_bgcolor"],  # background color (around plot)
        showlegend=params["showlegend"],
        uniformtext_minsize=params["uniformtext_minsize"],
        uniformtext_mode=params["uniformtext_mode"],
    )
    fig.update_yaxes(
        title=params["yaxis_title"],
        title_font_size=params["yaxis_title_font_size"],
        tickangle=params["yaxis_tickangle"],
        tickfont_size=params["yaxis_tickfont_size"],
        range=params["yaxis_range"],
        showgrid=params["yaxis_showgrid"],
        showline=params["yaxis_showline"],
        zeroline=params["yaxis_zeroline"],
        gridwidth=params["yaxis_gridwidth"],
        gridcolor=params["yaxis_gridcolor"],
        linewidth=params["yaxis_linewidth"],
        linecolor=params["yaxis_linecolor"],
        mirror=params["yaxis_mirror"],
    )

    fig.update_xaxes(
        title=params["xaxis_title"],
        title_font_size=params["xaxis_title_font_size"],
        tickangle=params["xaxis_tickangle"],
        tickfont_size=params["xaxis_tickfont_size"],
        range=params["xaxis_range"],
        showgrid=params["xaxis_showgrid"],
        showline=params["xaxis_showline"],
        zeroline=params["xaxis_zeroline"],
        gridwidth=params["xaxis_gridwidth"],
        gridcolor=params["xaxis_gridcolor"],
        linewidth=params["xaxis_linewidth"],
        linecolor=params["xaxis_linecolor"],
        mirror=params["xaxis_mirror"],
    )
    return fig