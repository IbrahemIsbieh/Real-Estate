import json
import math
from urllib.parse import parse_qs

from odoo import http
from odoo.http import request


class PropertyApi(http.Controller):

    # =========================================================
    # CREATE PROPERTY
    # POST /v1/property
    # =========================================================
    @http.route(
        "/v1/property",
        type="http",
        auth="none",
        methods=["POST"],
        csrf=False
    )
    def post_property(self):
        try:
            args = request.httprequest.data.decode("utf-8")
            vals = json.loads(args)

            property_record = request.env["property"].sudo().create(vals)

            return request.make_json_response(
                {
                    "message": "Property has been created successfully",
                    "id": property_record.id,
                    "name": property_record.name,
                },
                status=201,
            )

        except Exception as error:
            return request.make_json_response(
                {
                    "message": str(error),
                },
                status=400,
            )

    # =========================================================
    # CREATE PROPERTY - JSON RPC
    # POST /v1/property/jsonrpc
    # =========================================================
    @http.route(
        "/v1/property/jsonrpc",
        type="jsonrpc",
        auth="user",
        methods=["POST"],
        csrf=False
    )
    def post_property_jsonrpc(self):
        try:
            args = request.httprequest.data.decode("utf-8")
            vals = json.loads(args)

            property_record = request.env["property"].sudo().create(vals)

            return {
                "message": "Property has been created successfully",
                "id": property_record.id,
                "name": property_record.name,
            }

        except Exception as error:
            return {
                "message": str(error),
            }

    # =========================================================
    # UPDATE PROPERTY
    # PUT /v1/property/<property_id>
    # =========================================================
    @http.route(
        "/v1/property/<int:property_id>",
        type="http",
        auth="none",
        methods=["PUT"],
        csrf=False
    )
    def update_property(self, property_id):
        try:
            property_record = request.env["property"].sudo().search(
                [("id", "=", property_id)],
                limit=1,
            )

            if not property_record:
                return request.make_json_response(
                    {
                        "message": "ID does not exist",
                    },
                    status=404,
                )

            args = request.httprequest.data.decode("utf-8")
            vals = json.loads(args)

            property_record.write(vals)

            return request.make_json_response(
                {
                    "message": "Property has been updated successfully",
                    "id": property_record.id,
                    "name": property_record.name,
                },
                status=200,
            )

        except Exception as error:
            return request.make_json_response(
                {
                    "message": str(error),
                },
                status=400,
            )

    # =========================================================
    # GET PROPERTY LIST
    # GET /v1/property
    # =========================================================
    @http.route(
        "/v1/property",
        type="http",
        auth="none",
        methods=["GET"],
        csrf=False
    )
    def get_property_list(self):
        try:
            params = parse_qs(
                request.httprequest.query_string.decode("utf-8")
            )

            property_domain = []

            # Default values
            page = 1
            limit = 5

            # -------------------------------------------------
            # LIMIT
            # -------------------------------------------------
            if params.get("limit"):
                limit = int(params.get("limit")[0])

                if limit <= 0:
                    return request.make_json_response(
                        {
                            "message": "Limit must be greater than 0",
                        },
                        status=400,
                    )

            # -------------------------------------------------
            # PAGE
            # -------------------------------------------------
            if params.get("page"):
                page = int(params.get("page")[0])

                if page <= 0:
                    return request.make_json_response(
                        {
                            "message": "Page must be greater than 0",
                        },
                        status=400,
                    )

            # -------------------------------------------------
            # OFFSET
            # -------------------------------------------------
            offset = (page - 1) * limit

            # -------------------------------------------------
            # FILTER BY STATE
            # Example:
            # /v1/property?state=available
            # -------------------------------------------------
            if params.get("state"):
                state = params.get("state")[0]
                property_domain.append(
                    ("state", "=", state)
                )

            # -------------------------------------------------
            # SEARCH
            # -------------------------------------------------
            property_model = request.env["property"].sudo()

            property_ids = property_model.search(
                property_domain,
                offset=offset,
                limit=limit,
                order="id desc",
            )

            property_count = property_model.search_count(
                property_domain
            )

            # -------------------------------------------------
            # NO RECORDS
            # -------------------------------------------------
            if not property_ids:
                return request.make_json_response(
                    {
                        "message": "There are no records",
                        "pagination_info": {
                            "page": page,
                            "pages": math.ceil(
                                property_count / limit
                            ),
                            "total": property_count,
                        },
                    },
                    status=404,
                )

            # -------------------------------------------------
            # RESPONSE
            # -------------------------------------------------
            properties = [
                {
                    "id": property_record.id,
                    "name": property_record.name,
                    "ref": property_record.ref,
                    "description": property_record.description,
                    "bedroom": property_record.bedroom,
                }
                for property_record in property_ids
            ]

            return request.make_json_response(
                {
                    "properties": properties,
                    "pagination_info": {
                        "page": page,
                        "limit": limit,
                        "pages": math.ceil(
                            property_count / limit
                        ),
                        "total": property_count,
                    },
                },
                status=200,
            )

        except ValueError as error:
            return request.make_json_response(
                {
                    "message": f"Invalid parameter: {str(error)}",
                },
                status=400,
            )

        except Exception as error:
            return request.make_json_response(
                {
                    "message": str(error),
                },
                status=400,
            )

    # =========================================================
    # DELETE PROPERTY
    # DELETE /v1/property/<property_id>
    # =========================================================
    @http.route(
        "/v1/property/<int:property_id>",
        type="http",
        auth="user",
        methods=["DELETE"],
        csrf=False
    )
    def delete_property(self, property_id):
        try:
            property_record = request.env["property"].sudo().search(
                [("id", "=", property_id)],
                limit=1,
            )

            if not property_record:
                return request.make_json_response(
                    {
                        "message": "ID does not exist",
                    },
                    status=404,
                )

            property_record.unlink()

            return request.make_json_response(
                {
                    "message": "Property has been deleted successfully",
                },
                status=200,
            )

        except Exception as error:
            return request.make_json_response(
                {
                    "message": str(error),
                },
                status=400,
            )