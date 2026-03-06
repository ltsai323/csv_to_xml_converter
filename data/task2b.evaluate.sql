UPDATE public.module_info AS m
SET resolution = v.resolution
FROM ( VALUES

{ ",".join( ["(%s,%s)"%(db_value(moduleID),get_res(moduleID)) for moduleID in moduleIDs] ) }

) AS v(module_name, resolution)
WHERE m.module_name = v.module_name;
