function(f2py_add_module target_name)
   message("oops=${oops}")

   set(f2py_module_name ${target_name})
   set(fortran_src_file "${CMAKE_CURRENT_SOURCE_DIR}/${target_name}.f90")
#   message("## PYTHON_MODULE_EXTENSION = ${PYTHON_MODULE_EXTENSION}")

   set(generated_module_file ${CMAKE_CURRENT_BINARY_DIR}/${f2py_module_name}${PYTHON_MODULE_EXTENSION})
#   message("##generated_module_file = ${generated_module_file}")

   add_custom_target(${f2py_module_name} ALL
     DEPENDS ${generated_module_file}
     )
   
   if (	
   add_custom_command(
     OUTPUT ${generated_module_file}
     COMMAND ${F2PY_EXECUTABLE}
	    --build-dir _f2py_build
	    --opt="-O3" 
	    -DF2PY_REPORT_ON_ARRAY_COPY=1 
	    -DNPY_NO_DEPRECATED_API=NPY_1_7_API_VERSION 
	    -Dlong_double="long double"
        -m ${f2py_module_name}
        -c
        ${fortran_src_file}
     WORKING_DIRECTORY ${CMAKE_CURRENT_BINARY_DIR}
     )
   install(FILES ${generated_module_file} DESTINATION "${CMAKE_CURRENT_SOURCE_DIR}/..")

endfunction()