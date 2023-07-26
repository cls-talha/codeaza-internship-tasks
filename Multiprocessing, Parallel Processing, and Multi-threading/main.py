import threading
import time

class Search:
    def __init__(self, filepth: str) -> None:
        self.filepth = filepth
        self.data = []

        with open(filepth, 'r') as f:
            data = f.read().splitlines()
            self.data = [int(x) for x in data]

    def sort(self) -> None:
        self.data.sort()

    def binary_search(self, target: int, start: int, end: int) -> int:
        s = start
        e = end

        while s <= e:
            mid = s + (e - s) // 2
            if self.data[mid] == target:
                return mid
            elif self.data[mid] < target:
                s = mid + 1
            else:
                e = mid - 1
        return -1

if __name__ == "__main__":
    s = Search('data.txt')

    # Sorting in a separate thread
    sort_thread = threading.Thread(target=s.sort)
    sort_thread.start()

    # Binary search in the main thread
    start_time = time.time()
    result = s.binary_search(29996, 0, len(s.data) - 1)
    end_time = time.time()

    # Wait for the sorting thread to finish
    sort_thread.join()

    if result != -1:
        print("[INFO] Found at index:", result)
    else:
        print("[INFO] Element not found.")

    print("[INFO] Time taken:", end_time - start_time, "seconds")
