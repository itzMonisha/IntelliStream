# import time

# events = list(range(30))

# start = time.time()

# for event in events:

#     time.sleep(1)

# end = time.time()

# print(
#     f"Single Thread Time: {round(end-start, 2)} sec"
# )
# import time
# from concurrent.futures import ThreadPoolExecutor

# events = list(range(30))


# def process(event):

#     time.sleep(1)


# start = time.time()

# with ThreadPoolExecutor(
#     max_workers=3
# ) as executor:

#     executor.map(
#         process,
#         events
#     )

# end = time.time()

# print(
#     f"Multi Thread Time: {round(end-start, 2)} sec"
# )
single = 30
multi = 10

improvement = (
    (single - multi)
    / single
) * 100

print(
    f"Improvement: {improvement}%"
)
