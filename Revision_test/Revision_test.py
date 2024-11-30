from googletrans import Translator
from tkinter import messagebox
from tkinter import filedialog
from tkinter import font
from tkinter import *
from keyboard import add_hotkey, remove_hotkey
from time import time
from gtts import gTTS, gTTSError # Install gTTS.
from pyttsx3 import init # Install pyttsx3.
from playsound import playsound #HINT: Install playsound version 1.2.2
from os import remove


########################## Front-End ##########################
window = Tk()
window.title("Revision test")
window.geometry("350x400")
icon = PhotoImage(file=".\\rt_icon.png")
window.call("wm", "iconphoto", window._w, icon)
entxt_font = font.Font(family="tahoma", size=9, weight="bold")
fatxt_font = font.Font(family="Vazir", size=9, weight="bold")
sp_font = font.Font(family="Segoe UI", size=10)


def help_box():
    messagebox.showinfo("Revision test", "You can use the application in 4 steps:\n \
                        \n[1] Select mode. \
                        \n[2] Enter file path and press 'Enter'. (Press 'Enter' to open File Explorer) \
                        \n[3] Enter answer in the entry and press 'Enter' to check the answer. \
                        \n[4] To move to the next question, press 'Shift+Enter'.\
                        \n\n\nPublisher: MohammadAli \
                        \nGitHub: https://github.com/pairen1383/ \
                        \nVersion: 1.0.0")


def show_menu():
    global mode, path_ent, correct_answers, word_index, decrease, bgcolor, delta_time
    correct_answers = 0
    word_index = 0
    decrease = 0
    bgcolor = "#82ffda"
    delta_time = 0

    add_hotkey("Enter", menu_ent_key) # It will be removed in menu_ent_key.

    hbtn = Button(window, text="?", width=2, command=help_box)
    hbtn.place(x=325, y=0)

    mode_lb = Label(window, justify="left", text="Select the mode: ")
    mode_lb.place(x=2, y=2)

    mode = StringVar()
    rb1 = Radiobutton(window, variable=mode, value="meaning")
    rb1.select()
    rb1.place(x=2, y=20)
    r1_lb = Label(window, justify="left", text="Translation of words")
    r1_lb.place(x=20, y=20)

    rb2 = Radiobutton(window, variable=mode, value="synonym")
    rb2.place(x=2, y=45)
    r2_lb = Label(window, justify="left", text="Synonym of words")
    r2_lb.place(x=20, y=45)

    path_lb = Label(window, justify="left", text=f"Select the text file you want to test. ")
    path_lb.place(x=2, y=80)

    ent_lb = Label(window, justify="left", text="File path (.txt):")
    ent_lb.place(x=2, y=110)

    raw_text = StringVar()
    path_ent = Entry(window, justify="left", textvariable=raw_text, width=25)
    path_ent.place(x=83, y=110)

    path_btn = Button(window, text="\U0001F4C2", width=3, command=file_explorer)
    path_btn.place(x=240, y=105)
    start_btn = Button(window, text="Enter", width=8, command=menu_ent_key)
    start_btn.place(x=275, y=105)


def show_test(q_word: str):
    global mode, the_word, ent_lb, ans_ent, test_btn, pronun_on_off, start_time
    add_hotkey("Enter", test_ent_key) # It will be removed in test_ent_key.
    the_word = q_word

    hbtn = Button(window, text="?", width=2, command=help_box)
    hbtn.place(x=325, y=0)

    q_lb = Label(window, justify="left", text=f"what is the {mode.get()} of word: ")
    q_lb.place(x=2, y=2)

    q_word_lb = Label(window, justify="left", background="light blue", text=the_word)
    q_word_lb.place(x=160, y=2)

    pronun_on_off = BooleanVar()
    checkbox = Checkbutton(window, variable=pronun_on_off, onvalue=True, offvalue=False)
    checkbox.place(x=2, y=23)

    cblb = Label(window, justify="left", text="Always use offline pronunciation.")
    cblb.place(x=20, y=25)

    vbtn = Button(window, text=u"\U0001F50A", width=2, height=1, command=play_voice, font=sp_font)
    vbtn.place(x=300, y=0)

    ent_lb = Label(window, justify="left", text="Your answer:")
    ent_lb.place(x=2, y=70)

    raw_text = StringVar()
    justify_ans_ent = "right"
    font_ans_ent = fatxt_font
    if mode.get() == "synonym":
        justify_ans_ent = "left"
        font_ans_ent = entxt_font
    ans_ent = Entry(window, justify=justify_ans_ent, textvariable=raw_text, font=font_ans_ent, width=25)
    ans_ent.place(x=75, y=70)
    ans_ent.focus_set()

    test_btn = Button(window, text="Check", width=8, command=test_ent_key)
    test_btn.place(x=280, y=67)

    start_time = time()


def show_answer(user_answer: str):
    global trtxt, other_trtxt, syn_intxt, def_intxt, ent_lb, ans_ent, test_btn, gt_true_false, bgcolor, start_time, end_time, delta_time

    end_time = time()
    delta_time = delta_time + round(end_time - start_time)

    # Hotkey has been removed in test_ent_key.
    add_hotkey("Shift+Enter", test_administrator)

    # Delete input section
    ent_lb.destroy()
    ans_ent.destroy()
    test_btn.destroy()

    user_ans_lb = Label(window, justify="left", background="light yellow", text="Your answer: " + user_answer)
    user_ans_lb.place(x=2, y=50)

    gt_ans_lb = Label(window, justify="left", background=bgcolor, text=gt_true_false + " answer!")
    gt_ans_lb.place(x=2, y=75)
    next_btn = Button(window, text="Next", width=8, command=test_administrator)
    next_btn.place(x=270, y=60)

    trtxt = Label_Text_area(window, 2, 100, "Translated word:", "left", -40, 46, 1, fatxt_font, "", "right")
    other_trtxt = Label_Text_area(window, 2, 155, "Other translations:", "left", -40, 46, 3, fatxt_font, "", "right")
    syn_intxt = Label_Text_area(window, 2, 240, "Synonyms:", "left", 8, 40, 3, entxt_font, "", "left")
    def_intxt = Label_Text_area(window, 2, 320, "Definition:", "left", 8, 40, 3, entxt_font, "", "left")


def show_result():
    global correct_answers, word_index, decrease, delta_time

    add_hotkey("Enter", end_test_btn) # It will be removed in end_test_key.

    hbtn = Button(window, text="?", width=2, command=help_box)
    hbtn.place(x=325, y=0)

    correct_lb = Label(window, justify="left", text=f"Correct answers: {correct_answers}")
    correct_lb.place(x=2, y=0)

    total_lb = Label(window, justify="left", text=f"Number of words: {word_index - decrease}")
    total_lb.place(x=2, y=15)

    per_lb = Label(window, justify="left", text=f"Percentage of correct answers: {round((correct_answers * 100 / (word_index - decrease)), 1)}")
    per_lb.place(x=2, y=30)

    time_lb = Label(window, justify="left", text=f"Time spent: {delta_time // 60} (m), {delta_time % 60} (s)")
    time_lb.place(x=2, y=45)

    end_btn = Button(window, text="Menu", width=48, command=end_test_btn)
    end_btn.place(x=2, y=80)


class Label_Text_area:
    def __init__(self, wid_root, lb_x, lb_y, lb_txt, lb_justify, ta_scrollbar_x_margin, ta_width, ta_height, ta_font, ta_data, ta_justify) -> None:
        self.root = wid_root
        self.lb_x = lb_x
        self.lb_y = lb_y
        self.lb_txt = lb_txt
        self.lb_justify = lb_justify
        self.margin = ta_scrollbar_x_margin
        self.ta_width = ta_width
        self.ta_height = ta_height
        self.ta_font = ta_font
        self.ta_data = ta_data
        self.ta_justify = ta_justify

        if self.lb_txt != "":
            txt_lb = Label(self.root, justify=self.lb_justify, text=self.lb_txt)
            txt_lb.place(x=self.lb_x, y=self.lb_y)
        self.txt_area = Text(self.root, width=self.ta_width, height=self.ta_height, font=self.ta_font, wrap=WORD)
        self.sc = Scrollbar(self.root)
        self.sc.place(x=self.lb_x + self.margin + self.ta_width * 8, y=self.lb_y + 20) # Approximately 1 unit of width equals 8 units of x-position
        self.sc.config(command=self.txt_area.yview)
        self.txt_area.tag_configure("tg_name", justify=self.ta_justify) # Persian text is written from right to left.
        self.txt_area.insert(INSERT, self.ta_data)
        self.txt_area.tag_add("tg_name", 1.0, "end") # Add tag from beginning (Line 1 and index 0) to end.
        self.txt_area.place(x=self.lb_x, y=self.lb_y + 20) # The text area and scroll bar should be 20 y-position down.

    def update_ta(self, new_data):
        self.ta_data = new_data
        self.txt_area.delete("1.0", END) # Clear the Textarea.
        self.txt_area.insert(INSERT, self.ta_data)
        self.txt_area.tag_add("tg_name", 1.0, "end") # It must be applied every time.

# Persian text is written from right to left.
def justify_txt(tr_text, extra=[]):
    global trtxt, other_trtxt, syn_intxt, def_intxt
    trtxt.update_ta(tr_text)
    if extra != []:
        for obj in extra[0]:
            obj = obj.replace("{", "").replace("}", "") # Remove unwanted characters.
            obj.strip()
        other_trtxt.update_ta(" ،".join(extra[0]))
        syn_intxt.update_ta(", ".join(extra[1]))
        def_intxt.update_ta(extra[2])
    else:
        other_trtxt.update_ta("")
        syn_intxt.update_ta("")
        def_intxt.update_ta("")


########################## Back-End ##########################
def translate_txt(txt):
    translator = Translator()
    try:
        res = translator.translate(text=txt, src="en", dest="fa")
        try:
            extra_dt = [res.extra_data['all-translations'][0][1],
                    res.extra_data['all-translations'][0][2][0][1],
                    res.extra_data['definitions'][0][1][0][0]]
        except:
            return res.text.strip(), [[], []]
        # Remove the current word from synonyms
        for syw in extra_dt[1]:
            temp = syw
            syw = syw.strip(" !?,.")
            if syw.lower() == txt.lower():
                extra_dt[1].remove(temp)
                break
        extra_dt[1] = list(map(lambda x: x.lower(), extra_dt[1])) # Lowercase words
        return res.text.strip().lower(), extra_dt
    except TypeError: # Entry is empty.
        messagebox.showerror("Revision test", "Error: \nEnter a sentence or word!")
    except Exception as err:
        if str(err) == "[Errno 11001] getaddrinfo failed": # User is offline.
            messagebox.showerror("Revision test", "Error: \nPlease connect to the Internet.")
        else: # Another error.
            messagebox.showerror("Revision test", f"Error: \n{err}")
    return "", [[], []]


def play_voice():
    global the_word, pronun_on_off
    if pronun_on_off.get():
        play_voice_offline(the_word)
    else:
        play_voice_online(the_word)


def play_voice_online(get_txt):
    try:
        tts = gTTS(get_txt, timeout=3)
        tts.save(".\\never_save.mp3")
        playsound(".\\never_save.mp3")
        remove(".\\never_save.mp3")
    except gTTSError: # User is offline.
        remove(".\\never_save.mp3") # The corrupted file has not been deleted.
        # This is an offline voice maker.
        engine = init()
        engine.setProperty("rate", 120) # Text or word reading speed.
        engine.say(get_txt)
        engine.runAndWait()
    except Exception as err: # Always be careful.
        messagebox.showerror("Revision test", f"Error: \n{err}")


def play_voice_offline(get_txt):
    # This is an offline voice maker.
    engine = init()
    engine.setProperty("rate", 120) # Text or word reading speed.
    engine.say(get_txt)
    engine.runAndWait()


def test_administrator():
    global test_word_list, word_index

    # remove the show_answer hotkey, try/except show_menu.
    try:
        remove_hotkey("Shift+Enter")
    except:
        pass
    clear_window()
    if word_index != len(test_word_list):
        show_test(test_word_list[word_index])
        word_index += 1
    else:
        show_result()


def match_letters(input_word: str, tran_list: list):
    counter = 0
    for trw in tran_list:
        for i in range(min(len(input_word), len(trw))):
            if ord(input_word[i]) == ord(trw[i]): # Check unicode number
                counter += 1
        matching_percentage = round(counter / max(len(input_word), len(trw)), 2) * 100
        counter = 0
        if matching_percentage >= 85:
            return True
    return False


def judge_answer(entered_word: str):
    global the_word, correct_answers, mode, decrease, gt_true_false, bgcolor

    translated_word, other_data = translate_txt(the_word)
    if translated_word == "":
        add_hotkey("Enter", test_ent_key)
        return None
    entered_word = entered_word.replace("ي", "ی") # Make correct the unicode
    if mode.get() == "meaning":
        if (translated_word == entered_word) or (entered_word in other_data[0]) or (translated_word.replace("ئ", "ی") == entered_word) or (match_letters(entered_word, [translated_word,] + other_data[0])):
            gt_true_false = "Correct"
            bgcolor = "#82ffda"
            correct_answers += 1
        else:
            gt_true_false = "Wrong"
            bgcolor = "#fa7070"
    else:
        if other_data[1] != []:
            syn_list = []
            for sy in other_data[1]:
                syn_list.append(sy.strip(" !?,.").lower())
            if (entered_word in syn_list):
                gt_true_false = "Correct"
                bgcolor = "#82ffda"
                correct_answers += 1
            else:
                gt_true_false = "Wrong"
                bgcolor = "#fa7070"
        else:
            decrease += 1 
            messagebox.showwarning("Synonyms not found", "No synonyms were found for your word. This word will be removed from the word count.")
    show_answer(entered_word)
    if len(other_data) == 3:
        justify_txt(translated_word, other_data)
    else:
        justify_txt(translated_word)


def open_txt_file(file_path: str):
    with open(file_path, "r") as txtfile:
        all_words = txtfile.readlines()
        ctr = 0
        for i in range(0, len(all_words)):
            if (i-ctr) == len(all_words):
                break
            if "\n" in all_words[i-ctr]:
                all_words[i-ctr] = all_words[i-ctr][0:-1].strip(" ,.!?").lower()
            else:
                all_words[i-ctr] = all_words[i-ctr].strip(" ,.!?").lower() # Last line need an strip
            if all_words[i-ctr] == "":
                all_words.pop(i-ctr)
                ctr += 1
    return all_words


def file_explorer():
    global filename, path_ent

    filename = filedialog.askopenfilename(initialdir = "/", title = "Select file", filetypes = (("txt files","*.txt"),("all files","*.*")))
    path_ent.delete(0, END) # Safe to change path
    path_ent.insert(0, filename.strip()) # Insert the path to the entry


def menu_ent_key():
    global path_ent, test_word_list

    try:
        remove_hotkey("Enter") # remove the show_menu hotkey
    except:
        pass
    if path_ent.get() == "":
        file_explorer()
        add_hotkey("Enter", menu_ent_key)
    else:
        test_word_list = open_txt_file(path_ent.get()) # Get all of the word in text file
        test_administrator()


def test_ent_key():
    global ans_ent

    # try/except because of offline user
    try:
        remove_hotkey("Enter") # remove the show_test hotkey
    except:
        pass
    judge_answer(ans_ent.get().strip().lower())  # Get and delete spaces around the answer


def end_test_btn():
    remove_hotkey("Enter")
    clear_window()
    show_menu()


def clear_window():
    global window
    for widget in window.winfo_children():
        widget.destroy()


########################## Start ##########################
show_menu()
window.mainloop()