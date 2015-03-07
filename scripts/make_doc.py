import os
import shutil
import sys

# hack sys.path to be able to import markdown
sys.path.append(os.path.join(os.path.dirname(os.getcwd()),
    'www','src','Lib','browser'))
import markdown

# path of markdown files
md_doc_path = os.path.join(os.path.dirname(os.getcwd()),'www','doc')

static_doc_path = os.path.join(os.path.dirname(os.getcwd()),'www','static_doc')
src_paths = [static_doc_path, os.path.join(static_doc_path,'cookbook')]

for path in src_paths:
    if not os.path.exists(path):
        os.mkdir(path)

shutil.copy(os.path.join(md_doc_path,'doc_brython.css'),
    os.path.join(static_doc_path,'doc_brython.css'))

for lang in ['fr', 'en', 'es']: 
    dest_path = os.path.join(static_doc_path, lang)
    dest_paths = [dest_path, os.path.join(dest_path,'cookbook')]
        
    index = open(os.path.join(md_doc_path,lang,'index_static.html'), 'rb').read()
    index = index.decode('utf-8')

    for path in dest_paths:
        if not os.path.exists(path):
            os.mkdir(path)

    print('static doc %s' %lang)
    for i, (src_path, dest_path) in enumerate(zip([os.path.join(md_doc_path, lang),
        os.path.join(md_doc_path,lang,'cookbook')], dest_paths)):
        for filename in os.listdir(src_path):
            ext = os.path.splitext(filename)[1]
            if ext=='.md':
                src = open(os.path.join(src_path, filename), 'rb').read()
                src = src.decode('utf-8')
                html, scripts = markdown.mark(src)
                out = open(os.path.join(dest_path,filename[:-3]+'.html'), 'wb')
                html = index.replace('<content>',html)
                html = html.replace('<prefix>','/'.join(['..']*(i+1)))
                if i==1:
                    html = html.replace('class="navig" href="',
                        'class="navig" href="../')
                if scripts:
                    html = html.replace('<scripts>',
                        '<script type="text/python">%s\n</script>' %'\n'.join(scripts))
                out.write(html.encode('utf-8'))
                out.close()
            elif ext=='.txt':
                shutil.copy(os.path.join(src_path, filename),
                    os.path.join(dest_path, filename))