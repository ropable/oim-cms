from rest_framework import serializers
from tracking.models import DepartmentUser


class DepartmentUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = DepartmentUser

    # TODO
    #def create(self, validated_data):
    #    return DepartmentUser.objects.create(**validated_data)
    #
    #def update(self, instance, validated_data):
    #    instance.save()
    #    return instance
