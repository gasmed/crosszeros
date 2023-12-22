import tkinter as tk
from tkinter import messagebox
import random
import math

class CrossZerosGUI:
    def __init__(self, root, field_size):
        self.root = root
        self.root.title("Крестики-Нолики")
        self.max_field_size = 20  # Максимальный размер поля
        self.game_mode = None
        self.game_session = None
        self.buttons = [[None for _ in range(field_size)] for _ in range(field_size)]
        self.create_mode_selection_widgets()
        self.root.resizable(width=False, height=False)  # Отключение изменения размеров окна


    def create_mode_selection_widgets(self):
        mode_label = tk.Label(self.root, text="Выберите режим игры:")
        mode_label.grid(row=0, column=0, columnspan=2)

        human_vs_human_button = tk.Button(self.root, text="Человек против человека", command=lambda: self.start_game("human_vs_human"))
        human_vs_human_button.grid(row=1, column=0, padx=5, pady=5)

        human_vs_computer_button = tk.Button(self.root, text="Человек против компьютера", command=lambda: self.start_game("human_vs_computer"))
        human_vs_computer_button.grid(row=1, column=1, padx=5, pady=5)

    def start_game(self, mode):
        for widget in self.root.winfo_children():
            widget.destroy()

        self.game_mode = mode
        self.game_session = CrossZeros(min(10, self.max_field_size), self, mode)
        self.create_game_widgets()

    def create_game_widgets(self):
        button_width = 3
        button_height = 3

        for i in range(self.game_session.field_size):
            for j in range(self.game_session.field_size):
                btn = tk.Button(self.root, text="", width=button_width, height=button_height,
                                command=lambda row=i, col=j: self.on_button_click(row, col))
                btn.grid(row=i, column=j)
                self.buttons[i][j] = btn

    def on_button_click(self, row, col):
        if self.game_session.winner is not None:
            return  # Игра завершена, клики не обрабатываются

        if self.game_session.field[row][col] is not None:
            return  # Клетка уже занята, клики не обрабатываются

        if self.game_mode == "human_vs_human":
            self.game_step(row, col)
        elif self.game_mode == "human_vs_computer":
            if self.game_session.step % 2 == 0:
                self.game_step(row, col)
                self.root.after(500, self.computer_move)

    def game_step(self, row, col):
        if not self.game_session.game_step(row, col):
            self.update_gui()

            if self.game_session.winner is not None:
                winner_symbol = "X" if self.game_session.winner == 1 else "O"
                self.root.after(500, lambda: self.show_winner_message(winner_symbol))
                self.disable_buttons()

    def update_gui(self):
        for i in range(self.game_session.field_size):
            for j in range(self.game_session.field_size):
                if i < len(self.buttons) and j < len(self.buttons[i]):
                    symbol = self.game_session.field[i][j]
                    text = "X" if symbol == 1 else "O" if symbol == 0 else ""
                    color = "red" if symbol == 1 else "black"  # Красный цвет для крестика, черный для нолика
                    self.buttons[i][j].config(text=text, fg=color)

    def show_winner_message(self, winner_symbol):
        messagebox.showinfo("Игра окончена", f"Игрок {winner_symbol} победил!")

    def disable_buttons(self):
        for i in range(self.game_session.field_size):
            for j in range(self.game_session.field_size):
                self.buttons[i][j].config(state=tk.DISABLED)

    def computer_move(self):
        if self.game_session.winner is not None:
            return

        computer_row, computer_col = self.game_session.computer_move()
        self.game_session.game_step(computer_row, computer_col)
        self.update_gui()

        if self.game_session.winner is not None:
            winner_symbol = "X" if self.game_session.winner == 1 else "O"
            self.root.after(500, lambda: self.show_winner_message(winner_symbol))
            self.disable_buttons()

class CrossZeros(object):
    def __init__(self, field_size, gui, mode):
        self.field = [[None for _ in range(field_size)] for _ in range(field_size)]
        self.field_size = field_size
        self.step = 0
        self.winner = None
        self.gui = gui
        self.mode = mode
        self.max_field_size = 14  # Максимальный размер поля

    def game_step(self, row, col):
        if self.winner is not None:
            return False  # Игра уже завершена, запрещены новые ходы

        if self.field[row][col] is not None:
            return False  # Ячейка уже занята, запрещены новые ходы

        self.step += 1

        if self.step % 2:
            self.cross(row, col)
        else:
            self.zero(row, col)

        self.gui.update_gui()

        if self.win_condition():
            return False  # Если есть победитель, запрещены новые ходы

    def field_expansion(self, row, col):
        expansion_condition = 3  # Количество ячеек до границы
        max_field_size = self.max_field_size

        bottom_distance = self.field_size - row - 1
        right_distance = self.field_size - col - 1
        upper_distance = row
        left_distance = col

        # Рассматриваем различные сценарии для расширения поля
        bottom_distance = min(bottom_distance, expansion_condition)
        right_distance = min(right_distance, expansion_condition)
        upper_distance = min(upper_distance, expansion_condition)
        left_distance = min(left_distance, expansion_condition)

        # Проверка, нужно ли расширять поле
        if self.field_size < max_field_size:
            # Увеличение размера поля в данных, но не больше максимального размера
            new_field_size = min(max_field_size, self.field_size + (
                    expansion_condition - min(bottom_distance, right_distance, upper_distance, left_distance)))
            new_field = [[None for _ in range(new_field_size)] for _ in range(new_field_size)]

            for i in range(self.field_size):
                for j in range(self.field_size):
                    new_i = i + (expansion_condition - upper_distance)
                    new_j = j + (expansion_condition - left_distance)
                    if 0 <= new_i < new_field_size and 0 <= new_j < new_field_size:
                        new_field[new_i][new_j] = self.field[i][j]

            self.field = new_field
            self.field_size = new_field_size

            # Увеличивание размера поля в GUI, но не больше максимального размера
            new_buttons = [[None for _ in range(new_field_size)] for _ in range(new_field_size)]
            for i in range(new_field_size):
                for j in range(new_field_size):
                    btn = tk.Button(self.gui.root, text="", width=3, height=3,
                                    command=lambda r=i, c=j: self.gui.on_button_click(r, c))
                    btn.grid(row=i, column=j)
                    new_buttons[i][j] = btn

            self.gui.buttons = new_buttons

            # Помещение символа в отрегулированную позицию
            row += (expansion_condition - upper_distance)
            col += (expansion_condition - left_distance)

            if self.step % 2:
                self.cross(row, col)
            else:
                self.zero(row, col)

    def cross(self, row, col):
        if all(0 <= i < self.field_size for i in [row, col]):
            if self.field[row][col] is None:
                # Установка символа в ячейку
                self.field[row][col] = 1
                # Расширение поля после установки символа
                self.field_expansion(row, col)
                return 1
        return 0

    def zero(self, row, col):
        if all(0 <= i < self.field_size for i in [row, col]):
            if self.field[row][col] is None:
                # Установка символа в ячейку
                self.field[row][col] = 0
                # Расширение поля после установки символа
                self.field_expansion(row, col)
                return 1
        return 0

    def win_condition(self):
        for i in range(self.field_size):
            for j in range(self.field_size):
                horizontal = self.field[i][j:j + 5] if j + 5 <= self.field_size else []
                vertical = [self.field[i + k][j] for k in range(5)] if i + 5 <= self.field_size else []
                diagonal_right = [self.field[i + k][j + k] for k in range(5)] \
                    if i + 5 <= self.field_size and j + 5 <= self.field_size else []
                diagonal_left = [self.field[i - k][j - k] for k in range(5)] \
                    if i - 5 >= 0 and j - 5 >= 0 else []
                if any(row == [self.step % 2] * 5 for row in [horizontal, vertical, diagonal_left, diagonal_right]):
                    self.winner = self.step % 2
                    return True
        return False

    def computer_move(self):
        available_moves = [(i, j) for i in range(self.field_size) for j in range(self.field_size) if
                           self.field[i][j] is None]
        if available_moves:
            # Поиск последней занятей клетки
            last_move = None
            for i in range(self.field_size):
                for j in range(self.field_size):
                    if self.field[i][j] is not None:
                        last_move = (i, j)

            # Определение радиуса для выбора следующей клетки
            radius = 2  # Радиус равен 2

            # Фильтруются доступные клетки в пределах радиуса от последней занятой клетки
            valid_moves = [(i, j) for i, j in available_moves if
                           math.sqrt((i - last_move[0]) ** 2 + (j - last_move[1]) ** 2) <= radius]

            # Выбор следующей случайной клетки из валидных ходов
            if valid_moves:
                computer_row, computer_col = random.choice(valid_moves)
                return computer_row, computer_col

        return random.choice(available_moves)


if __name__ == "__main__":
    root = tk.Tk()
    game_gui = CrossZerosGUI(root, 10)
    root.mainloop()