import tkinter as tk
from tkinter import messagebox
import random

class MathsQuiz:
    def __init__(self, root):
        self.root = root
        self.root.title("Maths Quiz")

        # Initialize variables
        self.score = 0
        self.current_question = 1
        self.difficulty = None
        self.num1 = 0
        self.num2 = 0
        self.operation = ''
        self.correct_answer = 0
        self.attempt = 0

        # Create GUI layout
        self.create_widgets()

    def create_widgets(self):
        # Difficulty selection
        self.label = tk.Label(self.root, text="Choose Difficulty Level", font=("Arial", 14))
        self.label.pack(pady=10)

        self.easy_btn = tk.Button(self.root, text="Easy", command=lambda: self.start_quiz(1))
        self.easy_btn.pack(pady=5)
        
        self.moderate_btn = tk.Button(self.root, text="Moderate", command=lambda: self.start_quiz(2))
        self.moderate_btn.pack(pady=5)

        self.advanced_btn = tk.Button(self.root, text="Advanced", command=lambda: self.start_quiz(3))
        self.advanced_btn.pack(pady=5)

        # Question display
        self.question_label = tk.Label(self.root, text="", font=("Arial", 14))
        self.question_label.pack(pady=20)

        # Answer entry
        self.answer_entry = tk.Entry(self.root, font=("Arial", 14))
        self.answer_entry.pack()
        self.answer_entry.bind("<Return>", lambda event: self.check_answer())

        # Feedback
        self.feedback_label = tk.Label(self.root, text="", font=("Arial", 12))
        self.feedback_label.pack(pady=10)

        # Next question button
        self.next_btn = tk.Button(self.root, text="Next Question", command=self.next_question)
        self.next_btn.pack(pady=10)

        # Final score display
        self.final_score_label = tk.Label(self.root, text="", font=("Arial", 14))
        self.final_score_label.pack(pady=20)

    def start_quiz(self, difficulty):
        # Initialize variables for new quiz
        self.score = 0
        self.current_question = 1
        self.difficulty = difficulty
        self.next_question()

    def next_question(self):
        if self.current_question > 10:
            self.show_results()
            return

        # Reset attempts
        self.attempt = 0

        # Generate question
        self.num1 = self.random_int()
        self.num2 = self.random_int()
        self.operation = self.decide_operation()
        self.correct_answer = self.num1 + self.num2 if self.operation == '+' else self.num1 - self.num2

        # Update question label
        self.question_label.config(text=f"Question {self.current_question}: {self.num1} {self.operation} {self.num2} = ")
        self.answer_entry.delete(0, tk.END)
        self.feedback_label.config(text="")

    def check_answer(self):
        try:
            user_answer = int(self.answer_entry.get())
            if user_answer == self.correct_answer:
                points = 10 if self.attempt == 0 else 5
                self.score += points
                self.feedback_label.config(text="Correct!" if self.attempt == 0 else "Correct on second attempt!")
                self.current_question += 1
            else:
                self.attempt += 1
                if self.attempt < 2:
                    self.feedback_label.config(text="Incorrect. Try again.")
                else:
                    self.feedback_label.config(text=f"Incorrect. The correct answer was {self.correct_answer}.")
                    self.current_question += 1
            self.answer_entry.delete(0, tk.END)
        except ValueError:
            self.feedback_label.config(text="Please enter a valid number.")

    def show_results(self):
        self.final_score_label.config(text=f"Your final score is {self.score} out of 100.")
        grade = self.get_grade(self.score)
        messagebox.showinfo("Quiz Complete", f"Your grade is {grade}.")
        self.reset_quiz()

    def reset_quiz(self):
        # Reset GUI to start screen
        self.label.config(text="Choose Difficulty Level")
        self.question_label.config(text="")
        self.feedback_label.config(text="")
        self.final_score_label.config(text="")
        self.answer_entry.delete(0, tk.END)
        self.current_question = 1
        self.score = 0

    def random_int(self):
        if self.difficulty == 1:
            return random.randint(1, 9)  # Easy
        elif self.difficulty == 2:
            return random.randint(10, 99)  # Moderate
        elif self.difficulty == 3:
            return random.randint(1000, 9999)  # Advanced

    def decide_operation(self):
        return random.choice(['+', '-'])

    def get_grade(self, score):
        if score > 90:
            return "A+"
        elif score > 80:
            return "A"
        elif score > 70:
            return "B"
        elif score > 60:
            return "C"
        else:
            return "D"

# Main loop
root = tk.Tk()
app = MathsQuiz(root)
root.mainloop()
