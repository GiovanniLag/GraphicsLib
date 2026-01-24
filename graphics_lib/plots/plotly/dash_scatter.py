from __future__ import annotations

import socket
from collections.abc import Callable
from typing import TYPE_CHECKING, Any

import numpy as np

from graphics_lib.plots.plotly.scatter import ScatterPlot

if TYPE_CHECKING:
    from graphics_lib.colours import Palette
    from graphics_lib.typography import Typography


class DashScatterPlot(ScatterPlot):
    def __init__(
        self,
        x,
        y,
        detail_plot_data=None,
        detail_plot_type='line',
        detail_figsize=(500, 400),
        app_mode='auto',
        port=None,
        title='Interactive Scatter Plot',
        palette=None,
        typography=None,
        xlabel='X-axis',
        ylabel='Y-axis',
        figsize=(700, 600),
        labels=None,
        colors=None,
        sizes=None,
        marker='circle',
        opacity=0.7,
        gradient=False,
        show_legend=True,
        **kwargs
    ):
        self.detail_plot_data = detail_plot_data
        self.detail_plot_type = detail_plot_type
        self.detail_figsize = detail_figsize
        self.app_mode = app_mode
        self.port = port if port else self._find_free_port()
        self.app = None
        super().__init__(
            x=x, y=y, title=title, palette=palette, typography=typography,
            xlabel=xlabel, ylabel=ylabel, figsize=figsize, labels=labels,
            colors=colors, sizes=sizes, marker=marker, opacity=opacity,
            gradient=gradient, show_legend=show_legend, **kwargs
        )

    def _find_free_port(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(('', 0))
            s.listen(1)
            port = s.getsockname()[1]
        return port

    def _detect_jupyter(self):
        try:
            from IPython import get_ipython
            ipython = get_ipython()
            if ipython is not None:
                return 'IPKernelApp' in ipython.config
            return False
        except ImportError:
            return False

    def _get_plot_data_for_point(self, index):
        if self.detail_plot_data is None:
            return None
        if isinstance(self.detail_plot_data, list):
            if 0 <= index < len(self.detail_plot_data):
                return self.detail_plot_data[index]
            return None
        elif isinstance(self.detail_plot_data, dict):
            return self.detail_plot_data.get(index, None)
        elif callable(self.detail_plot_data):
            try:
                return self.detail_plot_data(index)
            except Exception:
                return None
        return None

    def _get_color(self, color_key='primary', fallback='#636EFA'):
        """Get color from palette or return fallback."""
        if self.palette is None:
            return fallback
        if color_key == 'primary':
            return str(self.palette.primary)
        return str(self.palette.colours.get(color_key, fallback))

    def _convert_to_plotly_figure(self, plot_data, index):
        """Convert various plot formats to Plotly figure.
        
        Parameters
        ----------
        plot_data : dict, plotly.graph_objects.Figure, matplotlib.figure.Figure,
                    or BasePlot
            The plot data or figure object.
        index : int
            The point index for default titles.
        
        Returns
        -------
        plotly.graph_objects.Figure
            A Plotly figure ready to display.
        """
        import plotly.graph_objects as go
        
        # Check if it's already a Plotly figure
        if isinstance(plot_data, go.Figure):
            return plot_data
        
        # Check if it's a BasePlot object from our library FIRST
        # (before checking for matplotlib figure, since plot objects contain figures)
        try:
            from graphics_lib.core.base import BasePlot
            from graphics_lib.backends.matplotlib import MatplotlibPlot
            from graphics_lib.backends.plotly import PlotlyPlot
            
            if isinstance(plot_data, BasePlot):
                # For matplotlib-based plots, render and get the figure
                if isinstance(plot_data, MatplotlibPlot):
                    # Render the plot if not already rendered
                    if plot_data.fig is None:
                        plot_data.render()
                    
                    if plot_data.fig is not None:
                        return self._matplotlib_to_plotly(plot_data.fig)
                
                # For plotly-based plots, get the figure directly
                elif isinstance(plot_data, PlotlyPlot):
                    if hasattr(plot_data, 'figure') and plot_data.figure is not None:
                        return plot_data.figure
                    # Render if needed
                    plot_data.render()
                    if hasattr(plot_data, 'figure'):
                        return plot_data.figure
        except (ImportError, AttributeError):
            pass
        
        # Check if it's a raw matplotlib figure
        try:
            from matplotlib.figure import Figure as MatplotlibFigure
            if isinstance(plot_data, MatplotlibFigure):
                return self._matplotlib_to_plotly(plot_data)
        except ImportError:
            pass
        
        # Check if it's a dict with a 'figure' key
        if isinstance(plot_data, dict) and 'figure' in plot_data:
            # Dict contains a figure object
            return self._convert_to_plotly_figure(plot_data['figure'], index)
        
        # Check if it's a dict with x/y data
        if isinstance(plot_data, dict):
            return self._create_detail_figure(index, plot_data)
        
        # Fallback: create empty figure with error message
        empty_fig = go.Figure()
        empty_fig.update_layout(
            title=f'Unsupported plot type: {type(plot_data).__name__}',
            annotations=[{
                'text': 'Unable to display this plot type',
                'xref': 'paper',
                'yref': 'paper',
                'showarrow': False,
                'font': {'size': 20}
            }]
        )
        return empty_fig
    
    def _matplotlib_to_plotly(self, mpl_fig):
        """Convert matplotlib figure to Plotly figure using image encoding.
        
        Parameters
        ----------
        mpl_fig : matplotlib.figure.Figure
            The matplotlib figure to convert.
        
        Returns
        -------
        plotly.graph_objects.Figure
            A Plotly figure displaying the matplotlib plot as an image.
        """
        import plotly.graph_objects as go
        import io
        import base64
        
        # Save matplotlib figure to bytes
        buf = io.BytesIO()
        mpl_fig.savefig(buf, format='png', dpi=100, bbox_inches='tight')
        buf.seek(0)
        
        # Encode to base64
        img_base64 = base64.b64encode(buf.read()).decode('utf-8')
        buf.close()
        
        # Create plotly figure with image
        fig = go.Figure()
        
        # Add invisible scatter to set up axes
        fig.add_trace(go.Scatter(
            x=[0, 1],
            y=[0, 1],
            mode='markers',
            marker={'opacity': 0},
            showlegend=False,
            hoverinfo='skip'
        ))
        
        # Add image
        fig.add_layout_image(
            dict(
                source=f'data:image/png;base64,{img_base64}',
                xref="x",
                yref="y",
                x=0,
                y=1,
                sizex=1,
                sizey=1,
                sizing="stretch",
                layer="above"
            )
        )
        
        # Configure layout
        fig.update_xaxes(showticklabels=False, showgrid=False, zeroline=False, range=[0, 1])
        fig.update_yaxes(showticklabels=False, showgrid=False, zeroline=False, range=[0, 1])
        fig.update_layout(
            width=self.detail_figsize[0],
            height=self.detail_figsize[1],
            margin={'l': 0, 'r': 0, 't': 0, 'b': 0},
            xaxis={'visible': False},
            yaxis={'visible': False},
            plot_bgcolor='white',
            paper_bgcolor='white'
        )
        
        return fig

    def _create_detail_figure(self, index, plot_data):
        import plotly.graph_objects as go
        x_data = plot_data.get('x', [])
        y_data = plot_data.get('y', [])
        detail_title = plot_data.get('title', f'Detail for Point {index}')
        
        # Get colors with fallbacks
        primary_color = self._get_color('primary', '#636EFA')
        text_color = self._get_color('text_primary', '#000000')
        bg_color = self._get_color('neutral_light', '#FFFFFF')
        
        fig = go.Figure()
        if self.detail_plot_type == 'line':
            fig.add_trace(go.Scatter(x=x_data, y=y_data, mode='lines',
                line={'color': primary_color}))
        elif self.detail_plot_type == 'scatter':
            fig.add_trace(go.Scatter(x=x_data, y=y_data, mode='markers',
                marker={'color': primary_color, 'size': 8}))
        elif self.detail_plot_type == 'bar':
            fig.add_trace(go.Bar(x=x_data, y=y_data,
                marker={'color': primary_color}))
        elif self.detail_plot_type == 'histogram':
            fig.add_trace(go.Histogram(x=y_data,
                marker={'color': primary_color}))
        fig.update_layout(
            title={'text': detail_title, 'x': 0.5, 'xanchor': 'center'},
            plot_bgcolor=bg_color, paper_bgcolor=bg_color,
            width=self.detail_figsize[0], height=self.detail_figsize[1],
            showlegend=False, margin={'l': 50, 'r': 20, 't': 50, 'b': 50}
        )
        return fig

    def _create_dash_app(self):
        is_jupyter = self._detect_jupyter() if self.app_mode == 'auto' else self.app_mode == 'inline'
        if is_jupyter:
            from jupyter_dash import JupyterDash
            self.app = JupyterDash(__name__)
        else:
            import dash
            self.app = dash.Dash(__name__)
        from dash import dcc, html
        from dash.dependencies import Input, Output
        import plotly.graph_objects as go
        self.app.layout = html.Div([
            html.Div([
                dcc.Graph(id='main-scatter', figure=self.figure,
                    style={'display': 'inline-block', 'width': '55%'}),
                dcc.Graph(id='detail-plot',
                    style={'display': 'inline-block', 'width': '45%'})
            ]),
            html.Div(id='click-info',
                style={'textAlign': 'center', 'padding': '10px'})
        ])
        @self.app.callback(
            [Output('detail-plot', 'figure'), Output('click-info', 'children')],
            [Input('main-scatter', 'clickData')]
        )
        def update_detail(clickData):
            if clickData is None:
                empty_fig = go.Figure()
                empty_fig.update_layout(title='Click a point to see details')
                return empty_fig, 'Click on a point in the scatter plot'
            point_index = clickData['points'][0]['pointIndex']
            plot_data = self._get_plot_data_for_point(point_index)
            if plot_data is None:
                empty_fig = go.Figure()
                empty_fig.update_layout(title='No data available')
                return empty_fig, f'Point {point_index}: No detail data available'
            detail_fig = self._convert_to_plotly_figure(plot_data, point_index)
            return detail_fig, f'Showing details for Point {point_index}'

    def run(self, debug=False, height=650):
        if self.detail_plot_data is None:
            print('No detail plot data provided.')
            super().show()
            return
        self._create_dash_app()
        is_jupyter = self._detect_jupyter() if self.app_mode == 'auto' else self.app_mode == 'inline'
        if is_jupyter:
            print('Starting Dash app in inline mode...')
            self.app.run(mode='inline', debug=debug, height=height, port=self.port)
        else:
            print(f'Starting Dash app on http://localhost:{self.port}')
            print('Press Ctrl+C to stop')
            self.app.run(debug=debug, port=self.port)

    def show(self):
        if self.detail_plot_data is not None:
            self.run()
        else:
            super().show()
