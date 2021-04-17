import sqlite3
lst = [
    "1.Традиционно в программировании используют синхронное программирование — последовательное выполнение инструкций с синхронными системными вызовами, которые полностью блокируют поток выполнения, пока системная операция, например чтение с диска, не завершится. ",
    "2.Но что делать, когда пользователей очень много? Если создавать на каждого хотя бы один поток, то производительность такого сервера резко упадёт из-за того, что контекст исполнения потока постоянно сменяется. Также на каждый поток создаётся свой контекст исполнения, включая память для стека, которая имеет минимальный размер в 4 КБ. Эту проблему может решить асинхронное программирование.",
    "3.Асинхронность в программировании — выполнение процесса в неблокирующем режиме системного вызова, что позволяет потоку программы продолжить обработку.",
    "4.Для написания асинхронной программы можно использовать callback-функции (от англ. callback — обратный вызов) — функции, которые будут вызваны асинхронно каким-либо обработчиком событий после завершения задачи.",
    "5.END!"]
#quote = 0





#conn = sqlite3.connect('имя_базы_данных.расширение(.db,.sqlite3)')
conn = sqlite3.connect('data.db')
cur = conn.cursor()
cur.execute(
    'CREATE TABLE IF NOT EXISTS users(\
user_id INTEGER UNIQUE,\
user_vote INTEGER,\
user_comment TEXT,\
emoji_flag BOOL)'
)  # Добавить comment_data
