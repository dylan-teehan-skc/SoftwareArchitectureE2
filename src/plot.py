import matplotlib.pyplot as plt


def save_and_show_cumulative(dates, cumulative_hours, path):
    path.parent.mkdir(parents=True, exist_ok=True)
    plt.plot(dates, cumulative_hours)
    plt.xlabel("Year")
    plt.ylabel("Cumulative EVA duration (hours)")
    plt.tight_layout()
    plt.savefig(path)
    plt.show()
