from django.contrib import admin
from .models import User, Contact, Pricing, Candidate, Vote, Position, Election


admin.site.register(User)
admin.site.register(Contact)
admin.site.register(Pricing)
admin.site.register(Candidate)
admin.site.register(Vote)
admin.site.register(Position)
admin.site.register(Election)
