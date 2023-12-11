from rest_framework import permissions

class UsuarioClusterPermiso(permissions.BasePermission):
    def has_permission(self, request, view):
        #allowed_endpoints =  ['medical-equipment-search-by-names', 'user-login-cluster']

        # Verifica si la vista actual está en la lista de endpoints permitidos para el usuario 'x'
        #return request.user.username == 'cluster' and view.url_name in allowed_endpoints
        allowed_endpoints = ['MedicalEquipmentSearchViewbyName', 'UserLoginView']

        # Verifica si el nombre de la clase de la vista actual está en la lista de endpoints permitidos para el usuario 'cluster'
        return request.user.user_name == 'cluster' and view.__class__.__name__ in allowed_endpoints
