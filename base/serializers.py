from rest_framework import serializers
from .models import customUser,ROLE_CHOICES,Transaction


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = customUser
        fields = ['username', 'email', 'password', 'role', 'first_name', 'last_name']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        user = customUser.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            role=validated_data['role'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
        )
        return user

    def update(self, instance, validated_data):
        instance.username = validated_data.get('username', instance.username)
        instance.email = validated_data.get('email', instance.email)
        instance.role = validated_data.get('role', instance.role)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        
        if 'password' in validated_data:
            instance.set_password(validated_data['password'])
        
        instance.save()
        return instance


class RoleAssignmentSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()
    role = serializers.ChoiceField(choices=[('admin', 'Admin'), ('manager', 'Manager'), ('user', 'User')])

    def validate_user_id(self, value):
        try:
            customUser.objects.get(pk=value)
        except customUser.DoesNotExist:
            raise serializers.ValidationError("User with this ID does not exist.")
        return value

class AddUserToGroupsSerializer(serializers.Serializer):
    username=serializers.CharField()
    groups = serializers.ChoiceField(choices=ROLE_CHOICES)


class PermissionAssignmentSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    permission_codename = serializers.CharField(max_length=255)


class TransactionSerializer(serializers.ModelSerializer):
    username = serializers.CharField(write_only=True)
    user = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Transaction
        fields = ['id', 'user', 'username', 'amount', 'description', 'created_at']
        extra_kwargs = {
            'user': {'read_only': True}
        }

class TransactionSerializers(serializers.ModelSerializer):
    class Meta:
        model=Transaction
        fields='__all__'


class PermissionAssignmentSerializer2(serializers.Serializer):
    username = serializers.CharField()
    app_label = serializers.CharField()
    model_name = serializers.CharField()
    permission_codenames = serializers.ListField(
        child=serializers.CharField(), 
        allow_empty=False,
        help_text="A list of permission codenames to assign to the user."
    )


class TransactionSerializer_data(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ['user', 'amount', 'description', 'created_at']
        read_only_fields = ['user', 'created_at']

    def create(self, validated_data):
        # Get the user from the context
        user = self.context['request'].user
        print('user----',user)
        validated_data.pop('user', None)
        # Create the transaction with the user and other validated data
        transaction = Transaction.objects.create(user=user, **validated_data)
        print('----',transaction)
        return transaction
    


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = customUser
        fields = ['username', 'email', 'password']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        user = customUser.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
        )
        return user

    def update(self, instance, validated_data):
        instance.username = validated_data.get('username', instance.username)
        instance.email = validated_data.get('email', instance.email)

        if 'password' in validated_data:
            instance.set_password(validated_data['password'])

        instance.save()
        return instance