import flet as ft

def first_app(page: ft.Page):
    first_name = ft.TextField(label="First name", autofocus=True)
    last_name = ft.TextField(label="Last name")
    greetings = ft.Column()

    def btn_click(e):
        greetings.controls.append(ft.Text(f"Hello from: {first_name.value} {last_name.value}!"))
        first_name.value = ""
        last_name.value = ""
        page.update()
        first_name.focus()

    page.add(
         first_name,
         last_name,
         ft.ElevatedButton("Say hello!", on_click=btn_click),
         greetings,
    )

ft.app(target=first_app, )
#ft.app(target=first_app, view=ft.AppView.WEB_BROWSER)

