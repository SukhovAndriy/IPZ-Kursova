import tkinter as tk
from logic import *

# Створення головного вікна
root = tk.Tk()
root.title("Хрестики-Нулики")
root.resizable(False, False)

# Функція для створення кнопки
def create_button(index):
    return tk.Button(root, text="", font=("Arial", 24), width=5, height=2, command=lambda: on_click(index))

# Створення кнопок ігрового поля
for i in range(9):
    btn = create_button(i)
    btn.grid(row=i // 3, column=i % 3)
    buttons.append(btn)  # Додаємо кнопку у список

# Додаємо кнопку перезапуску
reset_button = tk.Button(root, text="Перезапустити гру", font=("Arial", 14), command=reset_game)
reset_button.grid(row=3, column=0, columnspan=3, pady=10)

# Запуск головного циклу
root.mainloop()
