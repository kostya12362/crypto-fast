import os
import sys
import jinja2
from settings import config


class RenderTemplate:

    def __call__(self, base_html: str, **kwargs) -> str:
        template = os.path.join(config.BASE_DIR, 'templates', base_html)
        if not os.path.exists(template):
            print('No template file present: %s' % template)
            sys.exit()
        template_loader = jinja2.FileSystemLoader(searchpath="/")
        template_env = jinja2.Environment(loader=template_loader)
        temp = template_env.get_template(template)
        return str(temp.render(**kwargs))


render_template = RenderTemplate()
