# vim: set ts=4 et sw=4 sts=4 fileencoding=utf-8 :

import banian

urls = (
    ('^/$', 'banian.Index'),
    ('^/v1/ping$', 'banian.Ping'),
    ('^/v1/orga(?:/([0-9]+))?$', 'banian.Orga'),
    ('^/v1/role(?:/([0-9]+))?$', 'banian.Role'),
    ('^/v1/profile(?:/([0-9]+))?$', 'banian.Profile'),
    ('^/v1/team(?:/([0-9]+))?$', 'banian.Team'),
    ('^/v1/item(?:/([0-9]+))?$', 'banian.Items'),
    ('^/v1/attach(?:/([0-9]+))?$', 'banian.Attachs'),
)
