# vim: set et sw=4 sts=4:

# Copyright 2012 Dave Hughes.
#
# This file is part of dbsuite.
#
# dbsuite is free software: you can redistribute it and/or modify it under the
# terms of the GNU General Public License as published by the Free Software
# Foundation, either version 3 of the License, or (at your option) any later
# version.
#
# dbsuite is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
# A PARTICULAR PURPOSE.  See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with
# dbsuite.  If not, see <http://www.gnu.org/licenses/>.

from __future__ import (
    unicode_literals,
    print_function,
    absolute_import,
    division,
    )

from dbsuite.plugins.html.document import HTMLObjectDocument


class DatabaseDocument(HTMLObjectDocument):
    def generate_body(self):
        indexes = []
        if self.site.index_docs:
            ixdoc = self.site.first_index
            while ixdoc:
                indexes.append(ixdoc)
                ixdoc = ixdoc.next
        tag = self.tag
        body = super(DatabaseDocument, self).generate_body()
        tag._append(body, (
            tag.div(
                tag.h3('Description'),
                self.format_comment(self.dbobject.description),
                class_='section',
                id='description'
            ),
            tag.div(
                tag.h3('Schemas'),
                tag.p("""The following table contains all schemas (logical
                    object containers) in the database. Click on a schema
                    name to view the documentation for that schema,
                    including a list of all objects that exist within it."""),
                tag.table(
                    tag.thead(
                        tag.tr(
                            tag.th('Name', class_='nowrap'),
                            tag.th('Description', class_='nosort')
                        )
                    ),
                    tag.tbody((
                        tag.tr(
                            tag.td(self.site.link_to(schema), class_='nowrap'),
                            tag.td(self.format_comment(schema.description, summary=True))
                        ) for schema in self.dbobject.schema_list
                    )),
                    id='schema-ts',
                    summary='Database schemas'
                ),
                class_='section',
                id='schemas'
            ) if len(self.dbobject.schema_list) > 0 else '',
            tag.div(
                tag.h3('Tablespaces'),
                tag.p("""The following table contains all tablespaces
                    (physical object containers) in the database. Click on
                    a tablespace name to view the documentation for that
                    tablespace, including a list of all tables and/or
                    indexes that exist within it."""),
                tag.table(
                    tag.thead(
                        tag.tr(
                            tag.th('Name', class_='nowrap'),
                            tag.th('Description', class_='nosort')
                        )
                    ),
                    tag.tbody((
                        tag.tr(
                            tag.td(self.site.link_to(tbspace), class_='nowrap'),
                            tag.td(self.format_comment(tbspace.description, summary=True))
                        ) for tbspace in self.dbobject.tablespace_list
                    )),
                    id='tbspace-ts',
                    summary='Database tablespaces'
                ),
                class_='section',
                id='tbspaces'
            ) if self.site.tbspace_list and len(self.dbobject.tablespace_list) > 0 else '',
            tag.div(
                tag.h3('Alphabetical Indexes'),
                tag.p("""These are alphabetical lists of objects in the
                    database. Indexes are constructed by type (including
                    generic types like Relation which encompasses Tables,
                    Views, and Aliases), and entries are indexed by their
                    unqualified name."""),
                tag.ul(
                    tag.li(ixdoc.link())
                    for ixdoc in indexes
                ),
                class_='section',
                id='indexes'
            ) if len(indexes) > 0 else ''
        ))
        return body

