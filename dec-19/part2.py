import re
import collections
from typing import List


RuleCondition = collections.namedtuple('RuleCondition', ['prop', 'op', 'value'])
Rule = collections.namedtuple('Rule', ['condition', 'action'])


if __name__ == '__main__':
    workflows = {}
    objects = []
    rule_re = re.compile(r'([a-z])(.)([0-9]+):([a-z]+)', re.IGNORECASE)

    def parse_rule(rule_string):
        # unconditional rule
        if ':' not in rule_string:
            return Rule(None, rule_string)

        # conditional rule
        match = rule_re.match(rule_string)
        return Rule(
            RuleCondition(match.group(1), match.group(2), int(match.group(3))),
            match.group(4)
        )


    with open('data.txt') as f:
        workflow_re = re.compile(r'([a-z]+)\{([^}]+)\}')
        while True:
            line = f.readline()

            if line == '\n':
                break

            match = workflow_re.match(line)
            workflows[match.group(1)] = [
                parse_rule(x) for x in match.group(2).split(',')]

        # read objects
        obj_re = re.compile(r'([a-z]+)=([0-9]+)')
        while True:
            line = f.readline()

            if not line:
                break

            obj = {}
            for prop, val in obj_re.findall(line):
                obj[prop] = int(val)
            objects.append(obj)

    # find all paths that start at "in" workflow and lead to "A"
    # in this graph (assume no cycles) for each path we have a combination
    # of all rules that apply, we need to analytically count amount of
    # objects that comply with the rule

    accepts_paths = []

    def negate(condition: RuleCondition) -> RuleCondition:
        if condition.op == '<':
            return RuleCondition(condition.prop, '>', condition.value - 1)
        else:
            return RuleCondition(condition.prop, '<', condition.value + 1)

    def walk(workflow, conditions):
        if workflow == 'A':
            accepts_paths.append(conditions)
            return
        elif workflow == 'R':
            return

        extra_conditions = []
        for rule in workflows[workflow]:
            if rule.condition is None:
                # unconditional
                walk(rule.action, conditions + extra_conditions)
                return

            walk(rule.action, conditions + extra_conditions + [rule.condition])

            # going to next rules implies that this condition is not satisfied
            extra_conditions.append(negate(rule.condition))


    walk('in', [])

    # given all these paths by construction are not compatible with each other
    # we can just sum individual match counts

    # not very efficient way, but it does not matter really here
    def possible_combinations(conditions: List[RuleCondition]):
        combinations = 1
        for prop in ['x', 'm', 'a', 's']:
            matched_count = 0
            for val in range(1, 4000 + 1):
                val_matched = True

                # value should match ALL conditions
                for condition in conditions:
                    if condition.prop != prop:
                        continue
                    if condition.op == '>':
                        if not val > condition.value:
                            val_matched = False
                    else:
                        assert condition.op == '<'
                        if not val < condition.value:
                            val_matched = False

                if val_matched:
                    matched_count += 1
            combinations *= matched_count
        return combinations

    print(sum(possible_combinations(conditions) for conditions in accepts_paths))
