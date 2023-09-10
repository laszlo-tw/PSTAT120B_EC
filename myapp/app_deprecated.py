import numpy as np
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt

from shiny import App, ui

from enum import Enum


# class DISTRIBUTION(Enum):
#     EXPONENTIAL = 1
#     UNIFORM = 2
#     GAMMA = 3


# distributions = {DISTRIBUTION.EXPONENTIAL: "Exponential",
#                  DISTRIBUTION.UNIFORM: "Uniform", DISTRIBUTION.GAMMA: "Gamma"}

# https://numpy.org/doc/stable/reference/random/legacy.html
distributions = {np.random.exponential: "Exponential",
                 np.random.uniform: "Uniform", np.random.gamma: "Gamma"}


# TO-DO: fix exclusive ranges
def parameter_controls():
    distribution = input.dist()
    if distribution == np.random.exponential:
        return ui.panel_sidebar(
            ui.input_slider("exponential_rate", "Rate", 0,
                            200, value=1, step=0.05),
        )
    if distribution == np.random.uniform:
        return ui.panel_sidebar(
            ui.input_slider("uniform_range", "Range", -100,
                            100, value=(0, 1), step=0.05),
        )
    if distribution == np.random.gamma:
        return ui.panel_sidebar(
            ui.input_slider("gamma_shape", "Shape", 0,
                            200, value=1, step=0.05),
            ui.input_slider("gamma_rate", "Rate", -1,
                            200, value=1, step=0.05),
        )
    else:
        return  # crash the site, obviously


# numpy prefers scale parameter
def params():  # naming of this and the previous function is horrible
    distribution = input.dist()
    if distribution == np.random.exponential:
        return [1/input.exponential_rate(), input.sample_size()]
    if distribution == np.random.uniform:
        return [input.uniform_range()[1], input.uniform_range()[2], input.sample_size()]
    if distribution == np.random.gamma:
        return [input.gamma_shape(), 1/(input.gamma_rate()), input.sample_size()]
    else:
        return  # crash the site, obviously


def data():
    samples = [[input.dist()(params())]
               for i in range(input.number_of_samples())]
    sample_means = map(np.mean(), samples)
    return sample_means

# Part 1: ui ----
# app_ui = ui.page_fluid(
#     "Hello, world!",

#     ui.input_slider("n", "Choose a number n:", 0, 100, 40),
#     ui.output_text_verbatim("txt")
# )


app_ui = ui.page_fixed(
    ui.h2("The Central Limit Theorem (CLT)"),
    ui.markdown("""
        This app is based on a [Matplotlib example][0] that displays 2D data
        with a user-adjustable colormap. We use a range slider to set the data
        range that is covered by the colormap.

        [0]: https://matplotlib.org/3.5.3/gallery/userdemo/colormap_interactive_adjustment.html
    """),
    ui.layout_sidebar(
        ui.panel_sidebar(
            ui.input_radio_buttons("dist", "Population distribution",
                                   distributions),
            # ui.input_radio_buttons("dist", "Population distribution",
            #                        dict(viridis="Exponential",
            #                             gist_heat="Uniform", RdYlBu="Gamma")
            #                        ),
            ui.input_slider("sample_size", "Sample size", -1,
                            1, value=(-1, 1), step=0.05),
            ui.input_slider("number_of_samples", "Number of samples", -1,
                            1, value=(-1, 1), step=0.05),

            # TO-DO: add distribution parameter inputs (based on "dist" radio button input and DISTRIBUTIONS enum)
        ),
        parameter_controls(),
        ui.panel_main(
            ui.output_plot("plot")
        )
    )
)

# Part 2: server ----


# def server(input, output, session):
#     @output         # means that the result should be displayed on the web page
#     @render.text    # means that the result is text and not something else like an image
#     def txt():
#         return f"n*2 is {input.n() * 2}"

def server(input, output, session):
    @output
    @render.plot
    def plot():
        # fig, ax = plt.subplots()
        # im = ax.imshow(data2d, cmap=input.dist(),
        #                vmin=input.range()[0], vmax=input.range()[1])
        # fig.colorbar(im, ax=ax)
        # return fig

        fig = px.histogram(
            data(), x="Sample Mean Observations", nbins=20)
        return fig


# Combine into a shiny app.
# Note that the variable must be "app".
app = App(app_ui, server)
