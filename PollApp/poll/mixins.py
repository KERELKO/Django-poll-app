from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.detail import SingleObjectMixin
from django.core.exceptions import PermissionDenied


class OwnerQuerySetMixin:
    """
    Queryset for models that have 'owner' field,
    returns queryset where request.user is owner
    """

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(owner=self.request.user)


class OwnerEditMixin(
    LoginRequiredMixin, OwnerQuerySetMixin, SingleObjectMixin
):
    """
    Prevents user which is not owner of the instance of the model
    to edit the instance of the model
    """
    model = None

    def dispatch(self, request, *args, **kwargs):
        owner = self.get_object().owner
        if owner != self.request.user:
            raise PermissionDenied('You don\'t have permissions!')
        return super().dispatch(request, *args, **kwargs)
