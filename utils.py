def validate_float(prompt, min_val=None):
    while True:
        val = input(prompt).strip().lower()
        if val in ['e', 'c', 'p']:
            return val
        try:
            val_float = float(val.replace(',', ''))
            if min_val is not None and val_float < min_val:
                print("⚠️ Value too low. Try again.")
                continue
            if val_float > 1e12:
                print("⚠️ Value too large. Try again.")
                continue
            return val_float
        except ValueError:
            print("⚠️ Invalid number. Use digits only.")


def validate_int(prompt, min_val=None):
    while True:
        val = input(prompt).strip().lower()
        if val in ['e', 'c', 'p']:
            return val
        try:
            val_int = int(val.replace(',', ''))
            if min_val is not None and val_int < min_val:
                print("⚠️ Value too low. Try again.")
                continue
            if val_int > 1e6:
                print("⚠️ Value too large. Try again.")
                continue
            return val_int
        except ValueError:
            print("⚠️ Invalid number. Use digits only.")


def format_currency_jmd(amount):
    return f"J${amount:,.2f}"




