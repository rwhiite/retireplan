def plot_balance_text(accum_history, retire_history):
    print("\n📈 BALANCE OVER TIME\n")
    print("Accumulation = '█' | Depletion = '▓'\n")

    combined = accum_history + retire_history
    max_bal = max(combined) if combined else 1

    for i, bal in enumerate(combined, 1):
        bar_len = int((bal / max_bal) * 50)
        bar_char = '█' if i <= len(accum_history) else '▓'
        print(f"Year {i:2d} | {bar_char * bar_len} {bal:,.2f} JMD")

