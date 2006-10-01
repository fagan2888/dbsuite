#!/bin/env python
# $Header$
# vim: set noet sw=4 ts=4:

from db.trigger import Trigger
from output.html.w3.document import W3MainDocument

class W3TriggerDocument(W3MainDocument):
	def __init__(self, site, trigger):
		assert isinstance(trigger, Trigger)
		super(W3TriggerDocument, self).__init__(site, trigger)

	def create_sections(self):
		self.section('description', 'Description')
		self.add(self.p(self.format_description(self.dbobject.description)))
		self.section('attributes', 'Attributes')
		self.add(self.p("""The following table notes various "vital statistics"
			of the trigger."""))
		self.add(self.table(
			head=[(
				'Attribute',
				'Value',
				'Attribute',
				'Value'
			)],
			data=[
				(
					self.a('created.html', 'Created', popup=True),
					self.dbobject.created,
					self.a('createdby.html', 'Created By', popup=True),
					self.dbobject.definer,
				),
				(
					'Relation',
					self.a_to(self.dbobject.relation, qualifiedname=True),
					self.a('valid.html', 'Valid', popup=True),
					self.dbobject.valid,
				),
				(
					self.a('triggertiming.html', 'Timing', popup=True),
					self.dbobject.triggerTime,
					self.a('triggerevent.html', 'Event', popup=True),
					self.dbobject.triggerEvent,
				),
			]))
		self.section('sql', 'SQL Definition')
		self.add(self.p("""The SQL which created the trigger is given below.
			Note that, in the process of storing the definition of a trigger,
			DB2 removes much of the formatting, hence the formatting in the
			statement below (which this system attempts to reconstruct) is not
			necessarily the formatting of the original statement."""))
		self.add(self.pre(self.format_sql(self.dbobject.createSql, terminator='!'), attrs={'class': 'sql'}))
