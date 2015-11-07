
Ordered ManyToMany fields
=========================

When re-editing a previously saved model that has a ManyToMany field, the order of the recalled ids can be somewhat random.

The user sees Arnold, Bosco, Cooly in the interface; saves; comes back later to edit it and he sees Bosco, Cooly, Arnold.  So he files a bug report.


Problem
-------

Given these models::

    class Agent(models.Model):
        name = models.CharField(blank=True, max_length=100)

    class Apartment(models.Model):
        agents = models.ManyToManyField(Agent)

When the AutoCompleteSelectMultipleField saves it does so by saving each relationship in the order they were added in the interface.

But when Django ORM retrieves them, the order is not guaranteed::

    # This query does not have a guaranteed order (especially on postgres)
    # and certainly not the order that we added them.
    apartment.agents.all()

    # This retrieves the joined objects in the order of the join table pk
    # and thus gets them in the order they were added.
    apartment.agents.through.objects.filter(apt=self).select_related('agent').order_by('id')


Solution
--------

A proper solution would be to use a separate Through model, an order field and the ability to drag the items in the interface to rearrange.  But a proper Through model would also introduce extra fields and that would be out of the scope of ajax_selects.

However this method will also work.

Make a custom ManyToManyField::

    from django.db import models

    class AgentOrderedManyToManyField(models.ManyToManyField):

        """This fetches from the join table, then fetches the Agents in the fixed id order."""

        def value_from_object(self, object):
            rel = getattr(object, self.attname)
            qry = {self.related.var_name: object}
            qs = rel.through.objects.filter(**qry).order_by('id')
            aids = qs.values_list('agent_id', flat=True)
            agents = dict((a.pk, a) for a in Agent.objects.filter(pk__in=aids))
            return [agents[aid] for aid in aids if aid in agents]

    class Agent(models.Model):
        name = models.CharField(blank=True, max_length=100)

    class Apartment(models.Model):
        agents = AgentOrderedManyToManyField()
