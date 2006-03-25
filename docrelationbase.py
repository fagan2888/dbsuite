#!/bin/env python
# $Header$
# vim: set noet sw=4 ts=4:

from string import Template
from docbase import DocObjectBase
from docutil import formatIdentifier

__all__ = ['DocRelationObject', 'DocConstraint']

class DocRelationObject(DocObjectBase):
	"""Base class for database objects that belong directly to a relation"""
	
	def __getRelation(self):
		return self.parent
	
	def __getSchema(self):
		return self.parent.parent
	
	def __getDatabase(self):
		return self.parent.parent.parent
	
	relation = property(__getRelation, doc="""The relation that owns the object""")
	schema = property(__getSchema, doc="""The schema that contains the object""")
	database = property(__getDatabase, doc="""The database that contains the object""")

class DocConstraint(DocRelationObject):
	"""Base class for constraints that belong in a relation (e.g. primary keys, checks, etc.)"""
	
	def __getTable(self):
		return self.parent
	
	def getTypeName(self):
		return "Constraint"

	def getIdentifier(self):
		return "constraint_%s_%s_%s" % (self.relation.name, self.schema.name, self.name)

	def getFields(self):
		raise NotImplementedError
	
	def getDefinitionStr(self):
		raise NotImplementedError
	
	def __getCreateSql(self):
		sql = Template('ALTER TABLE $schema.$table ADD $constdef;')
		return sql.substitute({
			'schema': formatIdentifier(self.table.schema.name),
			'table': formatIdentifier(self.table.name),
			'constdef': self.definitionStr
		})
	
	def __getDropSql(self):
		sql = Template('ALTER TABLE $schema.$table DROP CONSTRAINT $const;')
		return sql.substitute({
			'schema': formatIdentifier(self.table.schema.name),
			'table': formatIdentifier(self.table.name),
			'const': formatIdentifier(self.name)
		})
	
	# Use the lambda trick to allow property getter methods to be overridden
	fields = property(lambda self: self.getFields(), doc="""The fields constrained by this constraint""")
	definitionStr = property(lambda self: self.getDefinitionStr(), doc="""The attributes of the constraint formatted for use in an ALTER TABLE or CREATE TABLE statement""")
	table = property(__getTable, doc="""The table that owns the constraint""")
	createSql = property(__getCreateSql, doc="""The SQL that can be used to create the constraint""")
	dropSql = property(__getDropSql, doc="""The SQL that can be used to drop the constraint""")

def main():
	pass

if __name__ == "__main__":
	main()