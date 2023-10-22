from itertools import product

def replace_and_clean(data, change_dict):

    for old_char, new_char in change_dict.items():
        data = data.replace(old_char, new_char)
    

    lines = data.split(".")
    cleaned_lines = []
    for line in lines:
        cleaned_line = "".join(char for char in line if char.isalpha() or char in ['"', ' '])
        cleaned_lines.append(cleaned_line)
    
    return cleaned_lines

def read_file(file_name):
    change_dict = {"\n": " ", "?": ".", "!" : ".", '?"' : '".', '!"' : '".', '."' : '".', ',"' : '",'}
    
    with open(file_name) as file:
        data = file.read()
    
    return replace_and_clean(data, change_dict)

            
def Name_sirs(cleaned_lines):
    sirs = set()
    for line in cleaned_lines:
        Names_in_line(sirs, line)
        
    return sorted(sirs)
    
#处理测试语句
def Names_in_line(sirs, line):
    words = line.split()
    index = 0 
    while index < len(words):
        clean_word = ""
        for char in words[index]:
            if char.isalpha():
                clean_word += char

        if clean_word == "Sir":
            index += 1
            sirs.add(words[index])
        
        if clean_word == "Sirs":
            index += 1
            while words[index] != "and":
                sirs.add(words[index])
                index += 1
            
            index += 1
            sirs.add(words[index])
        index += 1


def extract_sentence(line):
    begin = line.find('"')
    end = line.rfind('"')
    return line[begin + 1:end], line[:begin] + line[end + 1:]

def find_speaker_name(rest, keyword="Sir"):
    words = rest.split()
    index = words.index(keyword)
    return words[index + 1]

def replace_pronouns(sentence, name, sirs):
    sentence = sentence.replace("I ", f"{name} ")
    sentence = sentence.replace(" us ", " " + " ".join(sirs) + " ")
    return sentence

def speaker_conditions(cleaned_lines, sirs):
    conditions = {}
    for line in cleaned_lines:
        if '"' in line:
            sentence, rest = extract_sentence(line)
            name = find_speaker_name(rest)
            sentence = replace_pronouns(sentence, name, sirs)
            conditions[name] = conditions.get(name, []) + [sentence]
    return conditions

def check_condition(is_knight, condition, one_answer, sirs):# 判断speaker的每句话
    names = []
    roles = []
    for speaker in condition.split():
        if speaker in sirs:
            names.append(speaker)
            roles.append(one_answer[sirs.index(speaker)])
    
    if "Knight" in condition.split()[-1]:
        target = 1
    else:
        target = 0
        
    if "least one" in condition or "or" in condition:
        true_condition = roles.count(target) >= 1
    elif "most one" in condition:
        true_condition = roles.count(target) <= 1
    elif "xactly one" in condition:
        true_condition = roles.count(target) == 1
    else:
        true_condition = roles.count(target) == len(roles)
    
    return (is_knight and true_condition) or (not is_knight and not true_condition)


def find_posible_answer(cleaned_lines, sirs):
    posible_answer = []
    options = (0, 1)
    posible_answer = list(product(options, repeat=len(sirs)))
    
    conditions = speaker_conditions(cleaned_lines, sirs)
    answer = []
    for one_answer in posible_answer:
        is_answer = True
        for name, person_conditions in conditions.items():
            is_knight = one_answer[sirs.index(name)] == 1
            
            all_passed = True
            for condition in person_conditions:
                is_passed = check_condition(is_knight, condition, one_answer, sirs)
                if not is_passed:
                    all_passed = False
                    break
            if not all_passed:
                is_answer = False
                break
                
        if is_answer:
            answer.append(one_answer)
    return answer


def final_answer(answer, sirs): 
    loc = 0
    result_count = len(answer)

    while True:
        if result_count == 0:
            print("There is no solution.")
            break
        elif result_count > 1:
            print(f"There are {len(answer)} solutions.")
            break
        else:
            print("There is a unique solution:")
            unique_answer = answer[0]
            while loc < len(sirs):
                name = sirs[loc]
                if unique_answer[loc] == 1:
                    role = "Knight"
                else:
                    role = "Knave"
                print(f"Sir {name} is a {role}.")
                loc += 1
            break

def main():
    
    file_name = input("Which text file do you want to use for the puzzle? ")
    cleaned_lines = read_file(file_name)
    sirs = Name_sirs(cleaned_lines)
    print("The Sirs are: " + " ".join(sirs))
    
    answer = find_posible_answer(cleaned_lines, sirs)
    final_answer(answer, sirs)

main()
