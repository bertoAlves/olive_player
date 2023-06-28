from lxml import etree

tree = etree.parse('C:/Users/catar/OneDrive/Documentos/olive/api/player/database/db.xml')
str = etree.tostring(tree, pretty_print=True)

file = open('db_formatted.xml', 'wb')
file.write(str)