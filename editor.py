import flet as ft
import subprocess

def main(page: ft.Page):
    page.title = "Flet Code Editor"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    code_editor = ft.TextField(
        multiline=True,
        label="Code Editor",
        expand=True,
        height=300,
        width=800
    )

    terminal_output = ft.TextField(
        multiline=True,
        label="Terminal Output",
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

    run_button = ft.ElevatedButton(
        text="Run Code",
        on_click=run_code,
    )

    page.add(
        code_editor,
        run_button,
        terminal_output
    )

ft.app(target=main)
