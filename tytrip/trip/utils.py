menu = [
        {'title': "Главная", 'url_name': 'home'},
        {'title': "О сайте", 'url_name': 'about'},
        {'title': "Статьи", 'url_name': 'articles'},
        {'title': "Теги", 'url_name': 'tags'},
        {'title': "Темы", 'url_name': 'home'},
        {'title': "Добавить статью", 'url_name': 'add_page'},
        {'title': "Обратная связь", 'url_name': 'contact'},
        {'title': "Войти", 'url_name': 'login'},
        ]

class DataMixin:
    paginate_by = 3
