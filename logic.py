from tkinter import messagebox

# Глобальні змінні
current_player = "X"
board = [""] * 9  # Ігрове поле
buttons = []  # Масив кнопок (буде заповнено в interface.py)

# Функція перевірки переможця
def check_winner():
    win_combinations = [
        (0, 1, 2), (3, 4, 5), (6, 7, 8),  # Горизонтальні
        (0, 3, 6), (1, 4, 7), (2, 5, 8),  # Вертикальні
        (0, 4, 8), (2, 4, 6)  # Діагональні
    ]

    for a, b, c in win_combinations:
        if board[a] == board[b] == board[c] and board[a] != "":
            return board[a]  # Переможець (X або O)

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
