from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import Permission
from django.shortcuts import get_object_or_404
from .models import customUser,Transaction
from .serializers import PermissionAssignmentSerializer2,UserSerializer
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse
from django.contrib.contenttypes.models import ContentType
from base.serializers import TransactionSerializer_data,TransactionSerializers,TransactionSerializer
from base.decorator import check_permission
from rest_framework.permissions import IsAuthenticated

#Register user

"""
    {
        "username": "ramesh",
        "email": "john2@example.com",
        "password": "sakib@123",

    }
"""


class UserCreateUpdateView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({"message": "User created successfully", "user": UserSerializer(user).data},
                            status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk=None):
        try:
            user = customUser.objects.get(pk=pk)
        except customUser.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            user = serializer.save()
            return Response({"message": "User updated successfully", "user": UserSerializer(user).data},
                            status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)





##################   Assign permission to particular user    ######

from base.serializers import PermissionAssignmentSerializer2

class AssignPermissionView(APIView):

    """
    if user have permission view and change both and we send only add permission so add, add (permission) along with not remove other permission so we get 3 permission

    {
        "username": "vishal",
        "app_label": "base",
        "model_name": "transaction",
        "permission_codenames": ["add_transaction"]
    }
    """
    def post(self, request):
        serializer = PermissionAssignmentSerializer2(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            app_label = serializer.validated_data['app_label']
            model_name = serializer.validated_data['model_name']
            permission_codenames = serializer.validated_data['permission_codenames']

            try:
                # Get the user instance
                user = customUser.objects.get(username=username)

                # Get the content type for the specified model
                content_type = ContentType.objects.get(app_label=app_label, model=model_name.lower())

                for permission_codename in permission_codenames:
                    try:
                        # Get the specific permission
                        permission = Permission.objects.get(content_type=content_type, codename=permission_codename)

                        # Assign the permission to the user
                        user.user_permissions.add(permission)
                    except Permission.DoesNotExist:
                        return Response({'error': f'Permission with codename "{permission_codename}" not found.'}, 
                                        status=status.HTTP_404_NOT_FOUND)

                return Response({'message': 'Permissions assigned successfully'}, status=status.HTTP_200_OK)
            except customUser.DoesNotExist:
                return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
            except ContentType.DoesNotExist:
                return Response({'error': 'Model not found for the specified app and model name'}, status=status.HTTP_404_NOT_FOUND)
            except Exception as e:
                return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    """
    if user have permission view and change both and we send only add so first it remove existing permission than add add permission 

        {
        "username": "vishal",
        "app_label": "base",
        "model_name": "transaction",
        "permission_codenames": ["add_transaction"]
    }
    """
    def put(self, request):
        serializer = PermissionAssignmentSerializer2(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            app_label = serializer.validated_data['app_label']
            model_name = serializer.validated_data['model_name']
            permission_codenames = serializer.validated_data['permission_codenames']

            try:
                # Get the user instance
                user = customUser.objects.get(username=username)

                # Get the content type for the specified model
                content_type = ContentType.objects.get(app_label=app_label, model=model_name.lower())

                # Clear existing permissions related to this model
                permissions_to_remove = Permission.objects.filter(content_type=content_type)
                user.user_permissions.remove(*permissions_to_remove)

                # Iterate over the list of permission codenames to assign the new set
                for permission_codename in permission_codenames:
                    try:
                        permission = Permission.objects.get(content_type=content_type, codename=permission_codename)
                        user.user_permissions.add(permission)
                    except Permission.DoesNotExist:
                        return Response({'error': f'Permission with codename "{permission_codename}" not found.'}, 
                                        status=status.HTTP_404_NOT_FOUND)

                return Response({'message': 'Permissions replaced successfully'}, status=status.HTTP_200_OK)
            except customUser.DoesNotExist:
                return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
            except ContentType.DoesNotExist:
                return Response({'error': 'Model not found for the specified app and model name'}, status=status.HTTP_404_NOT_FOUND)
            except Exception as e:
                return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    
    """

    if user have view permission and we send view and change permission so it remove view and add change permisson only

    {
    "username": "vishal",
    "app_label": "base",
    "model_name": "transaction",
    "permission_codenames": ["view_transaction","add_transaction"]
    }
    """
    def patch(self, request):
        serializer = PermissionAssignmentSerializer2(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            app_label = serializer.validated_data['app_label']
            model_name = serializer.validated_data['model_name']
            permission_codenames = serializer.validated_data.get('permission_codenames', [])

            try:
                # Get the user instance
                user = customUser.objects.get(username=username)

                # Get the content type for the specified model
                content_type = ContentType.objects.get(app_label=app_label, model=model_name.lower())

                for permission_codename in permission_codenames:
                    try:
                        # Get the specific permission
                        permission = Permission.objects.get(content_type=content_type, codename=permission_codename)

                        # If the permission is already assigned, remove it
                        if user.user_permissions.filter(pk=permission.pk).exists():
                            user.user_permissions.remove(permission)
                        else:
                            # Otherwise, add the permission
                            user.user_permissions.add(permission)
                    except Permission.DoesNotExist:
                        return Response({'error': f'Permission with codename "{permission_codename}" not found.'}, 
                                        status=status.HTTP_404_NOT_FOUND)

                return Response({'message': 'Permissions updated successfully'}, status=status.HTTP_200_OK)
            except customUser.DoesNotExist:
                return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
            except ContentType.DoesNotExist:
                return Response({'error': 'Model not found for the specified app and model name'}, status=status.HTTP_404_NOT_FOUND)
            except Exception as e:
                return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



def Get_particular_user_permission(request):
    content_type = ContentType.objects.get_for_model(Transaction)
    permissions = Permission.objects.filter(content_type=content_type)
    user = customUser.objects.get(username='vishal')
    user_permissions = user.user_permissions.all()
    has_add_permission = user.has_perm(f'{Transaction._meta.app_label}.add_{Transaction._meta.model_name}')
    print(f"User Vishal has add transaction permission: {has_add_permission}")


    #all current user permission
    for i in user_permissions:
        print(i,'----')
    
    return HttpResponse('ok')



from rest_framework.authentication import BasicAuthentication

class CreateTransactionView(APIView):
    authentication_classes=[BasicAuthentication]
    permission_classes = [IsAuthenticated]


    @check_permission('view', Transaction)
    def get(self,request):
        t1=Transaction.objects.all()
        s1=TransactionSerializers(t1,many=True)
        return Response(s1.data)
    



    """
    {
    "amount": "100.00",
    "description": "Payment for services rendered"
    }
    """

    @check_permission('add', Transaction)
    def post(self, request):
        # Get the authenticated user from the request
        user = request.user

        # Deserialize and validate the request data
        serializer = TransactionSerializer_data(data=request.data,context={'request': request})
        if serializer.is_valid():
            # Create the transaction and associate it with the user
            transaction = serializer.save()
            return Response(TransactionSerializer_data(transaction).data, status=status.HTTP_201_CREATED)

        # Return validation errors if the data is not valid
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

    """
    {
    "amount": "150.00",
    "description": "Updated description for the transaction"
    }
    """
    @check_permission('change', Transaction)
    def put(self, request, pk=None):
        try:
            transaction = Transaction.objects.get(pk=pk)
        except Transaction.DoesNotExist:
            return Response({"error": "Transaction not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = TransactionSerializer(transaction, data=request.data, partial=True)
        if serializer.is_valid():
            transaction = serializer.save()
            return Response(TransactionSerializer(transaction).data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    """
    DELETE /transactions/1/
    """
    @check_permission('delete', Transaction)
    def delete(self, request, pk=None):
        try:
            transaction = Transaction.objects.get(pk=pk)
        except Transaction.DoesNotExist:
            return Response({"error": "Transaction not found"}, status=status.HTTP_404_NOT_FOUND)
        
        transaction.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    

from django.apps import apps
class AllModelPermissionsView(APIView):
    def get(self, request):
        data = []

        # Iterate over all installed apps
        for app in apps.get_app_configs():
            # Iterate over all models in each app
            for model in app.get_models():
                # Get the content type for the model
                content_type = ContentType.objects.get_for_model(model)

                # Get all permissions related to the model
                permissions = Permission.objects.filter(content_type=content_type)

                # Structure the model data with its permissions
                model_data = {
                    'app_label': app.label,
                    'model_name': model._meta.model_name,
                    'permissions': [{'codename': perm.codename, 'name': perm.name} for perm in permissions]
                }
                data.append(model_data)

        # Return the data as JSON response
        return Response(data)