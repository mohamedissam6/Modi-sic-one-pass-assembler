# class Node:
#     def _init_(self, data):
#         self.data = data
#         self.next_node = None

# class LinkedList:
#     def _init_(self):
#         self.head = None

#     def is_empty(self):
#         return self.head is None

#     def append(self, data):
#         new_node = Node(data)
#         if self.is_empty():
#             self.head = new_node
#         else:
#             current_node = self.head
#             while current_node.next_node:
#                 current_node = current_node.next_node
#             current_node.next_node = new_node

#     def prepend(self, data):
#         new_node = Node(data)
#         new_node.next_node = self.head
#         self.head = new_node

#     def delete(self, data):
#         if self.is_empty():
#             return

#         if self.head.data == data:
#             self.head = self.head.next_node
#             return

#         current_node = self.head
#         while current_node.next_node and current_node.next_node.data != data:
#             current_node = current_node.next_node

#         if current_node.next_node:
#             current_node.next_node = current_node.next_node.next_node

#     def display(self):
#         current_node = self.head
#         while current_node:
#             print(current_node.data, end=" -> ")
#             current_node = current_node.next_node
#         print("None")

class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

class LinkedList:
    def __init__(self):
        self.head = None

    def append(self, data):
        new_node = Node(data)
        if not self.head:
            self.head = new_node
        else:
            last_node = self.head
            while last_node.next:
                last_node = last_node.next
            last_node.next = new_node

    def get_last_element(self):
        if not self.head:
            return None  # Return None for an empty list
        current_node = self.head
        while current_node.next:
            current_node = current_node.next
        return current_node.data
    
    def delete_last_node(self):
        if not self.head:
            print("Linked list is empty.")
            return

        if not self.head.next:
            # If there is only one node, set the head to None
            self.head = None
            return

        current_node = self.head
        while current_node.next.next:
            current_node = current_node.next

        # Update the next pointer of the second-to-last node
        current_node.next = None

def add_linked_list_to_dict(dict, linked_list):
    curr_node = linked_list.head
    while curr_node:
        dict[curr_node.data] = 1
        curr_node = curr_node.next
