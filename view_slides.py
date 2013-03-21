import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import tornado.escape
import tornado.template
from tornado.options import define, options
import markdown
import re


REVEALJS_PATH = './reveal.js'
#STATIC_URL_BASE = "/reveal.js/"
STATIC_URL_BASE = "http://lab.hakim.se/reveal-js/"
MD_FILE = './my_slides.md'
CONTAINER_TEMPLATE = './my_slides_template.html'
data_separator="\n---\n"   #three dash as the slide separator
data_vertical="\n\n\n"     #two blank lines


define("port", default=8000, help="run on the given port", type=int)
define("address", default="0.0.0.0", help="run on localhost")
define("debug", default=False, type=bool, help="run in debug mode")
tornado.options.parse_command_line()
if options.debug:
    import tornado.autoreload
    import logging
    logging.getLogger().setLevel(logging.DEBUG)
    options.address = '0.0.0.0'


def md2html(md_text, sep=data_separator):
    out_text = ''
    for section in re.split(sep, md_text):
        #if len(re.split(data_vertical, section))>1:
        #    section = md2html(section, sep=data_vertical)
        #else:
        #    section = markdown.markdown(section)
        section = markdown.markdown(section)
        out_text += section + '\n</section>\n\n<section>\n'
    out_text = '<section>\n'+out_text+'\n</section>'
    return out_text


class MarkDownMixIn:
    '''This can be mixed with tornado.web.RequestHandler class to add
       "render_markdown" method to the instance.
    '''
    def render_markdown(self, mdfile, extensions=['tables', 'headerid'],
                        container_template='templates/container.html'):
        with file(mdfile) as input_file:
            text = input_file.read()
        html = md2html(text)
        return self.render(container_template, content=html,
                           static_path=STATIC_URL_BASE)


class MarkDownHandler(tornado.web.RequestHandler, MarkDownMixIn):
    def get(self):
        self.render_markdown(MD_FILE, extensions=[],
                             container_template=CONTAINER_TEMPLATE)

APP_LIST = [
    (r"/", MarkDownHandler),

    (r"/reveal.js/(.*)", tornado.web.StaticFileHandler, {"path": REVEALJS_PATH}),
    (r"/assets/(.*)", tornado.web.StaticFileHandler, {"path": "./assets"}),
]

settings = {}


def main():
    application = tornado.web.Application(APP_LIST, **settings)
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(options.port, address=options.address)
    loop = tornado.ioloop.IOLoop.instance()
    if options.debug:
        tornado.autoreload.start(loop)
        logging.info('Server is running on "%s:%s"...' % (options.address, options.port))

    loop.start()


if __name__ == "__main__":
    main()

