#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import datetime
import locale
import sys
import shutil
import sys  

import jinja2
import markdown

reload(sys)  
sys.setdefaultencoding('utf8')

LOCALE = 'es_DO.UTF-8' # Locale for use on dates formats and other backend stuff by python 
DEFAULT_LANG = 'es' # Default language for articles, goes in meta tag on site
DATE_FORMAT = '%Y-%m-%d' # Date format to use in the articles date

TAGS = ['Programación', 'Linux'] # General tags, for the meta keyworks tag
BLOG_NAME = '[ root@paranoia ~/blog ]# _' # Name of the blog, this is used for the title on <head></head> and the website header
AUTHOR = 'root' # Blog owner, for the meta author tag
BLOG_DESCRIPTION = 'Apuntes y notas de un newbie.' # Blog description, for the meta description tag

INDEX_FILE = "index.html" # The template file to render for generate de index file (using Jinja2)
ARTICLE_FILE = 'article.html' # Template file to render for generate the article/post (using Jinja2)
THEME_DIR = 'theme/' # Theme directory, where templates and css directories should be put
TEMPLATES_DIR = 'templates'   # Templates directory of jinja2 files
STATIC_PAGES = ['about.html', 'enlaces.html'] # List of static html pages, wich will not be proccessed with markdown
SOURCE_DIR = 'source/' # The directory of the plain text files in format markdown to generate the posts
IMAGES_DIR = 'images/' # Directory name of blog images
STYLES_DIR = 'css/'    # Directory name of css styles file
HTML_DIR = 'html/' # The output directory where the generated files will be put
SOURCE_FILE_EXT = 'md' # Extension of markdown files
OUTPUT_FILE_EXT = 'html' # Extension of ouput files

locale.setlocale(locale.LC_TIME, LOCALE)

class Article:
    def __init__(self):
        self.date = None
        self.title = ''
        self.tags = []
        self.lang = ''
        self.slug = ''
        self.author = ''
        self.content = ''


def convert_to_markdown(text):
    ''' Parse markdown formatted text into html '''
    html = markdown.markdown(text, extensions=['codehilite', 'extra'])
    return html

def proccess_template(file_name, template_name, template_vars, templates_dir=os.path.join(THEME_DIR, TEMPLATES_DIR), author=AUTHOR):
    ''' Convert a jinja2 template to a html file '''
    templateLoader = jinja2.FileSystemLoader(templates_dir) 
    templateEnv = jinja2.Environment( loader=templateLoader )
    template = templateEnv.get_template(template_name)
    
    template_vars['blog_name'] = BLOG_NAME
    template_vars['blog_description'] = BLOG_DESCRIPTION
    template_vars['author'] = author
    
    if not template_vars.has_key('tags'): template_vars['tags'] = ','.join([ tag.strip() for tag in TAGS ])
    
    outputText = template.render(template_vars)
    
    with open(os.path.join(HTML_DIR, '{0}.{1}'.format(file_name, OUTPUT_FILE_EXT)), 'w') as file:
       file.write(outputText)
       print("Created file %s.html" % (os.path.basename(file_name)))


def generate_article(date, title, content, tags, lang, file_name, author):
    ''' Generate article output file, render from jinja2 to html '''
    templateVars = { 
        'title' : title,
        'content' : content,
        'date' : date, 
        'tags' : ','.join([ tag.strip() for tag in tags ]),
        'lang' : lang
    }
    proccess_template(file_name, ARTICLE_FILE, templateVars, author=author)

       
def generate_index(articles):
    ''' Generate output file index for the articles of the blog '''
    articles.sort(key=lambda a: a.date, reverse=True)
    
    templateVars = { 
        'articles' : articles,
        'lang' : DEFAULT_LANG,
        'tags': ','.join([ tag.strip() for tag in TAGS ])
        }
    proccess_template('index', INDEX_FILE, templateVars)


def load_static_files():
    ''' Copy static files to destination folders '''
    try:
        if os.path.isdir(HTML_DIR):
            shutil.rmtree(HTML_DIR) # We will recreate output folder ahead

        # Copy images folder to output folder
        shutil.copytree(os.path.join(SOURCE_DIR, IMAGES_DIR),
                        os.path.join(HTML_DIR, IMAGES_DIR))
                        
        # Copy css folder to output folder
        shutil.copytree(os.path.join(THEME_DIR, STYLES_DIR),
                        os.path.join(HTML_DIR, STYLES_DIR))

        # Copy html static files to output folder     
        __static_pages = [ html for html in STATIC_PAGES 
                                if os.path.isfile(os.path.join(os.path.join(THEME_DIR, TEMPLATES_DIR), html)) 
                                    and html[-len(OUTPUT_FILE_EXT):] == OUTPUT_FILE_EXT ]
      
        for _html in __static_pages:
            proccess_template(_html[:-5], _html, {})
    except:
        print('An error has occured trying to load static files.')
        print(str(sys.exc_info()))
        sys.exit(-1)


if __name__ == "__main__":
    startTime = datetime.datetime.now()
    sources = [ f for f in os.listdir(SOURCE_DIR) 
                    if os.path.isfile(os.path.join(SOURCE_DIR, f)) 
                        and f[-(len(SOURCE_FILE_EXT)):] == SOURCE_FILE_EXT]
    articles = []
    
    print("Found %d articles to be proccessed!" % (len(sources)))
    
    load_static_files()
    
    for entry in sources:
        file = open(os.path.join(SOURCE_DIR, entry), 'r')
        header = True
        content = ''
        article = Article()

        with open(os.path.join(SOURCE_DIR, entry), 'r') as file:
           for line in file:
               values = line.split(':')
               if header and len(values) >= 2:
                   if values[0].strip().lower() == 'title':
                       article.title = ':'.join(values[1:]) if len(values) > 2 else values[1] # Just in case it has something like: "title: Word: any other words"
                   elif values[0].strip().lower() == 'tags':
                       article.tags = values[1].split(',')
                   elif values[0].strip().lower() == 'date':
                       _date = values[1].strip() # Forze? Maybe ;-)
                       try:
                          article.date = datetime.datetime.strptime(_date, DATE_FORMAT)
                       except:
                           print(sys.exc_info())
                           print('Date "{0}" on file name "{1}" is not valid, the correct format is "{2}".'.format(_date, os.path.basename(entry), DATE_FORMAT))
                           sys.exit(-1)
                   elif values[0].strip().lower() == 'slug':
                       article.slug = values[1].strip().replace(' ','-') # Just in case.
                   elif values[0].strip().lower() == 'lang':
                       article.lang = values[1].strip()
                   elif values[0].strip().lower() == 'author':
                       article.author = values[1].strip()
               else:
                   if header: header = False
                   content = content + line
                   
           if len(article.title) < 2:
               print("Tag title is required in header file!")
               print("File name: " + file.name)
               print("Exiting now!")
               sys.exit(-1)
           elif len(article.tags) == 0:
               print("Tag tags is required in header file, you must provide at least one tag to the article!")
               print("File name: " + file.name)
               sys.exit(-1)
           elif article.date is None:
               print("Tag date is required in header file!")
               print("File name: " + file.name)
               sys.exit(-1)
           else:
               if len(article.lang) == 0: article.lang = DEFAULT_LANG
               
               article.content = convert_to_markdown(content)
              
               article.slug = article.slug if len(article.slug) != 0 else os.path.basename(file.name)[:-len(SOURCE_FILE_EXT)]
               article.author = article.author if len(article.author) != 0 else AUTHOR
               
               generate_article(article.date, article.title, article.content, article.tags, article.lang, article.slug, article.author) 
                    
               articles.append(article)

    generate_index(articles)     # Generate index page
    
    print('{0} articles proccessed in {1} seconds!\nDone!'.format(len(articles), (datetime.datetime.now() - startTime)))

# vim: tabstop=8  expandtab  shiftwidth=4  softtabstop=4
