# SUTT Cab Pool Matcher

cli app for sutt backend task 1. add ride requests and it puts students in cabs, seniors get seats first.

## how to run

Use python 3, no extra packages

```
python3 main.py
```

run it in the same folder as cabs.json

menu:

1. add a ride request
2. show waiting students and cabs
3. find matches (just a preview, nobody is moved)
4. dispatch a cab
5. quit

## cab file

cabs are loaded from cabs.json at the start. its a list like this:

```json
[
  {
    "driver": "Ramesh",
    "seats": 4,
    "destination": "Delhi",
    "time_slot": "Morning"
  },
  {
    "driver": "Rajesh",
    "seats": 2,
    "destination": "Jaipur",
    "time_slot": "Evening"
  }
]
```

seats can be 1-4, destination is Delhi or Jaipur, time_slot is Morning/Afternoon/Evening/Night. if a cab has wrong values it gets skipped.

## how it works

there is one queue for each destination + time slot (like Delhi Morning). i make all 8 at the start so i dont have to check if the queue exists.

each queue is a heap. i push `(-year, request_n, request)`. heapq gives smallest first so -year makes the senior come first. request_n is 1,2,3... so if same year then whoever asked first comes first.

find matches uses heapq.nsmallest so it only looks and doesnt remove anyone. dispatch uses heappop which actually removes them.

## tricky situations

1. half empty cab - it still leaves (like 2/4). if nobody is waiting it doesnt leave and just shows a message.

2. no cabs left - student still gets added and gets a note that theres no cab right now. they never get removed, they just keep waiting.

3. same year - request_n breaks the tie, smaller = asked first. its always different so python never compares two RideRequest objects (that crashes).

4. 1000 students (n = students waiting, C = no of cabs)
   - add one: O(log n) because heappush
   - add 1000: O(n log n), its 1000 pushes
   - dispatch one cab: O(log n), max 4 heappops so basically log n
   - find open cab: O(C), loops over the cabs but there are only few

---

i have used a llm to make the readme file prettier
