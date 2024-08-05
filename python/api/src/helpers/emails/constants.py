from src import company_configs as cc


HTML_SKELETON = """
<html>
    <body>
        <table cellspacing="0" cellpadding="0" border="0" style="font-family: Roboto,'Helvetica Neue',Helvetica,Arial,sans-serif;">
            <tr>
                <td>

                    <table cellspacing="0" cellpadding="0" border="0" width="600" class="content-table" style="border-bottom: 1px solid #eeeee;">
                        <tr>
                            <td align="left" style="opacity: .75; padding: 5px 32px;">
                                <a href="{COMPANY_HOST}" target="_blank" rel="noopener"><img alt="{PRODUCT_IMG_ALT}" src="{PRODUCT_IMG}" height="32"/></a>
                            </td>
                        </tr>
                    </table>

                    {{}}

                    <table cellspacing="0" cellpadding="0" border="0" width="600" class="content-table" style="padding: 25px 32px; font-size: 9px; color: #757575;">
                        <tr><td><a href="{PRODUCT_HOST}"><img alt="{COMPANY_IMG_ALT}" src="{COMPANY_IMG}" height="14" style="opacity: .5;"/></a></td></tr>
                    </table>

                </td>
            </tr>
        </table>
    </body>
</html>
""".format(
    COMPANY_HOST=cc.CONFIG['HOST']['COMPANY'], PRODUCT_HOST=cc.CONFIG['HOST']['PRODUCT'],
    COMPANY_IMG=cc.CONFIG['LOGO']['COMPANY']['IMG'], COMPANY_IMG_ALT=cc.CONFIG['LOGO']['COMPANY']['ALT'],
    PRODUCT_IMG=cc.CONFIG['LOGO']['PRODUCT']['IMG'], PRODUCT_IMG_ALT=cc.CONFIG['LOGO']['PRODUCT']['ALT'],
)
