import csv
from collections import Counter


class DTree(object):

    def __init__(self, training_file):
        self.training_file = training_file
        self.root = None
        self.parse_csv()
        self.get_distinct_values()


    def parse_csv(self, dependent_index=-1):
        if dependent_index != -1:
            raise NotImplementedError

        reader = csv.reader(self.training_file)
        attributes = ['Clump_Thickness', 'Cell_Size_Uniformity', 'Cell_Shape_Uniformity', 'Marginal_Adhesion',
                      'Single_Epi_Cell_Size', 'Bare_Nuclei', 'Bland_Chromatin', 'Normal_Nucleoli', 'Mitosis', 'Class']
        data = []
        for row in reader:
            row = dict(zip(attributes, row))
            data.append(row)
        self.training_file.close()

        self.dependent = attributes[dependent_index]
        self.attributes = [a for a in attributes if a != self.dependent]
        self.all_attributes = attributes
        self.data = data


    def get_distinct_values(self):
        values = {}
        for attr in self.all_attributes:  # Use all attributes because ugly
            values[attr] = set(r[attr] for r in self.data)
        self.values = values


    def plot(self, x=1, y=1):
        self.root._plot()


    def decide(self, attributes):
        if len(attributes) != len(self.attribute_order):
            print(self.attribute_order)
            raise ValueError("supplied attributes do not match data")
        attrs_dict = dict(zip(self.attribute_order, attributes))
        return self.root._decide(attrs_dict)


    def test_file(self, testing_file, csv=None):
        import csv
        reader = csv.reader(testing_file)
        first_row = ['Clump_Thickness', 'Cell_Size_Uniformity', 'Cell_Shape_Uniformity', 'Marginal_Adhesion',
                     'Single_Epi_Cell_Size', 'Bare_Nuclei', 'Bland_Chromatin', 'Normal_Nucleoli', 'Mitosis', 'Class']

        if first_row == self.all_attributes or first_row == self.attributes:
            test_data = []
        else:
            test_data = [dict(zip(self.all_attributes, first_row))]
        for row in reader:
            row = dict(zip(self.all_attributes, row))
            test_data.append(row)

        testing_file.close()

        correct = 0.
        for row in test_data:
            formatted = [row[a] for a in self.attributes]
            decision = self.decide(formatted)
            try:
                expected_str = "(expected {0})".format(self.manOrBan(row[self.dependent]))
                if row[self.dependent] == self.ktheNumer(decision):
                    correct += 1
                    expected_str += ", CORRECT"
                else:
                    expected_str += ", INCORRECT"
            except KeyError:
                expected_str = ""

            print("{0} -> {1} {2}".format(formatted, self.manOrBan(self.ktheNumer(decision)), expected_str))
        print("% correct: {0}".format((correct / len(test_data)) * 100))


    def ktheNumer(self, str):
        for i in str:
            if i in '0123456789':
                return i;
        return -1


    def manOrBan(self, nr):
        if nr in '2':
            return 'benign'
        else:
            return 'malignant'


    def filter_subset(self, subset, attr, value):
        return [r for r in subset if r[attr] == value]


    def value_counts(self, subset, attr, value, base=False):
        counts = Counter()
        for row in subset:
            if row[attr] == value or base:
                counts[row[self.dependent]] += 1
        return counts


    def rules(self):
        return sorted(
            self.root._rules(),
            key=lambda t: (len(t), [p[1] for p in t if isinstance(p, tuple)])
        )


    def set_attributes(self, attributes):
        self.attribute_order = attributes


    def attr_counts(self, subset, attr):
        counts = Counter()
        for row in subset:
            counts[row[attr]] += 1
        return counts


    def depth(self):
        return self.root._depth(0)


    def num_leaves(self):
        if self.root.leaf:
            return 1
        else:
            return sum(c._num_leaves for c in self.root.children)


    def distinct_values(self):
        values_list = []
        for s in self.values.values():
            for val in s:
                values_list.append(val)
        return values_list


    def ktheEmrin(self):
        return self.training_file.name


    def numberOfRow(self):
        return ("Nr i rreshtave {}".format(len(self.data)))


    def BaseDateEntropy(self):
        return ("Base Date Entropy {}".format(self.get_base_entropy(self.data)))


class DTreeNode(object):

    def __init__(self, label, parent_value=None, properties={}, leaf=False):
        self.label = label
        self.children = []
        self.parent_value = parent_value
        self.properties = properties
        self.leaf = leaf


    def _plot(self, xoffset, yoffset):
        raise NotImplementedError


    def _decide(self, attrs_dict):
        if self.leaf:
            return self.label
        val = attrs_dict[self.label]
        for node in self.children:
            if val == node.parent_value:
                return node._decide(attrs_dict)
        raise ValueError("Invalid property found: {0}".format(val))


    def add_child(self, node):
        self.children.append(node)


    def num_children(self):
        return len(self.children)


    def _num_leaves(self):
        if self.leaf:
            return 1
        else:
            return sum(c.num_leaves for c in self.children)


    def _depth(self, init):
        if self.leaf:
            return init
        else:
            return max(c._depth(init + 1) for c in self.children)


    def _rules(self, parent=None, previous=()):
        rows = []
        if parent is not None:
            previous += ((parent.label, self.parent_value),)
        if self.leaf:
            previous += ((self.label),)
            rows.append(previous)
        else:
            for node in self.children:
                rows.extend(node._rules(self, previous))
        return rows
