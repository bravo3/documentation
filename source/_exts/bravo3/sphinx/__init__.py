from docutils.parsers.rst import Directive
from docutils import nodes


class HeroDirective(Directive):
    has_content = True

    def run(self):
        doc = nodes.inline()
        doc['classes'].append('hero')

        icon = nodes.inline()
        icon['classes'].append('fa fa-{}'.format(self.content[0]))
        doc.append(icon)

        for line in self.content[1:]:
            if not line:
                continue

            p = nodes.paragraph(None, line)
            doc.append(p)

        return [doc]


def setup(app):
    app.add_directive('hero', HeroDirective)
