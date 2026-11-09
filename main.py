from datetime import datetime

DESTINATIONS = ["Delhi", "Jaipur"]
TIME_SLOTS = ["Morning", "Afternoon", "Evening", "Night"]


def ask_year():
    while True:
        ans = input("Year (1 to 5): ").strip()
        if ans.isdigit() and 1 <= int(ans) <= 5:
            return int(ans)
        print(f"  '{ans}' is not a valid year. Enter a number from 1 to 5.")


def add(waiting, n):
    # name = ask_name()
    # destination = ask_place(DESTINATIONS)
    # time = ask_time(TIME_SLOTS)
    year = ask_year()

    # r = RideRequest(name, destination, time, year, n)
    # waiting.append(r)
    # print(f"Added" {r})


def show(waiting, cab):
    if len(waiting) == 0:
        print("Nobody is waiting")
    else:
        for r in waiting:
            print(f" {r}")


def main():
    print("BITS Cab Pool Matcher")
    waiting = []
    cab = []
    n = 1
    while True:
        print("1. Add a ride request")
        print("2. Show waiting students and cabs")
        print("3. Quit")
        choice = input("Choose an option: ").strip()

        if choice == "1":
            add(waiting, n)
            n += 1
        elif choice == "2":
            show(waiting, cab)
        elif choice == "3":
            break
        else:
            print("Enter 1, 2 or 3")


if __name__ == "__main__":
    main()
