from rest_framework import permissions

class IsOwner(permissions.BasePermission):
    """
    Object-level permission to only allow owners of an object to edit it.
    Assumes the model instance has an `owner` attribute.
    """

    def has_permission(self, request, view):
        return bool(
            request.user and
            request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):

        # Instance must have an attribute named `owner`.
        return obj.owner == request.user

# class BlocklistPermission(permissions.BasePermission):
#     """
#     Global permission check for blocked IPs.

#     """
#     blocklist='127.0.0.1'
#     def has_permission(self, request, view):
#         ip_addr = request.META['REMOTE_ADDR']
#         blocked = blocklist
#         # blocked = Blocklist.objects.filter(ip_addr=ip_addr).exists()
#         return not blocked
