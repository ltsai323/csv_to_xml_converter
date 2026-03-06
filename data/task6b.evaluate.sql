UPDATE public.module_info AS m
SET institution = v.institution
FROM ( VALUES

{ ",".join( ["(%s,'NTU')"%(db_value(moduleID)) for moduleID in moduleIDs] ) }

) AS v(module_name, institution)
WHERE m.module_name = v.module_name;
