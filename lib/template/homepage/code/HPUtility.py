import os
import re
import sys
import copy
import shutil

NAV = '''
    <div class="navigator">
	<nav class="mdnav navbar navbar-default">
	<div class="container">
          <div class="navbar-header">
            <button type="button" class="navbar-toggle collapsed" data-toggle="collapse" data-target="#navbar" aria-expanded="false" aria-controls="navbar">
              <span class="sr-only">Toggle navigation</span>
              <span class="icon-bar"></span>
              <span class="icon-bar"></span>
              <span class="icon-bar"></span>
            </button>
          </div>
        <div class="navlogo">
        <a href="${PATH:root}/../index.html">Homepage</a>
        </div>
		<div id="navbar" class="navbar-collapse collapse" aria-expanded="false" style="height: 1px;">
			<ul class="sections nav navbar-nav">
				__links__
			</ul>
		</div>
	</div>
	</nav>
    </div>
'''


def sites(generator):
    lines = []
    sections = generator.mdvar._global['sections'].split(',')
    for section in sections:
        dst = section.replace(' ', '')

        if not os.path.exists('source/' + dst):
            print 'Section ' + dst + ' doesn\'t exist!'
            sys.exit(1)

        if os.path.exists('published/' + dst):
            shutil.rmtree('published/' + dst)
            os.mkdir('published/' + dst)

        matchboj = re.match('(.*)', dst)

        nav_links = []
        for sec_term in sections:
            sec_term_dst = sec_term.replace(' ', '')
            if sec_term == section:
                nav_links.append('<li class="section-term md-inactive"><a href="${PATH:root}/../' +
                            sec_term_dst +
                            '/index.html">' +
                            sec_term +
                            '</a></li>')
            else:
                nav_links.append('<li class="section-term"><a href="${PATH:root}/../' +
                            sec_term_dst +
                            '/index.html">' +
                            sec_term +
                            '</a></li>')
        navigator = NAV.replace('__links__', '\n'.join(nav_links))

        generator.generateSite(matchboj, navigator)
        site_link = os.path.relpath(dst +
                                    '/index.html')

        lines.append('<li class="section-term"><a href="' +
                     site_link +
                     '">' +
                     section +
                     '</a></li>')

    return '\n'.join(lines)


RECENT_ITEM = '''
<div class="posts">
	<h1 class="content-subhead">__action__</h1>

	<section class="post">
	<header class="post-header">

	<h2 class="post-title"><a href="__link__">__title__</a></h2>

	<p class="post-meta">
	Posted in __date__
	</p>
	</header>

	<div class="post-description">
		<p>
        __description__
		</p>
	</div>
	<a class="readmore" href="__link__">(More...)</a>

	</section>
</div>
'''

def get_recent(generator):
    lines = []
    feeds = []
    for site in generator.site_cached.values():
        feeds.extend(site.generator.get_feed())

    feeds_ordered = sorted(feeds, key=lambda x: x[0], reverse=True)[:10]

    for feed in feeds_ordered:
        meta = feed[1]
        recent_item = copy.copy(RECENT_ITEM)
        recent_item = recent_item.replace('__action__', meta['action'])
        recent_item = recent_item.replace('__link__', meta['link'])
        recent_item = recent_item.replace('__title__', meta['title'])
        recent_item = recent_item.replace('__date__', meta['date'])
        recent_item = recent_item.replace('__description__', meta['description'])
        recent_item = recent_item.replace('${PREFIX}', meta['section'] + '/')
        lines.append(recent_item)

    return '\n'.join(lines)
