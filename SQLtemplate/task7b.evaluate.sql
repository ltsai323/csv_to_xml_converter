UPDATE public.module_inspect AS m
SET time_inspect = v.time_inspect::time
FROM ( VALUES

{ ",".join( ["(%s, TIME '00:00:00')"%(db_value(moduleID)) for moduleID in moduleIDs] ) }

) AS v(module_name, time_inspect)
WHERE m.module_name = v.module_name;
