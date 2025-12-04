from tkinter import *
from tkinter import messagebox
import re
from reportlab.pdfgen import canvas


# ---------- SUMMARY LOGIC (Simple & Works in Python 3.13) ----------
def summarize_text():
    text = input_text.get("1.0", END).strip()
    if not text:
        output_text.delete("1.0", END)
        output_text.insert("1.0", "Please enter some text first!")
        return

    sentences = re.split(r'(?<=[.!?]) +', text)

    if len(sentences) <= 2:
        output_text.delete("1.0", END)
        output_text.insert("1.0", "Text is too short to summarize!")
        return

    words = re.findall(r'\w+', text.lower())
    freq = {}
    for word in words:
        freq[word] = freq.get(word, 0) + 1

    sentence_scores = {}
    for sentence in sentences:
        for word in freq:
            if word in sentence.lower():
                sentence_scores[sentence] = sentence_scores.get(sentence, 0) + freq[word]

    summary_sentences = sorted(sentence_scores, key=sentence_scores.get, reverse=True)
    summary = " ".join(summary_sentences[:3])

    output_text.delete("1.0", END)
    output_text.insert("1.0", summary)


# ---------- CLEAR FUNCTION ----------
def clear_all():
    input_text.delete("1.0", END)
    output_text.delete("1.0", END)


# ---------- COPY FUNCTION ----------
def copy_summary():
    summary = output_text.get("1.0", END).strip()
    if summary:
        root.clipboard_clear()
        root.clipboard_append(summary)
        messagebox.showinfo("Copied!", "Summary copied to clipboard!")


# ---------- EXPORT PDF ----------
def export_pdf():
    summary = output_text.get("1.0", END).strip()
    if not summary:
        messagebox.showerror("Error", "No summary to export!")
        return

    pdf_file = "summary_output.pdf"
    c = canvas.Canvas(pdf_file)
    c.setFont("Helvetica", 12)

    y = 800
    for line in summary.split("\n"):
        c.drawString(40, y, line)
        y -= 20

    c.save()
    messagebox.showinfo("Success", f"Saved as {pdf_file}")


# ---------- DARK MODE ----------
dark = False
def toggle_dark_mode():
    global dark
    dark = not dark

    bg = "#2C3E50" if dark else "#EEF2F7"
    fg = "white" if dark else "#2C3E50"
    box_bg = "#34495E" if dark else "white"

    root.config(bg=bg)
    title.config(bg=bg, fg=fg)
    input_label.config(bg=bg, fg=fg)
    output_label.config(bg=bg, fg=fg)

    input_text.config(bg=box_bg, fg=fg)
    output_text.config(bg=box_bg, fg=fg)

    summarize_btn.config(bg="#4A90E2", fg="white")
    clear_btn.config(bg="#E74C3C", fg="white")
    copy_btn.config(bg="#27AE60", fg="white")
    pdf_btn.config(bg="#8E44AD", fg="white")
    dark_btn.config(bg="#F1C40F", fg="black")


# ---------- UI WINDOW ----------
root = Tk()
root.title("AI Text Summarizer (Pro Version)")
root.geometry("750x700")
root.config(bg="#EEF2F7")

title = Label(root, text="AI Text Summarizer Pro",
              font=("Calibri", 22, "bold"),
              bg="#EEF2F7", fg="#2C3E50")
title.pack(pady=15)

input_label = Label(root, text="Enter Text:", font=("Calibri", 14, "bold"),
                    bg="#EEF2F7", fg="#2C3E50")
input_label.pack()

input_text = Text(root, height=10, width=80, font=("Calibri", 12),
                  bd=2, relief=GROOVE, bg="white")
input_text.pack(pady=5)

# Buttons Row
btn_frame = Frame(root, bg="#EEF2F7")
btn_frame.pack(pady=10)

summarize_btn = Button(btn_frame, text="Summarize", font=("Calibri", 12, "bold"),
                       bg="#4A90E2", fg="white", padx=10, pady=5,
                       command=summarize_text)
summarize_btn.grid(row=0, column=0, padx=10)

clear_btn = Button(btn_frame, text="Clear", font=("Calibri", 12, "bold"),
                   bg="#E74C3C", fg="white", padx=10, pady=5,
                   command=clear_all)
clear_btn.grid(row=0, column=1, padx=10)

copy_btn = Button(btn_frame, text="Copy", font=("Calibri", 12, "bold"),
                  bg="#27AE60", fg="white", padx=10, pady=5,
                  command=copy_summary)
copy_btn.grid(row=0, column=2, padx=10)

pdf_btn = Button(btn_frame, text="Export PDF", font=("Calibri", 12, "bold"),
                 bg="#8E44AD", fg="white", padx=10, pady=5,
                 command=export_pdf)
pdf_btn.grid(row=0, column=3, padx=10)

dark_btn = Button(btn_frame, text="Dark Mode", font=("Calibri", 12, "bold"),
                  bg="#F1C40F", fg="black", padx=10, pady=5,
                  command=toggle_dark_mode)
dark_btn.grid(row=0, column=4, padx=10)

output_label = Label(root, text="Summary:", font=("Calibri", 14, "bold"),
                     bg="#EEF2F7", fg="#2C3E50")
output_label.pack()

output_text = Text(root, height=10, width=80, font=("Calibri", 12),
                   bd=2, relief=GROOVE, bg="white")
output_text.pack(pady=5)

root.mainloop()
