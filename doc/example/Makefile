build_all:
	knit -f html_example_2.pyz  -ofd output
	knit -f html_with_http_css_2.pyz  -ofd output
	knit -f html_with_local_css_2.pyz  -ofd output
	knit -f pdf_example_2.pyz  -ofd output
	knit -f pdf_full_2.pyz  -ofd output
	zen_con=sqlite:///example.db my_con_string=sqlite:///example.db knit -f pdf_sql_2.pyz  -ofd output
	zen_con=sqlite:///example.db my_con_string=sqlite:///example.db knit -f html_sql_2.pyz  -ofd output
	python demo.py


	knit -f html_example_1.py  -ofd output
	knit -f html_with_http_css_1.py  -ofd output
	knit -f html_with_local_css_1.py  -ofd output
	knit -f pdf_example_1.py  -ofd output
	knit -f pdf_full_1.py  -ofd output
	zen_con=sqlite:///example.db my_con_string=sqlite:///example.db knit -f pdf_sql_1.py  -ofd output
	zen_con=sqlite:///example.db my_con_string=sqlite:///example.db knit -f html_sql_1.py  -ofd output