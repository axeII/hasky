"""Parser

Syntactic analyzator for discovering grammar

"""
__author__ = "ales lerch"


class Latex:
    def __init__(self, data):
        self.data = data
        self.tempalte = """
\\documentclass{article}
\\usepackage[utf8]{inputenc}
\\begin{document}
%s
\\end{document}
"""

    def outprint(self):
        with open("default.tex", "w") as lat:
            lat.write(self.tempalte % self.data)
        return self.data
