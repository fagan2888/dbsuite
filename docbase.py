#!/bin/env python
# $Header$
# vim: set noet sw=4 ts=4:

"""Defines all abstract base classes"""

__all__ = ['DocBase']

class DocObjectBase(object):
	"""Base class for all documented database objects"""

	def __init__(self, parent, name):
		"""Initializes an instance of the class"""
		assert not parent or isinstance(parent, DocObjectBase)
		self.__parent = parent
		self.__name = name
	
	def getParent(self):
		return self.__parent
	
	def getName(self):
		return self.__name
	
	def getTypeName(self):
		return "Object"
	
	def getDescription(self):
		return "No description in system catalog"
	
	def getIdentifier(self):
		return id(self)

	def getQualifiedName(self):
		result = self.name
		if self.parent: result = self.parent.qualifiedName + "." + result
		return result

	def isSystemObject(self):
		"""Returns True if the database object is a system-defined object (like a system catalog table)"""
		result = self.name in set(["NULLID", "SQLJ", "SYSCAT", "SYSFUN", "SYSIBM", "SYSPROC", "SYSSTAT", "SYSTOOLS"])
		if self.parent: result |= self.parent.isSystemObject
		return result

	def __str__(self):
		"""Return a string representation of the object"""
		return self.qualifiedName
	
	# Use the lambda trick to make property getter methods "virtual"
	parent = property(lambda self: self.getParent(), doc="""Returns the parent database object (e.g. the parent of a table is a schema)""")
	identifier = property(lambda self: self.getIdentifier(), doc="""Returns a unique identifier for this object (suitable for use as the basis for a unique filename, for example)""")
	name = property(lambda self: self.getName(), doc="""Returns the unqualified name of the database object""")
	qualifiedName = property(lambda self: self.getQualifiedName(), doc="""Returns the fully qualified name of the database object""")
	typeName = property(lambda self: self.getTypeName(), doc="""Returns the human readable name of the object's type""")
	description = property(lambda self: self.getDescription(), doc="""Returns a brief description of the object""")

def main():
	pass

if __name__ == "__main__":
	main()
