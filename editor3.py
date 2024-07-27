import flet as ft
import subprocess
import jedi

def main(page: ft.Page):
    page.title = "Flet Code Editor with Intellisense"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    code_editor = ft.TextField(
        bgcolor="gray",
        multiline=True,
        label="Code Editor",
        expand=True,
        height=300,
        width=800,
        #value='print("Hello, world!")'
        value='print("Hola mundo")'
    )

    terminal_output = ft.TextField(
        bgcolor="gray",
        multiline=True,
        label="Terminal Output",
        expand=True,
        height=200,
        width=800,
        read_only=True
    )

    autocompletion_output = ft.TextField(
        bgcolor="gray",
        multiline=True,
        label="Intellisense Output",
        expand=True,
        height=200,
        width=800,
        read_only=True
    )

    def run_code(e):
        code = code_editor.value
        try:
            # Guarda el código en un archivo temporal
            with open("temp_code.py", "w") as f:
                f.write(code)
            
            # Ejecuta el código y captura la salida
            result = subprocess.run(
                ["python", "temp_code.py"],
                capture_output=True,
                text=True,
                timeout=5
            )
            
            output = result.stdout
            error = result.stderr

            # Actualiza la terminal con la salida del código
            terminal_output.value = output + error
            page.update()
        
        except Exception as ex:
            terminal_output.value = str(ex)
            page.update()

    def get_autocompletions(e):
        code = code_editor.value
        try:
            # Usar jedi para obtener sugerencias de autocompletado
            script = jedi.Script(code)
            completions = script.complete()
            suggestions = [f"{c.name} - {c.type}" for c in completions]
            autocompletion_output.value = "\n".join(suggestions)
            page.update()
        
        except Exception as ex:
            autocompletion_output.value = str(ex)
            page.update()

    run_button = ft.ElevatedButton(
        bgcolor="blue",
        color="black",
        text="Run Code",
        on_click=run_code,
    )

    autocomplete_button = ft.ElevatedButton(
        bgcolor="blue",
        color="black",
        text="Get Autocompletions",
        on_click=get_autocompletions,
    )

    page.add(
        code_editor,
        run_button,
        autocomplete_button,
        terminal_output,
        autocompletion_output
    )

ft.app(target=main)
