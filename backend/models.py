from django.db import models
from django.contrib.auth.models import User


class UserPortfolio(models.Model):
	"""Stores a generated portfolio for a specific authenticated user.

	The "result" field holds the raw response payload from the
	portfolio generation endpoint so the frontend can render it
	exactly the same way when the user returns.
	"""

	user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="portfolios")
	name = models.CharField(max_length=255, blank=True)
	sectors = models.JSONField(blank=True, null=True)
	commodities = models.JSONField(blank=True, null=True)
	result = models.JSONField()
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	class Meta:
		ordering = ["-created_at"]

	def __str__(self) -> str:  # pragma: no cover - simple convenience
		return self.name or f"Portfolio {self.pk} for {self.user.username}"

