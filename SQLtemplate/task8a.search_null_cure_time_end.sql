SELECT proto_name, cure_date_end, cure_time_end FROM public.proto_assembly
WHERE cure_date_end IS NOT NULL AND cure_time_end IS NULL
ORDER BY proto_no ASC
