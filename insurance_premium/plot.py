import matplotlib.pyplot as plt


def plot_insurance_premium_diff(data):
    series = data.loc['original_govern_share (hundred toman)']
    plt.bar(series.index, series.array)
    plt.ylabel("Share per person")
    plt.title("government insurance premium share per person")
    plt.show()
