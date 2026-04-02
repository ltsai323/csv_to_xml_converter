UPDATE public.module_info AS m
SET geometry = v.geometry
FROM ( VALUES

{ ",".join( ["(%s,%s)"%(db_value(moduleID),get_geo(moduleID)) for moduleID in moduleIDs] ) }

) AS v(module_name, geometry)
WHERE m.module_name = v.module_name;
