import flet as ft
import json

TASKS = {}  # Variável global para armazenar as tarefas

def load_tasks(json_db="tasks.json"):
    """Carregar tarefas do arquivo JSON."""
    global TASKS
    try:
        with open(json_db, "r", encoding="utf-8") as file:
            TASKS = json.load(file)
    except FileNotFoundError:
        TASKS = {}

def save_tasks(json_db="tasks.json"):
    """Salvar tarefas no arquivo JSON."""
    with open(json_db, "w", encoding="utf-8") as file:
        json.dump(TASKS, file, ensure_ascii=False, indent=4)

def main(page: ft.Page):
    """Função principal da interface."""
    page.title = "Gerenciador de Tarefas 2.0"
    page.theme_mode = ft.ThemeMode.DARK  # Ativa o modo escuro
    page.bgcolor = "#121212"  # Fundo em tom escuro

    load_tasks()

    selected_task_id = None  # ID da tarefa atualmente selecionada

    def refresh_task_list(filter_by=None):
        """Atualiza a lista de tarefas exibidas."""
        task_list.controls.clear()
        for task_id, task in TASKS.items():
            if filter_by == "concluídas" and not task["completed"]:
                continue
            elif filter_by == "em andamento" and task["completed"]:
                continue

            status = "✔" if task["completed"] else "❌"
            background_color = "#333333" if task_id == selected_task_id else "#1E1E1E"  # Destaque

            task_list.controls.append(
                ft.ListTile(
                    title=ft.Text(task["task"], size=16, color="white"),
                    subtitle=ft.Text(task["description"], color="gray"),
                    trailing=ft.Text(status, color="green" if task["completed"] else "red"),
                    bgcolor=background_color,
                    on_click=lambda e, task_id=task_id: select_task(task_id),
                )
            )
        page.update()

    def select_task(task_id):
        """Armazena e destaca a tarefa selecionada."""
        nonlocal selected_task_id
        selected_task_id = task_id
        refresh_task_list()

    def add_task(e):
        """Adiciona uma nova tarefa."""
        if not task_name.value or not task_description.value:
            page.show_snack_bar(ft.SnackBar(ft.Text("Preencha todos os campos!"), bgcolor="red"))
            return

        task_id = str(len(TASKS) + 1)
        TASKS[task_id] = {
            "task": task_name.value,
            "description": task_description.value,
            "completed": False,
        }
        save_tasks()
        refresh_task_list()
        task_name.value = ""
        task_description.value = ""
        page.update()

    def remove_task(e):
        """Remove a tarefa selecionada."""
        if selected_task_id and selected_task_id in TASKS:
            del TASKS[selected_task_id]
            save_tasks()
            refresh_task_list()
        else:
            page.show_snack_bar(ft.SnackBar(ft.Text("Selecione uma tarefa para remover!"), bgcolor="red"))

    def change_status(e):
        """Altera o status da tarefa selecionada."""
        if selected_task_id and selected_task_id in TASKS:
            TASKS[selected_task_id]["completed"] = not TASKS[selected_task_id]["completed"]
            save_tasks()
            refresh_task_list()
        else:
            page.show_snack_bar(ft.SnackBar(ft.Text("Selecione uma tarefa para alterar o status!"), bgcolor="red"))

    # Layout da interface
    task_name = ft.TextField(label="Nome da Tarefa", width=400)
    task_description = ft.TextField(label="Descrição da Tarefa", width=400)

    add_button = ft.ElevatedButton(text="Adicionar Tarefa", on_click=add_task)
    remove_button = ft.ElevatedButton(text="Remover Tarefa", on_click=remove_task)
    change_status_button = ft.ElevatedButton(text="Alterar Status", on_click=change_status)

    task_list = ft.ListView(expand=True, spacing=10, padding=20)

    page.add(
        ft.Column(
            [
                task_name,
                task_description,
                ft.Row([add_button, remove_button, change_status_button], alignment=ft.MainAxisAlignment.SPACE_EVENLY),
                task_list,
            ],
            expand=True,
            spacing=20,
        )
    )

    refresh_task_list()

if __name__ == "__main__":
    ft.app(target=main)
