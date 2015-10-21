import copy


def pre_process(generator):
    if 'partitions' not in generator.mdvar._global:
        return

    partitions = generator.mdvar._global['partitions'].split(',')
    for partition in partitions:
        generate_page(generator, partition)
        generate_body(generator, partition)
        generate_content(generator, partition)
        generate_sidebar(generator, partition, partitions)

    generate_sidebar(generator, 'home', partitions)
    generate_sidebar(generator, 'blog', partitions)

    generate_js(generator, partitions)



PAGE = '''
<!doctype html>
<html lang="en">
${SNIPPET:head}
${SNIPPET:partition_body}
</html>
'''
def generate_page(generator, partition):
    generator.loaded['page'].setContent(partition, PAGE.replace('partition', partition))


BODY = '''
<body>
<div id="layout">
	${SNIPPET:navigator}
    <div class="cover">
	    ${SNIPPET:partition_cover}
    </div>

    <div class="content">
	    ${SNIPPET:partition_content}
    </div>
</div>
</body>
'''
def generate_body(generator, partition):
    generator.loaded['snippet'].setContent(partition + '_body', BODY.replace('partition', partition))


CONTENT = '''
<div class="container">
${LIST:post_item[dst:posts][slices:5][filter:R_partition:${CALL:BlogSelector[name:get_cur_partition][arguments:R_partition]}]}
${CALL:BlogDirect[name:page_direct][arguments:posts,5,R_partition,${PATH:temp_cur_R_partition}]}
</div>
'''
def generate_content(generator, partition):
    generator.loaded['snippet'].setContent(partition + '_content', CONTENT.replace('R_partition', partition))


COVER = '''
<div class="container">
<h1><a class="" href="${PATH:root}/index.html">${GLOBAL:blogname}</a><a href="${RSS:}"><span class="glyphicon glyphicon-signal"></span></a></h1>
        <p>${GLOBAL:desc}</p>
</div>
<div class="subnav container">
<ul>
        to_replace
</ul>
</div>
'''
LI = '''
<li class="dropdown mdnav"><a href="#" class="dropdown-toggle" data-toggle="dropdown">
by partition
<span class="caret"></span></a>
ul_to_replace
</li>
'''
UL = '''
<ul class="dropdown-menu" role="menu">
${CALL:BlogSelector[name:generate_partition][arguments:r_partition,posts,r_cur_partition_page]}
</ul>
'''

def generate_sidebar(generator, cur_partition, partitions):
    cover = copy.deepcopy(COVER)

    li_lines = []
    for part in partitions:
        ul_lines = []
        ul_lines.append(UL.replace('r_cur_partition_page', cur_partition + '_page').replace('r_partition', part))
        to_append = LI.replace('partition', part.upper()).replace('ul_to_replace', '\n'.join(ul_lines))
        li_lines.append(to_append)

    cover = cover.replace('to_replace', '\n'.join(li_lines))

    if cur_partition == 'home':
        generator.loaded['snippet'].setContent('cover', cover)
    elif cur_partition == 'blog':
        generator.loaded['snippet'].setContent('blog_cover', cover)
    else:
        generator.loaded['snippet'].setContent(cur_partition + '_cover', cover)

JS_FRAMEWORK_BEGIN = '$(document).ready(function(){'
JS_FRAMEWORK_END= '})'
def generate_js(generator, partitions):
    lines = []
    for part in partitions:
        lines.append('$("#by'+ part + '").click(function() {')
        lines.append('$("#' + part + 'box").fadeToggle(100)')
        for otherpart in partitions:
            if otherpart is not part:
                lines.append('$("#' + otherpart + 'box").hide()')
        lines.append('})')

    lines.insert(0, JS_FRAMEWORK_BEGIN)
    lines.append(JS_FRAMEWORK_END)

    with open(generator.mdvar._path['dst_prefix'] + 'js/filter.js', 'w') as f:
        f.write('\n'.join(lines))
