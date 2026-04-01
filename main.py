from plotter import plot_vol_surface
def main():
    print("Running Vol Surface Project...")


    # Use the cubic interpolation to draw the IV surface

    fig = plot_vol_surface("AAPL")
    fig.show()

if __name__ == "__main__":
    main()