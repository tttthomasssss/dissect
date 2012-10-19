'''
Created on Oct 18, 2012

@author: georgianadinu
'''
import numpy as np
import unittest
from pipelines import build_core_space as bcs
from composes.semantic_space.space import Space
import composes.utils.io_utils as io_utils

class Test(unittest.TestCase):


    def setUp(self):
        self.dir_ = "/home/georgianadinu/work/localtoolkit/toolkit/src/unitest/pipelines_test_resources/"

    def tearDown(self):
        pass


    def _test_equal_spaces_structs(self, sp, new_sp):     
        self.assertListEqual(sp.id2row, new_sp.id2row)
        self.assertListEqual(sp.id2column, new_sp.id2column)
        self.assertDictEqual(sp.row2id, new_sp.row2id)
        self.assertDictEqual(sp.column2id, new_sp.column2id)
        
    def _test_equal_spaces_dense(self, sp, new_sp):

        self._test_equal_spaces_structs(sp, new_sp)
        np.testing.assert_array_equal(sp.cooccurrence_matrix.mat, 
                                      new_sp.cooccurrence_matrix.mat)
            
    def _test_equal_spaces_sparse(self, sp, new_sp):

        self._test_equal_spaces_structs(sp, new_sp)
        np.testing.assert_array_equal(sp.cooccurrence_matrix.mat.todense(), 
                                      new_sp.cooccurrence_matrix.mat.todense())
        
    def test_raises(self):
        
        self.assertRaises(SystemExit, bcs.main,["build_core_space.py", "-l",
                                                "~/work/localtoolkit/toolkit/src/unitest/pipelines_test_resources/log1.txt",
                                                "-h"])

    def test_simple_sparse(self):
            
        bcs.main(["build_core_space.py", 
                  "-l", "/home/georgianadinu/work/localtoolkit/toolkit/src/unitest/pipelines_test_resources/log1.txt",
                  "-i", "/home/georgianadinu/work/localtoolkit/toolkit/src/unitest/pipelines_test_resources/mat1", 
                  "-o", "/home/georgianadinu/work/localtoolkit/toolkit/src/unitest/pipelines_test_resources/",
                  "--input_format", "sm",
                  "--output_format", "sm"
                  ])
        
        s1 = Space.build(data="/home/georgianadinu/work/localtoolkit/toolkit/src/unitest/pipelines_test_resources/mat1.sm", format = "sm")
        s2 = Space.build(data="/home/georgianadinu/work/localtoolkit/toolkit/src/unitest/pipelines_test_resources/CORE_SS.mat1.sm", format="sm")
        s3 = io_utils.load("/home/georgianadinu/work/localtoolkit/toolkit/src/unitest/pipelines_test_resources/CORE_SS.mat1.pickle", Space)
        
        self._test_equal_spaces_sparse(s1, s2)
        self._test_equal_spaces_sparse(s1, s3)
        
    def test_simple_dense(self):
            
        bcs.main(["build_core_space.py", 
                  "-l", "/home/georgianadinu/work/localtoolkit/toolkit/src/unitest/pipelines_test_resources/log1.txt",
                  "-i", "/home/georgianadinu/work/localtoolkit/toolkit/src/unitest/pipelines_test_resources/mat2", 
                  "-o", "/home/georgianadinu/work/localtoolkit/toolkit/src/unitest/pipelines_test_resources/",
                  "--input_format", "dm",
                  "--output_format", "dm"
                  ])
        
        s1 = Space.build(data = self.dir_ + "mat2.dm", format = "dm")
        s2 = Space.build(data = self.dir_ + "CORE_SS.mat2.dm", format="dm")
        s3 = io_utils.load(self.dir_ + "CORE_SS.mat2.pickle", Space)
        
        self._test_equal_spaces_dense(s1, s2)
        self._test_equal_spaces_dense(s1, s3)        
 
        bcs.main(["build_core_space.py", 
                  "-l", "/home/georgianadinu/work/localtoolkit/toolkit/src/unitest/pipelines_test_resources/log1.txt",
                  "-i", "/home/georgianadinu/work/localtoolkit/toolkit/src/unitest/pipelines_test_resources/CORE_SS.mat2", 
                  "-o", "/home/georgianadinu/work/localtoolkit/toolkit/src/unitest/pipelines_test_resources/",
                  "--input_format", "pickle",
                  "--output_format", "dm"
                  ])
        
        s1 = io_utils.load(self.dir_ + "CORE_SS.CORE_SS.mat2.pickle", Space)
        s3 = io_utils.load(self.dir_ + "CORE_SS.mat2.pickle", Space)
        
        self._test_equal_spaces_dense(s1, s3)  
 
    def test_simple_ops(self):
        
        #x = matrix([[ -2.19426495e+00,   3.16751379e+00,  -3.89945798e-01],
        #x = np.mat([[1,2,3],[2,4,6],[4,675,43]])
        
        us = np.mat([[  2.19272110e+00,   3.03174768e+00],
                               [  4.38544220e+00,   6.06349536e+00],
                               [  6.76369708e+02,  -4.91431927e-02]])
        us2 = np.mat([[ 2.19426495e+00,   3.16751379e+00],
                      [ 4.38703714e+00,   6.14112794e+00],
                      [ 6.76380808e+02,  -5.01074549e-02]])
        

        bcs.main(["build_core_space.py", 
                  "-l", "/home/georgianadinu/work/localtoolkit/toolkit/src/unitest/pipelines_test_resources/log1.txt",
                  "-i", "/home/georgianadinu/work/localtoolkit/toolkit/src/unitest/pipelines_test_resources/mat3",
                  "-w", "raw",
                  "-s", "top_sum_3,top_length_3,top_sum_4",
                  "-r", "svd_2,svd_1",
                  "-o", "/home/georgianadinu/work/localtoolkit/toolkit/src/unitest/pipelines_test_resources/",
                  "--input_format", "dm",
                  "--output_format", "dm"
                  ])        
        
        s1 = Space.build(data = self.dir_ + "CORE_SS.mat3.raw.top_sum_3.svd_2.dm", format="dm")
        s2 = Space.build(data = self.dir_ + "CORE_SS.mat3.raw.top_sum_3.svd_1.dm", format="dm")
        s3 = Space.build(data = self.dir_ + "CORE_SS.mat3.raw.top_length_3.svd_2.dm", format="dm")
        s4 = Space.build(data = self.dir_ + "CORE_SS.mat3.raw.top_length_3.svd_1.dm", format="dm")
        s5 = Space.build(data = self.dir_ + "CORE_SS.mat3.raw.top_sum_4.svd_2.dm", format="dm")
        s6 = Space.build(data = self.dir_ + "CORE_SS.mat3.raw.top_sum_4.svd_1.dm", format="dm")
            
        self._test_equal_spaces_dense(s1, s3)            
        self._test_equal_spaces_dense(s2, s4)
        
        np.testing.assert_array_almost_equal(abs(s1.cooccurrence_matrix.mat), abs(us), 2)
        np.testing.assert_array_almost_equal(abs(s2.cooccurrence_matrix.mat), abs(us[:,0:1]), 2)
        np.testing.assert_array_almost_equal(abs(s5.cooccurrence_matrix.mat), abs(us2), 2)
        np.testing.assert_array_almost_equal(abs(s6.cooccurrence_matrix.mat), abs(us2[:,0:1]), 2)

        self._test_equal_spaces_structs(s3, s5)
        self._test_equal_spaces_structs(s2, s6)
        
        
        bcs.main(["build_core_space.py", 
          "-l", "/home/georgianadinu/work/localtoolkit/toolkit/src/unitest/pipelines_test_resources/log1.txt",
          "-i", "/home/georgianadinu/work/localtoolkit/toolkit/src/unitest/pipelines_test_resources/mat3",
          "--weighting", "raw",
          "--selection", "top_sum_3,top_length_3,top_sum_4",
          "--reduction", "svd_2,svd_1",
          "-o", "/home/georgianadinu/work/localtoolkit/toolkit/src/unitest/pipelines_test_resources/",
          "--input_format", "sm",
          "--output_format", "dm"
          ])        
        
        s1 = Space.build(data = self.dir_ + "CORE_SS.mat3.raw.top_sum_3.svd_2.dm", format="dm")
        s2 = Space.build(data = self.dir_ + "CORE_SS.mat3.raw.top_sum_3.svd_1.dm", format="dm")
        s3 = Space.build(data = self.dir_ + "CORE_SS.mat3.raw.top_length_3.svd_2.dm", format="dm")
        s4 = Space.build(data = self.dir_ + "CORE_SS.mat3.raw.top_length_3.svd_1.dm", format="dm")
        s5 = Space.build(data = self.dir_ + "CORE_SS.mat3.raw.top_sum_4.svd_2.dm", format="dm")
        s6 = Space.build(data = self.dir_ + "CORE_SS.mat3.raw.top_sum_4.svd_1.dm", format="dm")
            
        self._test_equal_spaces_dense(s1, s3)            
        self._test_equal_spaces_dense(s2, s4)
        
        np.testing.assert_array_almost_equal(abs(s1.cooccurrence_matrix.mat), abs(us), 2)
        np.testing.assert_array_almost_equal(abs(s2.cooccurrence_matrix.mat), abs(us[:,0:1]), 2)
        np.testing.assert_array_almost_equal(abs(s5.cooccurrence_matrix.mat), abs(us2), 2)
        np.testing.assert_array_almost_equal(abs(s6.cooccurrence_matrix.mat), abs(us2[:,0:1]), 2)

        self._test_equal_spaces_structs(s3, s5)
        self._test_equal_spaces_structs(s2, s6)
        
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.test1']
    unittest.main()