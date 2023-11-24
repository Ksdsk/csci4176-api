import math

class Student:
    def __init__(self, id, belbin_traits):
        self.id = id
        self.belbin_traits = belbin_traits

def find_best_trait(student, disallowed_traits = []):
    best_trait_rank = -1
    best_trait = None
    for trait in student.belbin_traits:
        if best_trait_rank < student.belbin_traits[trait] and trait not in disallowed_traits:
            best_trait = trait
            best_trait_rank = student.belbin_traits[trait]
    return best_trait

traits1 = {
    "coordinator": 10, 
    "resource_investigator": 1, 
    "specialist": 1, 
    "shaper": 1, 
    "plant": 1, 
    "teamworker": 1, 
    "implementer": 1, 
    "monitor_evaluator": 1, 
    "completer_finisher": 1
}

traits2 = {
    "coordinator": 1, 
    "resource_investigator": 10, 
    "specialist": 1, 
    "shaper": 1, 
    "plant": 1, 
    "teamworker": 1, 
    "implementer": 1, 
    "monitor_evaluator": 1, 
    "completer_finisher": 1
}

traits3 = {
    "coordinator": 1, 
    "resource_investigator": 1, 
    "specialist": 10, 
    "shaper": 1, 
    "plant": 1, 
    "teamworker": 1, 
    "implementer": 1, 
    "monitor_evaluator": 1, 
    "completer_finisher": 1
}

traits4 = {
    "coordinator": 1, 
    "resource_investigator": 1, 
    "specialist": 1, 
    "shaper": 10, 
    "plant": 1, 
    "teamworker": 1, 
    "implementer": 1, 
    "monitor_evaluator": 1, 
    "completer_finisher": 1
}

traits5 = {
    "coordinator": 1, 
    "resource_investigator": 1, 
    "specialist": 1, 
    "shaper": 1, 
    "plant": 10, 
    "teamworker": 1, 
    "implementer": 1, 
    "monitor_evaluator": 1, 
    "completer_finisher": 1
}

traits6 = {
    "coordinator": 1, 
    "resource_investigator": 1, 
    "specialist": 1, 
    "shaper": 1, 
    "plant": 1, 
    "teamworker": 10, 
    "implementer": 1, 
    "monitor_evaluator": 1, 
    "completer_finisher": 1
}

traits7 = {
    "coordinator": 1, 
    "resource_investigator": 1, 
    "specialist": 1, 
    "shaper": 1, 
    "plant": 1, 
    "teamworker": 1, 
    "implementer": 10, 
    "monitor_evaluator": 1, 
    "completer_finisher": 1
}

traits8 = {
    "coordinator": 1, 
    "resource_investigator": 1, 
    "specialist": 1, 
    "shaper": 1, 
    "plant": 1, 
    "teamworker": 1, 
    "implementer": 1, 
    "monitor_evaluator": 10, 
    "completer_finisher": 1
}

traits9 = {
    "coordinator": 1, 
    "resource_investigator": 1, 
    "specialist": 1, 
    "shaper": 1, 
    "plant": 1, 
    "teamworker": 1, 
    "implementer": 1, 
    "monitor_evaluator": 1, 
    "completer_finisher": 10
}

traits10 = {
    "coordinator": 10, 
    "resource_investigator": 10, 
    "specialist": 10, 
    "shaper": 1, 
    "plant": 1, 
    "teamworker": 10, 
    "implementer": 1, 
    "monitor_evaluator": 10, 
    "completer_finisher": 10
}

traits11 = {
    "coordinator": 1, 
    "resource_investigator": 10, 
    "specialist": 0, 
    "shaper": 1, 
    "plant": 1, 
    "teamworker": 1, 
    "implementer": 11, 
    "monitor_evaluator": 100, 
    "completer_finisher": 1
}

students = [
    Student("1", traits1),
    Student("2", traits2),
    Student("3", traits3),
    Student("4", traits4),
    Student("5", traits5),
    Student("6", traits6),
    Student("7", traits7),
    Student("8", traits8),
    Student("9", traits9),
    Student("10", traits10),
    Student("11", traits11),
]

trait_stacks = {
    "coordinator": [], 
    "resource_investigator": [], 
    "specialist": [], 
    "shaper": [], 
    "plant": [], 
    "teamworker": [], 
    "implementer": [], 
    "monitor_evaluator": [], 
    "completer_finisher": []
}

max_team_size = 6
teams = {i:[] for i in range(math.ceil(len(students)/max_team_size))}
print(teams)

# Prime stacks
for student in students:
    trait_stacks[find_best_trait(student)].append(student)

# Sort stacks
for trait in trait_stacks:
    trait_stacks[trait].sort(key=lambda student: student.belbin_traits[trait])

# Verify
for trait in trait_stacks:
    print(trait)
    for student in trait_stacks[trait]:
        print(student.belbin_traits[trait])

# Belbin Distribution
enrolled_count = 0
current_team = 0
unassigned_students = students
while enrolled_count < len(students):
    for trait in trait_stacks:
        if len(trait_stacks[trait]) > 0:
            student = trait_stacks[trait].pop()
            if len(teams[current_team]) == max_team_size:
                current_team += 1
            teams[current_team].append(student)
            enrolled_count += 1

# Verify
print("-------------------")
for team in teams:
    print(team)
    for student in teams[team]:
        print(find_best_trait(student))
