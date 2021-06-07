class ActQuestion:
    rules = None #[(rule, dissapear on click(0 or 1)),...]
    items = None #[(item, correct),...]

    def return_all(self):
        return {
            'rules':self.rules, 
            'items':self.items
        }
