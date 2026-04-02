UPDATE public.back_wirebond AS m
SET technician = v.technician
FROM ( VALUES

{ ",".join( ["(%s, 'oc')"%(db_value(moduleID)) for moduleID in moduleIDs] ) }

) AS v(module_name, technician)
WHERE m.module_name = v.module_name;
