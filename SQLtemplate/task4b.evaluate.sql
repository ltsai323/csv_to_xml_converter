UPDATE public.module_info AS m
SET roc_version = v.roc_version
FROM ( VALUES

{ ",".join( ["(%s,%s)"%(db_value(moduleID),get_rocv(moduleID)) for moduleID in moduleIDs] ) }

) AS v(module_name, roc_version)
WHERE m.module_name = v.module_name;
