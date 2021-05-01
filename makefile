gen:
	python debug.py gen
lexer:
	@python debug.py lexer
onlylexer:
	@python debug.py onlylexer
parser:
	@python debug.py parser
onlyparser:
	@python debug.py onlyparser
ast:
	@python debug.py ast
onlyast:
	@python debug.py onlyast
clean:
	python debug.py clean
