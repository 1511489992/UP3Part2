# -*- coding: utf-8 -*-
"""
Created on Sat Jul  5 11:38:58 2014

@author: zzhang
"""
import pickle

class Index:
    def __init__(self, name):
        self.name = name
        self.msgs = [];
        self.index = {}
        self.total_msgs = 0
        self.total_words = 0
        
    def get_total_words(self):
        return self.total_words
        
    def get_msg_size(self):
        return self.total_msgs
        
    def get_msg(self, n):
        return self.msgs[n]
        
    # implement
    def add_msg(self, m):
        self.msgs.append(m)
        self.total_msgs += 1
        return
        
    def add_msg_and_index(self, m):
        self.add_msg(m)
        line_at = self.total_msgs - 1
        self.indexing(m, line_at)

    # implement
    def indexing(self, m, l):
        words = m.split()
        for a_word in words:
            self.index[a_word] = self.index.get(a_word, []) + [l]         
        return

    # implement: query interface
                     
    def search(self, term):
        '''
        return a list of tupple. if index the first sonnet (p1.txt), then
        call this function with term 'thy' will return the following:
        [(7, " Feed'st thy light's flame with self-substantial fuel,"),
         (9, ' Thy self thy foe, to thy sweet self too cruel:'),
         (9, ' Thy self thy foe, to thy sweet self too cruel:'),
         (12, ' Within thine own bud buriest thy content,')]
                  
        ''' 
        msgs = []
        for l_num in self.index[term]:
            msgs.append((l_num, self.get_msg(l_num)))
        return msgs

class PIndex(Index):
    def __init__(self, name):
        super().__init__(name)
        roman_int_f = open('roman.txt.pk', 'rb')
        self.int2roman = pickle.load(roman_int_f)
        roman_int_f.close()
        self.load_poems()
        
        # implement: 1) open the file for read, then call
        # the base class's add_msg_and_index
    def load_poems(self):
        poem_file = open(self.name, 'r')
        for line in poem_file:
            self.add_msg_and_index(line)
        poem_file.close()
        return
    
        # implement: p is an integer, get_poem(1) returns a list,
        # each item is one line of the 1st sonnet
    def get_poem(self, p):
        poem = []
        #find the starting line
        poem_num = self.int2roman[p] + '.'
        start_l = self.search(poem_num)[0][0]
        #fing the end
        next_poem_num = self.int2roman[p+1] + '.'
        end_l = self.search(next_poem_num)[0][0]
        #retrieve lines
        for i in range(start_l, end_l):
            poem.append(self.msgs[i])
        return poem

if __name__ == "__main__":
    sonnets = PIndex("AllSonnets.txt")
    # the next two lines are just for testing
    p3 = sonnets.get_poem(3)
    s_love = sonnets.search("love")
