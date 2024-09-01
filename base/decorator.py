from functools import wraps
from django.http import JsonResponse

# def role_based_permissions(view_func):
#     """
#     Decorator to enforce role-based permissions:
#     - Manager: POST requests
#     - Superuser: POST, PUT, DELETE requests
#     - User: GET requests
#     """
#     @wraps(view_func)
#     def _wrapped_view(request, *args, **kwargs):
#         if request.method == 'POST':
#             if not (request.user.is_authenticated and (request.user.role == 'manager' or request.user.is_superuser)):
#                 return JsonResponse({'detail': 'You do not have permission to perform this action.'}, status=403)
#         elif request.method in ['PUT', 'DELETE']:
#             if not (request.user.is_authenticated and request.user.is_superuser):
#                 return JsonResponse({'detail': 'You do not have permission to perform this action.'}, status=403)
#         elif request.method == 'GET':
#             if not (request.user.is_authenticated and (request.user.role == 'user' or request.user.is_superuser or request.user.role == 'manager')):
#                 return JsonResponse({'detail': 'You do not have permission to perform this action.'}, status=403)
#         return view_func(request, *args, **kwargs)
#     return _wrapped_view





from functools import wraps
from rest_framework.response import Response
from rest_framework import status

def check_permission(permission_codename, model_class):
    """
    Decorator to check if the user has a specific permission for a given model.
    
    Args:
        permission_codename (str): The codename of the permission to check (e.g., 'add', 'change').
        model_class (class): The model class for which the permission is being checked.
    
    Returns:
        func: The wrapped function if the permission check passes.
    """
    def decorator(func):
        @wraps(func)
        def wrapper(self, request, *args, **kwargs):
            # Construct the permission string dynamically
            permission = f'{model_class._meta.app_label}.{permission_codename}_{model_class._meta.model_name}'
            if not request.user.has_perm(permission):
                return Response({"detail": f"You do not have permission to {permission_codename} {model_class._meta.verbose_name_plural}."},
                                status=status.HTTP_403_FORBIDDEN)
            return func(self, request, *args, **kwargs)
        return wrapper
    return decorator
