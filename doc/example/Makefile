build_all:
	knit -f html_example.pyz  -ofd output
	knit -f html_with_http_css.pyz  -ofd output
	knit -f html_with_local_css.pyz  -ofd output
	knit -f pdf_example.pyz  -ofd output
	knit -f pdf_full.pyz  -ofd output
	zen_con=sqlite:///example.db my_con_string=sqlite:///example.db knit -f pdf_sql.pyz  -ofd output
	zen_con=sqlite:///example.db my_con_string=sqlite:///example.db knit -f html_sql.pyz  -ofd output
	python demo.py
