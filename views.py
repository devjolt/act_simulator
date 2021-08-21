from django.shortcuts import render
from random import randint, shuffle
from collections import Counter

def home(request):
    return render(request, 'act_simulator/home.html')

def error_detection(request):
    '''
    1. Choose a type of sentence
    2. generate sentence
    3. select between 0-4 changes
    4. assign indicator of selected number to correct
    5. select character indexes to change
    6. change indexed characters appropriately
    7.
    '''
    def rand_letter(case = 'rand'):
        if case == 'rand':
            return chr(randint(65,90)) if randint(0,1) == 1 else chr(randint(97, 122))
        elif case == 'upper':
            return chr(randint(65,90))
        elif case == 'lower':
            return chr(randint(97, 122))
        
    def rand_word(length, case = 'rand'):
        if case == 'rand':
            if randint(0,1) == 0:
                word = [rand_letter('upper') for i in range(length)]
            else:
                word = [rand_letter('lower') for i in range(length)]
        elif case == 'mixed':
            word = [rand_letter() for i in range(length)]        
        else:
            word = [rand_letter(case) for i in range(length)]       
        return ''.join(word)
        
    def num_word(length):
        return ''.join([str(randint(0,9)) for i in range(length)])

    extension_list = ('com', 'co.uk', 'net', 'org', 'gov', 'eu', 'gov.uk', rand_word(3, 'lower'))

    def user_name():
        #usernames: [1-3]numbers + word OR word + int{1-3}, 
        print('user_name')
        num_str = num_word(randint(2,5))
        word = rand_word(randint(2,5))
        return num_str + word if randint(0,1)==0 else word+num_str

    def email():
        #email: username@domain.ext
        uname = user_name()
        domain = rand_word(randint(3, 8), 'lower')
        extension = extension_list[randint(0,len(extension_list)-1)]
        print('email module')
        return uname + '@' + domain + '.' + extension

    def url():
        print('url module')
        protocol = 'http' if randint(0,1) == 1 else 'https'
        domain = rand_word(randint(4, 8), 'lower')
        extension = extension_list[randint(0,len(extension_list)-1)]
        return protocol + '://www.' + domain + '.' + extension

    def number_plates():
        #number_plates:
        #[a-z] [1-9]{1-3} [a-z]{3} OR [A-Z]{2}[1-9]{2} [A-Z]{3}
        print('number plate module')
        three_letters = rand_word(3, 'upper')#needed whatever else happens
        if randint(0,1) == 0:
            first = rand_letter('upper')
            second = num_word(3)
            return first + ' ' + second + ' ' + three_letters
        else:
            first = rand_word(2,'upper')
            second = num_word(2)
            return first + second + ' ' + three_letters
   
    def letters_numbers():
        print('letters_numbers module')
        letters = rand_word(randint(1,3), 'upper')
        numbers = num_word(randint(4,6))
        return letters + ' ' + numbers

    def l_nnn_nnn():
        print('l_nnn_nnn module')
        letter = rand_letter('upper')
        three_numbers = num_word(3)
        more_numbers = num_word(3)
        return letter + ' ' + three_numbers + ' ' + more_numbers

    def select_sentence():
        sentences = (
            user_name, email, url, number_plates, letters_numbers, l_nnn_nnn
            )
        return sentences[randint(0, len(sentences)-1)]()
        
    def make_differences():
        return randint(0, 4)

    def replacer(sentence, indexes):
        """
        passed in index values are alnum
        """
        new_sentence = ''
        for i in range(len(sentence)):
            if i in indexes:
                #if number, replace with random number
                #elif letter, replace with random letter
                if sentence[i].isdecimal():
                    new_sentence += num_word(1)
                elif sentence[i].isalpha():
                    if sentence[i].isupper():
                        new_sentence += rand_letter('upper')
                    elif sentence[i].islower():
                        new_sentence += rand_letter('lower')
            else:
                new_sentence += sentence[i]
        return new_sentence

    def make_sentence_two(sentence, differences):
        indexes = set()
        print(differences)
        while len(indexes) != differences: #until set contains differences values
            index = randint(0, len(sentence)-1)#pick a random character from the sentence
            if sentence[index].isalnum():#if the character isalnum, add that value to indexes
                indexes.update({index})
        
        return replacer(sentence, indexes) 

    def make_items(differences):
        items = []
        for i in range(5):
            if differences == i:
                items.append({'name':f'{i}', 'indicator':'correct'})
            else:
                items.append({'name':f'{i}', 'indicator':'incorrect'})
        return items
        
    instructions = (
        'Study these sentences carefully, comparing the characters and their order.',
        'The copy (Sentence 2) may or may not have errors in it compared to the original. Click the "Next Step" button to answer.',
    )
    
    differences = make_differences()
    sentence_one = select_sentence()
    sentence_two = make_sentence_two(sentence_one, differences)
    items = make_items(differences)
    context = {
        'assessment_title':'Error Detection',
        'instructions':instructions,
        'rule_one':sentence_one,
        'rule_two':sentence_two,
        'prompt':'',
        'items':items,
    }

    return render(request, 'act_simulator/error_detection.html', context)

def orientation(request):
    '''
    two sentences:
    color_sentence: white over black OR black over white
    orientation_sentence:hor_dir ver_dir over hor_dir ver_dir
    
    either sentence could be first
    '''

    arrows = {
        'White':{'Up Right':'\u2b00', 'Up Left':'\u2b01', 'Down Right':'\u2b02', 'Down Left':'\u2b03'},
        'Black':{'Up Right':'\u2b08', 'Up Left':'\u2b09', 'Down Right':'\u2b0a', 'Down Left':'\u2b0b'},
        }

    def choose_from(iterable):
        return iterable[randint(0, len(iterable)-1)]

    def select_correct():
        #deal with top
        top_color, bottom_color = ('White', 'Black') if randint(0,1) == 0 else ('Black', 'White')
        direction = [i for i in arrows['White'].keys()]
        top_direction,bottom_direction = choose_from(direction), choose_from(direction)
        correct = {
            'top':{'color':top_color, 'direction':top_direction},
            'bottom':{'color':bottom_color, 'direction':bottom_direction},
            }
        return correct

    def make_rules(correct):
        #top above bottom OR bottom below top
        if randint(0,1):
            rule_one = ' '.join([correct['top']['color'],'ABOVE',correct['bottom']['color']])
        else:
            rule_one = ' '.join([correct['bottom']['color'],'BELOW',correct['top']['color']])
        if randint(0,1):
            rule_two = ' '.join([correct['top']['direction'],'ABOVE',correct['bottom']['direction']])
        else:
            rule_two = ' '.join([correct['bottom']['direction'],'BELOW',correct['top']['direction']])
        return rule_one, rule_two

    def select_top_bottom():
        top_color, bottom_color = ('White', 'Black') if randint(0,1) == 0 else ('Black', 'White')
        direction = [i for i in arrows['White'].keys()]
        top_direction,bottom_direction = choose_from(direction), choose_from(direction)
        item = (arrows[top_color][top_direction],arrows[bottom_color][bottom_direction])
        return item

    def make_items(correct):
        items_set = set()
        correct_item = (#make correct item and add to set
            arrows[correct['top']['color']][correct['top']['direction']],
            arrows[correct['bottom']['color']][correct['bottom']['direction']],
            )
        items_set.add(correct_item)
        while len(items_set) != 6:#add other items till 6
            items_set.add(select_top_bottom())
        #label items correct or incorrect
        items = []
        for item in items_set:
            if item == correct_item:
                items.append({'name':{'top':item[0],'bottom':item[1]}, 'indicator':'correct'})
            else:
                items.append({'name':{'top':item[0],'bottom':item[1]}, 'indicator':'incorrect'})
        return items

    instructions = (
        "Study the rules below carefully. Which set of arrows below obeys both of these rules?",
        "Select your answer by clicking on the set of arrows which correctly shows the rule you have just learned."
        )

    correct = select_correct()
    rule_one, rule_two = make_rules(correct)
    items = make_items(correct)

    context = {
        'assessment_title':'Orientation',
        'instructions':instructions,
        'rule_one':rule_one,
        'rule_two':rule_two,
        'prompt':'Options',
        'items':items,
        'link':'orientation',
    }
    return render(request, 'act_simulator/orientation.html', context)

def reasoning_categories(request):
    
    main_dict = {
        'living' : {
                'Fish':('Cod', 'Haddock', 'Salmon', 'Tuna', 'Mackrel', 'Baracuda'),
                'Tree':('Ash', 'Yew', 'Oak', 'Sycamore'),
                'Bird':('Duck', 'Hawk', 'Sparrow', 'Eagle'),
                'Vegetable':('Cabbage', 'Cucumber', 'Potato', 'Carrot', 'Brocoli', 'Cauliflower', 'Lettuce'),
                'Flower':('Rose', 'Dandelion', 'Buttercup', 'Daffodil'),
                'Insect':('Moth', 'Wasp', 'Mosquito', 'Ant', 'Beetle', 'Horsefly'),
        },
        'things' : {
                'Tool':('Knife', 'Hammer', 'Screwdriver', 'File', 'Wrench', 'Spanner', 'Ruler'),
                'Building':('House', 'Igloo', 'Theatre', 'Hospital', 'Flat', 'Castle', 'Bungalow'),
                'Clothing':('Hat', 'Coat', 'Glove', 'Sock', 'Boot'),
                'Sport':('Cricket', 'Hockey', 'Rugby', 'Cycling', 'Swimming'),
                'Gas':('Oxygen', 'Hydrogen', 'Nitrogen', 'Helium'),
                'Drink':('Water', 'Lemonade', 'Cocoa', 'Juice', 'Milk'),
                'Metal':('Copper', 'Steel', 'Lead', 'Iron', 'Mercury'),
                'Transport':('Car', 'Truck', 'Train', 'Helicopter', 'Taxi', 'Bicycle', 'Motorbike'),
        }
    }

    def choose_from(iterable):
        if type(iterable) is dict:
            iterable = [key for key, value in iterable.items()]        
        return iterable[randint(0, len(iterable)-1)]

    def two_from(category, disallowed = []):
        found = set()
        while len(found) != 2:
            new = choose_from(category)
            if new not in disallowed:
                found.add(new)
        cat_list = []
        for item in found:
            cat_dict = {}
            cat_dict[item] = choose_from(category[item])
            cat_list.append(cat_dict)
        return tuple(cat_list)

    def make_items_statement_and_order(items_dict):#where items dict is a tuple of two key value pairs
        #select between above/below, before/after
        positions = ('before', 'after') if randint(0,1) == 0 else ('above', 'below')
        categories = []
        for item in items_dict:#putting category keys into lists for use in statements
            for key, value in item.items():
                categories.append(key)

        if randint(0,1):#statement uses first item
            statement = f"{categories[0]} {positions[0]} {categories[1]}" 
        else:#statement uses second item
            statement = f"{categories[1]} {positions[1]} {categories[0]}" 
            
        ordered_items = []
        for item in items_dict:#putting category values into lists for use in ordered_tuples to build answers
            for key, value in item.items():
                ordered_items.append(value)
        return statement, categories, ordered_items

    def make_incorrect_answers(cats_in_order, order):#correct order is ordered list of 4 items  
        #make a list of all categories in correct order so we can mess with it
        #make seven incorrect answers:
        #1. reverse living and thing
        incorrect1 = [
            choose_from(main_dict[order[1]][cats_in_order[2]]),
            choose_from(main_dict[order[1]][cats_in_order[3]]),
            choose_from(main_dict[order[0]][cats_in_order[0]]),
            choose_from(main_dict[order[0]][cats_in_order[1]]),
            ]
        #2. for living, reverse cats
        incorrect2 = [
            choose_from(main_dict[order[0]][cats_in_order[1]]),
            choose_from(main_dict[order[0]][cats_in_order[0]]),
            choose_from(main_dict[order[1]][cats_in_order[2]]),
            choose_from(main_dict[order[1]][cats_in_order[3]]),
            ]
        #3. for things reverse cats
        incorrect3 = [
            choose_from(main_dict[order[0]][cats_in_order[0]]),
            choose_from(main_dict[order[0]][cats_in_order[1]]),
            choose_from(main_dict[order[1]][cats_in_order[3]]),
            choose_from(main_dict[order[1]][cats_in_order[2]]),
            ]
        #4. for living, non matching cats
        #replace one category in first:
        while True:
            new = choose_from(main_dict[order[0]])
            if new not in cats_in_order[:2]:
                break
        if randint(0,1) == 0:
            cats_in_order[0] = new
        else:
            cats_in_order[1] = new
        incorrect4 = [
            choose_from(main_dict[order[0]][cats_in_order[0]]),
            choose_from(main_dict[order[0]][cats_in_order[1]]),
            choose_from(main_dict[order[1]][cats_in_order[2]]),
            choose_from(main_dict[order[1]][cats_in_order[3]]),
            ]
        #5. replace one category in second
        while True:
            new = choose_from(main_dict[order[1]])
            if new not in cats_in_order[2:]:
                break
        if randint(0,1) == 0:
            cats_in_order[2] = new
        else:
            cats_in_order[3] = new
        incorrect5 = [
            choose_from(main_dict[order[0]][cats_in_order[0]]),
            choose_from(main_dict[order[0]][cats_in_order[1]]),
            choose_from(main_dict[order[1]][cats_in_order[2]]),
            choose_from(main_dict[order[1]][cats_in_order[3]]),
            ]
        
        #6. reverse both cats
        incorrect6 = [
            choose_from(main_dict[order[0]][cats_in_order[1]]),
            choose_from(main_dict[order[0]][cats_in_order[0]]),
            choose_from(main_dict[order[1]][cats_in_order[3]]),
            choose_from(main_dict[order[1]][cats_in_order[2]]),
            ]
        
        #7. random cats
        if randint(0,1) == 0:
            incorrect7 = [
                choose_from(main_dict[order[0]][cats_in_order[randint(0,1)]]),
                choose_from(main_dict[order[1]][cats_in_order[2]]),
                choose_from(main_dict[order[1]][cats_in_order[3]]),
                choose_from(main_dict[order[0]][cats_in_order[randint(0,1)]]),
                ]
        else:
            incorrect7 = [
                choose_from(main_dict[order[1]][cats_in_order[randint(2,3)]]),
                choose_from(main_dict[order[0]][cats_in_order[0]]),
                choose_from(main_dict[order[0]][cats_in_order[1]]),
                choose_from(main_dict[order[1]][cats_in_order[randint(2,3)]]),
                ]

        return (incorrect1, incorrect2, incorrect3, incorrect4, incorrect5, incorrect6, incorrect7)

    def make_statements_and_correct_and_incorrect():
        living_dicts = two_from(main_dict['living'])
        things_dicts = two_from(main_dict['things'])
        
        living_statement, living_cats, living_items = make_items_statement_and_order(living_dicts)
        things_statement, things_cats, things_items = make_items_statement_and_order(things_dicts)
        positions = ('before', 'after') if randint(0,1) == 0 else ('above', 'below')
        #decide whether living or things comes first and generate ordered answer list accordingly
        order = ('living', 'things') if randint(0,1) == 0  else ('things','living')

        cats_in_order = []
        
        if order[0] == 'living':
            correct_order = []
            for item in living_items:
                correct_order.append(item)
            for item in things_items:
                correct_order.append(item)

            cats_in_order = []
            for item in living_cats:
                cats_in_order.append(item)
            for item in things_cats:
                cats_in_order.append(item)

            if randint(0,1):
                living_things_statement = f'Living {positions[0]} Things'
            else:
                living_things_statement = f'Things {positions[1]} Living'

        else:
            correct_order = []
            for item in things_items:
                correct_order.append(item)
            for item in living_items:
                correct_order.append(item)

            cats_in_order = []
            for item in things_cats:
                cats_in_order.append(item)
            for item in living_cats:
                cats_in_order.append(item)

            if randint(0,1):
                living_things_statement = f'Things {positions[0]} Living'
            else:
                living_things_statement = f'Living {positions[1]} Things'
        
        incorrect = make_incorrect_answers(cats_in_order, order)

        items = []
        for item in incorrect:
            items.append({'name':{'one':item[0], 'two':item[1], 'three':item[2], 'four':item[3]}, 'indicator':'incorrect'})
        items.append({'name':{'one':correct_order[0], 'two':correct_order[1], 'three':correct_order[2], 'four':correct_order[3]}, 'indicator':'correct'})
        shuffle(items)
        shuffle(items)

        if randint(0,1):
            rule_one = living_statement
            rule_three = things_statement
        else:
            rule_three = living_statement
            rule_one = things_statement
        rule_two = living_things_statement
        
        return rule_one, rule_two, rule_three, items

    rule_one, rule_two, rule_three, items = make_statements_and_correct_and_incorrect()
    instructions = (
        "Read and memorise the rules; click the 'Next Step' button and the rules will disappear.",
        "Look at the lists of items and identify the one which matches the rules you read.",
        "Select your answer by clicking the correct list."
    )
    prompt = ''
    context = {
            'assessment_title':'Reasoning categories',
            'instructions':instructions,
            'rule_one':rule_one,
            'rule_two':rule_two,
            'rule_three':rule_three,
            'prompt':prompt,
            'items':items,
            'link':'reasoning_categories',
        }
    return render(request, 'act_simulator/reasoning_categories.html', context)


def number_fluency(request):
    '''
    two sums displayed one by one
    answer displayed
    '''
    def generate_top_bottom():
        #top and bottom must be within 5 of each other
        top = randint(16, 50)
        bottom = randint(top, top + 3) if randint(0,1)==0 else randint(top-3, top)
        return top, bottom#seed is top in this case

    def correct_answer(top, bottom):
        top_indicator, bottom_indicator, same_indicator = 'incorrect','incorrect','incorrect'
        if top > bottom:
            top_indicator = 'correct'
        elif bottom > top:
            bottom_indicator = 'correct'
        elif int(top) == int(bottom):
            same_indicator = 'correct'
        return top_indicator, bottom_indicator, same_indicator

    def mult_get_factors(num):
        factors =[] 
        for i in range(2, num):
            if num % i == 0:
                fac1, fac2 = i, num // i
                factors += ((fac1, fac2),)
        #print(num, factors)
        factors = factors[randint(0, len(factors)-1)]
        return factors[0], factors[1]
        
    def div_get_mults(num):
        mult = randint(2, 10)
        #if num * mult > 100, mult must be 2, 5, or 10
        valid_mult = False
        while valid_mult == False:
            if num * mult > 99:
                if mult not in (2, 5, 10):
                    mult = randint(2, 10)
                    continue
            valid_mult = True
        mult1, mult2 = num * mult, mult
        return mult1, mult2
            
    def add_get_addends(num):
        #don't allow this if num is less than 15
        addend1 = randint(3, num//2)
        while num - addend1 <= 0:
            addend1 = randint(2, num//2)
        addend2 = num - addend1
        return addend1, addend2

    def sub_get_minuend_substrahend(num):
        substrahend = randint(2, num)
        minuend = num + substrahend
        return  minuend,substrahend

    def select_op():
        ops = ('+', '-', '*', '/')
        return ops[randint(0, len(ops)-1)]

    def generate_expression(num):
        op = select_op()
        op_dict = {
                '+': add_get_addends,
                '-': sub_get_minuend_substrahend,
                '*': mult_get_factors,
                '/': div_get_mults
                }
        num1, num2 = op_dict[op](num)
        #print(num, '=', num1, op, num2)
        return f"{num1} {op} {num2}"

    def display_respond(top_exp, bottom_exp):
        top = f'Top: {top_exp}\r'
        sys.stdout.write(top)
        input()
        bottom = f'Bottom: {bottom_exp}\r'
        sys.stdout.write(bottom)
        input()
        response = input('''\rWhich is greater:\nt = Top\nb = Bottom\ns = Same\n>>> ''').strip(' ')
        response_dict = {'t':'top', 'b':'bottom', 's':'same'}
        return response_dict[response]

    def mark(response, correct):
        if response == correct:
            return True
        else:
            return False

    while True:
        try:
            top, bottom = generate_top_bottom() #select numbers
            print('answers: ', top, bottom)
            top_indicator,bottom_indicator,same_indicator = correct_answer(top, bottom) #identify correct answer
            print('indicators: ',top_indicator, bottom_indicator, same_indicator)
            top_exp = generate_expression(top)
            print('top expression: ', top_exp)
            bottom_exp = generate_expression(bottom)
            print('bottom expression: ', bottom_exp)
            break
        except ValueError:
            print('Trying new seeds...')

    instructions = (
        "Read and memorise the rule; click the 'Next Step' button and the rule will disappear.",
        "Look at the item list. How many of these match the previous rule? Click on the 'Next Step' button once you know the answer.",
        "Select your answer by clicking the correct number."
    )

    items = (
        {"name":'Top', "indicator":top_indicator},
        {'name':'Bottom', 'indicator':bottom_indicator},
        {'name':'Same', 'indicator':same_indicator},
    )

    context = {
        'assessment_title':'Number Fluency',
        'instructions':instructions,
        'rule_one':top_exp,
        'rule_two':bottom_exp,
        'prompt':'Which is greater',
        'items':items,
        'link':'number_fluency'
        }
    return render(request, 'act_simulator/number_fluency.html', context)

def word_rules(request):
    word_dict = {
            'fish':('cod', 'hadock', 'salmon', 'tuna', 'mackrel', 'baracuda'),
            'tree':('ash', 'yew', 'oak', 'sycamore'),
            'country':('France', 'Germany', 'Italy', 'Scotland', 'Ireland', 'Wales', 'England', 'Belgium'),
            'vegetable':('cabbage', 'cucumber', 'potato', 'carrot', 'brocoli', 'cauliflower', 'lettuce'),
            'transport':('car', 'truck', 'train', 'helicopter', 'taxi', 'bicycle', 'motorbike'),
            'clothing':('hat', 'coat', 'glove', 'sock', 'boot'),
            'insect':('moth', 'wasp', 'mosquito', 'ant', 'beetle', 'horsefly'),
            'tool':('knife', 'hammer', 'screwdriver', 'file', 'wrench', 'spanner', 'ruler'),
            'building':('house', 'igloo', 'theatre', 'hospital', 'flat', 'castle', 'bungalow'),
            'flower':('rose', 'dandelion', 'buttercup', 'daffodil'),
            'sport':('cricket', 'hockey', 'rugby', 'cycling', 'swimming'),
            'gas':('oxygen', 'hydrogen', 'nitrogen'),
            'drink':('water', 'lemonade', 'cocoa', 'juice', 'milk'),
            'metal':('copper', 'steel', 'lead', 'iron', 'mercury'),
            'bird':('duck', 'hawk', 'sparrow', 'eagle'),
        }

    def choose_from(iterable):
        return iterable[randint(0, len(iterable)-1)]

    def pick_types(number_different_types):
        types = set()
        word_types = tuple(word_dict.keys())
        while len(types) != number_different_types:
            types.add(choose_from(word_types))
        return tuple(types)

    def add_single_incorrect_type(types):
        types = set(types)
        word_types = tuple(word_dict.keys())
        while len(set(types)) < 2:
            types.add(choose_from(word_types))
        return tuple(types)

    def pick_correct(word_type):
        return choose_from(word_dict[word_type])

    def pick_incorrect(word_type, option_types):
        #pick a word not from the word type:
        selected = word_type
        while selected == word_type:
            selected = choose_from(option_types)
        return choose_from(word_dict[selected])

    def make_rule_types_list(possible_types):
        return [choose_from(possible_types[:1]) for i in range(3)]
            
    def make_type_word_tuples(option_types, chosen_types, incorrect):
        types_list = []
        while len(types_list) != 3:
            word_type = choose_from(option_types)
            if incorrect > 0:
                word = pick_incorrect(word_type, option_types)
                incorrect -= 1
            else:
                word = pick_correct(word_type)
            types_list.append((word_type, word))
        shuffle(types_list)
        return tuple(types_list)

    def make_rules(rules_tuples):
        rule_one = ' '.join([item[0].capitalize() for item in rules_tuples])
        rule_two = ' '.join([item[1].capitalize() for item in rules_tuples])
        return rule_one, rule_two

    def make_items(incorrect):
        print(incorrect)
        items = []
        for i in range(4):
            if i == (3 - incorrect):
                items.append({'name':f'{i}', 'indicator':'correct'})
            else:
                items.append({'name':f'{i}', 'indicator':'incorrect'})
        return items

        
    instructions = (
        "Read and memorise the rule; click the 'Next Step' button and the rule will disappear.",
        "Look at the item list. How many of these match the previous rule? Click on the 'Next Step' button once you know the answer.",
        'Select your answer by clicking the correct number.',
    )


    number_different_types = 1 if randint(0,5) == 0 else 2
    number_incorrect = randint(0,3)
    possible_types = pick_types(number_different_types)#the options we are using               
    rule_types_list = make_rule_types_list(possible_types)
    if number_incorrect != 0:#if we need more than one incorrect type, add it!
        if len(possible_types) < 2:
            possible_types = add_single_incorrect_type(possible_types)
    type_word_tuples = make_type_word_tuples(possible_types, rule_types_list, number_incorrect)
    rule_one, rule_two = make_rules(type_word_tuples)
    items = make_items(number_incorrect)
    
    context = {
        'assessment_title':'Error Detection',
        'instructions':instructions,
        'rule_one':rule_one,
        'rule_two':rule_two,
        'prompt':'Options',
        'items':items,
        'link':'word_rules'
    }
    
    return render(request, 'act_simulator/word_rules.html', context)

def deductive_reasoning(request):

    item_lists = {
        'jobs':{
            'items':('pilot','policeman', 'fireman', 'soldier', 'sailor', 'engineer', 'teacher'),
            'valid':('distance','happiness')
            },
        'events':{
            'items':('confirmation', 'reference', 'reservation', 'attendance', 'interview'),
            'valid':('distance','time')
            },
        'fish':{
            'items':('cod', 'trout', 'salmon', 'pike', 'tuna', 'baracuda'),
            'valid':('distance','time','size','speed')
            },
        'terrain':{
            'items':('desert', 'river', 'lake', 'tundra', 'mountain', 'hill'),
            'valid':('distance','time', 'temperature', 'height')
            },
        'buildings':{
            'items':('cinema','house', 'school', 'hospital', 'hotel', 'shop', 'gym'),
            'valid':('distance','size', 'temperature', 'height')
            },
        'structures':{
            'items':('monument', 'bridge', 'tower', 'pylon', 'mosque', 'flagpole', 'lamp post'),
            'valid':('distance','size', 'height', 'temperature')
            },
        'vehicles':{
            'items':('train', 'ship', 'bus', 'motorcycle', 'helicopter', 'bicycle'),
            'valid':('distance', 'speed')
            },
        }

    descriptors = {
        'distance':{'less':'nearer than', 'more':'further than', 'least':'nearest', 'most':'furthest'},
        'time':{'less':'before', 'more':'after', 'least':'first', 'most':'last'},
        'happiness':{'less':'happier than','more':'sadder than','least':'happiest', 'most':'saddest'},
        'temperature':{'less':'hotter than','more':'cooler than','least':'hottest', 'most':'coolest'},
        'size':{'less':'smaller than','more':'larger than','least':'smallest', 'most':'largest'},
        'height':{'less':'lower than','more':'higher than','least':'lowest', 'most':'highest'},
        'speed':{'less':'slower than','more':'faster than','least':'slowest', 'most':'fastest'},
        }

    def choose_from(iterable):
        return iterable[randint(0, len(iterable)-1)]

    def select_dict():
        category = tuple(item_lists.keys())
        return choose_from(category)

    def select_descriptors(category):
        desc_choice = choose_from(item_lists[category]['valid'])
        return descriptors[desc_choice]

    def make_ordered_list(chosen):
        chosen_items = set()
        while len(chosen_items) != 3:
            chosen_items.add(choose_from(item_lists[chosen]['items']).capitalize())
        return tuple(chosen_items)

    def get_rules_data(three_ordered_items):
        rules_data = set()
        while len(rules_data) < 2:
            items_values = set()
            while len(items_values) < 2:
                item = choose_from(three_ordered_items)
                value = three_ordered_items.index(item)
                items_values.add((item, value))
            rules_data.add(tuple(items_values))
        return tuple(rules_data)

    def make_rule_with(rules_data, adjectives):
        #assign comparative adjective to each rule
        #make rule
        #assign superlative adjective as answer
        list_rules_strings = []
        for rule in rules_data:
            if rule[0][1] - rule[1][1] < 0:
                comparative = adjectives['less']
            else:
                comparative = adjectives['more']
            list_rules_strings.append(' '.join([rule[0][0], comparative, rule[1][0]]))
        return list_rules_strings

    def get_mode(sample):
        c = Counter(sample)
        return [k for k, v in c.items() if v == c.most_common(1)[0][1]]

    def make_prompt_answer(rules_data, adjectives):
        #print(rules_data)
        print(adjectives)
        #get all values into a list
        value_list = []
        for rule in rules_data:
            value_list.append(rule[0][1])
            value_list.append(rule[1][1])
        mode = get_mode(value_list)[0]
        if mode == 0:
            superlative = adjectives['least']
            answer_value = 0
        elif mode == 1:
            if randint(0,1):
                superlative = adjectives['least']
                answer_value = 0
            else:
                superlative = adjectives['most']
                answer_value = 2
        elif mode == 2:
            superlative = adjectives['most']
            answer_value = 2
        prompt = "Which is " + superlative + '?'
        return prompt, answer_value

    def make_rules_prompt_answer_value(three_ordered_items, adjectives):
        rules_data = get_rules_data(three_ordered_items)
        completed_rules = make_rule_with(rules_data, adjectives)
        prompt, answer_value = make_prompt_answer(rules_data, adjectives)
        return completed_rules[0], completed_rules[1], prompt, answer_value

    def make_items(three_ordered_items, answer_value):
        items = []
        for i in range(3):
            indicator = "correct" if i == answer_value else "incorrect"
            items.append({'name':f'{three_ordered_items[i].capitalize()}', 'indicator':indicator})
        shuffle(items)
        return items

    instructions = (
        "Read and memorise the rule; click the 'Next Step' button and the rule will disappear.",
        "Look at the item list. How many of these match the previous rule? Click on the 'Next Step' button once you know the answer.",
        'Select your answer by clicking the correct number.'
        )

    chosen = select_dict()
    adjectives = select_descriptors(chosen)
    three_ordered_items = make_ordered_list(chosen)
    rule_one, rule_two, prompt, answer_value = make_rules_prompt_answer_value(three_ordered_items, adjectives)
    items = make_items(three_ordered_items, answer_value)

    context = {
        'assessment_title':'Deductive Reasoning',
        'instructions':instructions,
        'rule_one':rule_one,
        'rule_two':rule_two,
        'prompt':prompt,
        'items':items,
        'link':'deductive_reasoning',
    }    

    return render(request, 'act_simulator/deductive_reasoning.html', context)

#alphabet test
