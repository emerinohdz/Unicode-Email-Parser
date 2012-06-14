# coding: utf-8
#
# Copyright (C) 2011 by Edgar Merino (http://devio.us/~emerino)
#
# Licensed under the Artistic License 2.0 (The License). 
# You may not use this file except in compliance with the License.
# You may obtain a copy of the License at:
#
#    http://www.perlfoundation.org/artistic_license_2_0
#
# THE PACKAGE IS PROVIDED BY THE COPYRIGHT HOLDER AND CONTRIBUTORS "AS
# IS" AND WITHOUT ANY EXPRESS OR IMPLIED WARRANTIES. THE IMPLIED
# WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE, OR
# NON-INFRINGEMENT ARE DISCLAIMED TO THE EXTENT PERMITTED BY YOUR LOCAL
# LAW. UNLESS REQUIRED BY LAW, NO COPYRIGHT HOLDER OR CONTRIBUTOR WILL
# BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, OR CONSEQUENTIAL
# DAMAGES ARISING IN ANY WAY OUT OF THE USE OF THE PACKAGE, EVEN IF
# ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
#
# Requerimientos: python >= 2.5

from email.parser import Parser
from email.header import Header, decode_header
from email.Iterators import typed_subpart_iterator

class UnicodeParser(Parser):
    """
    Esta clase devuelve las cabeceras de un correo
    electrónico como cadenas unicode.
    """

    def __init__(self):
        Parser.__init__(self)

    def parse(self, fp, headersonly=False):
        data = Parser.parse(self, fp, headersonly)
        orig_data = {}
    
        for key, value in data.items():
            orig_data[key.lower()] = value

        def get_unicode_header(header):
            return unicode_header(orig_data[header.lower()])

        data.__getitem__ = get_unicode_header

        return data

def unicode_header(header):
    decoded_header = decode_header(header)
    header = ""

    for part in decoded_header:
        if part[1]:
            header += unicode(part[0], part[1])
        else:
            header += part[0]

        header += " "

    return header

def unicode_email_body(email):
    body = ""

    if email.is_multipart():
        for part in typed_subpart_iterator(email, "text", "plain"):
            charset = part.get_content_charset()

            # Si no se especificó un encoding intentamos con iso-8859-1
            if not charset:
                charset = "iso-8859-1"

            body += unicode(part.get_payload(decode=True), charset)
    else:
        charset = email.get_content_charset()

        if not charset:
            charset = "iso-8859-1"

        body = unicode(email.get_payload(decode=True), charset)

    return body

