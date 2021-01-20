from tkinter import *
from tkinter import ttk
from random import shuffle


NUMBER_COLOR = "gray"
NUMBER_COLOR2 = "red"
NUMBER_COLOR3 = "blue"
options = ["50 elements", "100 elements", "200 elements", "350 elements", "500 elements", "1000 elements", "2000 elements"]

# Deletes a frame and loads the next one
def delete_frame(frame, func):
    frame.destroy()
    func()


# Displays sort menu
def sort_menu():
    menu_frame = Frame(root, bg="black")
    menu_frame.place(relwidth=1, relheight=1)

    quicksort = Button(menu_frame, text="Quick Sort", command=lambda: delete_frame(menu_frame, quick_sort))
    quicksort.place(rely=.2, relx=0.3, relwidth=.4, relheight=.1)

    mergesort = Button(menu_frame, text="Merge Sort", command=lambda: delete_frame(menu_frame, merge_sort))
    mergesort.place(rely=.35, relx=0.3, relwidth=.4, relheight=.1)

    selectionsort = Button(menu_frame, text="Selection Sort", command=lambda: delete_frame(menu_frame, selection_sort))
    selectionsort.place(rely=.5, relx=0.3, relwidth=.4, relheight=.1)

    insertionsort = Button(menu_frame, text="Insertion Sort", command=lambda: delete_frame(menu_frame, insertion_sort))
    insertionsort.place(rely=.65, relx=0.3, relwidth=.4, relheight=.1)

# Reset the counter to 0 and modifies the label
def reset_counter():
    global count
    count = 0
    swap_label.config(text=f"Operations: {count}")

# Increments the counter by one and modifies the label
def add_counter():
    global count
    count += 1
    swap_label.config(text=f"Operations: {count}")

# Initializes a sorting frame with labels and buttons
def initialize_sort_frame(sortname):
    global count
    count = 0

    container_frame = Frame(root, bg="yellow")
    container_frame.place(relwidth=1, relheight=1)

    sort_frame = Frame(container_frame, bg="orange")
    sort_frame.place(relwidth=1, relheight=.1)

    global play_button
    play_button = Button(sort_frame, text="►")
    play_button.place(rely=.1, relx=.025, relwidth=.075, relheight=.8)

    sort_label = Label(sort_frame, text=sortname, font=("Sans-serif", 20), bg="orange", fg="black")
    sort_label.place(rely=.1, relx=0.1, relwidth=.3, relheight=.8)

    global swap_label
    swap_label = Label(sort_frame, text="Operations: 0", font=("Sans-serif", 14), bg="orange", fg="black")
    swap_label.place(rely=.1, relx=0.35, relwidth=.3, relheight=.8)

    global menu_option
    menu_option = ttk.Combobox(sort_frame, values=options, state="readonly")
    menu_option.set(options[0])
    menu_option.place(rely=.2, relx=0.65, relwidth=.2, relheight=.6)

    back_button = Button(sort_frame, text="←", command=lambda: delete_frame(container_frame, sort_menu))
    back_button.place(rely=.1, relx=.9, relwidth=.075, relheight=.8)

    return container_frame

# Get the selected number of elements
def get_number_elements():
    return int(menu_option.get().split()[0])


# Creates the selected number of elements and places them
def create_numbers(frame):
    global numbers
    global widths
    n = get_number_elements()
    numbers = [Frame(frame, bg=NUMBER_COLOR) for i in range(n)]
    width = 1/n
    heights = [(i+1) * width for i in range(n)]
    widths = [i * width for i in range(n)]
    shuffle(heights)

    for i, n in enumerate(numbers):
        n.place(relwidth=width, relheight=heights[i], relx=widths[i], rely=1-heights[i])


# On change number of elements, reset counter, delete all current elements and create new ones
def change_element(frame):
    reset_counter()
    for widget in frame.winfo_children():
        widget.destroy()

    create_numbers(frame)

# Swap two elements and their frames
def swap(i1, i2, frame):
    global numbers

    numbers[i1].place_configure(relx=widths[i2])
    numbers[i2].place_configure(relx=widths[i1])
    frame.update()

    numbers[i1], numbers[i2] = numbers[i2], numbers[i1]

# Change the color of an element
def change_color(color, frame):
    frame.config(bg=color)


def quick_sort_algorithm(left, right, frame):

    add_counter()
    if left < right:
        pivot = left
        change_color(NUMBER_COLOR3, numbers[pivot])

        i = left
        j = right

        while i < j:
            while numbers[pivot].winfo_y() <= numbers[i].winfo_y() and i < j:
                add_counter()
                change_color(NUMBER_COLOR, numbers[i])
                i += 1
                change_color(NUMBER_COLOR3, numbers[i])

            while numbers[pivot].winfo_y() > numbers[j].winfo_y():
                add_counter()
                change_color(NUMBER_COLOR, numbers[j])
                j -= 1
                change_color(NUMBER_COLOR2, numbers[j])

            if i < j:
                swap(i, j, frame)

        swap(pivot, j, frame)

        change_color(NUMBER_COLOR, numbers[pivot])
        change_color(NUMBER_COLOR, numbers[i])
        change_color(NUMBER_COLOR, numbers[j])

        quick_sort_algorithm(left, j-1, frame)
        quick_sort_algorithm(j+1, right, frame)


# Quick sort frame menu
def quick_sort():
    sort_frame = initialize_sort_frame("Quick Sort")
    number_frame = Frame(sort_frame, bg="black")
    number_frame.place(relwidth=1, relheight=.9, rely=.1)
    menu_option.bind("<<ComboboxSelected>>", lambda x: change_element(number_frame))
    create_numbers(number_frame)
    play_button.configure(command=lambda: quick_sort_algorithm(0, get_number_elements()-1, number_frame))


def merge(start, mid, end, frame):
    L = numbers[start:mid]
    R = numbers[mid:end]

    i = 0
    j = 0
    k = start

    for l in range(k, end):
        add_counter()
        if j >= len(R) or (i < len(L) and L[i].winfo_y() >= R[j].winfo_y()):
            change_color(NUMBER_COLOR2, L[i])
            numbers[l] = L[i]
            change_color(NUMBER_COLOR, L[i])
            change_color(NUMBER_COLOR2, numbers[l])
            numbers[l].place_configure(relx=widths[l])
            frame.update()
            change_color(NUMBER_COLOR, numbers[l])
            i += 1
        else:
            change_color(NUMBER_COLOR2, R[j])
            numbers[l] = R[j]
            change_color(NUMBER_COLOR, R[j])
            change_color(NUMBER_COLOR2, numbers[l])
            numbers[l].place_configure(relx=widths[l])
            frame.update()
            change_color(NUMBER_COLOR, numbers[l])
            j += 1


def merge_sort_algorithm(left, right, frame):
    add_counter()
    if right - left > 1:
        middle = int((left + right) / 2)

        merge_sort_algorithm(left, middle, frame)
        merge_sort_algorithm(middle, right, frame)
        merge(left, middle, right, frame)


# Merge sort menu
def merge_sort():
    sort_frame = initialize_sort_frame("Merge Sort")
    number_frame = Frame(sort_frame, bg="black")
    number_frame.place(relwidth=1, relheight=.9, rely=.1)
    menu_option.bind("<<ComboboxSelected>>", lambda x: change_element(number_frame))
    create_numbers(number_frame)
    play_button.configure(command=lambda: merge_sort_algorithm(0, get_number_elements(), number_frame))


def selection_sort_algorithm(frame):
    for i in range(len(numbers)):
        min_i = i
        add_counter()
        for j in range(i+1, len(numbers)):
            add_counter()
            add_counter()
            if numbers[min_i].winfo_y() < numbers[j].winfo_y():
                add_counter()
                change_color(NUMBER_COLOR, numbers[min_i])
                min_i = j
                change_color(NUMBER_COLOR2, numbers[min_i])
        add_counter()
        swap(i, min_i, frame)
        change_color(NUMBER_COLOR, numbers[i])


# Selection sort menu
def selection_sort():
    sort_frame = initialize_sort_frame("Selection Sort")
    number_frame = Frame(sort_frame, bg="black")
    number_frame.place(relwidth=1, relheight=.9, rely=.1)
    menu_option.bind("<<ComboboxSelected>>", lambda x: change_element(number_frame))
    create_numbers(number_frame)
    play_button.configure(command=lambda: selection_sort_algorithm(number_frame))


def insertion_sort_algorithm(frame):
    for i in range(1, len(numbers)):
        j = i
        while j and numbers[j-1].winfo_y() <= numbers[j].winfo_y():
            add_counter()
            change_color(NUMBER_COLOR2, numbers[j])
            add_counter()
            swap(j-1, j, frame)
            add_counter()
            change_color(NUMBER_COLOR, numbers[j])
            add_counter()
            j -= 1
        change_color(NUMBER_COLOR, numbers[j])

# Insertion sort menu
def insertion_sort():
    sort_frame = initialize_sort_frame("Insertion Sort")
    number_frame = Frame(sort_frame, bg="black")
    number_frame.place(relwidth=1, relheight=.9, rely=.1)
    menu_option.bind("<<ComboboxSelected>>", lambda x: change_element(number_frame))
    create_numbers(number_frame)
    play_button.configure(command=lambda: insertion_sort_algorithm(number_frame))


# Creating main window
width = 900
height = 800

root = Tk()
root.geometry(f"{width}x{height}")
root.title("Sort Visualizer")

sort_menu()

root.mainloop()
