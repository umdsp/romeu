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
        
register.tag('alpha_list', print_alpha_list)