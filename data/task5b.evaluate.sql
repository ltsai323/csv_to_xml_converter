UPDATE public.module_info AS m
SET sen_thickness = v.sen_thickness
FROM ( VALUES

{ ",".join( ["(%s,%s)"%(db_value(moduleID),get_senthick(moduleID)) for moduleID in moduleIDs] ) }

) AS v(module_name, sen_thickness)
WHERE m.module_name = v.module_name;
