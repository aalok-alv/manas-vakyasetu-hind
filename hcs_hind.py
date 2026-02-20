import customtkinter as ctk
import pyttsx3
import re

# ---------------- SPEECH ENGINE ----------------
engine = pyttsx3.init()
engine.setProperty('rate', 140)

# Try to find Hindi voice, else fallback
voices = engine.getProperty('voices')
hindi_voice_found = False

for voice in voices:
    if "hindi" in voice.name.lower() or "india" in voice.name.lower():
        engine.setProperty('voice', voice.id)
        hindi_voice_found = True
        break




# hindi_map = {
#     "अ":"a","आ":"aa","इ":"i","ई":"ee","उ":"u","ऊ":"oo",
#     "ए":"e","ऐ":"ai","ओ":"o","औ":"au",

#     "क":"k","ख":"kh","ग":"g","घ":"gh","ङ":"n",
#     "च":"ch","छ":"chh","ज":"j","झ":"jh","ञ":"n",
#     "ट":"t","ठ":"th","ड":"d","ढ":"dh","ण":"n",
#     "त":"t","थ":"th","द":"d","ध":"dh","न":"n",
#     "प":"p","फ":"ph","ब":"b","भ":"bh","म":"m",
#     "य":"y","र":"r","ल":"l","व":"v",
#     "श":"sh","ष":"sh","स":"s","ह":"h",

#     "ा":"aa","ि":"i","ी":"ee","ु":"u","ू":"oo",
#     "े":"e","ै":"ai","ो":"o","ौ":"au","्":""
# }

# def hindi_to_roman(text):
#     result = ""
#     for char in text:
#         result += hindi_map.get(char, char)
#     print(result)
#     return result







def speak(text):
    if text.strip() != "":

        engine.say(text)
        engine.runAndWait()


# ---------------- MAIN CLASS ----------------
class HindiMatrix:

    def __init__(self, root):

        self.root = root
        self.root.title("HAWKING - Hindi Mode")

        root.attributes('-fullscreen', True)
        self.root.state("zoomed")

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.rows = 12  # 1 action + 9 alphabet
        self.cols = 5

        self.labels = []
        self.current_row = 0
        self.current_col = 0
        self.stage = "col"
        self.selected_history = ""

        self.main_frame = ctk.CTkFrame(self.root, corner_radius=15)
        self.main_frame.pack(expand=True, fill="both", padx=20, pady=20)

        for r in range(self.rows + 5):
            self.main_frame.grid_rowconfigure(r, weight=1)
        for c in range(self.cols + 2):
            self.main_frame.grid_columnconfigure(c, weight=1)

        # History box
        self.history_entry = ctk.CTkEntry(
            self.main_frame, font=("Arial", 28, "bold"), justify="left"
        )
        self.history_entry.grid(row=0, column=0,
                                columnspan=self.cols+1,
                                pady=10, padx=10, sticky="nsew")

        self.create_grid()

        self.status = ctk.CTkLabel(
            self.main_frame,
            text="स्तंभ चुनें",
            font=("Arial", 20)
        )
        self.status.grid(row=self.rows+4,
                         column=0,
                         columnspan=self.cols+1,
                         sticky="nsew")

        self.highlight_selection()

        self.root.bind("<Delete>", self.matrix_navigation)
        self.root.bind("<Return>", self.confirm_selection)
        self.root.bind("<Escape>", lambda e: self.root.destroy())


    # ---------------- GRID ----------------
    def create_grid(self):

        self.labels = []

        # Action row
        actions = ["बोलें", "साफ", "हटाएँ", "स्पेस", "बंद"]
        action_row = []

        for c in range(self.cols):
            lbl = ctk.CTkLabel(
                self.main_frame,
                text=actions[c],
                font=("Arial", 18, "bold"),
                fg_color="gray25",
                corner_radius=8
            )
            lbl.grid(row=1, column=c,
                     sticky="nsew", padx=5, pady=5)
            action_row.append(lbl)

        self.labels.append(action_row)

        # Hindi letters + matras
        letters = [
            "अ","आ","इ","ई","उ",
            "ऊ","ए","ऐ","ओ","औ",
            "क","ख","ग","घ","ङ",
            "च","छ","ज","झ","ञ",
            "ट","ठ","ड","ढ","ण",
            "त","थ","द","ध","न",
            "प","फ","ब","भ","म",
            "य","र","ल","व",
            "श","ष","स","ह",
            "ा","ि","ी","ु","ू",
            "े","ै","ो","ौ","्"
        ]

        index = 0

        for r in range(2, self.rows+1):
            row_labels = []
            for c in range(self.cols):

                if index < len(letters):
                    letter = letters[index]
                else:
                    letter = ""

                lbl = ctk.CTkLabel(
                    self.main_frame,
                    text=letter,
                    font=("Arial", 28),
                    fg_color="gray15",
                    corner_radius=8
                )

                lbl.grid(row=r, column=c,
                         sticky="nsew", padx=5, pady=5)

                row_labels.append(lbl)
                index += 1

            self.labels.append(row_labels)


    # ---------------- HIGHLIGHT ----------------
    def highlight_selection(self):

        for r in range(self.rows):
            for c in range(self.cols):
                base_color = "gray25" if r == 0 else "gray15"
                self.labels[r][c].configure(fg_color=base_color)

        if self.stage == "col":
            for r in range(self.rows):
                self.labels[r][self.current_col].configure(
                    fg_color="royalblue4"
                )
            self.status.configure(text="पंक्ति चुनें")
        else:
            for c in range(self.cols):
                self.labels[self.current_row][c].configure(
                    fg_color="seagreen4"
                )
            self.status.configure(text="चयन की पुष्टि करें")


    # ---------------- NAVIGATION ----------------
    def matrix_navigation(self, event):

        if self.stage == "col":
            self.current_col = (self.current_col + 1) % self.cols
        else:
            self.current_row = (self.current_row + 1) % self.rows

        self.highlight_selection()


    # ---------------- CONFIRM ----------------
    def confirm_selection(self, event):

        if self.stage == "col":
            self.stage = "row"
            self.highlight_selection()
            return

        selected_text = self.labels[self.current_row][self.current_col].cget("text")

        matras = ["ा","ि","ी","ु","ू","े","ै","ो","ौ","्"]

        if self.current_row == 0:

            if selected_text == "साफ":
                self.selected_history = ""

            elif selected_text == "हटाएँ":
                self.selected_history = self.selected_history[:-1]

            elif selected_text == "स्पेस":
                self.selected_history += " "

            elif selected_text == "बोलें":
                speak(self.selected_history)

            elif selected_text == "बंद":
                self.root.destroy()

        else:

            if selected_text != "":
                if selected_text in matras and self.selected_history:
                    self.selected_history += selected_text
                else:
                    self.selected_history += selected_text

        self.history_entry.delete(0, "end")
        self.history_entry.insert(0, self.selected_history)

        self.stage = "col"
        self.current_row = 0
        self.current_col = 0
        self.highlight_selection()


# ---------------- RUN ----------------
if __name__ == "__main__":
    root = ctk.CTk()
    app = HindiMatrix(root)
    root.mainloop()

