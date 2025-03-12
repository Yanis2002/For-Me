from flask import Flask, render_template_string
import socket
import threading
import random

# Константы
SERVER_PORT = 2222  # Порт для вашего сервера
CLIENT_TARGET_IP = "192.168.7.90"  # IP удаленного сервера
CLIENT_TARGET_PORT = 3333  # Порт удаленного сервера
WEB_PORT = 5000  # Порт для веб-интерфейса

# Настройки для генерации ответов
MIN_STEPS = 100
MAX_STEPS = 1000
MIN_DTIME = 1000
MAX_DTIME = 5000

# Flask-приложение для веб-интерфейса
app = Flask(__name__)

def send_command_to_server(command):
    """Отправка команды на сервер."""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.connect(('127.0.0.1', SERVER_PORT))  # Подключаемся к локальному серверу
            sock.sendall(command.encode('utf-8'))
            response = sock.recv(1024).decode('utf-8')
            print(f"[*] Ответ от сервера: {response}")
            return response
    except Exception as e:
        print(f"[!] Ошибка при отправке команды: {e}")
        return f"Ошибка: {e}"

@app.route('/')
def index():
    """Главная страница с кнопками."""
    return render_template_string('''
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Управление сервоприводами</title>
        </head>
        <body>
            <h1>Управление сервоприводами</h1>
            <button onclick="sendCommand(1)">Get Steps 1</button>
            <button onclick="sendCommand(2)">Get Steps 2</button>
            <p id="response"></p>
            <script>
                function sendCommand(servoNum) {
                    fetch(`/send_command/${servoNum}`)
                        .then(response => response.text())
                        .then(data => {
                            document.getElementById("response").innerText = data;
                        })
                        .catch(error => {
                            document.getElementById("response").innerText = "Ошибка: " + error;
                        });
                }
            </script>
        </body>
        </html>
    ''')

@app.route('/send_command/<int:servo_num>')
def send_command(servo_num):
    """Обработка запроса на отправку команды."""
    command = f"[getsteps {servo_num}]"
    response = send_command_to_server(command)  # Используем переименованную функцию
    return response

def handle_client(client_socket):
    """Обработка данных от клиента."""
    try:
        # Получаем данные от клиента
        data = client_socket.recv(1024).decode('utf-8').strip()
        print(f"[*] Получено: {data}")

        # Проверяем формат запроса [getsteps X]
        if data.startswith("[getsteps ") and data.endswith("]"):
            servo_num = data[10:-1].strip()
            if servo_num in ["1", "2"]:
                # Генерируем случайные значения для ответа
                steps = random.randint(MIN_STEPS, MAX_STEPS)
                direction = "forw" if random.random() > 0.5 else "back"
                dtime = random.randint(MIN_DTIME, MAX_DTIME)

                # Формируем ответ
                response = f"[servo: {servo_num}; steps: {steps}; dir: {direction}; dtime: {dtime}]"

                # Отправляем ответ на удаленный сервер
                print(f"[*] Отправляем ответ на {CLIENT_TARGET_IP}:{CLIENT_TARGET_PORT}: {response}")

                try:
                    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as target_sock:
                        target_sock.settimeout(5)
                        target_sock.connect((CLIENT_TARGET_IP, CLIENT_TARGET_PORT))
                        target_sock.sendall(response.encode('utf-8'))
                        print(f"[+] Ответ успешно отправлен")
                except Exception as e:
                    print(f"[!] Ошибка при отправке ответа: {e}")

            else:
                error_msg = f"[!] Неверный номер сервопривода: {servo_num}"
                print(error_msg)
                client_socket.sendall(error_msg.encode('utf-8'))
        else:
            error_msg = f"[!] Неверный формат запроса. Ожидается: [getsteps X], где X - 1 или 2"
            print(error_msg)
            client_socket.sendall(error_msg.encode('utf-8'))

    except Exception as e:
        print(f"[!] Ошибка при обработке клиента: {e}")
    finally:
        client_socket.close()

def start_server():
    """Запуск сервера."""
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    try:
        # Привязываем сервер ко всем интерфейсам
        server.bind(('0.0.0.0', SERVER_PORT))
        server.listen(5)
        print(f"[*] Сервер запущен на порту {SERVER_PORT}")

        while True:
            client, addr = server.accept()
            print(f"[+] Принято соединение от {addr[0]}:{addr[1]}")

            # Запускаем обработчик клиента в отдельном потоке
            client_handler = threading.Thread(target=handle_client, args=(client,))
            client_handler.daemon = True
            client_handler.start()

    except KeyboardInterrupt:
        print("\n[*] Завершение работы сервера...")
    except Exception as e:
        print(f"[!] Ошибка сервера: {e}")
    finally:
        if server:
            server.close()
try:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as target_sock:
        target_sock.settimeout(5)
        print(f"[*] Пытаюсь подключиться к {CLIENT_TARGET_IP}:{CLIENT_TARGET_PORT}")
        target_sock.connect((CLIENT_TARGET_IP, CLIENT_TARGET_PORT))
        print(f"[*] Подключение успешно. Отправляю данные: {response}")
        target_sock.sendall(response.encode('utf-8'))
        print(f"[+] Ответ успешно отправлен")
except Exception as e:
    print(f"[!] Ошибка при отправке ответа: {e}")

def start_flask():
    """Запуск Flask-приложения."""
    print(f"[*] Веб-интерфейс запущен на порту {WEB_PORT}")
    app.run(host='0.0.0.0', port=WEB_PORT)

if __name__ == "__main__":
    # Запуск сервера в отдельном потоке
    server_thread = threading.Thread(target=start_server)
    server_thread.daemon = True
    server_thread.start()

    # Запуск Flask-приложения в основном потоке
    start_flask()
