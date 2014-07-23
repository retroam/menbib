import httplib as http
from framework import request
from framework.exceptions import HTTPError
from website.project.decorators import must_be_contributor_or_public

from website.project.decorators import must_have_addon
from website.project.views.node import _view_project
from website.addons.menbib.api import Mendeley
from website.addons.menbib.client import get_node_addon_client
from citeproc import CitationStylesStyle, CitationStylesBibliography
from citeproc import Citation, CitationItem
from citeproc import formatter
from citeproc.source.json import CiteProcJSON
from flask import send_file
import StringIO
from website.addons.menbib import settings as menbib_settings
from framework.status import push_status_message as flash
from flask import redirect


def _page_content(node, node_addon):
    """Return the info to be rendered for a library..
    """
    #
    # Check permissions if authorized
    has_access = False
    has_auth = bool(node_addon.user_settings and node_addon.user_settings.has_auth)
    if has_auth:
        has_access = True

    collection = ""
    view_string = "All Items"
    collection_names = []
    items = []
    error_statement = ""
    CITATION_STYLES = ""
    EXPORT_FORMAT = ""

    return {
        'complete': True,
        'gh_user': node_addon.owner,
        'view_string': view_string,
        'collection_names':collection_names,
        'citation_styles': CITATION_STYLES,
        'export_formats':EXPORT_FORMAT,
        'error_statement': error_statement,
        'items': items,
        'collection':collection,
        'has_auth': has_auth,
        'has_access': has_access,
        'api_url': node.url,

    }

def parse_library(connect, menbib):

    user_library = connect.library(menbib.user_settings)
    document_id = user_library['document_ids']
    doc_meta = []
    for idx in range(0, len(document_id)):
        meta = connect.document_details(menbib.user_settings, document_id[idx])
        date_parts = []

        if meta.get('year', '0') != 0:
            date_parts.append([meta['year']])
        elif meta.get('month', '0') != 0:
            date_parts.append([meta['month']])
        elif meta.get('day', '0') != 0:
            date_parts.append([meta['day']])

        author = []
        second_line = ''
        for idy in range(0, len(meta['authors'])):
            author.append({
                'family':meta['authors'][idy]['surname'],
                'given': meta['authors'][idy]['forename'],
            })
            second_line = second_line + meta['authors'][idy]['forename'] + ' ' \
                           + meta['authors'][idy]['surname'] + ', '
        second_line = second_line[:-2]
        second_line = second_line + ' (' + str(meta.get('year', '0')) + ')'

        third_line = meta['published_in'] + ' ' \
            + meta.get('volume', '') + ' '  \
            + '(' + meta.get('issue', '') + ')' + 'p.' + \
            meta.get('pages', '')

        doc_meta.append({
            "author": author,
            "id": meta['id'],
            "issued": {
            "date-parts": date_parts,
            },
            "title": meta.get('title', "").replace('.', ''),
            "type": meta.get('type', "").lower(),
            "abstract": meta.get('abstract', ""),
            "publisher": meta.get('published_in', ""),
            "volume": meta.get('volume', ""),
            "page": meta.get('pages', ""),
            "URL": meta.get('url', " "),
            "second_line": second_line,
            "third_line": third_line,
                    })

    return doc_meta


def _collection(client):
    connect = Mendeley.from_settings(client.user_settings)
    user_library = connect.library(client.user_settings)

    documentId = user_library['document_ids']
    doc_meta = []
    for idx in range(0,len(documentId)-1):
        meta = connect.document_details(client.user_settings,documentId[idx])
        doc_meta.append({
            "id": meta['id'],
            "title":meta['title'],
            "publisher": meta['published_in'],
            "type": "book",
            })

    return doc_meta


def _get_citation(library, document_id, style):

    bib_source = CiteProcJSON(library)
    bib_style = CitationStylesStyle(style)
    bibliography = CitationStylesBibliography(bib_style, bib_source, formatter.plain)

    for id in range(0, len(document_id)):
        citation = Citation([CitationItem(library[id]['id'])])
        bibliography.register(citation)

    return bibliography.bibliography()


@must_be_contributor_or_public
@must_have_addon('menbib', 'node')
def menbib_get_page_info(node_addon, auth, **kwargs):

    folder = request.args.get('folder')

    if node_addon.user_settings is None:
        flash('Authorize Mendeley add-on in Settings', 'warning')
        raise HTTPError(http.FORBIDDEN)
    node = node_addon.owner
    user_settings = node_addon.user_settings
    client = get_node_addon_client(node_addon)
    client.from_settings(user_settings)
    client.refresh_access_token()
    user_folders = client.folders()
    user_library = client.library()
    user_folders_id = []
    user_folders_name = []

    for idx in range(0, len(user_folders)):
        user_folders_id.append(user_folders[idx]['id'])
        user_folders_name.append(user_folders[idx]['name'])

    if folder is not None:
        idx = user_folders_name.index(folder)
        folder_documentId = client.folder_details(user_folders_id[idx])
        documentId = folder_documentId['document_ids']
    else:
        documentId = user_library['document_ids']

    doc_meta = []

    for idx in range(0, len(documentId)):
        meta = client.document_details(documentId[idx])
        author = []
        second_line = ''
        for idy in range(0,len(meta['authors'])):
            author.append({
            'family':meta['authors'][idy]['surname'],
            'given': meta['authors'][idy]['forename'],
            })
            second_line = second_line + meta['authors'][idy]['forename'] + ' ' \
                           + meta['authors'][idy]['surname'] + ', '
        second_line = second_line[:-2]
        second_line = second_line + ' (' + str(meta.get('year','0')) + ')'

        third_line = meta['published_in'] + ' ' \
                  + meta.get('volume', '') + ' '  \
                  + '(' + meta.get('issue', '') + ')' + ' p. ' + \
          meta.get('pages', '')

        doc_meta.append({
            "author": author,
            "id": meta['id'],
            "issued": {
            "date-parts": [
                [
                    meta.get('year','0'),
                    meta.get('month','0'),
                    meta.get('day','0'),
                ]
            ]
            },
            "title": meta.get('title',"").replace('.',''),
            "type": meta.get('type',"").lower(),
            "abstract": meta.get('abstract',""),
            "publisher": meta.get('published_in',""),
            "volume": meta.get('volume',""),
            "page": meta.get('pages',""),
            "url": meta.get('url'," "),
            "second_line": second_line,
            "third_line": third_line.replace('()', '').strip(' p. '),
             })

    data = _view_project(node, auth, primary=True)

    rv = _page_content(node, node_addon)
    rv.update({
        'addon_page_js': user_settings.config.include_js.get('page'),
        'addon_page_css': user_settings.config.include_css.get('page'),
        'items': doc_meta,
        'citation_styles': menbib_settings.CITATION_STYLES,
        'export_formats': menbib_settings.EXPORT_FORMATS,
        'folder_names': user_folders_name,
    })
    rv.update(user_settings.config.to_json())
    rv.update(data)

    return rv

@must_be_contributor_or_public
@must_have_addon('menbib', 'node')
def menbib_get_export(node_addon, *args, **kwargs):

    node = node_addon.owner
    user_settings = node_addon.user_settings
    client = get_node_addon_client(node_addon)
    client.from_settings(user_settings)
    client.refresh_access_token()

    library = client.library()

    if node:

        keys = request.args.getlist('allKeys')
        format = request.args.get('format')

        if format not in menbib_settings.EXPORT_FORMATS:
            raise HTTPError(http.BAD_REQUEST), "Export format not recognized"

        if keys:
            export = _get_citation(library, keys, format)
            export = export.encode('utf-8')
            print export
        else:
            export = 'No Items specified'

        strIO = StringIO.StringIO()
        strIO.write(str(export))
        strIO.seek(0)

        return send_file(strIO, attachment_filename="menbib_export_"+format+".txt", as_attachment=True)

    else:
        raise HTTPError(http.BAD_REQUEST)

@must_be_contributor_or_public
@must_have_addon('menbib', 'node')
def menbib_get_citation(node_addon, *args, **kwargs):

    node = node_addon.owner
    user_settings = node_addon.user_settings
    client = get_node_addon_client(node_addon)
    client.from_settings(user_settings)
    client.refresh_access_token()

    library = client.library()

    if node:
        keys = request.json.get('allKeys')
        style = request.json.get('style')

        if style not in menbib_settings.CITATION_STYLES:
            raise HTTPError(http.BAD_REQUEST), "Export format not recognized"
        else:
            style = menbib_settings.CITATION_STYLES[style]

        if keys:
            citations = _get_citation(library, keys, style)
        else:
            citations = '<span>No Items specified</span>'



        citations = citations.replace(' .', '.<br>')

        return citations
    else:
        raise HTTPError(http.BAD_REQUEST)

