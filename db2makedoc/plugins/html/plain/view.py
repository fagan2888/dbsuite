# vim: set noet sw=4 ts=4:

from db2makedoc.db import View
from db2makedoc.plugins.html.plain.document import PlainMainDocument, PlainGraphDocument

class PlainViewDocument(PlainMainDocument):
	def __init__(self, site, view):
		assert isinstance(view, View)
		super(PlainViewDocument, self).__init__(site, view)
	
	def _create_sections(self):
		fields = [obj for (name, obj) in sorted(self.dbobject.fields.items(), key=lambda (name, obj): name)]
		triggers = [obj for (name, obj) in sorted(self.dbobject.triggers.items(), key=lambda (name, obj): name)]
		dependencies = [obj for (name, obj) in sorted(self.dbobject.dependencies.items(), key=lambda (name, obj): name)]
		dependents = [obj for (name, obj) in sorted(self.dbobject.dependents.items(), key=lambda (name, obj): name)]
		self._section('description', 'Description')
		self._add(self._p(self._format_comment(self.dbobject.description)))
		self._section('attributes', 'Attributes')
		self._add(self._table(
			head=[(
				'Attribute',
				'Value',
				'Attribute',
				'Value'
			)],
			data=[
				(
					'Created',
					self.dbobject.created,
					'Owner',
					self.dbobject.owner,
				),
				(
					'Columns',
					len(self.dbobject.fields),
					'Read Only',
					self.dbobject.read_only,
				),
				(
					'Dependent Relations',
					len(self.dbobject.dependent_list),
					'Dependencies',
					len(self.dbobject.dependency_list),
				)
			]))
		if len(fields) > 0:
			self._section('fields', 'Fields')
			self._add(self._table(
				head=[(
					'#',
					'Name',
					'Type',
					'Nulls',
					'Description'
				)],
				data=[(
					field.position + 1,
					field.name,
					field.datatype_str,
					field.nullable,
					self._format_comment(field.description, summary=True)
				) for field in fields]
			))
		if len(triggers) > 0:
			self._section('triggers', 'Triggers')
			self._add(self._table(
				head=[(
					'Name',
					'Timing',
					'Event',
					'Description'
				)],
				data=[(
					self._a_to(trigger, qualifiedname=True),
					trigger.trigger_time,
					trigger.trigger_event,
					self._format_comment(trigger.description, summary=True)
				) for trigger in triggers]
			))
		if len(dependents) > 0:
			self._section('dependents', 'Dependent Relations')
			self._add(self._table(
				head=[(
					'Name',
					'Type',
					'Description'
				)],
				data=[(
					self._a_to(dep, qualifiedname=True),
					dep.type_name,
					self._format_comment(dep.description, summary=True)
				) for dep in dependents]
			))
		if len(dependencies) > 0:
			self._section('dependencies', 'Dependencies')
			self._add(self._table(
				head=[(
					'Name',
					'Type',
					'Description'
				)],
				data=[(
					self._a_to(dep, qualifiedname=True),
					dep.type_name,
					self._format_comment(dep.description, summary=True)
				) for dep in dependencies]
			))
		self._section('diagram', 'Diagram')
		self._add(self._img_of(self.dbobject))
		self._section('sql', 'SQL Definition')
		self._add(self._pre(self._format_sql(self.dbobject.create_sql),
			attrs={'class': 'sql'}))

class PlainViewGraph(PlainGraphDocument):
	def __init__(self, site, view):
		assert isinstance(view, View)
		super(PlainViewGraph, self).__init__(site, view)

	def _create_graph(self):
		super(PlainViewGraph, self)._create_graph()
		view = self.dbobject
		view_node = self._add_dbobject(view, selected=True)
		for dependent in view.dependent_list:
			dep_node = self._add_dbobject(dependent)
			dep_edge = dep_node.connect_to(view_node)
			dep_edge.label = '<uses>'
			dep_edge.arrowhead = 'onormal'
		for dependency in view.dependency_list:
			dep_node = self._add_dbobject(dependency)
			dep_edge = view_node.connect_to(dep_node)
			dep_edge.label = '<uses>'
			dep_edge.arrowhead = 'onormal'
