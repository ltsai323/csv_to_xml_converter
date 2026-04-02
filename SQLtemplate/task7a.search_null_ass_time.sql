SELECT module_name FROM public.module_inspect
WHERE date_inspect IS NOT NULL AND time_inspect IS NULL
ORDER BY module_no ASC
