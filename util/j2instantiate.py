#!/bin/env python3

import jinja2 
import sys
import dotenv

if __name__ == "__main__":

    values=dotenv.dotenv_values()

    env = jinja2.Environment(
        loader=jinja2.FileSystemLoader("."),
        autoescape=jinja2.select_autoescape()
    )
    template = env.get_template(sys.argv[1])
    print(template.render(**values))
