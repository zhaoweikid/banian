# vim: set ts=4 et sw=4 sts=4 fileencoding=utf-8 :

import banian

urls = (
    ('^/', banian.Index),
    ('^/v1/role', banian.Role),
    ('^/v1/role/([0-9]+)', banian.Role),
    ('^/v1/team', banian.Team),
    ('^/v1/team/([0-9]+)', banian.Team),
    ('^/v1/item', banian.Item),
    ('^/v1/item/([0-9]+)', banian.Item),
    #('^/v1/item', banian.Item),
    ('^/v1/attach', banian.Attach),
    ('^/v1/attach/([0-9]+)', banian.Attach),
)
