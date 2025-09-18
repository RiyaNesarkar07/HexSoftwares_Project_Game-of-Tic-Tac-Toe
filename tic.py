import customtkinter as ctk
import random

ctk.set_appearance_mode("System")  # Options: "Light", "Dark", "System"
ctk.set_default_color_theme("blue")  # Options: "blue", "green", "dark-blue"

class TicTacToeApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Tic-Tac-Toe")
        self.geometry("400x500")
        self.resizable(False, False)
        self.board = [' '] * 9
        self.user = '❌'
        self.comp = '⭕'
        self.buttons = []
        self.create_widgets()

    def create_widgets(self):
        self.label = ctk.CTkLabel(self, text="Your Turn", font=("Helvetica", 20))
        self.label.pack(pady=20)

        self.frame = ctk.CTkFrame(self)
        self.frame.pack()

        for i in range(9):
            btn = ctk.CTkButton(self.frame, text=' ', width=100, height=100, font=("Helvetica", 32),
                                corner_radius=10, command=lambda i=i: self.user_move(i))
            btn.grid(row=i//3, column=i%3, padx=5, pady=5)
            self.buttons.append(btn)

        self.restart_btn = ctk.CTkButton(self, text="Restart", command=self.restart, width=120)
        self.restart_btn.pack(pady=20)

    def user_move(self, index):
        if self.board[index] == ' ':
            self.board[index] = self.user
            self.buttons[index].configure(text=self.user, text_color="red", state="disabled")
            if self.check_winner(self.user):
                self.highlight_winner(self.user)
                self.end_game("You win!")
            elif ' ' not in self.board:
                self.end_game("It's a draw!")
            else:
                self.label.configure(text="Computer's Turn")
                self.after(500, self.computer_move)

    def computer_move(self):
        move = random.choice([i for i in range(9) if self.board[i] == ' '])
        self.board[move] = self.comp
        self.buttons[move].configure(text=self.comp, text_color="blue", state="disabled")
        if self.check_winner(self.comp):
            self.highlight_winner(self.comp)
            self.end_game("Computer wins!")
        elif ' ' not in self.board:
            self.end_game("It's a draw!")
        else:
            self.label.configure(text="Your Turn")

    def check_winner(self, mark):
        combos = [(0,1,2),(3,4,5),(6,7,8),
                  (0,3,6),(1,4,7),(2,5,8),
                  (0,4,8),(2,4,6)]
        return any(self.board[a]==self.board[b]==self.board[c]==mark for a,b,c in combos)

    def highlight_winner(self, mark):
        combos = [(0,1,2),(3,4,5),(6,7,8),
                  (0,3,6),(1,4,7),(2,5,8),
                  (0,4,8),(2,4,6)]
        for a, b, c in combos:
            if self.board[a] == self.board[b] == self.board[c] == mark:
                for i in (a, b, c):
                    self.buttons[i].configure(fg_color="#32CD32")  # Lime green
                break

    def end_game(self, result):
        for btn in self.buttons:
            btn.configure(state="disabled")
        self.label.configure(text=result)

        popup = ctk.CTkToplevel(self)
        popup.geometry("300x200")
        popup.title("🎉 Game Over")
        popup.grab_set()

        emoji = "🏆" if "win" in result.lower() else "🤖" if "computer" in result.lower() else "😐"

        result_label = ctk.CTkLabel(popup, text=f"{emoji} {result}", font=("Helvetica", 20))
        result_label.pack(pady=30)

        play_again_btn = ctk.CTkButton(popup, text="Play Again", command=lambda: [popup.destroy(), self.restart()])
        play_again_btn.pack(pady=10)

        exit_btn = ctk.CTkButton(popup, text="Exit", command=self.destroy)
        exit_btn.pack(pady=5)

    def restart(self):
        self.board = [' '] * 9
        for btn in self.buttons:
            btn.configure(text=' ', state="normal", fg_color="transparent")
        self.label.configure(text="Your Turn")

if __name__ == "__main__":
    app = TicTacToeApp()
    app.mainloop()
