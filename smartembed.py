import os
import pickle
import numpy as np
from gensim.models.fasttext import FastText
from scipy.spatial.distance import pdist, cdist, squareform
from scipy.spatial import distance
import sys
import os.path


base_path = os.path.dirname(__file__)
dirs_add = (
    "contract_level/Normalize/",
    'contract_level/Vectorize/',
    'contract_level/Crawl',
    'todo/', 
    ""
)
for _dir in dirs_add:
    sys.path.append(os.path.join(base_path, _dir))

from contract_normalization import Contract_Norm
from contract_vectorize import Contract_Vec
from contract_crawl import Contract_Detail
from config import Config
from clone_detect import Clone_Detect 

class SmartEmbed(object): 

    def __init__(self):

        self.USERINPUT = os.path.join(base_path, "todo/USERINPUT/")
        self.contract_model_path = os.path.join(base_path, "contract_level/Model/FastText/fasttext_model")
        self.fasttext_model = self.get_fasttext_model()

    def get_fasttext_model(self):
        '''
            load fasttext model
        '''
        FASTTEXT_MODEL = FastText.load(self.contract_model_path)
        return FASTTEXT_MODEL

    def save_to_file(self, user_in):
        '''
            save user input into file
        '''
        if not os.path.exists( self.USERINPUT ):
            os.makedirs(self.USERINPUT)
        with open( self.USERINPUT + 'user_input.sol', 'w') as handle:
            handle.write(user_in)

    def parser(self):
        '''
            parse the user_input.sol into AST 
            EDIT: i think Java doesn't see same env variables as Python so we need to
            change to the directory. otherwise it doesn't find the Tokenize class
        '''
        cwd = os.getcwd()
        os.chdir(base_path)
        cmd = "java -classpath ./contract_level/Parse/antlr4.jar:./contract_level/Parse/target/ \
                    Tokenize ./todo/USERINPUT/user_input.sol ./todo/CONTRACT_RESULT/"
        
        os.system(cmd) 
        os.chdir(cwd)

        
    def normalizer(self):
        '''
            normalize 
        '''
        # print("entering normalizer...")
        cn = Contract_Norm(os.path.join(base_path, "todo/CONTRACT_RESULT/"))    
        return cn.line_span, cn.normalized_tokens

    def vectorizer(self, norm_result):
        # print("entering vectorizer...")
        cv = Contract_Vec(norm_result, self.fasttext_model)
        return cv.vector
    
    def get_vector(self, user_input):
        self.save_to_file(user_input)
        self.parser()
        norm_result = self.normalizer()
        vec_result = self.vectorizer(norm_result)
        return vec_result 

    def get_similarity(self, vec1, vec2):
        numerator = distance.cdist(vec1.reshape(1, 150), vec2, 'euclidean')
        denominator = np.linalg.norm(vec1, axis=1) + np.linalg.norm(vec2)
        similarity = 1 - np.divide(numerator, denominator)
        return similarity[0][0]

def main():
    se = SmartEmbed()
    user_input1 = open('./todo/test.sol', 'r').read()
    contract_vector1 = se.get_vector(user_input1)

    user_input2 = open('./todo/KOTH.sol', 'r').read()
    contract_vector2 = se.get_vector(user_input2)
    similarity = se.get_similarity(contract_vector1, contract_vector2)
    print("similarity score:", similarity, type(similarity))



if __name__ == '__main__':
    main()
