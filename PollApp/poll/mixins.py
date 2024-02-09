from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import get_object_or_404


class OwnerQuerySetMixin:
	def get_queryset(self):
		qs = super().get_queryset()
		return qs.filter(owner=self.request.user)


class OwnerEditMixin(LoginRequiredMixin, OwnerQuerySetMixin):
	model = None

	def get_model(self):
		return self.model

	def dispatch(self, request, *args, **kwargs):
		owner = get_object_or_404(self.get_model(), id=self.kwargs['pk']).owner
		if owner != self.request.user:
			return HttpResponse('You don\'t have permissions!')
		return super().dispatch(request, *args, **kwargs)
