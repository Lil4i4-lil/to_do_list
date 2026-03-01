from waitress import serve
from to_do_list.to_do_list.wsgi import application

if __name__ == '__main__':
    print("Сервер запущен на http://0.0.0.0:8000")
    serve(
        application,
        host='0.0.0.0',
        port=8000,
        threads=4
    )