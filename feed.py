import yaml
import xml.etree.ElementTree as xml_tree

with open('feed.yaml', 'r') as file:
    yaml_data = yaml.safe_load(file)

    #creates the rss elelement, and adds all of these attributes from args[1]
    rss_element = xml_tree.Element('rss', {'version':'2.0', 
    'xmlns:itunes':'http://www.itunes.com/dtds/podcast-1.0.dtd', 
    'xmlns:content':'http://purl.org/rss/1.0/modules/content/'
    })

#Creates the channel element inside the rss element
channel_element = xml_tree.SubElement(rss_element, 'channel')

#holds url for the GitHub page
#Saved as var to make things easier for everyone
link_prefix = yaml_data['link']

#Generates the subelements in the channel element of the rss element
xml_tree.SubElement(channel_element, 'title').text = yaml_data['title']
xml_tree.SubElement(channel_element, 'format').text = yaml_data['format']
xml_tree.SubElement(channel_element, 'subtitle').text = yaml_data['subtitle']
xml_tree.SubElement(channel_element, 'itunes:author').text = yaml_data['author']
xml_tree.SubElement(channel_element, 'description').text = yaml_data['description']

#the image element is different the image link is inside the tag like an attribute.
#the image is reached by combining the "link_prefix"(website url) and the value of "image"
#from "yaml_data".
xml_tree.SubElement(channel_element, 'itunes:image', {'href':link_prefix + yaml_data['image']})
xml_tree.SubElement(channel_element, 'itunes:category', {'text': yaml_data['category']})
xml_tree.SubElement(channel_element, 'language').text = yaml_data['language']
xml_tree.SubElement(channel_element, 'link').text = link_prefix


"""
Each item in the Rss feed is an episode of the podcast with various metadata about the episode
they can be iterated through with a loop
"""

for  item in yaml_data['item']:
    item_element = xml_tree.SubElement(channel_element, 'item')
    xml_tree.SubElement(item_element, 'title').text=item['title']
    xml_tree.SubElement(item_element, 'itunes:author').text=yaml_data['author']
    xml_tree.SubElement(item_element, 'description').text=item['description']
    xml_tree.SubElement(item_element, 'itunes:duration').text=item['duration']
    xml_tree.SubElement(item_element, 'pubDate').text=item['published']
    xml_tree.SubElement(item_element, 'title').text=item['title']

    #each item has an enclosure tag in it contains: URL, length, type  of the item
    enclosure = xml_tree.SubElement(item_element, 'enclosure', {
        'url' : link_prefix + item['file'], 
        'type': 'audio/mpeg', 
        'length': item['length']
        })
#generates the actual Rss tree
output_tree = xml_tree.ElementTree(rss_element)
#generates a new file called podcast.xml with the data from output_tree
output_tree.write('podcast.xml', encoding='UTF-8', xml_declaration =True)