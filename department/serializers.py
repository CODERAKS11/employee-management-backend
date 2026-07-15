import re
from rest_framework import serializers
from .models import Department

class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = '__all__'

    def validate_department_name(self, value):
        value = value.strip()
        
        # 1. Length Check
        if len(value) < 2:
            raise serializers.ValidationError("Department name is too short.")
            
        # 2. Composition Check (Allow letters, spaces, ampersands, hyphens, brackets)
        if not re.match(r"^[a-zA-Z\s&\-\(\)]+$", value):
            raise serializers.ValidationError(
                "Department name can only contain letters, spaces, and symbols like &, -, (, )."
            )
            
        # 3. Case-Insensitive Uniqueness Check
        qs = Department.objects.filter(department_name__iexact=value)
        if self.instance: # Exclude current department if updating
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise serializers.ValidationError(
                f"A department named '{value}' already exists."
            )
            
        return value
