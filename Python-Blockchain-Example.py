#!/usr/bin/env python
# coding: utf-8

# Let's build a Cryptocurrency! Example used for Adept Canberra Workshop 1: Python, Crypto and Blockchains

# In[1]:


import hashlib
import time

class Block:

    def __init__(self, index, proof_no, prev_hash, data, timestamp=None):
        #first block class

        self.index = index
        self.proof_no = proof_no
        self.prev_hash = prev_hash
        self.data = data
        self.timestamp = timestamp or time.time()

    @property
    def calculate_hash(self):
        #calculates the cryptographic hash of every block
        
        block_of_string = "{}{}{}{}{}".format(self.index, self.proof_no,
                                              self.prev_hash, self.data,
                                              self.timestamp)

        return hashlib.sha256(block_of_string.encode()).hexdigest()

    def __repr__(self):
        #return block parameters in nice format
        return "{} - {} - {} - {} - {}".format(self.index, self.proof_no,
                                               self.prev_hash, self.data,
                                               self.timestamp)


# In[2]:


class BlockChain:

    def __init__(self):
         # constructor method
        self.chain = []
        self.current_data = []
        self.nodes = set()
        self.construct_genesis() # constructs the genesis block on creation of chain
        
    def construct_genesis(self):
        # constructs the first block
        self.construct_block(proof_no=0, prev_hash=0)


    def construct_block(self, proof_no, prev_hash):
        # constructs a new block and adds it to the chain
        block = Block(
            index=len(self.chain),
            proof_no=proof_no,
            prev_hash=prev_hash,
            data=self.current_data)
        self.current_data = []

        self.chain.append(block)
        return block
    
    @staticmethod
    def check_validity(block, prev_block):
         # checks whether the blockchain is valid
        if prev_block.index + 1 != block.index:
            return False

        elif prev_block.calculate_hash != block.prev_hash:
            return False

        elif not BlockChain.verifying_proof(block.proof_no, prev_block.proof_no):
            return False

        elif block.timestamp <= prev_block.timestamp:
            return False

        return True

    def new_data(self, sender, recipient, quantity):
          # adds a new transaction to the data of the transactions
        self.current_data.append({
            'sender': sender,
            'recipient': recipient,
            'quantity': quantity
        })
        return True

    @staticmethod
    def proof_of_work(last_proof):
        # protects the blockchain from attack
        '''this simple algorithm identifies a number f' such that hash(ff') contain 4 leading zeroes
             f is the previous f'
             f' is the new proof
            '''
        proof_no = 0
        while BlockChain.verifying_proof(proof_no, last_proof) is False:
            proof_no += 1

        return proof_no


    @staticmethod
    def verifying_proof(last_proof, proof):
        #verifying the proof: does hash(last_proof, proof) contain 4 leading zeroes?

        guess = f'{last_proof}{proof}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:4] == "0000"
    
    @property
    def latest_block(self):
        # returns the last block in the chain
        return self.chain[-1]


# In[3]:


blockchain = BlockChain() #create new Blockchain instance


# In[4]:


print(blockchain.chain) #check out the Genesis block 


# In[5]:


blockchain.new_data(
    sender="0",  #it implies that this node has created a new block
    recipient="Adept Canberra",  #let's send Adept some coins!
    quantity=
    1,  #creating a new block (or identifying the proof number) is awarded with 1
)


# In[6]:


last_block = blockchain.latest_block #grab the last block in the chain


# In[7]:


last_proof_no = last_block.proof_no #and from this last block, we grab the proof no


# In[8]:


last_hash = last_block.calculate_hash #and the its (the last block's) hash


# In[9]:


proof_no = blockchain.proof_of_work(last_proof_no) #we then calculate the next proof no from the previous, check our new_data is valid


# In[10]:


block = blockchain.construct_block(proof_no, last_hash) #we then construct our new block and add it to the chain


# In[11]:


print(blockchain.chain) #and see it append to the chain!

