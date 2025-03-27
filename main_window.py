import tkinter as tk
from tkinter import messagebox

# Створення головного вікна
root = tk.Tk()
root.title("Хрестики-Нулики")
root.resizable(False, False)

# Глобальні змінні
current_player = "X"
board = [""] * 9  # Ігрове поле


# Функція перевірки перемоги
def check_winner():
    # Всі можливі виграшні комбінації
    win_combinations = [
        (0, 1, 2), (3, 4, 5), (6, 7, 8),  # Горизонтальні
        (0, 3, 6), (1, 4, 7), (2, 5, 8),  # Вертикальні
        (0, 4, 8), (2, 4, 6)  # Діагональні
    ]

    for combo in win_combinations:
        a, b, c = combo
        if board[a] == board[b] == board[c] and board[a] != "":
            return board[a]  # Повертаємо переможця (X або O)

    if "" not in board:
        return "Нічия"  # Якщо всі клітинки заповнені і немає переможця

    return None  # Гра триває


# Функція обробки кліку по кнопці
def on_click(index):
    global current_player

    if board[index] == "":  # Якщо клітинка порожня
        board[index] = current_player
        buttons[index].config(text=current_player, state="disabled")

        winner = check_winner()
        if winner:
            if winner == "Нічия":
                messagebox.showinfo("Гра закінчена", "Нічия!")
            else:
                messagebox.showinfo("Гра закінчена", f"Гравець {winner} переміг!")
            reset_game()
        else:
            # Змінюємо гравця
            current_player = "O" if current_player == "X" else "X"


# Функція перезапуску гри
def reset_game():
    global current_player, board
    current_player = "X"
    board = [""] * 9
    for button in buttons:
        button.config(text="", state="normal")


# Створення кнопок для ігрового поля
buttons = []
def create_button(index):
    return tk.Button(root, text="", font=("Arial", 24), width=5, height=2, command=lambda: on_click(index))

buttons = []
for i in range(9):
    btn = create_button(i)  # Викликаємо функцію для створення кнопки
    btn.grid(row=i // 3, column=i % 3)
    buttons.append(btn)


# Додаємо кнопку для перезапуску гри
reset_button = tk.Button(root, text="Перезапустити гру", font=("Arial", 14),
                         command=reset_game)
reset_button.grid(row=3, column=0, columnspan=3, pady=10)

# Запуск головного циклу
root.mainloop()
