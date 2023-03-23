from django.contrib.auth.backends import BaseBackend
from .models import Organization

#required use like this
# from django.contrib.auth.decorators import permission_required

# @permission_required('your_app.view_feature')
# def view_feature(request):
#     # View code here
# here your_app refers to

class FeaturePermissionBackend(BaseBackend):
    def has_perm(self, user_obj, perm, obj=None):
        if not user_obj.is_authenticated:
            return False

        if not obj or not isinstance(obj, Organization):
            return False

        # Check if the organization has the required feature
        feature_name = perm.split('.')[1]
        if obj.features.filter(name=feature_name).exists():
            return True

        # Check if the organization has a feature group that includes the required feature
        feature_group_name = feature_name + '_group'
        if obj.feature_groups.filter(name=feature_group_name, features__name=feature_name).exists():
            return True

        # Check if the organization has a feature plan that includes the required feature
        if obj.feature_plans.filter(features__name=feature_name).exists():
            return True

        # Check if the organization has a custom feature plan that includes the required feature
        if obj.custom_feature_plans.filter(features__name=feature_name).exists():
            return True

        return False
