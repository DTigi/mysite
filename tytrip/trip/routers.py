from rest_framework import routers

'''mapping – связка типа запроса (GET, POST и т.п.) и соответствующего метода вьюсета;
name – название маршрута;
detail – список или отдельная запись;
initkwargs – дополнительные аргументы для коллекции kwargs, которые передаются конкретному представлению при срабатывании маршрута.'''

class MyCustomRouter(routers.SimpleRouter):
    routes = [
        routers.Route(url=r'^{prefix}$',
                      mapping={'get': 'list'},
                      name='{basename}-list',
                      detail=False,
                      initkwargs={'suffix': 'List'}),
        routers.Route(url=r'^{prefix}/{lookup}$',
                      mapping={'get': 'retrieve'},
                      name='{basename}-detail',
                      detail=True,
                      initkwargs={'suffix': 'Detail'})
    ]