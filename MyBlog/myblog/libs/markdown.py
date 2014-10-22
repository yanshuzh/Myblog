#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
from StringIO import StringIO
import misaka as m

from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import get_lexer_by_name

from tornado.escape import to_unicode
from tornado.escape import xhtml_escape


class AkioRender(m.HtmlRenderer, m.SmartyPants):

    def block_code(self, text, lang):
        if lang:
            lexer = get_lexer_by_name(lang, stripall=True)
        else:
            return '<pre><code>%s</code></pre>' % xhtml_escape(text.strip())

        formatter = HtmlFormatter(
            noclasses=False,
            linenos=True,
        )

        return '<div class="highlight-pre">%s</div>' % \
                        highlight(text, lexer, formatter)

    def autolink(self, link, is_email):
        if is_email:
            mailto = "".join(['&#%d;' % ord(letter) for letter in "mailto:"])
            email = "".join(['&#%d;' % ord(letter) for letter in link])
            url = mailto + email
            return '<a href="%(url)s">%(link)s</a>' % {'url': url, 'link': email}

        title = link.replace('http://', '').replace('https://', '')
        if len(title) > 30:
            title = title[:24] + "..."

        pattern = r'http://v.youku.com/v_show/id_([a-zA-Z0-9\=]+).html'
        match = re.match(pattern, link)
        if not match:
            pattern = r'http://v.youku.com/v_show/id_([a-zA-Z0-9\=]+).html'
            match = re.match(pattern, link)
        if match:
            value = (
                r'<div><embed src='
                r'"http://player.youku.com/player.php/sid/%(id)s/v.swf" '
                r'quality="high" width="480" height="400" '
                r'type="application/x-shockwave-flash" /></div>'
            ) % {'id': match.group(1)}
            return value

        return '<a href="%s">%s</a>' % (link, title)

def markdown(text):
    text = to_unicode(text)
    render = AkioRender(flags=m.HTML_USE_XHTML)
    md = m.Markdown(
        render,
        extensions=m.EXT_FENCED_CODE | m.EXT_AUTOLINK,
    )
    return md.render(text)

