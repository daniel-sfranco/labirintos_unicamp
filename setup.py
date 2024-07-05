from cx_Freeze import setup, Executable

setup(
    name="Labirintos Unicamp",
    version="1.0",
    description="Criado por: Daniel Franco e Vinícius Oliveira",
    executables=[Executable("main.py")],
    include_modules=["pygame", "pygame.image", "pygame.font", "time", "random", "typing", "sys", "os"],
    data_dirs=["audio", "img", "fonts"]
)
