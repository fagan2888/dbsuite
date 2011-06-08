# vim: set noet sw=4 ts=4:

from dbsuite.db import Table
from dbsuite.plugins.html.document import HTMLObjectDocument, GraphObjectDocument

class AliasDocument(HTMLObjectDocument):
	def generate_body(self):
		tag = self.tag
		body = super(AliasDocument, self).generate_body()
		is_table = isinstance(self.dbobject.final_relation, Table)
		tag._append(body, (
			tag.div(
				tag.h3('Description'),
				self.format_comment(self.dbobject.description),
				class_='section',
				id='description'
			),
			tag.div(
				tag.h3('Attributes'),
				tag.p_attributes(self.dbobject),
				tag.table(
					tag.thead(
						tag.tr(
							tag.th('Attribute'),
							tag.th('Value'),
							tag.th('Attribute'),
							tag.th('Value')
						)
					),
					tag.tbody(
						tag.tr(
							tag.td(self.site.url_document('created.html').link()),
							tag.td(self.dbobject.created),
							tag.td(self.site.url_document('createdby.html').link()),
							tag.td(self.dbobject.owner)
						),
						tag.tr(
							tag.td('Alias For'),
							tag.td(self.site.link_to(self.dbobject.relation), colspan=3)
						)
					),
					summary='Alias attributes'
				),
				class_='section',
				id='attributes'
			),
			tag.div(
				tag.h3('Fields'),
				tag.p_relation_fields(self.dbobject),
				tag.table(
					tag.thead(
						tag.tr(
							tag.th('#', class_='nowrap'),
							tag.th('Name', class_='nowrap'),
							tag.th('Type', class_='nowrap'),
							tag.th('Nulls', class_='nowrap'),
							tag.th('Key Pos', class_='nowrap') if is_table else '',
							tag.th('Cardinality', class_='nowrap commas') if is_table else '',
							tag.th('Description', class_='nosort')
						)
					),
					tag.tbody((
						tag.tr(
							tag.td(field.position, class_='nowrap'),
							tag.td(field.name, class_='nowrap'),
							tag.td(field.datatype_str, class_='nowrap'),
							tag.td(field.nullable, class_='nowrap'),
							tag.td(field.key_index, class_='nowrap') if is_table else '',
							tag.td(field.cardinality, class_='nowrap') if is_table else '',
							tag.td(self.format_comment(field.description, summary=True))
						) for field in self.dbobject.field_list
					)),
					id='field-ts',
					summary='Alias fields'
				),
				class_='section',
				id='fields'
			) if len(self.dbobject.field_list) > 0 else '',
			tag.div(
				tag.h3('Dependent Relations'),
				tag.p_dependent_relations(self.dbobject),
				tag.p_tablesort(),
				tag.table(
					tag.thead(
						tag.tr(
							tag.th('Name', class_='nowrap'),
							tag.th('Type', class_='nowrap'),
							tag.th('Description', class_='nosort')
						)
					),
					tag.tbody((
						tag.tr(
							tag.td(self.site.link_to(dep), class_='nowrap'),
							tag.td(self.site.type_names[dep.__class__], class_='nowrap'),
							tag.td(self.format_comment(dep.description, summary=True))
						) for dep in self.dbobject.dependent_list
					)),
					id='dep-ts',
					summary='Alias dependents'
				),
				class_='section',
				id='dependents'
			) if len(self.dbobject.dependent_list) > 0 else '',
			tag.div(
				tag.h3('Diagram'),
				tag.p_diagram(self.dbobject),
				self.site.img_of(self.dbobject),
				class_='section',
				id='diagram'
			) if self.site.object_graph(self.dbobject) else '',
			tag.div(
				tag.h3('SQL Definition'),
				tag.p_sql_definition(self.dbobject),
				self.format_sql(self.dbobject.create_sql, number_lines=True, id='sql-def'),
				class_='section',
				id='sql'
			) if self.dbobject.create_sql else ''
		))
		return body


class AliasGraph(GraphObjectDocument):
	def generate(self):
		graph = super(AliasGraph, self).generate()
		alias = self.dbobject
		alias_node = graph.add(alias, selected=True)
		target_node = graph.add(alias.relation)
		target_edge = alias_node.connect_to(target_node)
		target_edge.label = '<for>'
		target_edge.arrowhead = 'onormal'
		for dependent in alias.dependent_list:
			dep_node = graph.add(dependent)
			dep_edge = dep_node.connect_to(alias_node)
			dep_edge.label = '<uses>'
			dep_edge.arrowhead = 'onormal'
		return graph
