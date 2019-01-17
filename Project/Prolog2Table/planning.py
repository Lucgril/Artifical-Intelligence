import pandas as pd
import numpy as np
import time
from pyswip import Prolog


class Prolog2Table:
    def parse_file(self, filename):
        with open(filename) as f:
            content = f.readlines()

            # Remove also whitespace characters like `\n` at the end of each line
            result = [x.strip() for x in content]

            # Remove empty string due to empty line (space)
            result = list(filter(None, result))

            # Remove dot and space from each sentence
            for x in range(len(result)):
                str = result[x]
                result[x] = str[:-1]
                result[x] = result[x].replace(" ", "")

            return result

    def is_fact(self, sentence):
        if ":-" not in sentence:
            return True
        else:
            return False

    def is_rule(self, sentence):
        if ":-" in sentence:
            return True
        else:
            return False

    def get_objects_in_fact(self, sentence):
        start = "("
        end = ")"

        if 'not' in sentence:
            first_atom = sentence.split('(')[1]
            x = sentence[sentence.find(start, 3) + len(start):sentence.rfind(end)]
            atom = x[x.find(start) + len(start):x.rfind(end)]
        else:
            first_atom = sentence.split('(')[0]
            atom = sentence[sentence.find(start) + len(start):sentence.rfind(end)]

        if ',' not in atom:
            return first_atom, atom
        else:
            atoms = atom.split(',')
            return first_atom, atoms

    def get_complicated_objects_in_fact(self, sentence):
        first_atom = []
        atoms = []

        if ';' in sentence or '),' in sentence or ('not' in sentence and '),' in sentence) or (
                'not' in sentence and ';' in sentence):
            if ';' in sentence:
                new_sentence = sentence.split(';')

            elif '),' in sentence:
                z = sentence.replace('),', '):')
                new_sentence = z.split(':')

            for string in new_sentence:
                x, y = self.get_objects_in_fact(string)
                first_atom.append(x)
                atoms.append(y)

        elif 'not' in sentence:
            first_atom, atoms = self.get_objects_in_fact(sentence)

        return first_atom, atoms

    # Create the table and fill it in with the correct values of the facts
    def create_table(self, content, df):
        count = 0
        for i in range(len(content)):
            if self.is_fact(content[i]):
                if ';' in content[i] or 'not' in content[i]:
                    first_atom, atoms = self.get_complicated_objects_in_fact(content[i])
                else:
                    first_atom, atoms = self.get_objects_in_fact(content[i])

                if isinstance(atoms, str) or (isinstance(atoms, list) and (not isinstance(atoms[0], list))):
                    # Check if the new column can be added
                    if first_atom not in df:
                        df[first_atom] = np.NaN

                    # Check if a value is already contained in the dataframe. If False,
                    # a new row is created. Instead, if True, the index of the values alreay
                    # contained is taken
                    if not (str(atoms) in df.values):
                        df.loc[count, 'object'] = str(atoms)

                        if 'not' in content[i]:
                            df.loc[count, first_atom] = 0
                        else:
                            df.loc[count, first_atom] = 1
                        count += 1
                    else:
                        select_indices = list(np.where(df["object"] == str(atoms))[0])

                        if 'not' in content[i]:
                            df.loc[select_indices, first_atom] = 0
                        else:
                            df.loc[select_indices, first_atom] = 1

                # This condition is for the fact with the and or with the or
                elif isinstance(atoms, list) and isinstance(atoms[0], list):
                    if ';' in content[i]:
                        new_sentence = content[i].split(';')
                    elif '),' in content[i]:
                        z = content[i].replace('),', '):')
                        new_sentence = z.split(':')

                    for j in range(len(atoms)):
                        # Check if the new column can be added
                        if first_atom[j] not in df:
                            df[first_atom[j]] = np.NaN

                        # Check if a value is already contained in the dataframe. If False,
                        # a new row is created. Instead, if True, the index of the values alreay
                        # contained is taken
                        if not (str(atoms[j]) in df.values):
                            df.loc[count, 'object'] = str(atoms[j])

                            if 'not' in new_sentence[j]:
                                df.loc[count, first_atom[j]] = 0
                            else:
                                df.loc[count, first_atom[j]] = 1
                            count += 1
                        else:
                            select_indices = list(np.where(df["object"] == str(atoms[j]))[0])

                            if 'not' in new_sentence[j]:
                                df.loc[select_indices, first_atom[j]] = 0
                            else:
                                df.loc[select_indices, first_atom[j]] = 1

        df.fillna('-', inplace=True)
        return df

    # Add all the facts in the prolog database
    def add_fact_to_db(self, content):
        try:
            for i in range(len(content)):
                if self.is_fact(content[i]):
                    if ';' not in content[i]:
                        prolog.assertz(content[i])
                    else:
                        tmp = content[i].split(';')
                        for fact in tmp:
                            prolog.assertz(fact)
            return True
        except Exception:
            return False

    def add_rule_to_db(self, first_atom, content):
        try:
            values = []
            if isinstance(content, dict):
                for key, value in content.items():
                    if len(content) == 1:
                        prolog.assertz(first_atom + '(' + value + ')')
                        return True
                    else:
                        values.append(value)
                prolog.assertz(str(first_atom) + '(' + str(values[0]) + ',' + str(values[1]) + ')')
                return True
            elif isinstance(content, list):
                prolog.assertz(str(first_atom) + '(' + str(content[0]) + ',' + str(content[1]) + ')')
                return True
        except Exception:
            return False

    def add_rule(self, content, df):
        for i in range(len(content)):
            if self.is_rule(content[i]):
                tmp = content[i].split(':-')

                # Add function of the rule in the table as column
                column = tmp[0].split('(')[0]

                if column not in df:
                    df[column] = np.NaN

                # Make the query with the right-hand-side of the current rule
                result = list(prolog.query(tmp[1]))
                count = 0
                arg = tmp[0].split('(')[1]

                if ',' in arg:
                    arg = arg[:-1].split(',')
                    for e in arg:
                        if len(e) == 1 and e.isupper():
                            count += 1

                            # print("result" + str(result))
                for element in result:
                    if self.add_rule_to_db(column, element):
                        row = []
                        print(element)
                        if len(element) == 1 and count == 1:
                            if len(arg[0]) == 1 and arg[0].isupper():
                                row.extend([list(element.values())[0], arg[1]])
                            elif len(arg[1]) == 1 and arg[1].isupper():
                                row.extend([arg[0], list(element.values())[0]])
                            if not self.add_rule_to_db(column, row):
                                print("Something was wrong with the prolog rule query")

                        elif len(element) < 3:
                            for key, value in element.items():
                                if isinstance(value, int):
                                    value = str(value)
                                row.append(value)
                        else:
                            x, y = self.get_objects_in_fact(tmp[0])

                            for key, value in element.items():
                                if key in y:
                                    if isinstance(value, int):
                                        value = str(value)
                                    row.append(value)
                                    y.remove(key)

                        if ';' in tmp[1] or 'not' in tmp[1] or '),' in tmp[1]:
                            first_atom, atoms = self.get_complicated_objects_in_fact(tmp[1])
                        else:
                            first_atom, atoms = self.get_objects_in_fact(tmp[1])

                        # Check if a possible new row can be added
                        if len(row) > 1 and (not str(row) in df.object.values):
                            lun = len(df.index)
                            df.loc[lun, 'object'] = str(row)

                            if len(element) < 3:
                                if isinstance(first_atom, str):
                                    if 'not' in tmp[1]:
                                        df.loc[lun, first_atom] = 0
                                    else:
                                        df.loc[lun, first_atom] = 1

                                elif isinstance(first_atom, list):
                                    z = tmp[1].replace('),', '):')
                                    new_sentence = z.split(':')

                                    for j in range(len(first_atom)):
                                        if 'not' in new_sentence[j]:
                                            df.loc[lun, first_atom[j]] = 0
                                        else:
                                            df.loc[lun, first_atom[j]] = 1
                        # Row without couple
                        if len(row) == 1:
                            df.loc[df['object'] == row[0], [column]] = 1
                        # Row with couple
                        else:
                            df.loc[df['object'] == str(row), [column]] = 1
                    else:
                        print("Something was wrong with the prolog rule query")

        df.fillna('-', inplace=True)
        return df


class Table2Prolog:
    def create_fact(self, df, f):
        columns = list(df)
        objects = df['object'].values.tolist()

        for obj in objects:
            for col in columns:
                if df.loc[df.object == obj, col].values[0] == 1:
                    if ',' not in obj:
                        f.write(col + '(' + obj + ').\n')
                    else:
                        x = obj[1:-1].split(',')
                        f.write(col + '(' + x[0][1:-1] + ', ' + x[1][2:-1] + ').\n')

                elif df.loc[df.object == obj, col].values[0] == 0:
                    if ',' not in obj:
                        f.write('not(' + col + '(' + obj + ')).\n')
                    else:
                        x = obj[1:-1].split(',')
                        f.write('not(' + col + '(' + x[0][1:-1] + ', ' + x[1][2:-1] + ')).\n')
        return f

    def create_rule(self, df, df_fact, df_rule, f):
        columns_fact = list(df_fact)
        columns_rule = list(df_rule)
        objects = df_fact['object'].values.tolist()
        dic = {}

        for obj in objects:
            columns = []
            for col_rule in columns_rule:
                tmp = []
                if df.loc[df.object == obj, col_rule].values[0] == 1:
                    for col_fact in columns_fact:
                        if df_fact.loc[df_fact.object == obj, col_fact].values[0] == 1:
                            columns.append(col_fact)
                        elif df_fact.loc[df_fact.object == obj, col_fact].values[0] == 0:
                            columns.append("not(" + col_fact)
                    tmp.extend([col_rule, obj])
                    if len(columns) == 1:
                        if columns[0] not in dic:
                            dic[columns[0]] = tmp
                    elif len(columns) == 2:
                        if repr(columns) not in dic:
                            dic[repr(columns)] = tmp

        for key, value in dic.items():
            if '[' not in key and ']' not in key:
                if '[' not in value[1] and ']' not in value[1]:
                    if 'not' not in key:
                        f.write(value[0] + '(X) :- ' + key + '(X).\n')
                    else:
                        f.write(value[0] + '(X) :- ' + key + '(X)).\n')
                else:
                    if 'not' not in key:
                        f.write(value[0] + '(X,Y) :- ' + key + '(X,Y).\n')
                    else:
                        f.write(value[0] + '(X,Y) :- ' + key + '(X,Y)).\n')
            else:
                key = key[1:-1].split(',')

                if isinstance(value, list):
                    f.write(value[0] + '(X) :- ' + key[0][1:-1] + '(X),' + key[1][2:-1] + '(X).\n')
                else:
                    f.write(value + '(X) :- ' + key[0][1:-1] + '(X),' + key[1][2:-1] + '(X).\n')

        return f

    def create_complicated_rule(self, df, df_fact_added, df_fact, df_rule, f):
        columns_fact = list(df_fact)
        columns_rule = list(df_rule)
        objects = df_fact['object'].values.tolist()
        objects_added = df_fact_added['object'].values.tolist()
        dic = {}
        first_method = False
        second_method = False
        third_method = False

        for obj_added in objects_added:
            obj_added_new = obj_added[1:-1].split(',')

            for col_rule in columns_rule:
                if df.loc[df.object == obj_added, col_rule].values[0] == 1:
                    y = None
                    final_element = []
                    first_element = None
                    second_element = None

                    for obj_added in objects_added:
                        for col_fact in columns_fact:
                            if df_fact_added.loc[df_fact_added.object == obj_added, col_fact].values[0] == 1:
                                dic[col_rule] = col_fact
                                third_method = True
                                break

                    for obj in objects:
                        if '[' in obj and ']' in obj:
                            x = obj[1:-1].split(',')

                            if obj_added_new[0][1:-1] == x[0][1:-1]:
                                for col_fact in columns_fact:
                                    if df_fact.loc[df_fact.object == obj, col_fact].values[0] == 1:
                                        first_element = col_fact
                                        break

                                for obj2 in objects:
                                    if '[' in obj2 and ']' in obj2:
                                        k = obj2[1:-1].split(',')

                                        if x[1][1:] == k[0] and obj_added_new[1][1:] == k[1][1:]:
                                            for col_fact2 in columns_fact:
                                                if df_fact.loc[df_fact.object == obj2, col_fact2].values[0] == 1:
                                                    second_element = col_fact2
                                                    first_method = True
                                                    break
                                        elif x[1][1:] == k[1][1:] and obj_added_new[1][1:] == k[0]:
                                            for col_fact2 in columns_fact:
                                                if df_fact.loc[df_fact.object == obj2, col_fact2].values[0] == 1:
                                                    second_element = col_fact2
                                                    second_method = True
                                                    break

                                if second_element is not None:
                                    final_element.extend([first_element, second_element])

                                    if col_rule not in dic:
                                        dic[col_rule] = final_element

                                    break

        for key, value in dic.items():
            if first_method:
                f.write(key + '(X,Y) :- ' + value[0] + '(X,Z), ' + value[1] + '(Z,Y).\n')
            elif second_method:
                f.write(key + '(X,Y) :- ' + value[0] + '(X,Z), ' + value[1] + '(Y,Z).\n')
            elif third_method:
                f.write(key + '(X,Y) :- ' + value + '(X,Y).\n')

        f.close()


if __name__ == "__main__":
    prolog2Table = Prolog2Table()
    prolog = Prolog()
    prolog.consult('rules.pl')

    content = prolog2Table.parse_file('test.pl')

    columns = ['object']
    df_result = pd.DataFrame(columns=columns)

    if prolog2Table.add_fact_to_db(content):
        df_result = prolog2Table.create_table(content, df_result)
        df_result.loc[len(df_result.index), 'object'] = '----------'
        df_result['----------'] = '-'
        df_result = prolog2Table.add_rule(content, df_result)

        timestr = time.strftime("%Y%m%d-%H%M%S")
        #print(df_result)
        df_result.to_csv('outputs/' + 'table_' + timestr + '.csv', sep='\t', encoding='utf-8')
    else:
        print("Something was wrong with the prolog fact query")

    time.sleep(60)

    df = pd.read_csv('outputs/table_20190114-110354.csv', sep=',', header=None)
    table2Prolog = Table2Prolog()

    index = df[df['object'] == '----------'].index.values.astype(int)[0]

    df_fact = df.loc[: index - 1, : '----------']
    df_fact = df_fact.drop(['----------'], axis=1)

    df_rule = df.loc[:, '----------':]
    df_rule = df_rule.drop(['----------'], axis=1)

    file = table2Prolog.create_fact(df_fact, open("prova.pl", "w+"))

    file = table2Prolog.create_rule(df, df_fact, df_rule, file)

    df_fact_added = df.loc[index + 1:, : '----------']
    df_fact_added = df_fact_added.drop(['----------'], axis=1)

    if df_fact_added.shape[0] == 0:
        file.close()
    else:
        table2Prolog.create_complicated_rule(df, df_fact_added, df_fact, df_rule, file)

