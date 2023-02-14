from datetime import datetime

import humanize

from odoo import http
from odoo.http import request


class DefiSnippet1Controller(http.Controller):
    @http.route(
        ["/defi_snippet_1/helloworld"],
        type="json",
        auth="public",
        website=True,
        methods=["POST", "GET"],
        csrf=False,
    )
    def hello_world(self):
        return {"hello": "Hello World!"}

    @http.route(
        ["/defi_snippet_1/portal_time/<int:portal_time>"],
        type="http",
        auth="public",
        website=True,
    )
    def get_page_portal_time(self, portal_time=None):
        env = request.env(context=dict(request.env.context))

        demo_model_portal_cls = env["demo.model.portal"]
        if portal_time:
            demo_model_portal_id = (
                demo_model_portal_cls.sudo().browse(portal_time).exists()
            )
        else:
            demo_model_portal_id = None
        dct_value = {"demo_model_portal_id": demo_model_portal_id}

        # Render page
        return request.render(
            "defi_snippet_1.demo_model_portal_unit_list_show_time_item_structure",
            dct_value,
        )

    @http.route(
        ["/defi_snippet_1/portal_time_list"],
        type="json",
        auth="public",
        website=True,
    )
    def get_portal_time_list(self):
        env = request.env(context=dict(request.env.context))

        demo_model_portal_cls = env["demo.model.portal"]
        demo_model_portal_ids = (
            demo_model_portal_cls.sudo()
            .search([], order="create_date desc", limit=3)
            .ids
        )
        portal_times = demo_model_portal_cls.sudo().browse(
            demo_model_portal_ids
        )

        lst_time_diff = []
        timedate_now = datetime.now()
        # fr_CA not exist
        # check .venv/lib/python3.7/site-packages/humanize/locale/
        _t = humanize.i18n.activate("fr_FR")
        for demo_model_portal_id in portal_times:
            diff_time = timedate_now - demo_model_portal_id.create_date
            str_diff_time = humanize.naturaltime(diff_time).capitalize() + "."
            lst_time_diff.append(str_diff_time)
        humanize.i18n.deactivate()

        dct_value = {"portal_times": portal_times, "lst_time": lst_time_diff}

        # Render page
        return request.env["ir.ui.view"].render_template(
            "defi_snippet_1.demo_model_portal_list_list_show_time_item_structure",
            dct_value,
        )
