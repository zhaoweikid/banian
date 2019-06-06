# vim: set ts=4 et sw=4 sts=4 fileencoding=utf-8 :

import banian

urls = (
    ('^/bn/v1/ping$', 'banian.Ping'),
    ('^/bn/v1/orga/(create|query|modify)?$', 'banian.Orga'),
    ('^/bn/v1/role/(create|query|modify)?$', 'banian.Role'),
    ('^/bn/v1/profile/(create|query|modify)?$', 'banian.Profile'),
    ('^/bn/v1/team/(create|query|modify)?$', 'banian.Team'),
    ('^/bn/v1/item/(create|query|modify)?$', 'banian.Items'),
    ('^/bn/v1/attach/(create|query|modify)?$', 'banian.Attachs'),
)
