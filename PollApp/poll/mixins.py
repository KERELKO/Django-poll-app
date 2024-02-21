from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.detail import SingleObjectMixin
from django.http import HttpResponse


class OwnerQuerySetMixin:
	"""
	Queryset for models that have 'owner' field, 
	return queryset where request.user is owner
	"""
	def get_queryset(self):
		qs = super().get_queryset()
		return qs.filter(owner=self.request.user)


class OwnerEditMixin(
	LoginRequiredMixin, 
	OwnerQuerySetMixin,
	SingleObjectMixin):
	"""
	Prevent user which is not owner of the instance
	to edit the instance
	"""
	model = None

	def dispatch(self, request, pk, *args, **kwargs):
		owner =self.get_object().owner
		if owner != self.request.user:
			return HttpResponse('You don\'t have permissions!')
		return super().dispatch(request, *args, **kwargs)
