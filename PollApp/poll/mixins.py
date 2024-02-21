from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import get_object_or_404


class OwnerQuerySetMixin:
	"""
	Queryset for models that have 'owner' field, 
	return queryset where request.user is owner
	"""
	def get_queryset(self):
		qs = super().get_queryset()
		return qs.filter(owner=self.request.user)


class OwnerEditMixin(LoginRequiredMixin, OwnerQuerySetMixin):
	"""
	Prevent user which is not owner of the instance
	to edit the instance
	"""
	model = None

	def get_model(self):
		return self.model

	def dispatch(self, request, *args, **kwargs):
		owner = get_object_or_404(
			self.get_model(),
			id=self.kwargs['pk']
		).owner
		if owner != self.request.user:
			return HttpResponse('You don\'t have permissions!')
		return super().dispatch(request, *args, **kwargs)
