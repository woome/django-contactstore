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
                <form method="POST" action="{xdjango:action_url()}">
                    <input type="submit" 
                        id="done_selecting_ff_friends" 
                        class="find_friends_button done_selecting_ff_friends" 
                        value="find friends">
                    </input>
                    <ul class="friends">
                        <xsl:apply-templates select="xdjango:contacts()//xdjango:contact"/>
                    </ul>
                    <input type="submit" 
                        id="done_selecting_ff_friends_bottom" 
                        class="find_friends_button done_selecting_ff_friends" 
                        value="find friends">
                    </input>
                </form>
            </body>
        </html>
    </xsl:template>

    <xsl:template match="xdjango:contact">
        <label for="{@id}">
            <li>
                <input type="checkbox" name="contact_id" id="{@id}" value="{@id}"/>
                <xsl:value-of select="@email"/>
            </li>
        </label>
    </xsl:template>

</xsl:stylesheet>
