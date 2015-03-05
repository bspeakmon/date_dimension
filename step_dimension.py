#!/usr/bin/env python

import argparse


class StepDimensionGenerator(object):

    INSERT_TEMPLATE = """
      INSERT INTO step_dim (step_dim_key, total_steps, this_step, steps_remaining) VALUES ({}, {}, {}, {});"""

    def __init__(self, max_steps, output_file):
        self.max_steps = max_steps
        self.output_file = output_file

    def generate(self):
        row_key = 1
        inserts = []
        for session in range(self.max_steps + 1):
            for step in range(1, session + 1):
                inserts.append(
                    self.INSERT_TEMPLATE.format(
                        row_key, session, step, session - step
                        )
                    )
                row_key += 1

        for insert in inserts:
            self.output_file.write(insert)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('steps', metavar='S', type=int, default=100,
                        help="Number of steps in the biggest session.")
    parser.add_argument('-o', '--output-file', type=argparse.FileType('w'),
                        default='step_dimension_inserts.sql',
                        help='Output destination for the INSERT script.')

    args = parser.parse_args()
    StepDimensionGenerator(args.steps, args.output_file).generate()
