"""

"""

import os
import json
import base64
import urllib
import datetime

import requests
from requests_oauthlib import OAuth2Session


from . import settings as menbib_settings





mendeley_cache = {}


class Mendeley(object):

    def __init__(self, access_token=None, token_type=None, refresh_token=None):

        self.access_token = access_token
        self.token_type = token_type
        self.refresh_token = refresh_token
        if access_token and refresh_token:
            self.session = OAuth2Session(
                menbib_settings.CLIENT_ID,
                token={
                    'access_token': access_token,
                    'token_type': token_type,
                    'refresh_token': refresh_token,
                }
            )
        # else:
        #     self.session = requests

    @classmethod
    def from_settings(cls, settings):
        if settings:
            return cls(
                access_token=settings.access_token,
                token_type=settings.token_type,
                refresh_token=settings.refresh_token
            )
        return cls()



    def user(self, user=None):
        """Fetch a user or the authenticated user.

        :param user: Optional Mendeley user name; will fetch authenticated
            user if omitted
        :return dict: Mendeley API response

        """
        url = (
            os.path.join(menbib_settings.API_URL, 'users', user)
            if user
            else os.path.join(menbib_settings.API_URL, 'profiles','info','me')
        )

        return self.session.get(url)

    def revoke_token(self):

        if self.access_token is None:
            return
        else:
            self.access_token = None

        return self.access_token

    def library(self):
        """Get library from user collection
        """
        url = os.path.join(menbib_settings.API_URL, 'library')
        return self.session.get(url).json()

    def folders(self):
        """Get folders from user collection
        """
        url = os.path.join(menbib_settings.API_URL, 'library', 'folders')
        return self.session.get(url).json()

    # def folder_details(self, folder_id):
    #     """Get folders from user collection
    #     """
    #     return self._send(
    #         os.path.join(menbib_settings.API_URL, 'library', 'folders', folder_id)
    #     )
    #
    # def document_details(self, doc_id):
    #     """Get document details from user collection
    #     """
    #     return self._send(
    #         os.path.join(menbib_settings.API_URL, 'library', 'documents', doc_id)
    #     )

    # def get_folders(self):
    #     pass
    #
    #
    # def get_folder_contents(self):
    #     pass
    #
    # def parse_library(connect, mendeley):
    #
    #     user_library = connect.library(mendeley.user_settings)
    #     document_id = user_library['document_ids']
    #     doc_meta = []
    #     for idx in range(0, len(document_id)):
    #         meta = connect.document_details(mendeley.user_settings, document_id[idx])
    #         date_parts = []
    #
    #         if meta.get('year', '0') != 0:
    #             date_parts.append([meta['year']])
    #         elif meta.get('month', '0') != 0:
    #             date_parts.append([meta['month']])
    #         elif meta.get('day', '0') != 0:
    #             date_parts.append([meta['day']])
    #
    #
    #
    #         author = []
    #         second_line = ''
    #         for idy in range(0, len(meta['authors'])):
    #             author.append({
    #                 'family':meta['authors'][idy]['surname'],
    #                 'given': meta['authors'][idy]['forename'],
    #             })
    #             second_line = second_line + meta['authors'][idy]['forename'] + ' ' \
    #                            + meta['authors'][idy]['surname'] + ', '
    #         second_line = second_line[:-2]
    #         second_line = second_line + ' (' + str(meta.get('year', '0')) + ')'
    #
    #         third_line = meta['published_in'] + ' ' \
    #             + meta.get('volume', '') + ' '  \
    #             + '(' + meta.get('issue', '') + ')' + 'p.' + \
    #             meta.get('pages', '')
    #
    #         doc_meta.append({
    #             "author": author,
    #             "id": meta['id'],
    #             "issued": {
    #             "date-parts": date_parts,
    #             },
    #             "title": meta.get('title', "").replace('.', ''),
    #             "type": meta.get('type', "").lower(),
    #             "abstract": meta.get('abstract', ""),
    #             "publisher": meta.get('published_in', ""),
    #             "volume": meta.get('volume', ""),
    #             "page": meta.get('pages', ""),
    #             "URL": meta.get('url', " "),
    #             "second_line": second_line,
    #             "third_line": third_line,
    #                     })
    #
    #     return doc_meta
    #
    #
    # def _get_citation(library, document_id, style):
    #
    #     bib_source = CiteProcJSON(library)
    #     bib_style = CitationStylesStyle(style)
    #     bibliography = CitationStylesBibliography(bib_style, bib_source, formatter.plain)
    #
    #     for id in range(0, len(document_id)):
    #         citation = Citation([CitationItem(library[id]['id'])])
    #         bibliography.register(citation)
    #
    #     return bibliography.bibliography()