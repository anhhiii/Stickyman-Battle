class DecisionNode:
    def __init__(self, condition=None, true_branch=None, false_branch=None, action=None):
        self.condition = condition  
        self.true_branch = true_branch  
        self.false_branch = false_branch  
        self.action = action  

    def decide(self, context):
        if self.action is not None:
            return self.action  

        if self.condition(context):
            return self.true_branch.decide(context)
        else:
            return self.false_branch.decide(context)

def is_enemy_nearby(context):
    return abs(context['stickman']['x'] - context['enemy']['x']) < 100

def attack():
    return "attack"

def move_back_and_forth():
    return "move_back_and_forth"

def build_decision_tree():

    attack_node = DecisionNode(action=attack)
    move_back_and_forth_node = DecisionNode(action=move_back_and_forth)
    root_node = DecisionNode(condition=is_enemy_nearby, true_branch=attack_node, false_branch=move_back_and_forth_node)

    return root_node
