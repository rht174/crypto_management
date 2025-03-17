from rest_framework import permissions


class OrganizationSpecificAccess(permissions.BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False

        if request.method in permissions.SAFE_METHODS:
            return True

        org_id = request.data.get('org_id')
        if org_id:
            return request.user.owned_organizations.filter(id=org_id).exists()
        return False

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return request.user.organizations.filter(id=obj.org_id.id).exists()
        return obj.org_id.owner == request.user
