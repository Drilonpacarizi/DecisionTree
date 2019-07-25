import dtree
import math


class ID3(dtree.DTree):

    def create_tree(self, parent_subset=None, parent=None, parent_value=None,
                    remaining=None):

        if parent_subset is None:
            subset = self.data
        else:
            subset = self.filter_subset(parent_subset,
                                        parent.label,
                                        parent_value)

        if remaining is None:
            remaining = self.attributes

        use_parent = False
        counts = self.attr_counts(subset, self.dependent)
        if not counts:

            subset = parent_subset
            counts = self.attr_counts(subset, self.dependent)
            use_parent = True

        if len(counts) == 1:
            node = dtree.DTreeNode(
                label=counts.keys(),
                leaf=True,
                parent_value=parent_value
            )
        elif not remaining or use_parent:
            most_common = max(counts, key=lambda k: counts[k])
            node = dtree.DTreeNode(
                label=most_common,
                leaf=True,
                parent_value=parent_value,
                properties={'estimated': True}
            )
        else:
            igains = []
            for attr in remaining:
                igains.append((attr, self.information_gain(subset, attr)))

            max_attr = max(igains, key=lambda a: a[1])

            node = dtree.DTreeNode(
                max_attr[0],
                properties={'information_gain': max_attr[1]},
                parent_value=parent_value
            )

        if parent is None:
            self.set_attributes(self.attributes)
            self.root = node
        else:
            parent.add_child(node)

        if not node.leaf:
            new_remaining = remaining[:]
            new_remaining.remove(node.label)
            for value in self.values[node.label]:
                self.create_tree(
                    parent_subset=subset,
                    parent=node,
                    parent_value=value,
                    remaining= new_remaining
                )

    def information_gain(self, subset, attr):

        gain = self.get_base_entropy(subset)
        counts = self.attr_counts(subset, attr)
        total = float(sum(counts.values()))
        for value in self.values[attr]:
            gain += -((counts[value]/total)*self.entropy(subset, attr, value))
        return gain

    def get_base_entropy(self, subset):

        return self.entropy(subset, self.dependent, None, base=True)

    def entropy(self, subset, attr, value, base=False):

        counts = self.value_counts(subset, attr, value, base)
        total = float(sum(counts.values()))
        entropy = 0
        for dv in counts:
            proportion = counts[dv] / total
            entropy += -(proportion*math.log(proportion, 2))
        return entropy


if __name__ == '__main__':
    import argparse
    import pprint
    import sys

    parser = argparse.ArgumentParser()
    parser.add_argument('training_file', type=argparse.FileType('r'))
    parser.add_argument('-t', '--testing_file', nargs='?', const=None,
                        default=False, type=argparse.FileType('r'))
    parser.add_argument('-d', '--decide', action='store_true')
    parser.add_argument('-r', '--rules', action='store_true')

    args = parser.parse_args()
    print(args.testing_file)
    if args.testing_file is None:
        sys.exit('Testing File nuk eshte')



    id3 = ID3(args.training_file)

    id3.create_tree()

    if args.rules:
        pprint.pprint(id3.rules(), width=400)

    if args.testing_file:
        id3.test_file(args.testing_file)

    if args.decide:
        id3.decision_repl()

    print("Per data set : {} , {} , ku {}".format(id3.ktheEmrin(), id3.numberOfRow(), id3.BaseDateEntropy()))

