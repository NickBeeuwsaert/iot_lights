import colander

class LightSchema(colander.MappingSchema):
    id = colander.SchemaNode(colander.String())
    name = colander.SchemaNode(colander.String())
    hue = colander.SchemaNode(
        colander.Integer(),
        validator=colander.Range(0, 360)
    )
    brightness = colander.SchemaNode(
        colander.Integer(),
        validator=colander.Range(1, 100)
    )
    state = colander.SchemaNode(
        colander.Boolean()
    )

class EventSchema(colander.MappingSchema):
    def schema_type(self):
        return colander.Mapping(unknown='preserve')

    type = colander.SchemaNode(
        colander.String(),
        validator=colander.OneOf([
            'addLight',
            'changeLight'
        ])
    )
    light = LightSchema()
