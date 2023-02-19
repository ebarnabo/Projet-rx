import tkinter as tk
from datetime import datetime
from tkinter import simpledialog
from tkinter import messagebox

root = tk.Tk()
root.withdraw()


def quit(root):
    root.destroy()



# Demande le pseudo de l'utilisateur avec une boîte de dialogue
user_name = simpledialog.askstring("Pseudo", "Entrez votre pseudo :")



# Affiche la fenêtre principale
root = tk.Toplevel()
root.title("Super Chat 2.0")
root.resizable(False, False)

# Positionne la fenêtre au centre de l'écran
window_width = root.winfo_screenwidth()
window_height = root.winfo_screenheight()
x = (window_width // 2) - (1200 // 2) # 1200 largeur
y = (window_height // 2) - (300 // 2) # 300 hauteur
root.geometry(f"1200x300+{x}+{y}")

messages_frame = tk.Frame(root)
scrollbar = tk.Scrollbar(messages_frame)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
message_list = tk.Listbox(messages_frame, height=15, width=50, yscrollcommand=scrollbar.set)
message_list.pack(side=tk.LEFT, fill=tk.BOTH)
messages_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)

# Affiche la liste des utilisateurs connectés au chat
users_frame = tk.Frame(root)
users_label = tk.Label(users_frame, text="Utilisateurs connectés")
users_label.pack(side=tk.TOP)
users_list = tk.Listbox(users_frame, height=15, width=20)
users_list.pack(side=tk.LEFT, fill=tk.BOTH)
users_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=5, pady=5)
entry_frame = tk.Frame(root, bd=2, padx=5, pady=5)
email_icon = tk.Label(entry_frame, text="✉️", font=("Arial", 120))
email_icon.pack(side=tk.TOP, padx=(0, 0), pady=(0, 20))
entry_field = tk.Text(entry_frame, bd=0, font=("Arial", 12),insertbackground="#6876EC",selectbackground="#6876EC",borderwidth=0, height=5, width=50, fg="white")
#entry_field.config(insertbackground="#6876EC", insertwidth=3, selectbackground="#6876EC", selectforeground="black")
entry_field.pack(side=tk.LEFT, padx=5, pady=5, expand=True)
entry_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=5, pady=5)

# Création du bouton pour les réactions emojis
reactions_button = tk.Button(entry_frame, text="😀", bg="blue", font=("Arial", 12), bd=0, relief=tk.FLAT)
reactions_button.pack(side=tk.TOP)

# Liste des emojis de réaction
reactions_list = [u'👍', u'👎', u'❤️', u'😂', u'😢', u'😠']

# Fonction pour ajouter une réaction emoji à la zone de texte
def add_reaction_emoji(emoji):
    entry_field.insert(tk.END, emoji)

# Fonction pour afficher la liste des réactions emojis
def show_reactions_list(event=None):
    # Création de la fenêtre popup
    popup_window = tk.Toplevel(root)
    popup_window.geometry(f"+{1080}+{350}") # positionne la fenêtre popup à droite et en dessous de la fenêtre principale
    popup_window.resizable(False, False)
    popup_window.overrideredirect(True) # enlève les bordures et les boutons de la fenêtre popup

    # Création de la liste des réactions emojis
    for emoji in reactions_list:
        emoji_button = tk.Button(popup_window, text=emoji,font=("Arial", 12), bd=0, relief=tk.FLAT, command=lambda e=emoji: (add_reaction_emoji(e), popup_window.destroy()))
        emoji_button.pack(side=tk.BOTTOM, padx=5, pady=5)

# Ajout de l'événement d'affichage de la liste des réactions emojis
reactions_button.bind("<Button-1>", show_reactions_list)


def add_message(msg):
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    message_list.insert(tk.END, f"[{current_time}] {msg}")

def send_message(event=None):
    msg = entry_field.get("1.0", "end-1c") # récupère le texte de la zone de texte, sans le caractère de fin de ligne
    add_message("😂"+user_name+": "+ msg)
    entry_field.delete("1.0", tk.END) # efface le contenu de la zone de texte


def add_user(user):
    users_list.insert(tk.END, user)


def on_closing():
    if messagebox.askokcancel("Quitter", "Êtes-vous sûr de vouloir quitter l'application ?"):
        root.destroy()


#tk.Button(root, text="Quit", command=lambda root=root:quit(root)).pack()

root.protocol("WM_DELETE_WINDOW", on_closing)


send_button = tk.Button(entry_frame, text="Envoyer", bg="blue", font=("Arial", 12), bd=0, relief=tk.FLAT, command=send_message)
send_button.pack(side=tk.RIGHT)

entry_field.bind("<Return>", send_message)

root.mainloop()
