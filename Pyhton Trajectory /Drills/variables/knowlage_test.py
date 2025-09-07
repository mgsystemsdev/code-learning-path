sample_test = """Hello world. 
This is a test. 
"""

def test_sample():
    result = len(sample_test)
    words = len(sample_test.split())
    lines = len(sample_test.split('\n'))
    print(f" character: {result}")
    print(f" words: {words}")
    print(f" lines: {lines}")
    

test_sample()

