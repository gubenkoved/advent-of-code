import re
import collections


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

    # all starts with "in" workflow
    active = [('in', obj) for obj in objects]
    accepted, rejected = [], []

    def process(workflow, obj):
        # process rules
        for rule in workflows[workflow]:
            if rule.condition is None:
                return rule.action

            prop = obj.get(rule.condition.prop)
            rule_matched = False
            if rule.condition.op == '<':
                rule_matched = prop < rule.condition.value
            elif rule.condition.op == '>':
                rule_matched = prop > rule.condition.value

            if rule_matched:
                return rule.action

        assert 'indecisive'

    while active:
        snapshot = list(active)
        active = []
        for workflow, obj in snapshot:
            new_workflow = process(workflow, obj)
            if new_workflow == 'A':
                accepted.append(obj)
            elif new_workflow == 'R':
                rejected.append(obj)
            else:
                active.append((new_workflow, obj))

    print(accepted)
    print(sum(sum(obj.values()) for obj in accepted))
