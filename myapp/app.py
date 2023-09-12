import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm

from shiny import App, ui, render

app_ui = ui.page_fixed(
    ui.h2("The Central Limit Theorem (CLT)"),
    ui.layout_sidebar(
        ui.panel_sidebar(

            ui.h5(ui.strong("Population Distribution")),
            ui.input_radio_buttons(
                "dist", "Select Distribution", dict(exponential="Exponential", uniform="Uniform", binomial="Binomial", poisson="Poisson", normal="Normal", gamma="Gamma", chisquare="Chi-Squared")),

            # parameter controls: Shiny documentation says "A more powerful (but slower) way to conditionally show UI content is to use ui."
            # but idk how to do that
            # note: in future implementations it may be better to switch the slider inputs in this section to text inputs (with restrictions on possible values)
            ui.h5(ui.strong("Population Parameters")),
            ui.panel_conditional("input.dist === 'exponential'", ui.input_slider("exponential_rate", "Rate", 0.05,
                                                                                 200, value=1, step=0.05),

                                 ),
            ui.panel_conditional("input.dist === 'uniform'", ui.input_slider("uniform_range", "Range", -100,
                                                                             100, value=(0, 1), step=0.05),

                                 ),
            ui.panel_conditional("input.dist === 'binomial'", ui.input_slider("binomial_n", "n (Total Trials)", 0,
                                                                              200, value=10, step=1),
                                 ui.input_slider("binomial_p", "p (Probability of Success)", 0,
                                                 1, value=0.5, step=0.05),
                                 ),
            ui.panel_conditional("input.dist === 'poisson'", ui.input_slider("poisson_rate", "Rate", 0.05,
                                                                             200, value=1, step=0.05),

                                 ),
            ui.panel_conditional("input.dist === 'normal'", ui.input_slider("normal_loc", "Location (Mean)", -100,
                                                                            100, value=0, step=0.05),
                                 ui.input_slider("normal_scale", "Scale (Standard Deviation )", 0,
                                                 200, value=1, step=0.05),
                                 ),
            ui.panel_conditional("input.dist === 'gamma'", ui.input_slider("gamma_shape", "Shape", 0.05,
                                                                           200, value=1, step=0.05),
                                 ui.input_slider("gamma_rate", "Rate", 0.05,
                                                 200, value=1, step=0.05),
                                 ),
            ui.panel_conditional("input.dist === 'chisquare'", ui.input_slider("chisquare_df", "Degrees of Freedom", 1,
                                                                               200, value=1, step=1),
                                 ),

            ui.h5(ui.strong("Experiment Controls")),
            ui.input_slider("sample_size", "Sample size", 1,
                            10000, value=100, step=1),
            ui.input_slider("number_of_samples", "Number of samples", 1,
                            10000, value=100, step=1),

        ),
        ui.panel_main(
            ui.output_plot("plot")
        )
    )
)


def server(input, output, session):
    @output
    @render.plot
    def plot():

        # TO-DO: address the following concerns
        # is this logic supposed to be here in the server function?
        # is it possible at all to abstractify this? i tried with global functions but it wasn't allowing me to access input (clearly i don't sufficiently understand how this web app works..)
        samples = []
        distribution = input.dist()
        if distribution == "exponential":
            samples = [np.random.exponential(
                1/input.exponential_rate(), input.sample_size()) for i in range(input.number_of_samples())]
            expected_value = 1/input.exponential_rate()
            standard_deviation = np.sqrt(
                (1/input.exponential_rate()) ** 2 / input.sample_size())
        if distribution == "uniform":
            samples = [np.random.uniform(input.uniform_range()[0], input.uniform_range()[
                                         1], input.sample_size()) for i in range(input.number_of_samples())]
            expected_value = (input.uniform_range()[
                              0] + input.uniform_range()[1])/2
            standard_deviation = np.sqrt((input.uniform_range()[
                1] - input.uniform_range()[0]) ** 2)/(12*input.sample_size())
        if distribution == "binomial":
            samples = [np.random.binomial(input.binomial_n(), input.binomial_p(
            ), input.sample_size()) for i in range(input.number_of_samples())]
            expected_value = input.binomial_n() * input.binomial_p()
            standard_deviation = np.sqrt(
                (input.binomial_n()*input.binomial_p()*(1 - input.binomial_p()))/input.sample_size())
        if distribution == "poisson":
            samples = [np.random.poisson(
                input.poisson_rate(), input.sample_size()) for i in range(input.number_of_samples())]
            expected_value = input.poisson_rate()
            standard_deviation = np.sqrt(
                input.poisson_rate()/input.sample_size())
        if distribution == "normal":
            samples = [np.random.normal(input.normal_loc(), input.normal_scale(
            ), input.sample_size()) for i in range(input.number_of_samples())]
            expected_value = input.normal_loc()
            standard_deviation = np.sqrt(
                (input.normal_scale() ** 2)/input.sample_size())
        if distribution == "gamma":
            samples = [np.random.gamma(input.gamma_shape(
            ), 1/(input.gamma_rate()), input.sample_size()) for i in range(input.number_of_samples())]
            expected_value = input.gamma_shape() * (1/input.gamma_rate())
            standard_deviation = np.sqrt(
                (input.gamma_shape()*((1/input.gamma_rate())**2))/input.sample_size())
        if distribution == "chisquare":
            samples = [np.random.chisquare(input.chisquare_df(
            ), input.sample_size()) for i in range(input.number_of_samples())]
            expected_value = input.chisquare_df()
            standard_deviation = np.sqrt(
                (2*input.chisquare_df())/input.number_of_samples())

        sample_means = list(map(np.mean, samples))

        fig = plt.figure()
        ax = fig.add_subplot()  # don't really understand what this is tbh

        # formatting
        # TO-DO: improve formatting
        plt.title('Sample Means Density Plot')
        plt.xlabel('Sample Mean Observations')
        plt.ylabel('Frequency')
        ax.legend()

        # plot observed sample mean distribution
        ax.hist(sample_means, bins=25, density=True,
                color='lightskyblue', label='Observed sample means')
        t0 = np.mean(sample_means)
        observed = 'Observed mean of sample means: ' + \
            str(round(t0, 5))
        ax.axvline(t0, color='steelblue', linewidth=2,
                   label=observed)
        # potential future feature: add a curve to represent the observed distribution and compare with the normal curve?

        # plot expected distribution
        # xmin, xmax = plt.xlim()
        xmin, xmax = ((expected_value - 5*standard_deviation),
                      (expected_value + 5*standard_deviation))
        x = np.linspace(xmin, xmax, 100)
        p = norm.pdf(x, expected_value, standard_deviation)

        ax.plot(x, p, 'k', color='darkslateblue', linewidth=2,
                label="Expected normal distribution")
        expected = 'Expected mean of sample means: ' + \
            str(round(expected_value, 5))
        ax.axvline(x=expected_value, color='darkslateblue',
                   linewidth=2, label=expected)

        plt.legend()

        return fig
        # return ax
        # what does it mean to return fig vs return ax


app = App(app_ui, server)
