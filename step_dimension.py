#!/usr/bin/env python

import argparse


class StepDimensionGenerator(object):

    CREATE_TEMPLATE = """CREATE TABLE {} (
        {} int,
        total_steps int,
        this_step int,
        steps_remaining int);\n"""

    INSERT_TEMPLATE = """INSERT INTO step_dim (step_dim_key, total_steps, this_step, steps_remaining) VALUES ({}, {}, {}, {});\n"""

    def __init__(self, max_steps, output_file, table_name, pk_column):
        self.max_steps = max_steps
        self.output_file = output_file
        self.table_name = table_name
        self.pk_column = pk_column

    def generate(self):

        create_statement = self.CREATE_TEMPLATE.format(self.table_name, self.pk_column)
        self.output_file.write(create_statement)

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

    insert_group = parser.add_argument_group("Insert generation")
    insert_group.add_argument('-s', '--steps', type=int, default=100,
                        help="Number of steps in the biggest session.")
    insert_group.add_argument('-o', '--output-file', type=argparse.FileType('w'),
                        default='create_step_dimension.sql',
                        help='Output destination for the CREATE/INSERT script.')

    create_group = parser.add_argument_group("Table creation")
    create_group.add_argument('--table-name', default='step_dim',
                              help='Name of the step dimension table.')
    create_group.add_argument('--primary-key-column', default="step_dim_key",
                              help='Namem of the primary key column.')

    args = parser.parse_args()
    StepDimensionGenerator(args.steps, args.output_file, args.table_name,
                           args.primary_key_column).generate()
