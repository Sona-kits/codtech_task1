import tkinter as tk
from tkinter import filedialog, messagebox
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
from heapq import nlargest

# Download NLTK data
nltk.download('punkt')
nltk.download('stopwords')

def summarize_text(text, num_sentences=3):
    stop_words = set(stopwords.words('english'))
    sentences = sent_tokenize(text)
    words = word_tokenize(text.lower())
    words = [w for w in words if w.isalnum() and w not in stop_words]

    freq = {}
    for word in words:
        freq[word] = freq.get(word, 0) + 1

    sentence_scores = {}
    for i, sentence in enumerate(sentences):
        for word in word_tokenize(sentence.lower()):
            if word in freq:
                sentence_scores[i] = sentence_scores.get(i, 0) + freq[word]

    top_indices = nlargest(num_sentences, sentence_scores, key=sentence_scores.get)
    summary = ' '.join([sentences[i] for i in sorted(top_indices)])
    return summary

def generate_summary():
    input_text = input_box.get("1.0", tk.END).strip()
    if not input_text:
        messagebox.showwarning("No Input", "Please enter some text to summarize.")
        return
    summary = summarize_text(input_text)
    output_box.delete("1.0", tk.END)
    output_box.insert(tk.END, summary)

def save_summary():
    summary = output_box.get("1.0", tk.END).strip()
    if not summary:
        messagebox.showinfo("Nothing to Save", "No summary available to save.")
        return
    file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
    if file_path:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(summary)
        messagebox.showinfo("Saved", "Summary saved successfully!")

# Create GUI window
window = tk.Tk()
window.title("Text Summarizer - CodTech Internship Task")
window.geometry("800x600")
window.config(bg="lightgray")

# Title
title = tk.Label(window, text="Text Summarization Tool", font=("Arial", 16, "bold"), bg="lightgray", fg="black")
title.pack(pady=10)

# Input text
tk.Label(window, text="Enter your text below:", bg="lightgray", fg="black").pack()
input_box = tk.Text(window, height=10, width=100, wrap=tk.WORD, bg="white", fg="black")
input_box.pack(padx=10, pady=5)

# Button frame
btn_frame = tk.Frame(window, bg="lightgray")
btn_frame.pack(pady=10)

tk.Button(btn_frame, text="Generate Summary", command=generate_summary, bg="green", fg="white", padx=10, pady=5).grid(row=0, column=0, padx=10)
tk.Button(btn_frame, text="Save Summary", command=save_summary, bg="blue", fg="white", padx=10, pady=5).grid(row=0, column=1, padx=10)

# Output text
tk.Label(window, text="Summary:", bg="lightgray", fg="black").pack()
output_box = tk.Text(window, height=10, width=100, wrap=tk.WORD, bg="white", fg="black")
output_box.pack(padx=10, pady=5)

# Run the app
window.mainloop()
