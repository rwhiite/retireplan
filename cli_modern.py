from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich import box
from rich.prompt import Prompt
from utils import validate_float, validate_int, format_currency_jmd
from algorithms import fixedInvestor, variableInvestor, finallyRetired, maximumExpensed
from visualize import plot_balance_text

console = Console()

def print_header():
    """Display the application header with branding"""
    header = Text()
    header.append("RetirePlan", style="bold cyan")
    header.append(" Pro", style="bold magenta")
    
    panel = Panel(
        Text("Your Personal Retirement Planning Assistant", style="italic white", justify="center"),
        title=header,
        border_style="cyan",
        box=box.DOUBLE,
        padding=(1, 2)
    )
    console.print()
    console.print(panel)
    console.print()

def print_menu():
    """Display the main menu with styled options"""
    table = Table(
        show_header=False,
        box=box.ROUNDED,
        border_style="blue",
        padding=(0, 2)
    )
    
    table.add_column("Option", style="cyan bold", width=8)
    table.add_column("Description", style="white")
    
    table.add_row("1", "💰 Fixed Growth Investment")
    table.add_row("2", "📊 Variable Growth Investment")
    table.add_row("3", "⏳ Years Until Depletion")
    table.add_row("4", "🎯 Optimal Withdrawal Amount")
    table.add_row("5", "📈 Visualize Balance Timeline")
    table.add_row("", "")
    table.add_row("E", "🚪 Exit", style="dim")
    table.add_row("C", "🗑️  Clear All Data", style="dim")
    
    console.print(Panel(table, title="[bold white]Main Menu[/bold white]", border_style="blue", box=box.ROUNDED))
    console.print()

def print_result(label, value):
    """Display calculation results in a styled panel"""
    result_text = Text()
    result_text.append(f"{label}\n", style="bold cyan")
    result_text.append(value, style="bold green")
    
    console.print()
    console.print(Panel(
        result_text,
        title="[bold green]✓ Result[/bold green]",
        border_style="green",
        box=box.HEAVY,
        padding=(1, 2)
    ))
    console.print()

def print_error(message):
    """Display error messages in a styled panel"""
    console.print()
    console.print(Panel(
        f"[bold yellow]{message}[/bold yellow]",
        title="[bold red]⚠ Warning[/bold red]",
        border_style="red",
        box=box.ROUNDED
    ))
    console.print()

def print_exit():
    """Display goodbye message"""
    console.print()
    console.print(Panel(
        "[bold cyan]Thank you for using RetirePlan Pro![/bold cyan]\n[white]Plan wisely, retire comfortably. 🌴[/white]",
        border_style="cyan",
        box=box.DOUBLE
    ))
    console.print()

def print_cleared():
    """Display data cleared message"""
    console.print()
    console.print(Panel(
        "[bold yellow]All data has been cleared.[/bold yellow]\n[white]Starting fresh...[/white]",
        title="[bold orange1]🗑️  Data Reset[/bold orange1]",
        border_style="yellow",
        box=box.ROUNDED
    ))
    console.print()

def print_navigation_help():
    """Display navigation help"""
    console.print("[dim]Navigation: P=Previous | B=Back to Menu | C=Clear | E=Exit[/dim]\n")

def styled_input(prompt_text, style="cyan"):
    """Custom styled input prompt"""
    console.print(f"[{style}]➤[/{style}] [bold white]{prompt_text}[/bold white]", end=" ")
    return input().strip()

def main():
    print_header()
    accum_history = []
    retire_history = {}

    while True:
        print_menu()
        choice = styled_input("Enter your choice", style="bold cyan").lower()

        if choice == "e":
            print_exit()
            break
        elif choice == "c":
            accum_history.clear()
            retire_history.clear()
            print_cleared()
            continue
        elif choice == "b":
            # Already at main menu
            console.print("[dim]Already at main menu[/dim]\n")
            continue

        # ----------------- Fixed Growth -----------------
        if choice == "1":
            console.print("\n[bold cyan]═══ Fixed Growth Investment ═══[/bold cyan]\n")
            print_navigation_help()
            
            # Step 1: Principal
            while True:
                principal = validate_float("💰 Initial principal: ", 0)
                if principal == 'e':
                    print_exit()
                    return
                elif principal == 'c':
                    accum_history.clear()
                    retire_history.clear()
                    print_cleared()
                    break
                elif principal == 'b':
                    break
                elif principal == 'p':
                    console.print("[dim]Already at first step[/dim]\n")
                    continue
                else:
                    break
            
            if principal in ['c', 'b']:
                continue
            
            # Step 2: Rate
            while True:
                rate = validate_float("📈 Annual growth rate (e.g. 0.05 = 5%): ", 0)
                if rate == 'e':
                    print_exit()
                    return
                elif rate == 'c':
                    accum_history.clear()
                    retire_history.clear()
                    print_cleared()
                    break
                elif rate == 'b':
                    break
                elif rate == 'p':
                    # Go back to principal
                    principal = validate_float("💰 Initial principal: ", 0)
                    if principal in ['e', 'c', 'b', 'p']:
                        if principal == 'e':
                            print_exit()
                            return
                        elif principal == 'c':
                            accum_history.clear()
                            retire_history.clear()
                            print_cleared()
                            break
                        elif principal == 'b':
                            break
                        elif principal == 'p':
                            console.print("[dim]Already at first step[/dim]\n")
                            continue
                    continue
                else:
                    break
            
            if rate in ['c', 'b'] or principal in ['c', 'b']:
                continue
            
            # Step 3: Years
            while True:
                years = validate_int("🕒 Years until retirement: ", 1)
                if years == 'e':
                    print_exit()
                    return
                elif years == 'c':
                    accum_history.clear()
                    retire_history.clear()
                    print_cleared()
                    break
                elif years == 'b':
                    break
                elif years == 'p':
                    # Go back to rate
                    rate = validate_float("📈 Annual growth rate (e.g. 0.05 = 5%): ", 0)
                    if rate in ['e', 'c', 'b']:
                        if rate == 'e':
                            print_exit()
                            return
                        elif rate == 'c':
                            accum_history.clear()
                            retire_history.clear()
                            print_cleared()
                            break
                        elif rate == 'b':
                            break
                    elif rate == 'p':
                        principal = validate_float("💰 Initial principal: ", 0)
                        if principal in ['e', 'c', 'b']:
                            if principal == 'e':
                                print_exit()
                                return
                            elif principal == 'c':
                                accum_history.clear()
                                retire_history.clear()
                                print_cleared()
                                break
                            elif principal == 'b':
                                break
                        elif principal == 'p':
                            console.print("[dim]Already at first step[/dim]\n")
                    continue
                else:
                    break
            
            if years in ['c', 'b'] or rate in ['c', 'b'] or principal in ['c', 'b']:
                continue
            
            # Step 4: Contribution
            while True:
                contribution = validate_float("💵 Annual contribution: ", 0)
                if contribution == 'e':
                    print_exit()
                    return
                elif contribution == 'c':
                    accum_history.clear()
                    retire_history.clear()
                    print_cleared()
                    break
                elif contribution == 'b':
                    break
                elif contribution == 'p':
                    # Go back to years
                    years = validate_int("🕒 Years until retirement: ", 1)
                    if years in ['e', 'c', 'b']:
                        if years == 'e':
                            print_exit()
                            return
                        elif years == 'c':
                            accum_history.clear()
                            retire_history.clear()
                            print_cleared()
                            break
                        elif years == 'b':
                            break
                    continue
                else:
                    break
            
            if contribution in ['c', 'b']:
                continue
            
            balance, accum_history = fixedInvestor(principal, rate, years, contribution)
            print_result("Accumulated Balance", format_currency_jmd(balance))

        # ----------------- Variable Growth -----------------
        elif choice == "2":
            console.print("\n[bold cyan]═══ Variable Growth Investment ═══[/bold cyan]\n")
            print_navigation_help()
            
            # Step 1: Principal
            while True:
                principal = validate_float("💰 Initial principal: ", 0)
                if principal == 'e':
                    print_exit()
                    return
                elif principal == 'c':
                    accum_history.clear()
                    retire_history.clear()
                    print_cleared()
                    break
                elif principal == 'b':
                    break
                elif principal == 'p':
                    console.print("[dim]Already at first step[/dim]\n")
                    continue
                else:
                    break
            
            if principal in ['c', 'b']:
                continue
            
            # Step 2: Number of years
            while True:
                num_years = validate_int("🕒 Number of years: ", 1)
                if num_years == 'e':
                    print_exit()
                    return
                elif num_years == 'c':
                    accum_history.clear()
                    retire_history.clear()
                    print_cleared()
                    break
                elif num_years == 'b':
                    break
                elif num_years == 'p':
                    # Go back to principal
                    principal = validate_float("💰 Initial principal: ", 0)
                    if principal in ['e', 'c', 'b']:
                        if principal == 'e':
                            print_exit()
                            return
                        elif principal == 'c':
                            accum_history.clear()
                            retire_history.clear()
                            print_cleared()
                            break
                        elif principal == 'b':
                            break
                    elif principal == 'p':
                        console.print("[dim]Already at first step[/dim]\n")
                    continue
                else:
                    break
            
            if num_years in ['c', 'b'] or principal in ['c', 'b']:
                continue
            
            # Step 3: Rate list with proper previous navigation
            console.print(f"\n[bold yellow]Enter growth rate for each year:[/bold yellow]\n")
            rateList = []
            current_year = 0
            
            while current_year < num_years:
                r = validate_float(f"📊 Year {current_year+1} growth rate (e.g. 0.05 = 5%): ")
                
                if r == 'e':
                    print_exit()
                    return
                elif r == 'c':
                    accum_history.clear()
                    retire_history.clear()
                    print_cleared()
                    break
                elif r == 'b':
                    break
                elif r == 'p':
                    if current_year == 0:
                        # Go back to num_years
                        num_years = validate_int("🕒 Number of years: ", 1)
                        if num_years in ['e', 'c', 'b']:
                            break
                        elif num_years == 'p':
                            principal = validate_float("💰 Initial principal: ", 0)
                            if principal in ['e', 'c', 'b']:
                                break
                        rateList = []
                        current_year = 0
                        console.print(f"\n[bold yellow]Enter growth rate for each year:[/bold yellow]\n")
                        continue
                    else:
                        # Go back to previous year
                        current_year -= 1
                        rateList.pop()
                        console.print(f"[dim]← Back to Year {current_year+1}[/dim]\n")
                        continue
                else:
                    rateList.append(r)
                    current_year += 1
            
            if r in ['c', 'b'] or num_years in ['c', 'b']:
                continue
            
            # Step 4: Contribution
            while True:
                contribution = validate_float("💵 Annual contribution: ", 0)
                if contribution == 'e':
                    print_exit()
                    return
                elif contribution == 'c':
                    accum_history.clear()
                    retire_history.clear()
                    print_cleared()
                    break
                elif contribution == 'b':
                    break
                elif contribution == 'p':
                    # Go back to rate list (restart from last year)
                    if rateList:
                        rateList.pop()
                        current_year = len(rateList)
                        console.print(f"\n[bold yellow]Enter growth rate for each year:[/bold yellow]\n")
                        console.print(f"[dim]Continuing from Year {current_year+1}[/dim]\n")
                        
                        while current_year < num_years:
                            r = validate_float(f"📊 Year {current_year+1} growth rate (e.g. 0.05 = 5%): ")
                            if r in ['e', 'c', 'b', 'p']:
                                break
                            rateList.append(r)
                            current_year += 1
                        
                        if r in ['e', 'c', 'b']:
                            break
                    continue
                else:
                    break
            
            if contribution in ['c', 'b']:
                continue
            
            balance, accum_history = variableInvestor(principal, rateList, contribution)
            print_result("Accumulated Balance", format_currency_jmd(balance))

        # ----------------- Years Until Depletion -----------------
        elif choice == "3":
            if not accum_history:
                print_error("Please run a growth simulation first (Option 1 or 2)")
                continue
            
            console.print("\n[bold cyan]═══ Years Until Depletion ═══[/bold cyan]\n")
            print_navigation_help()
            
            # Step 1: Rate
            while True:
                rate = validate_float("📉 Post-retirement growth rate (e.g. 0.03): ", 0)
                if rate == 'e':
                    print_exit()
                    return
                elif rate == 'c':
                    accum_history.clear()
                    retire_history.clear()
                    print_cleared()
                    break
                elif rate == 'b':
                    break
                elif rate == 'p':
                    console.print("[dim]Already at first step[/dim]\n")
                    continue
                else:
                    break
            
            if rate in ['c', 'b']:
                continue
            
            # Step 2: Expense
            while True:
                expense = validate_float("💵 Annual withdrawal amount: ", 0)
                if expense == 'e':
                    print_exit()
                    return
                elif expense == 'c':
                    accum_history.clear()
                    retire_history.clear()
                    print_cleared()
                    break
                elif expense == 'b':
                    break
                elif expense == 'p':
                    # Go back to rate
                    rate = validate_float("📉 Post-retirement growth rate (e.g. 0.03): ", 0)
                    if rate in ['e', 'c', 'b']:
                        if rate == 'e':
                            print_exit()
                            return
                        elif rate == 'c':
                            accum_history.clear()
                            retire_history.clear()
                            print_cleared()
                            break
                        elif rate == 'b':
                            break
                    elif rate == 'p':
                        console.print("[dim]Already at first step[/dim]\n")
                    continue
                else:
                    break
            
            if expense in ['c', 'b'] or rate in ['c', 'b']:
                continue
            
            years, history = finallyRetired(accum_history[-1], expense, rate)
            retire_history["custom"] = history
            print_result("Years Until Depletion", f"{years} years")

        # ----------------- Optimal Withdrawal -----------------
        elif choice == "4":
            if not accum_history:
                print_error("Please run a growth simulation first (Option 1 or 2)")
                continue
            
            console.print("\n[bold cyan]═══ Optimal Withdrawal Calculator ═══[/bold cyan]\n")
            print_navigation_help()
            
            # Step 1: Rate
            while True:
                rate = validate_float("📉 Post-retirement growth rate (e.g. 0.03): ", 0)
                if rate == 'e':
                    print_exit()
                    return
                elif rate == 'c':
                    accum_history.clear()
                    retire_history.clear()
                    print_cleared()
                    break
                elif rate == 'b':
                    break
                elif rate == 'p':
                    console.print("[dim]Already at first step[/dim]\n")
                    continue
                else:
                    break
            
            if rate in ['c', 'b']:
                continue
            
            # Step 2: Retirement years
            while True:
                retirement_years = validate_int("🕒 Expected retirement duration (years): ", 1)
                if retirement_years == 'e':
                    print_exit()
                    return
                elif retirement_years == 'c':
                    accum_history.clear()
                    retire_history.clear()
                    print_cleared()
                    break
                elif retirement_years == 'b':
                    break
                elif retirement_years == 'p':
                    # Go back to rate
                    rate = validate_float("📉 Post-retirement growth rate (e.g. 0.03): ", 0)
                    if rate in ['e', 'c', 'b']:
                        if rate == 'e':
                            print_exit()
                            return
                        elif rate == 'c':
                            accum_history.clear()
                            retire_history.clear()
                            print_cleared()
                            break
                        elif rate == 'b':
                            break
                    elif rate == 'p':
                        console.print("[dim]Already at first step[/dim]\n")
                    continue
                else:
                    break
            
            if retirement_years in ['c', 'b'] or rate in ['c', 'b']:
                continue
            
            optimal = maximumExpensed(accum_history[-1], rate, retirement_years)
            print_result("Optimal Annual Withdrawal 🎯", format_currency_jmd(optimal))
            years, history = finallyRetired(accum_history[-1], optimal, rate, years=retirement_years)
            retire_history["optimal"] = history

        # ----------------- Visualization -----------------
        elif choice == "5":
            if not retire_history:
                print_error("Please run a depletion simulation first (Option 3 or 4)")
                continue

            available = []
            if "custom" in retire_history:
                available.append("1")
            if "optimal" in retire_history:
                available.append("2")

            if len(available) == 1:
                sub_choice = available[0]
                if sub_choice == "1":
                    console.print("\n[bold cyan]═══ Custom Withdrawal Visualization ═══[/bold cyan]")
                    plot_balance_text(accum_history, retire_history["custom"])
                elif sub_choice == "2":
                    console.print("\n[bold cyan]═══ Optimal Withdrawal Visualization ═══[/bold cyan]")
                    plot_balance_text(accum_history, retire_history["optimal"])
                continue
            else:
                while True:
                    console.print("\n[bold cyan]═══ Choose Visualization ═══[/bold cyan]\n")
                    print_navigation_help()
                    
                    viz_table = Table(show_header=False, box=box.ROUNDED, border_style="blue", padding=(0, 2))
                    viz_table.add_column("Option", style="cyan bold", width=8)
                    viz_table.add_column("Description", style="white")
                    
                    if "custom" in retire_history:
                        viz_table.add_row("1", "📊 Custom Withdrawal Depletion")
                    if "optimal" in retire_history:
                        viz_table.add_row("2", "🎯 Optimal Withdrawal Depletion")
                    viz_table.add_row("", "")
                    viz_table.add_row("B", "◀ Back to Main Menu", style="dim")
                    viz_table.add_row("E", "🚪 Exit", style="dim")
                    viz_table.add_row("C", "🗑️  Clear All Data", style="dim")
                    
                    console.print(viz_table)
                    console.print()
                    
                    sub_choice = styled_input("Enter choice", style="bold cyan").lower()
                    
                    if sub_choice == "e":
                        print_exit()
                        return
                    elif sub_choice == "c":
                        accum_history.clear()
                        retire_history.clear()
                        print_cleared()
                        break
                    elif sub_choice == "b":
                        break
                    elif sub_choice == "p":
                        console.print("[dim]Already at first step (use B to go back to main menu)[/dim]\n")
                        continue
                    elif sub_choice == "1" and "1" in available:
                        console.print("\n[bold cyan]═══ Custom Withdrawal Visualization ═══[/bold cyan]")
                        plot_balance_text(accum_history, retire_history["custom"])
                        break
                    elif sub_choice == "2" and "2" in available:
                        console.print("\n[bold cyan]═══ Optimal Withdrawal Visualization ═══[/bold cyan]")
                        plot_balance_text(accum_history, retire_history["optimal"])
                        break
                    else:
                        print_error("Invalid option. Please try again.")
        else:
            print_error("Invalid choice. Please select a valid option.")

if __name__ == "__main__":
    main()