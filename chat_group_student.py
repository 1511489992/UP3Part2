S_ALONE = 0
S_TALKING = 1

#==============================================================================
# Group class:
# member fields: 
#   - An array of items, each a Member class
#   - A dictionary that keeps who is a chat group
# member functions:
#    - join: first time in
#    - leave: leave the system, and the group
#    - list_my_peers: who is in chatting with me?
#    - list_all: who is in the system, and the chat groups
#    - connect: connect to a peer in a chat group, and become part of the group
#    - disconnect: leave the chat group but stay in the system
#==============================================================================

class Group:
    
    def __init__(self):
        self.members = {}
        self.chat_grps = {}
        self.grp_ever = 0
        
    def join(self, name):
        self.members[name] = S_ALONE
        return
        
        
    #implement        
    def is_member(self, name):
        if name in self.members:
            return True
        else:
            return False
            
    #implement
    def leave(self, name):
        try:
            if self.members[name] == S_TALKING:
                self.disconnect(name)
            del self.members[name]
        except:
             print("Error: {} is not a member".format(name))
        finally:
            return
        
    #implement                
    def find_group(self, name):
        found = False
        group_key = 0
        for k,v in self.chat_grps.items():
            if name in v:
                found = True
                group_key = k
                break
        return found, group_key
        
    #implement                
    def connect(self, me, peer):
        #Error: user is not a member
        if not (self.is_member(me) and self.is_member(peer)):
            print("Error: {} and/or {} is not a member".format(me, peer))
            return
        #Error: user has already been in a group
        if self.members[me] == S_TALKING:
            self.disconnect(me)
        #if peer is in a group, join it
        peer_in_group, group_key = self.find_group(peer)
        # otherwise, create a new group with you and your peer
        if peer_in_group:
            self.chat_grps[group_key].append(me)
        else:
            self.grp_ever += 1
            self.chat_grps[self.grp_ever] = [me] + [peer]
        #set the user's state
        self.members[me] = S_TALKING
        self.members[peer] = S_TALKING
        return

    #implement                
    def disconnect(self, me):
        #Error: user is not a member
        if not self.is_member(me):
            print("Error: {} is not a member".format(me))
            return
        #Error: user is not in a group
        if self.members[me] == S_ALONE:
            print("Error: {} isn't in any group".format(me))
            return
        #set the user's state
        self.members[me] = S_ALONE
        # find myself in the group, quit
        for grp_key,group in self.chat_grps.items():
            if me in group:
                group.remove(me)
                break
        if len(group) == 1:
            self.members[group[0]] = S_ALONE
            del self.chat_grps[grp_key]
        return
        
    def list_all(self):
        # a simple minded implementation
#        full_list = "Users: ------------" + "\n"
#        full_list += str(self.members) + "\n"
#        full_list += "Groups: -----------" + "\n"
#        full_list += str(self.chat_grps) + "\n"
#        return full_list
        full_list = "Users: ------------" + "\n"
        for k,v in self.members.items():
            full_list += k + ' - '
            if v == S_ALONE:
                full_list += 'ALONE\n'
            else:
                full_list += 'TALKING\n'
        full_list += "Groups: -----------" + "\n"
        for k,v in self.chat_grps.items():
            full_list += '  {:<8}'.format(k) + str(v) + '\n'
        full_list += '\n'
        return full_list

    #implement
    def list_me(self, me):
        # return a list, "me" followed by other peers in my group
        if self.members[me] == S_ALONE:
            return ['Error']
        my_list = [me]
        for k,v in self.chat_grps.items():
            if me in v:     
                for peer in v:
                    if peer != me:
                        my_list.append(peer)
                break
        return my_list

if __name__ == "__main__":    
	g = Group()
	g.join('a')
	g.join('b')
	print(g.list_all())

	g.connect('a', 'b')
	print(g.list_all())
  
 
