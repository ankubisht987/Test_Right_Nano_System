from summarize import main as run_summary
from plot_chart import main as run_chart


def main():
    print("Step 1: Summarizing device data...")
    run_summary()
    print("\nStep 1 complete.")

    print("\nStep 2: Creating chart...")
    run_chart()
    print("\nStep 2 complete. END!!!!!")


if __name__ == "__main__":
    main()
