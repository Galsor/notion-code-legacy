
#TODO: This is a TODO test
def foo():
    pass

class Bar:
    def __init__(self):
        #FIXME change semf with self
        semf.baz = "baz"
        #BUG Doesn't work, don't knwo why.
        display("supercool message")
