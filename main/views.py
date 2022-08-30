from rest_framework import viewsets, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken

from .models import User
from .serializers import UserSerializer, CreateUserSerializer, ChangePasswordSerializer


# Create your views here.
class AuthViewSet(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'email': user.email
        })


class UserViewSet(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = User.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CreateUserSerializer

        if self.action == 'change_password':
            return ChangePasswordSerializer

        return UserSerializer

    @action(detail=True, methods=['put'])
    def change_password(self, request, pk=None):
        user = self.get_object()
        serializer = ChangePasswordSerializer(data=request.data, context=dict(user=user))

        if serializer.is_valid():
            user.set_password(serializer.validated_data['new_password'])
            user.save()
            return Response(status=status.HTTP_204_NO_CONTENT)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
