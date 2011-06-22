<?xml version="1.0" encoding="utf-8"?>
<xsl:stylesheet  version="1.0"
    xmlns="http://www.w3.org/1999/xhtml"
    xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:xdjango="http://djangoproject.com/template/xslt"
    extension-element-prefixes="xdjango"
    exclude-result-prefixes="xdjango xsl">

    <xsl:template match="/">
        <html>
            <body>
                <h2>your invites have been sent</h2>
            </body>
        </html>
    </xsl:template>

</xsl:stylesheet>
