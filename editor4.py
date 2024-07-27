import tkinter as tk
from tkinter import scrolledtext
import subprocess

# Define las palabras clave y colores de resaltado
KEYWORDS = {
    "print": "red",
    "def": "blue",
    "import": "green",
    "class": "purple"
}

def highlight_code(text_widget):
    # Elimina todos los tags de resaltado previos
    text_widget.tag_delete("highlight")
    
    # Configura los tags de resaltado para cada color
    for keyword, color in KEYWORDS.items():
        text_widget.tag_configure(f"highlight_{keyword}", foreground=color)
        
        start_index = "1.0"
        while True:
            start_index = text_widget.search(keyword, start_index, nocase=1, stopindex=tk.END)
            if not start_index:
                break
            end_index = f"{start_index}+{len(keyword)}c"
            text_widget.tag_add(f"highlight_{keyword}", start_index, end_index)
            start_index = end_index

def run_code():
    # Obtén el código del Text widget
    code = code_editor.get("1.0", tk.END)
    
    # Guarda el código en un archivo temporal
    with open("temp_code.py", "w") as f:
        f.write(code)
    
    # Ejecuta el código y captura la salida
    try:
        result = subprocess.run(
            ["python", "temp_code.py"],
            capture_output=True,
            text=True,
            timeout=5
        )
        output = result.stdout
        error = result.stderr
        terminal_output.config(state=tk.NORMAL)
        terminal_output.delete("1.0", tk.END)
        terminal_output.insert(tk.END, output + error)
        terminal_output.config(state=tk.DISABLED)
    except Exception as ex:
        terminal_output.config(state=tk.NORMAL)
        terminal_output.delete("1.0", tk.END)
        terminal_output.insert(tk.END, str(ex))
        terminal_output.config(state=tk.DISABLED)

def main():
    global code_editor, terminal_output
    
    root = tk.Tk()
    root.title("Code Editor")
    
    # Configura el color de fondo y el color del texto para el tema oscuro
    bg_color = "#2E2E2E"  # Color de fondo oscuro
    fg_color = "#D3D3D3"  # Color de texto claro
    
    root.configure(bg=bg_color)

    # Crear el área de texto para el editor de código
    code_editor = scrolledtext.ScrolledText(root, wrap=tk.WORD, height=20, width=80, bg=bg_color, fg=fg_color, insertbackground=bg_color)
    code_editor.pack()
    
    # Crear un botón para ejecutar el código
    run_button = tk.Button(root, text="Run Code", command=run_code, bg="#4B4B4B", fg="white")
    run_button.pack()
    
    # Crear el área de texto para mostrar la salida del terminal
    terminal_output = scrolledtext.ScrolledText(root, wrap=tk.WORD, height=10, width=80, bg=bg_color, fg=fg_color, state=tk.DISABLED)
    terminal_output.pack()

    # Resalta el código en el editor cada vez que se modifica
    code_editor.bind("<KeyRelease>", lambda event: highlight_code(code_editor))

    root.mainloop()

if __name__ == "__main__":
    main()






