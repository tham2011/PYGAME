import tkinter as tk
from tkinter import messagebox

# Một bảng Sudoku ví dụ (0 là ô trống)
board = [
    [5, 3, 0, 0, 7, 0, 0, 0, 0],
    [6, 0, 0, 1, 9, 5, 0, 0, 0],
    [0, 9, 8, 0, 0, 0, 0, 6, 0],
    [8, 0, 0, 0, 6, 0, 0, 0, 3],
    [4, 0, 0, 8, 0, 3, 0, 0, 1],
    [7, 0, 0, 0, 2, 0, 0, 0, 6],
    [0, 6, 0, 0, 0, 0, 2, 8, 0],
    [0, 0, 0, 4, 1, 9, 0, 0, 5],
    [0, 0, 0, 0, 8, 0, 0, 7, 9]
]

# Hàm kiểm tra lời giải có hợp lệ hay không
def is_valid_solution(board):
    for row in range(9):
        seen = set()
        for col in range(9):
            value = board[row][col]
            if value != 0 and value in seen:
                return False
            seen.add(value)

    for col in range(9):
        seen = set()
        for row in range(9):
            value = board[row][col]
            if value != 0 and value in seen:
                return False
            seen.add(value)

    for box_row in range(0, 9, 3):
        for box_col in range(0, 9, 3):
            seen = set()
            for r in range(3):
                for c in range(3):
                    value = board[box_row + r][box_col + c]
                    if value != 0 and value in seen:
                        return False
                    seen.add(value)

    return True

# Hàm lấy giá trị từ các ô nhập và cập nhật bảng
def update_board():
    for row in range(9):
        for col in range(9):
            entry = entries[row][col]
            if entry is not None:  # Kiểm tra nếu entry hợp lệ
                value = entry.get()
                board[row][col] = int(value) if value.isdigit() else 0

# Hàm kiểm tra lời giải khi nhấn nút "Kiểm tra"
def check_solution():
    update_board()
    if is_valid_solution(board):
        messagebox.showinfo("Kết quả", "Chúc mừng! Lời giải đúng!")
    else:
        messagebox.showerror("Kết quả", "Lời giải sai. Vui lòng thử lại.")

# Tạo cửa sổ chính
root = tk.Tk()
root.title("Sudoku")

# Tạo lưới các ô nhập
entries = []

for row in range(9):
    row_entries = []
    for col in range(9):
        entry = tk.Entry(root, width=2, font=('Arial', 18), justify='center')
        entry.grid(row=row, column=col)
        if board[row][col] != 0:
            entry.insert(0, str(board[row][col]))
            entry.config(state='disabled')  # Khóa các ô đã có sẵn
        row_entries.append(entry)  # Lưu từng dòng vào mảng phụ
    entries.append(row_entries)  # Thêm mảng phụ vào mảng chính

# Nút "Kiểm tra"
check_button = tk.Button(root, text="Kiểm tra", command=check_solution)
check_button.grid(row=9, columnspan=9)

root.mainloop()