class ConsoleInput:
    def __init__(self, read=input):
        self.read = read

    def ask_filename(self):
        return self.read("Enter the data filename: ").strip()

    def ask_country(self):
        return self.read("Enter a country (USA or Russia): ").strip()


class ConsoleOutput:
    def __init__(self, write=print):
        self.write = write

    def show_country_total(self, country, hours):
        self.write(f"Total EVA duration for {country}: {hours:.2f} hours")

    def show_categories(self, counts):
        classified = sum(counts.values())
        self.write("EVA duration categories (all EVAs with a duration):")
        for category, count in counts.items():
            percentage = count / classified * 100 if classified else 0
            self.write(f"{category}: {count} EVAs ({percentage:.2f}%)")
