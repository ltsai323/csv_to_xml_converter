UPDATE public.proto_assembly AS m
SET cure_time_end = v.cure_time_end::time
FROM ( VALUES

{ ",".join( ["(%s, TIME '00:00:00')"%(db_value(moduleID)) for moduleID in moduleIDs] ) }

) AS v(proto_name, cure_time_end)
WHERE m.proto_name = v.proto_name;
