from rest_framework import permissions


class IsAdminOrReadOnly(permissions.BasePermission):
    '''Мой собственный класс, который прописал сам для ограничений прав доступа.
    Чтобы удалять данные мог только администратор, а читать данные могли все'''

    #переопределим метод has_permission,потому что мы будем делать ограничения прав доступа ну уровне всего запроса
    def has_permission(self, request, view):
        #проверим,если пришедший запрос безопасный (только для чтения, а не изменения или удаления)
        if request.method in permissions.SAFE_METHODS:
            #то мы предоставляем права доступа для всех
            return True
        #а иначе, если запрос небезопасный, то мы должны проверить, что пользователь является админом
        return bool(request.user and request.user.is_staff) #трочка подсмотрена под капотом IsAdminUser в методе has_permission

class IsOwnerOrReadOnly(permissions.BasePermission):
    #скопирован из оф.документации.Нужен для того,чтобы посты мог изменять только автор,
    # а все остальные пользователи могли лишь читать
    """
    Object-level permission to only allow owners of an object to edit it.
    Assumes the model instance has an `owner` attribute.
    """

    def has_object_permission(self, request, view, obj):
        # переопределяем уже метод has_object_permission, т.к. тут уже идет ограничение прав на уровне конкретного объекта(статьи автора)
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Instance must have an attribute named `owner`.
        #если юзер, который пришел с этим запросом равен юзеру из БД
        return obj.user == request.user  # прописываем obj.user а не obj.owner как в документации, потому что в БД у нас используется user
