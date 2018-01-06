#!/usr/bin/python

class Player:
    def __init__(self, name, form, cost, position):
        self.name = name
        self.form = form
        self.cost = cost
        self.position = position

    def get_position(self):
        return self.position

    def get_form(self):
        return self.form

    def get_cost(self):
        return self.cost

    def get_name(self):
        return self.name
