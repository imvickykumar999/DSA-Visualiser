import tkinter as tk
import random

class BubbleSortVisualizer:
    def __init__(self, root):
        self.root = root
        self.root.title("Bubble Sort Visualization")

        self.canvas = tk.Canvas(root, width=600, height=400, bg="white")
        self.canvas.grid(row=0, column=0, columnspan=2, padx=10, pady=5)

        self.btn_next = tk.Button(root, text="Next", command=self.next_step)
        self.btn_next.grid(row=1, column=1, padx=10, pady=5)

        self.btn_previous = tk.Button(root, text="Previous", command=self.previous_step)
        self.btn_previous.grid(row=1, column=0, padx=10, pady=5)

        self.data = [random.randint(1, 100) for _ in range(10)]
        self.steps = []
        self.current_step = 0

        self.generate_steps()
        self.draw_bars(self.data)

    def generate_steps(self):
        data = self.data[:]
        n = len(data)
        for i in range(n):
            for j in range(0, n - i - 1):
                self.steps.append((data[:], j, j+1))
                if data[j] > data[j + 1]:
                    data[j], data[j + 1] = data[j + 1], data[j]
                    self.steps.append((data[:], j, j+1))
        self.steps.append((data[:], -1, -1))  # Final state

    def draw_bars(self, data, highlight_indices=()):
        self.canvas.delete("all")
        c_height = 400
        c_width = 600
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

if __name__ == "__main__":
    root = tk.Tk()
    app = BubbleSortVisualizer(root)
    root.mainloop()
