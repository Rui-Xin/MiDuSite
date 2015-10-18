def sort_img(entries):
    return sorted(entries, reverse=True, key=lambda x: int(x.meta['img'].replace('.jpg', '')))


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
<div id="layout" class="pure-g">
	${SNIPPET:navigator}
    <div class="sidebar pure-u-1 pure-u-md-1-4">
	    ${SNIPPET:partition_sidebar}
    </div>

    <div class="content pure-u-1 pure-u-md-3-4">
	    ${SNIPPET:partition_content}
    </div>
</div>
</body>
'''
def generate_body(generator, partition):
    generator.loaded['snippet'].setContent(partition + '_body', BODY.replace('partition', partition))


CONTENT = '''
<div id="thumbs" align="center">
${LIST:img_item[dst:info][slices:20][filter:R_partition:${CALL:Selector[name:get_cur_partition][arguments:R_partition]}]}
${CALL:Direct[name:page_direct][arguments:info,20,R_partition,${PATH:temp_cur_R_partition}]}

	<script src="${PATH:root}/js/lightbox.js"></script>
</div>
'''
def generate_content(generator, partition):
    generator.loaded['snippet'].setContent(partition + '_content', CONTENT.replace('R_partition', partition))


SIDEBAR = '''
<div class="header">
	<h1 class="brand-title"><a href="${PATH:root}/index.html">${GLOBAL:camerarollname}</a></h1>

	<ul class="nav-list">
    ul_to_replace
	</ul>
	</br>

    box_to_replace
</div>
'''
LI = '''
<li id="bypartition" class="nav-item">
<a class="pure-button">by cap_partition</a>
</li>
'''
BOX = '''
<div id="r_partitionbox" style="display:none" class="pure-menu pure-menu-scrollable custom-restricted">
<ul class="pure-menu-list">
${CALL:Selector[name:generate_partition][arguments:r_partition,info,r_cur_partition_page]}
</ul>
</div>
'''
BOX_V = '''
<div id="r_partitionbox" class="pure-menu pure-menu-scrollable custom-restricted">
<ul class="pure-menu-list">
${CALL:Selector[name:generate_partition][arguments:r_partition,info,r_cur_partition_page]}
</ul>
</div>
'''
def generate_sidebar(generator, cur_partition, partitions):
    sidebar = SIDEBAR

    li_lines = []
    box_lines = []
    for part in partitions:
        li_lines.append(LI.replace('cap_partition', part.upper()).replace('partition', part))
        if cur_partition == part:
            box_lines.append(BOX_V.replace('r_cur_partition_page', cur_partition + '_page').replace('r_partition', part))
        else:
            box_lines.append(BOX.replace('r_cur_partition_page', cur_partition + '_page').replace('r_partition', part))
    sidebar = sidebar.replace('ul_to_replace', '\n'.join(li_lines))
    sidebar = sidebar.replace('box_to_replace', '\n'.join(box_lines))

    if cur_partition == 'home':
        generator.loaded['snippet'].setContent('sidebar', sidebar)
    else:
        generator.loaded['snippet'].setContent(cur_partition + '_sidebar', sidebar)

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
