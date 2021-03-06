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


class TablespaceDocument(HTMLObjectDocument):
    def generate_body(self):
        tag = self.tag
        body = super(TablespaceDocument, self).generate_body()
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
                            tag.td(self.site.url_document('tables.html').link()),
                            tag.td(len(self.dbobject.table_list))
                        ),
                        tag.tr(
                            tag.td(self.site.url_document('createdby.html').link()),
                            tag.td(self.dbobject.owner),
                            tag.td(self.site.url_document('indexes.html').link()),
                            tag.td(len(self.dbobject.index_list))
                        ),
                        tag.tr(
                            tag.td(self.site.url_document('tbspacetype.html').link()),
                            tag.td(self.dbobject.type, colspan=3)
                        )
                    ),
                    summary='Tablespace attributes'
                ),
                class_='section',
                id='attributes'
            ),
            tag.div(
                tag.h3('Tables'),
                tag.p("""The following table lists all tables that store
                    their data (but not necessarily their indexes or LOB
                    data) in this tablespace. Click on a table's name to
                    view the documentation for that table."""),
                tag.table(
                    tag.thead(
                        tag.tr(
                            tag.th('Name', class_='nowrap'),
                            tag.th('Description', class_='nosort')
                        )
                    ),
                    tag.tbody((
                        tag.tr(
                            tag.td(self.site.link_to(table), class_='nowrap'),
                            tag.td(self.format_comment(table.description, summary=True))
                        ) for table in self.dbobject.table_list
                    )),
                    id='table-ts',
                    summary='Tablespace tables'
                ),
                class_='section',
                id='tables'
            ) if len(self.dbobject.table_list) > 0 else '',
            tag.div(
                tag.h3('Indexes'),
                tag.p("""The following table lists all indexes that store
                    their data in this tablespace, and the tables each
                    index applies to. Click on an index's name to view the
                    documentation for that index. Click on a table's name
                    to view the documentation for that table."""),
                tag.table(
                    tag.thead(
                        tag.tr(
                            tag.th('Name', class_='nowrap'),
                            tag.th('Applies To', class_='nowrap'),
                            tag.th('Description', class_='nosort')
                        )
                    ),
                    tag.tbody((
                        tag.tr(
                            tag.td(self.site.link_to(index), class_='nowrap'),
                            tag.td(self.site.link_to(index.table), class_='nowrap'),
                            tag.td(self.format_comment(index.description, summary=True))
                        ) for index in self.dbobject.index_list
                    )),
                    id='index-ts',
                    summary='Tablespace indexes'
                ),
                class_='section',
                id='indexes'
            ) if len(self.dbobject.index_list) > 0 else ''
        ))
        return body

