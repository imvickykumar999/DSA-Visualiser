import tkinter as tk
import random

class SortingVisualizer:
    def __init__(self, root):
        self.root = root
        self.root.title("Sorting Algorithm Visualizer")

        self.canvas = tk.Canvas(root, width=800, height=400, bg="white")
        self.canvas.grid(row=0, column=0, columnspan=3, padx=10, pady=5)

        self.btn_next = tk.Button(root, text="Next", command=self.next_step)
        self.btn_next.grid(row=1, column=2, padx=10, pady=5)

        self.btn_previous = tk.Button(root, text="Previous", command=self.previous_step)
        self.btn_previous.grid(row=1, column=0, padx=10, pady=5)

        self.btn_reset = tk.Button(root, text="Reset", command=self.reset)
        self.btn_reset.grid(row=1, column=1, padx=10, pady=5)

        self.algorithm_var = tk.StringVar(value="Bubble Sort")
        self.dropdown = tk.OptionMenu(root, self.algorithm_var, "Bubble Sort", "Selection Sort", "Insertion Sort", "Merge Sort", "Quick Sort", "Heap Sort", command=self.algorithm_changed)
        self.dropdown.grid(row=2, column=1, padx=10, pady=5)

        self.data = [random.randint(1, 100) for _ in range(10)]
        self.steps = []
        self.current_step = 0

        self.generate_steps()
        self.draw_bars(self.data)

    def algorithm_changed(self, *args):
        self.reset()

    def generate_steps(self):
        algorithm = self.algorithm_var.get()
        self.steps = []
        if algorithm == "Bubble Sort":
            self.bubble_sort(self.data[:])
        elif algorithm == "Selection Sort":
            self.selection_sort(self.data[:])
        elif algorithm == "Insertion Sort":
            self.insertion_sort(self.data[:])
        elif algorithm == "Merge Sort":
            self.merge_sort(self.data[:])
        elif algorithm == "Quick Sort":
            self.quick_sort(self.data[:])
        elif algorithm == "Heap Sort":
            self.heap_sort(self.data[:])

    def draw_bars(self, data, highlight_indices=()):
        self.canvas.delete("all")
        c_height = 400
        c_width = 800
        bar_width = c_width / (len(data) + 1)
        offset = 30
        spacing = 10
        normalized_data = [i / max(data) for i in data]
        for i, height in enumerate(normalized_data):
            x0 = i * bar_width + offset + spacing
            y0 = c_height - height * 300
            x1 = (i + 1) * bar_width + offset
            y1 = c_height
            color = "red" if i in highlight_indices else "blue"
            self.canvas.create_rectangle(x0, y0, x1, y1, fill=color)
            self.canvas.create_text(x0 + 2, y0, anchor=tk.SW, text=str(data[i]))
        self.canvas.update_idletasks()

    def next_step(self):
        if self.current_step < len(self.steps) - 1:
            self.current_step += 1
            data, i, j = self.steps[self.current_step]
            self.draw_bars(data, highlight_indices=(i, j))

    def previous_step(self):
        if self.current_step > 0:
            self.current_step -= 1
            data, i, j = self.steps[self.current_step]
            self.draw_bars(data, highlight_indices=(i, j))

    def reset(self):
        self.data = [random.randint(1, 100) for _ in range(10)]
        self.current_step = 0
        self.generate_steps()
        self.draw_bars(self.data)

    def bubble_sort(self, data):
        n = len(data)
        for i in range(n):
            for j in range(0, n-i-1):
                self.steps.append((data[:], j, j+1))
                if data[j] > data[j+1]:
                    data[j], data[j+1] = data[j+1], data[j]
                    self.steps.append((data[:], j, j+1))
        self.steps.append((data[:], -1, -1))

    def selection_sort(self, data):
        n = len(data)
        for i in range(n):
            min_idx = i
            for j in range(i+1, n):
                self.steps.append((data[:], min_idx, j))
                if data[j] < data[min_idx]:
                    min_idx = j
                    self.steps.append((data[:], i, min_idx))
            data[i], data[min_idx] = data[min_idx], data[i]
            self.steps.append((data[:], i, min_idx))
        self.steps.append((data[:], -1, -1))

    def insertion_sort(self, data):
        for i in range(1, len(data)):
            key = data[i]
            j = i-1
            while j >= 0 and key < data[j]:
                data[j+1] = data[j]
                j -= 1
                self.steps.append((data[:], j+1, j))
            data[j+1] = key
            self.steps.append((data[:], j+1, i))
        self.steps.append((data[:], -1, -1))

    def merge_sort(self, data):
        self._merge_sort(data, 0, len(data)-1)

    def _merge_sort(self, data, left, right):
        if left < right:
            mid = (left + right) // 2
            self._merge_sort(data, left, mid)
            self._merge_sort(data, mid+1, right)
            self._merge(data, left, mid, right)

    def _merge(self, data, left, mid, right):
        L = data[left:mid+1]
        R = data[mid+1:right+1]
        i = j = 0
        k = left
        while i < len(L) and j < len(R):
            if L[i] < R[j]:
                data[k] = L[i]
                i += 1
            else:
                data[k] = R[j]
                j += 1
            self.steps.append((data[:], left + i, mid + 1 + j))
            k += 1
        while i < len(L):
            data[k] = L[i]
            i += 1
            k += 1
            self.steps.append((data[:], left + i, mid + 1 + j))
        while j < len(R):
            data[k] = R[j]
            j += 1
            k += 1
            self.steps.append((data[:], left + i, mid + 1 + j))
        self.steps.append((data[:], -1, -1))

    def quick_sort(self, data):
        self._quick_sort(data, 0, len(data) - 1)

    def _quick_sort(self, data, low, high):
        if low < high:
            pi = self._partition(data, low, high)
            self._quick_sort(data, low, pi-1)
            self._quick_sort(data, pi+1, high)

    def _partition(self, data, low, high):
        pivot = data[high]
        i = low - 1
        for j in range(low, high):
            self.steps.append((data[:], j, high))
            if data[j] < pivot:
                i = i + 1
                data[i], data[j] = data[j], data[i]
                self.steps.append((data[:], i, j))
        data[i + 1], data[high] = data[high], data[i + 1]
        self.steps.append((data[:], i + 1, high))
        return i + 1

    def heap_sort(self, data):
        n = len(data)
        for i in range(n // 2 - 1, -1, -1):
            self._heapify(data, n, i)
        for i in range(n-1, 0, -1):
            data[i], data[0] = data[0], data[i]
            self.steps.append((data[:], i, 0))
            self._heapify(data, i, 0)
        self.steps.append((data[:], -1, -1))

    def _heapify(self, data, n, i):
        largest = i
        l = 2 * i + 1
        r = 2 * i + 2
        if l < n and data[l] > data[largest]:
            largest = l
        if r < n and data[r] > data[largest]:
            largest = r
        if largest != i:
            data[i], data[largest] = data[largest], data[i]
            self.steps.append((data[:], i, largest))
            self._heapify(data, n, largest)

if __name__ == "__main__":
    root = tk.Tk()
    app = SortingVisualizer(root)
    root.mainloop()
