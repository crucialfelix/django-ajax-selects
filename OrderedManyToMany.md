
Ordered ManyToMany fields without a full Through model
======================================================

When re-editing a previously saved model that has a ManyToMany field, the order of the recalled ids can be somewhat random.  
The user sees Arnold, Bosco, Cooly in the interface, saves, comes back later to edit it and he sees Bosco, Cooly, Arnold.  So he files a bug report.

A proper solution would be to use a separate Through model, an order field and the ability to drag the items in the interface to rearrange.  But a proper Through model would also introduce extra fields and that would be out of the scope of ajax_selects.  Maybe some future version.

It is possible however to offer an intuitive experience for the user: save them in the order they added them and the next time they edit it they should see them in same order.

Problem
-------

    class Agent(models.Model):
        name = models.CharField(blank=True, max_length=100)
    
    class Apartment(models.Model):
        agents = models.ManyToManyField(Agent)

When the AutoCompleteSelectMultipleField saves it does so by saving each relationship in the order they were added in the interface.
 
    # this query does not have a guaranteed order (especially on postgres)
    # and certainly not the order that we added them
    apartment.agents.all()


    # this retrieves the joined objects in the order of their id (the join table id)
    # and thus gets them in the order they were added
    apartment.agents.through.objects.filter(apt=self).select_related('agent').order_by('id')


Temporary Solution
------------------

    class AgentOrderedManyToManyField(models.ManyToManyField):
        """     regardless of using a through class,
                only the Manager of the related field is used for fetching the objects for many to many interfaces.
                with postgres especially this means that the sort order is not determinable other than by the related field's manager.

            this fetches from the join table, then fetches the Agents in the fixed id order
            the admin ensures that the agents are always saved in the fixed id order that the form was filled out with
        """
        def value_from_object(self,object):
            from company.models import Agent
            rel = getattr(object, self.attname)
            qry = {self.related.var_name:object}
            qs = rel.through.objects.filter(**qry).order_by('id')
            aids = qs.values_list('agent_id',flat=True)
            agents = dict( (a.pk,a) for a in Agent.objects.filter(pk__in=aids) )
            try:
                return [agents[aid] for aid in aids ]
            except KeyError:
                raise Exception("Agent is missing: %s > %s" % (aids,agents))

    class Apartment(models.Model):
        agents = AgentOrderedManyToManyField()


    class AgentLookup(object):

        def get_objects(self,ids):
            # now that we have a dependable ordering
            # we know the ids are in the order they were originally added
            # return models in original ordering
            ids = [int(id) for id in ids]
            agents = dict( (a.pk,a) for a in Agent.objects.filter(pk__in=ids) )
            return [agents[aid] for aid in ids]

