# vim: set ts=4 et sw=4 sts=4 fileencoding=utf-8 :

urls = (
    ('^/bn/v1/ping$', 'banian.Ping'),
    ('^/bn/v1/profile/(create|query|modify)?$', 'userprof.Profile'),
    ('^/bn/v1/orga/(create|query|modify)?$', 'banian.Orga'),
    ('^/bn/v1/role/(create|query|modify)?$', 'banian.Role'),
    ('^/bn/v1/team/(create|query|modify|join|quit)?$', 'team.Team'),
    ('^/bn/v1/tag/(create|query|modify)?$', 'banian.Tag'),
    ('^/bn/v1/product/(create|query|modify)?$', 'banian.Product'),
    ('^/bn/v1/plan/(create|query|modify)?$', 'plan.Plan'),
    ('^/bn/v1/item/(create|query|modify)?$', 'plan.Item'),
    ('^/bn/v1/discuss/(create|query|modify)?$', 'plan.Discuss'),
    ('^/bn/v1/attach/(create|query|modify)?$', 'plan.Attach'),
)
