UPDATE public.module_info AS m
SET bp_material = v.bp_material
FROM ( VALUES

{ ",".join( ["(%s,%s)"%(db_value(moduleID),get_bpmaterial(moduleID)) for moduleID in moduleIDs] ) }

) AS v(module_name, bp_material)
WHERE m.module_name = v.module_name;
