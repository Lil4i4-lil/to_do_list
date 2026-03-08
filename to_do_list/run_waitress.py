from to_do_list.wsgi import application
from waitress import serve

if __name__ == '__main__':
    print("Сервер запущен на http://127.0.0.1:8000")
    serve(
        application,
        host='0.0.0.0',
        port=8000,
        threads=4,
        url_scheme='http'
    )