from flaskapi.schemas import BaseSchema, prisma_models
from pydantic import create_model
from flask import Request, Response, jsonify, request, make_response, Blueprint
from prisma import Prisma
import prisma.models

db = Prisma(auto_register=True)


class Resource(Blueprint):
    def __init__(self, schema: BaseSchema,
                 model: prisma.models.BaseModel, *args, **kwargs):
        super().__init__(model.__name__, __name__, *args, **kwargs)
        self.schema = schema
        self.model = model

        @self.route(f'/api/{model.__name__}', methods=['GET'])
        async def get_all():
            try:
                await db.connect()
                response = jsonify(await self.model.prisma().find_many())
                return response
            except Exception as e:
                return jsonify(await self.model.prisma().find_many())
            finally:
                await db.disconnect()

        @self.route(f'/api/{model.__name__}/<id>', methods=['GET'])
        async def get_one(id: str):
            try:
                await db.connect()
                response = jsonify(await self.model.prisma().find_unique(where={'id': id}))
                return response
            except Exception as e:
                return jsonify(await self.model.prisma().find_unique(where={'id': id}))
            finally:
                await db.disconnect()

        @self.route(f'/api/{model.__name__}', methods=['POST'])
        async def create():
            try:
                await db.connect()
                print(request.__dict__)
                response = jsonify(await self.model.prisma().create(data=request.json))
                return response
            except Exception as e:
                return jsonify(await self.model.prisma().create(data=request.json))
            finally:
                await db.disconnect()

        @self.route(f'/api/{model.__name__}/<id>', methods=['PUT'])
        async def update(id: str):
            try:
                await db.connect()
                response = jsonify(await self.model.prisma().update(where={'id': id}, data=request.json))
                return response
            except Exception as e:
                return jsonify(await self.model.prisma().update(where={'id': id}, data=request.json))
            finally:
                await db.disconnect()

        @self.route(f'/api/{model.__name__}/<id>', methods=['DELETE'])
        async def delete(id: str):
            try:
                await db.connect()
                response = jsonify(await self.model.prisma().delete(where={'id': id}))
                return response
            except Exception as e:
                return jsonify(await self.model.prisma().delete(where={'id': id}))
            finally:
                await db.disconnect()

        @self.route(f'/api/{model.__name__}/<field>/<value>', methods=['GET'])
        async def get_by_field(field: str, value: str):
            try:
                await db.connect()
                response = jsonify(await self.model.prisma().find_many(where={field: value}))
                return response
            except Exception as e:
                return jsonify(await self.model.prisma().find_many(where={field: value}))
            finally:
                await db.disconnect()

        @self.route(f'/api/{model.__name__}/<field>/<value>/<operator>',
                    methods=['GET'])
        async def get_by_field_operator(field: str, value: str, operator: str):
            """Operator can be one of: gt, gte, lt, lte, in, not_in, contains, starts_with, ends_with, not"""
            try:
                await db.connect()
                response = jsonify(await self.model.prisma().find_many(where={field: {operator: value}}))
                return response
            except Exception as e:
                return jsonify(await self.model.prisma().find_many(where={field: {operator: value}}))
            finally:
                await db.disconnect()

        @self.route(f'/api/{model.__name__}/schema', methods=['GET'])
        def get_schema():
            return jsonify({
                'schema': self.model.schema_json()
            })
