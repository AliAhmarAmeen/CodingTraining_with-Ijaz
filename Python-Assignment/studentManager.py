import tkinter as tk
from tkinter import messagebox

# Helper functions to process student data
def load_student_data(filename="studentMarks.txt"):
    students = []
    try:
        with open(filename, "r") as file:
            lines = file.readlines()
            num_students = int(lines[0].strip())
            for line in lines[1:]:
                student_data = line.strip().split(",")
                student_code = int(student_data[0])
                student_name = student_data[1]
                marks = list(map(int, student_data[2:5]))
                exam_mark = int(student_data[5])
                total_coursework = sum(marks)
                total_score = total_coursework + exam_mark
                percentage = (total_score / 160) * 100
                grade = calculate_grade(percentage)
                students.append({
                    "code": student_code,
                    "name": student_name,
                    "coursework": total_coursework,
                    "exam": exam_mark,
                    "percentage": percentage,
                    "grade": grade,
                    "total": total_score
                })
    except FileNotFoundError:
        messagebox.showerror("File Not Found", f"File '{filename}' not found.")
    return students

def calculate_grade(percentage):
    if percentage >= 70:
        return 'A'
    elif percentage >= 60:
        return 'B'
    elif percentage >= 50:
        return 'C'
    elif percentage >= 40:
        return 'D'
    else:
        return 'F'

def view_all_records():
    display_text = ""
    for student in students:
        display_text += f"Name: {student['name']}\n" \
                        f"Code: {student['code']}\n" \
                        f"Coursework: {student['coursework']}\n" \
                        f"Exam Mark: {student['exam']}\n" \
                        f"Percentage: {student['percentage']:.2f}%\n" \
                        f"Grade: {student['grade']}\n\n"
    average_percentage = sum(student['percentage'] for student in students) / len(students)
    display_text += f"Total Students: {len(students)}\n" \
                    f"Average Percentage: {average_percentage:.2f}%"
    display_area.config(state=tk.NORMAL)
    display_area.delete("1.0", tk.END)
    display_area.insert(tk.END, display_text)
    display_area.config(state=tk.DISABLED)

def view_individual_record():
    student_name = name_entry.get().strip()
    student = next((s for s in students if s['name'].lower() == student_name.lower()), None)
    if student:
        display_text = f"Name: {student['name']}\n" \
                       f"Code: {student['code']}\n" \
                       f"Coursework: {student['coursework']}\n" \
                       f"Exam Mark: {student['exam']}\n" \
                       f"Percentage: {student['percentage']:.2f}%\n" \
                       f"Grade: {student['grade']}"
        display_area.config(state=tk.NORMAL)
        display_area.delete("1.0", tk.END)
        display_area.insert(tk.END, display_text)
        display_area.config(state=tk.DISABLED)
    else:
        messagebox.showinfo("Student Not Found", f"No record found for '{student_name}'.")

def show_highest_score():
    if students:
        highest_student = max(students, key=lambda s: s['total'])
        display_student(highest_student)
    else:
        messagebox.showinfo("No Records", "No student records available.")

def show_lowest_score():
    if students:
        lowest_student = min(students, key=lambda s: s['total'])
        display_student(lowest_student)
    else:
        messagebox.showinfo("No Records", "No student records available.")

def display_student(student):
    display_text = f"Name: {student['name']}\n" \
                   f"Code: {student['code']}\n" \
                   f"Coursework: {student['coursework']}\n" \
                   f"Exam Mark: {student['exam']}\n" \
                   f"Percentage: {student['percentage']:.2f}%\n" \
                   f"Grade: {student['grade']}"
    display_area.config(state=tk.NORMAL)
    display_area.delete("1.0", tk.END)
    display_area.insert(tk.END, display_text)
    display_area.config(state=tk.DISABLED)

# Initialize students list from file
students = load_student_data()

# Tkinter GUI setup
root = tk.Tk()
root.title("Student Manager")

# GUI Components
frame = tk.Frame(root)
frame.pack(pady=20)

view_all_button = tk.Button(frame, text="View All Records", command=view_all_records)
view_all_button.grid(row=0, column=0, padx=5, pady=5)

view_individual_button = tk.Button(frame, text="View Individual Record", command=view_individual_record)
view_individual_button.grid(row=0, column=1, padx=5, pady=5)

highest_score_button = tk.Button(frame, text="Show Highest Score", command=show_highest_score)
highest_score_button.grid(row=1, column=0, padx=5, pady=5)

lowest_score_button = tk.Button(frame, text="Show Lowest Score", command=show_lowest_score)
lowest_score_button.grid(row=1, column=1, padx=5, pady=5)

name_label = tk.Label(frame, text="Student Name:")
name_label.grid(row=2, column=0, padx=5, pady=5)
name_entry = tk.Entry(frame)
name_entry.grid(row=2, column=1, padx=5, pady=5)

# Display area
display_area = tk.Text(root, width=50, height=20, state=tk.DISABLED, wrap="word")
display_area.pack(pady=10)

# Run Tkinter main loop
root.mainloop()
