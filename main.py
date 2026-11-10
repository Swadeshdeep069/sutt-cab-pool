from datetime import datetime
import json
import heapq

DESTINATIONS = ["Delhi", "Jaipur"]
TIME_SLOTS = ["Morning", "Afternoon", "Evening", "Night"]


class RideRequest:
    def __init__(
        self, name, destination, time_slot, year, request_n, submitted_at=None
    ):
        self.name = name
        self.destination = destination
        self.time_slot = time_slot
        self.year = year
        self.request_n = request_n
        if submitted_at is None:
            submitted_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        self.submitted_at = submitted_at

    def __str__(self):
        return f"{self.name} (Year {self.year}) - {self.destination}, {self.time_slot} - asked at {self.submitted_at}"


class Cab:
    def __init__(self, driver, seats, destination, time_slot):
        self.driver = driver
        self.seats = seats
        self.destination = destination
        self.time_slot = time_slot
        self.has_left = False
        self.passengers = []

    def free_seats(self):
        return self.seats - len(self.passengers)

    def __str__(self):
        status = "LEFT" if self.has_left else "open"
        return (
            f"{self.driver} | {self.destination}, {self.time_slot} | "
            f"{len(self.passengers)}/{self.seats} seats | {status}"
        )


def ask_place(places):
    while True:
        print("Where do u want to go?")
        for i, p in enumerate(places, start=1):
            print(f" {i}. {p}")
        ans = input("> ").strip()

        if ans.isdigit() and 1 <= int(ans) <= len(places):
            return places[int(ans) - 1]
        for p in places:
            if ans.lower() == p.lower():
                return p
        print(f"  Sorry, we don't go to '{ans}'. Pick from the list.")


def ask_time(slots):
    while True:
        print("When do u wanna go?")
        for i, s in enumerate(slots, start=1):
            print(f" {i}. {s}")
        ans = input("> ").strip()

        if ans.isdigit() and 1 <= int(ans) <= len(slots):
            return slots[int(ans) - 1]
        for s in slots:
            if ans.lower() == s.lower():
                return s
        print(f"  '{ans}' is not a valid time slot. Pick from the list.")


def ask_name():
    while True:
        name = input("Student name: ").strip()
        if name:
            return name
        print(" Name cant be empty, try again")


def ask_year():
    while True:
        ans = input("Year (1 to 5): ").strip()
        if ans.isdigit() and 1 <= int(ans) <= 5:
            return int(ans)
        print(f"  '{ans}' is not a valid year. Enter a number from 1 to 5.")


def add(waiting, cab, n):
    name = ask_name()
    destination = ask_place(DESTINATIONS)
    time = ask_time(TIME_SLOTS)
    year = ask_year()

    r = RideRequest(name, destination, time, year, n)
    heapq.heappush(waiting[(destination, time)], (-year, n, r))
    print(f"Added {r}")

    if find_cab(cab, destination, time) is None:
        print(
            " Note: no open cab for this trip right now, Youll stay in the waiting list."
        )


def show(waiting, cab):
    print("\n--- Waiting(senior first) ---")
    nobody = True
    for key in waiting:
        heap = waiting[key]
        if len(heap) == 0:
            continue
        nobody = False
        d, s = key
        print(f"\n{d}, {s}:")
        if find_cab(cab, d, s) is None:
            print("(no cab for this trip, waiting)")
        for e in sorted(heap):
            print(f"   {e[2]}")
    if nobody:
        print("Nobody is waiting")

    print("\n--- Cabs ---")
    if len(cab) == 0:
        print("No cabs loaded")
    else:
        for c in cab:
            print(f" {c}")


def load_cabs(filename):
    try:
        with open(filename) as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"Could not find '{filename}'. Please add a cab file.")
        return []
    except json.JSONDecodeError:
        print(f"'{filename}' is not valid JSON. Please fix it.")
        return []

    cabs = []
    for c in data:
        try:
            driver = c["driver"]
            seats = int(c["seats"])
            destination = c["destination"]
            time_slot = c["time_slot"]
        except (KeyError, ValueError, TypeError):
            print(f"Skipping a broken cab entry: {c}")
            continue

        if (
            destination not in DESTINATIONS
            or time_slot not in TIME_SLOTS
            or not 1 <= seats <= 4
        ):
            print(f"Skipping cab with bad values: {c}")
            continue

        cabs.append(Cab(driver, seats, destination, time_slot))

    print(f"Loaded {len(cabs)} cabs from {filename}")
    return cabs


def find_cab(cabs, dest, slot):
    for c in cabs:
        if not c.has_left and c.destination == dest and c.time_slot == slot:
            return c
    return None


def find_match(waiting, cab):
    print("\n--- Matches(preview) ---")
    taken = {}
    found = False

    for c in cab:
        if c.has_left:
            continue
        found = True
        k = (c.destination, c.time_slot)
        done = taken.get(k, 0)

        top = heapq.nsmallest(done + c.free_seats(), waiting[k])
        picks = [e[2] for e in top[done:]]
        taken[k] = done + len(picks)

        print(f"\n{c}")
        if len(picks) == 0:
            print(" nobody waiting for this trip")
        for p in picks:
            print(f" -> {p}")

    if not found:
        print("No open cabs there")


def dispatch(waiting, cab):
    print("--- Dispatch cab---")
    destination = ask_place(DESTINATIONS)
    time = ask_time(TIME_SLOTS)
    c = find_cab(cab, destination, time)
    if c is None:
        print(f"no cab for {destination}, {time}")
        return

    h = waiting[(destination, time)]
    if len(h) == 0:
        print(f"Nobody is waiting for {destination}, {time}")
        return

    while cab.free_seats() > 0 and len(h) > 0:
        b = heapq.heappop(h)
        cab.passengers.append(b[2])
    cab.has_left = True

    print(f"cab left! {cab}")
    for s in cab.passengers:
        print(f"  - {s.name} (Year {s.year})")


def main():
    print("BITS Cab Pool Matcher")
    waiting = {}
    for d in DESTINATIONS:
        for s in TIME_SLOTS:
            waiting[(d, s)] = []
    cab = load_cabs("cabs.json")
    n = 1
    while True:
        print("1. Add a ride request")
        print("2. Show waiting students and cabs")
        print("3. Find matches")
        print("4. Dispatch a cab")
        print("5. Quit")
        choice = input("Choose an option: ").strip()

        if choice == "1":
            add(waiting, cab, n)
            n += 1
        elif choice == "2":
            show(waiting, cab)
        elif choice == "3":
            find_match(waiting, cab)
        elif choice == "4":
            dispatch(waiting, cab)
        elif choice == "5":
            break
        else:
            print("Enter from 1 to 5")


if __name__ == "__main__":
    main()
