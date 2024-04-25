import yaml
import xml.etree.ElementTree as xml_tree

with open('feed.yaml', 'r') as file:
  yaml_data = yaml.safe_load(file)

  rss_element = xml_tree.Element('rss', {'version':'2.0',
    'xmlns:itunes':'http://www.itunes.com/dtds/podcast-1.0.dtd',
    'xmlns:content':'http://purl.org/rss/1.0/modules/content/'})

channel_element = xml_tree.SubElement(rss_element, 'channel')

link_prefix = yaml_data['link']

xml_tree.SubElement(channel_element, 'title').text = yaml_data['title']
xml_tree.SubElement(channel_element, 'format').text = yaml_data['format']
xml_tree.SubElement(channel_element, 'subtitle').text = yaml_data['subtitle']
xml_tree.SubElement(channel_element, 'itunes:author').text = yaml_data['author']
xml_tree.SubElement(channel_element, 'description').text = yaml_data['description']
xml_tree.SubElement(channel_element, 'itunes:image', {'href': link_prefix + yaml_data['image']})
xml_tree.SubElement(channel_element, 'language').text = yaml_data['language']
xml_tree.SubElement(channel_element, 'link').text = link_prefix

xml_tree.SubElement(channel_element, 'itunes:category', {'text': yaml_data['category']})

for item in yaml_data['item']:
    item_element = xml_tree.SubElement(channel_element, 'item')
    
    title_element = xml_tree.SubElement(item_element, 'title')
    title_element.text = item['title']

    author_element = xml_tree.SubElement(item_element, 'itunes:author')
    author_element.text = yaml_data['author']

    description_element = xml_tree.SubElement(item_element, 'description')
    description_element.text = item['description']

    duration_element = xml_tree.SubElement(item_element, 'itunes:duration')
    duration_element.text = item['duration']

    pubdate_element = xml_tree.SubElement(item_element, 'pubDate')
    pubdate_element.text = item['published']

    enclosure_attributes = {
        'url': link_prefix + item['file'],
        'type': 'audio/mpeg',
        'length': item['length']
    }
    enclosure_element = xml_tree.SubElement(item_element, 'enclosure', enclosure_attributes)


output_tree = xml_tree.ElementTree(rss_element)
output_tree.write('podcast.xml', encoding='UTF-8', xml_declaration=True)
