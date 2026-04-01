import numpy as np
import datetime
import plotly.graph_objects as go
from scipy.interpolate import CloughTocher2DInterpolator
from filter_options import get_vol_surface_data
# Use the cubic interpolation to draw the IV surface

def plot_vol_surface(ticker):
    final_options = get_vol_surface_data(ticker)
    cubic_interpolator=CloughTocher2DInterpolator(list(zip(final_options["strike_price"],
    final_options["DTE"])), final_options["computed_iv"])
    strike_grid = np.linspace(min(final_options["strike_price"]), max(final_options["strike_price"]))
    DTE_grid = np.linspace(min(final_options["DTE"]), max(final_options["DTE"]))
    X, Y=np.meshgrid(strike_grid, DTE_grid)

    IV_vals = cubic_interpolator(X, Y)
    fig = go.Figure(data=[go.Surface(x=strike_grid, y=DTE_grid, 
                                 z=IV_vals, colorscale="Jet", surfacecolor = IV_vals)])
    
    # Add the title

    now_str = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")

    fig.update_layout(title=f"Cubic interpolated volatility surface for {ticker} <br> Generated at {now_str}", 
                  autosize=False, width=500, height=500, 
                  margin=dict(l=50, r=50, t=90, b=50))
    

    fig.update_scenes(xaxis_title_text="Strike Price", yaxis_title_text="DTE", zaxis_title_text="Implied Volatility")

    # Add the grid line

    Y_rev, X_rev = np.meshgrid(DTE_grid, strike_grid)

    line_marker=dict(color="black", width=2)

    for x, y, z in zip(X, Y, IV_vals):
        fig.add_trace(go. Scatter3d(x=x, y=y, z=z, mode="lines", line=line_marker, showlegend=False))

    for x, y, z in zip(X_rev, Y_rev, IV_vals.T):
        fig.add_trace(go. Scatter3d(x=x, y=y, z=z, mode="lines", line=line_marker, showlegend=False))

    return fig