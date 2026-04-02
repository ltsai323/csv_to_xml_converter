SELECT proto_name FROM public.proto_assembly
WHERE cure_date_end IS NOT NULL AND cure_time_end IS NULL
ORDER BY proto_no ASC
