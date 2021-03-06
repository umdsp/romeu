# Copyright (C) 2012  University of Miami
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software Foundation,
# Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.

from django import template

register = template.Library()

def print_alpha_list(parser, token):
    try:
        tag_name, insert_text = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError("%r tag requires a single argument" % token.contents.split()[0])
        
    if not (insert_text[0] == insert_text[-1] and insert_text[0] in ('"', "'")):
        raise template.TemplateSyntaxError("%r tag's argument must be wrapped in quotes" % tag_name)
    
    return AlphaListNode(insert_text[1:-1])
    
class AlphaListNode(template.Node):
    def __init__(self, insert_text):
        self.insert_text = insert_text
    
    def render(self, context):
        alphalist = '<ul id="alphaselect">\n'
        alphalist += '<li><a href="/' + self.insert_text + '/">All</a></li>'
        alphalist += '<li><a href="/' + self.insert_text + '/a">A</a></li>'
        alphalist += '<li><a href="/' + self.insert_text + '/b">B</a></li>'
        alphalist += '<li><a href="/' + self.insert_text + '/c">C</a></li>'
        alphalist += '<li><a href="/' + self.insert_text + '/d">D</a></li>'
        alphalist += '<li><a href="/' + self.insert_text + '/e">E</a></li>'
        alphalist += '<li><a href="/' + self.insert_text + '/f">F</a></li>'
        alphalist += '<li><a href="/' + self.insert_text + '/g">G</a></li>'
        alphalist += '<li><a href="/' + self.insert_text + '/h">H</a></li>'
        alphalist += '<li><a href="/' + self.insert_text + '/i">I</a></li>'
        alphalist += '<li><a href="/' + self.insert_text + '/j">J</a></li>'
        alphalist += '<li><a href="/' + self.insert_text + '/k">K</a></li>'
        alphalist += '<li><a href="/' + self.insert_text + '/l">L</a></li>'
        alphalist += '<li><a href="/' + self.insert_text + '/m">M</a></li>'
        alphalist += '<li><a href="/' + self.insert_text + '/n">N</a></li>'
        alphalist += '<li><a href="/' + self.insert_text + '/o">O</a></li>'
        alphalist += '<li><a href="/' + self.insert_text + '/p">P</a></li>'
        alphalist += '<li><a href="/' + self.insert_text + '/q">Q</a></li>'
        alphalist += '<li><a href="/' + self.insert_text + '/r">R</a></li>'
        alphalist += '<li><a href="/' + self.insert_text + '/s">S</a></li>'
        alphalist += '<li><a href="/' + self.insert_text + '/t">T</a></li>'
        alphalist += '<li><a href="/' + self.insert_text + '/u">U</a></li>'
        alphalist += '<li><a href="/' + self.insert_text + '/v">V</a></li>'
        alphalist += '<li><a href="/' + self.insert_text + '/w">W</a></li>'
        alphalist += '<li><a href="/' + self.insert_text + '/x">X</a></li>'
        alphalist += '<li><a href="/' + self.insert_text + '/y">Y</a></li>'
        alphalist += '<li><a href="/' + self.insert_text + '/z">Z</a></li>'
        alphalist += '<li><a href="/' + self.insert_text + '/0">#</a></li>'
        alphalist += '</ul>'
        return alphalist
       
@register.simple_tag
def print_tags(tag_objects, query_str):
        result_dict = {}
        tag_list = "";
        for k,v in tag_objects:
                for obj in v:
                        for tag_name in obj.tags.names():
                                if tag_name in result_dict:
                                        result_dict[tag_name] += 1
                                else:
                                        result_dict[tag_name] = 1
        for key,val in result_dict.iteritems():
                tag_list += "<a href='/taggeditems?" + query_str + "&tag=" + key +"' onclick = \"$('#eventTags').tagit('createTag', '"+key+"');\">" + key + "(" + str(val) + ")</a>&nbsp;&nbsp;&nbsp;&nbsp;"
        return tag_list
 
register.tag('alpha_list', print_alpha_list)
