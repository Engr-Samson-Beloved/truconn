from .models import Org, AccessRequest
from rest_framework import serializers
from accounts.models import CustomUser


class OrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Org
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='name', read_only=True)  

    class Meta:
        model = CustomUser
        fields = ['id', 'name', 'email'] 
        read_only_fields = ['id', 'name', 'email']

class AccessRequestSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)          
    organization = UserSerializer(read_only=True)

    class Meta:
        model = AccessRequest
        fields = ['id', 'user', 'organization', 'consent', 'status', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']


class CitizenListSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()
    access_requests = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = ['id', 'full_name', 'access_requests']

    def get_full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"

    def get_access_requests(self, obj):
        request = self.context.get('request')
        organization = Org.objects.get(user=request.user)

        requests = AccessRequest.objects.filter(user=obj, organization=organization)

        result = []
        for r in requests:
            result.append({
                'consent': r.consent.name,
                'purpose': r.purpose,
                'status': r.status,
                'requested_at': r.requested_at
            })
        return result
